#########################################################################
#
# Copyright (C) 2016 OSGeo
# Copyright (C) 2022 King's College London
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

from typing import List

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.core.management.base import BaseCommand, CommandError
from rdflib import Graph, Literal
from rdflib.namespace import RDF, RDFS, SKOS, DC, DCTERMS
from rdflib.util import guess_format

from geonode.base.models import (
    Thesaurus,
    ThesaurusKeyword,
    ThesaurusKeywordLabel,
)

SUPPORTED_LANGUAGES = ["fr", "de", "en", "it", "es"]
DEFAULT_LANG = getattr(settings, "THESAURUS_DEFAULT_LANG", "en")


def __apply_lower_case__(value: str, lower_case: bool):
    if lower_case:
        return value.lower()
    return value


class Command(BaseCommand):
    help = "Load a thesaurus in RDF format into DB"

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            "-d",
            "--dry-run",
            action="store_true",
            dest="dryrun",
            default=False,
            help="Only parse and print the thesaurus file, without perform insertion in the DB.",
        )

        parser.add_argument(
            "--name",
            dest="name",
            help="Identifier name for the thesaurus in this GeoNode instance.",
        )

        parser.add_argument(
            "--defaultlang",
            dest="default_lang",
            type=str,
            default=DEFAULT_LANG,
            help="change default language.",
        )

        parser.add_argument(
            "--force-lower-case",
            dest="lower_case",
            action="store_true",
            help="all tkeywords and and tkeywordlabels are stored in lower case ...",
        )

        parser.add_argument(
            "--file", dest="file", help="Full path to a thesaurus in RDF format."
        )

    def handle(self, **options):
        input_file = options.get("file")
        name = options.get("name")
        dryrun = options.get("dryrun")
        defaultlang = options.get("default_lang")
        lower_case = options.get("lower_case")

        if not input_file:
            raise CommandError("Missing thesaurus rdf file path (--file)")

        if not name:
            raise CommandError("Missing identifier name for the thesaurus (--name)")

        self.load_thesaurus(input_file, name, defaultlang, not dryrun, lower_case)

    def load_thesaurus(self, input_file, name, defaultlang, store, lower_case):
        g = Graph()
        self.stderr.write(self.style.SUCCESS(f" using defaultlang: {defaultlang} ..."))
        # if the input_file is an UploadedFile object rather than a file path the Graph.parse()
        # method may not have enough info to correctly guess the type; in this case supply the
        # name, which should include the extension, to guess_format manually...
        rdf_format = None
        if isinstance(input_file, UploadedFile):
            self.stderr.write(
                self.style.WARNING(f"Guessing RDF format from {input_file.name}...")
            )
            rdf_format = guess_format(input_file.name)
        g.parse(input_file, format=rdf_format)

        # An error will be thrown here there is more than one scheme in the file
        scheme = g.value(None, RDF.type, SKOS.ConceptScheme, any=False)

        if scheme is None:
            raise CommandError("ConceptScheme not found in file")

        available_titles = [t for t in g.objects(scheme) if isinstance(t, Literal)]
        thesaurus_title = value_for_language(available_titles, defaultlang)
        description = g.value(scheme, DC.description, None, default=thesaurus_title)
        date_issued = g.value(scheme, DCTERMS.issued, None, default="2024-01-01")

        self.stderr.write(
            self.style.SUCCESS(
                f'Thesaurus "{thesaurus_title}", desc: {description} issued at {date_issued}'
            )
        )

        # Define Thesaurus Data
        thesaurus = Thesaurus()
        thesaurus.identifier = name
        thesaurus.description = description
        thesaurus.title = thesaurus_title
        thesaurus.about = str(scheme)
        thesaurus.date = date_issued

        if store:
            thesaurus.save()

        for concept in g.subjects(RDF.type, SKOS.Concept):
            try:
                pref = __apply_lower_case__(
                    preferredLabel(g, concept, defaultlang)[0][1], lower_case
                )
            except:
                self.style.ERROR(
                    f"could not find {str(concept) } in default language {defaultlang} ..."
                )
                continue
            about = __apply_lower_case__(str(concept), lower_case)

            self.stderr.write(self.style.SUCCESS(f"Concept: {str(pref)} ({about})"))

            # Store Keyword
            tk = ThesaurusKeyword()
            tk.thesaurus = thesaurus
            tk.about = about
            tk.alt_label = pref
            try:
                if store:
                    tk.save()

                for _, pref_label in preferredLabel(g, concept):
                    lang = __apply_lower_case__(pref_label.language, lower_case)
                    label = __apply_lower_case__(str(pref_label), lower_case)
                    if lang in SUPPORTED_LANGUAGES:
                        self.stderr.write(
                            self.style.SUCCESS(f"  Label {lang}: {label}")
                        )

                        tkl = ThesaurusKeywordLabel()
                        tkl.keyword = tk
                        tkl.lang = lang
                        tkl.label = label

                        if store:
                            tkl.save()
            except:
                print(f"could not save: {str(pref)}, duplicate ...")


def value_for_language(available: List[Literal], default_lang: str) -> str:
    sorted_lang = sorted(
        available,
        key=lambda literal: "" if literal.language is None else literal.language,
    )
    for item in sorted_lang:
        if item.language is None:
            return str(item)
        elif item.language.split("-")[0] == default_lang:
            return str(item)
    return str(available[0])


def preferredLabel(
    g,
    subject,
    lang=None,
    default=None,
    label_properties=(SKOS.prefLabel, RDFS.label),
):
    """
    Find the preferred label for subject.

    By default prefers skos:prefLabels over rdfs:labels. In case at least
    one prefLabel is found returns those, else returns labels. In case a
    language string (e.g., "en", "de" or even "" for no lang-tagged
    literals) is given, only such labels will be considered.

    Return a list of (labelProp, label) pairs, where labelProp is either
    skos:prefLabel or rdfs:label.

    Copied from rdflib 6.1.1
    """

    if default is None:
        default = []

    # setup the language filtering
    if lang is not None:
        if lang == "":  # we only want not language-tagged literals

            def langfilter(l_):
                return l_.language is None

        else:

            def langfilter(l_):
                return l_.language == lang

    else:  # we don't care about language tags

        def langfilter(l_):
            return True

    for labelProp in label_properties:
        labels = list(filter(langfilter, g.objects(subject, labelProp)))
        if len(labels) == 0:
            continue
        else:
            return [(labelProp, l_) for l_ in labels]
    return default
