# geonode-agrovoc-importer
Django management command to import agrovoc theusaurus into GeoNode.

To run the import command copy it into your geonode project via:
```bash
cp load_agrovoc_thesaurus.py ~/path/to/geonode/geonode/base/management/commands/load_agrovoc_thesaurus.py
```

It then appears in your list of available commands in **python manage.py help**. Now you can get yourself an overview about the functionality with printing help:

```bash
p manage.py load_agrovoc_thesaurus --help
usage: manage.py load_agrovoc_thesaurus [-h] [-d] [--name NAME] [--file FILE] [--title TITLE] [--description DESCRIPTION] [--version] [-v {0,1,2,3}] [--settings SETTINGS] [--pythonpath PYTHONPATH]
                                        [--traceback] [--no-color] [--force-color] [--skip-checks]

Load the AGROVOC in RDF format into GeoNode-DB

options:
  -h, --help            show this help message and exit
  -d, --dry-run         Only parse and print the thesaurus file, without perform insertion in the DB.
  --name NAME           Identifier name for the thesaurus in this GeoNode instance.
  --file FILE           Full path to a thesaurus in RDF format.
  --title TITLE         title to set in the base_thesaurus table for the agrovoc thesaurus
  --description DESCRIPTION
                        description to set in the base_thesaurus table for the agrovoc thesaurus
  --version             show program's version number and exit
  -v {0,1,2,3}, --verbosity {0,1,2,3}
                        Verbosity level; 0=minimal output, 1=normal output, 2=verbose output, 3=very verbose output
  --settings SETTINGS   The Python path to a settings module, e.g. "myproject.settings.main". If this isn't provided, the DJANGO_SETTINGS_MODULE environment variable will be used.
  --pythonpath PYTHONPATH
                        A directory to add to the Python path, e.g. "/home/djangoprojects/myproject".
  --traceback           Raise on CommandError exceptions
  --no-color            Don't colorize the command output.
  --force-color         Force colorization of the command output.
  --skip-checks         Skip system checks.
```

 Before you run the command you have to download the agrovoc. You can do so from https://www.fao.org/agrovoc/releases (like https://data.apps.fao.org/catalog/dataset/agrovoc-2024-04/resource/9e78d388-1e52-41b2-a748-9645de136eca). After downloading and unziping the agrovoc RDF-File you can load the file into GeoNode via:

```bash
python manage.py load_agrovoc_thesaurus --name AGROVOC --file agrovoc_core.rdf
```

**Please notice: running this script will require a big amount of memory (~12.5GB)**

# geonode-gemet-importer
Django management command to import GEMET theusaurus into GeoNode.

**THIS IS A COPY WITH MINOR CHANGES FROM https://github.com/GeoNode/geonode/blob/4.2.2/geonode/base/management/commands/load_thesaurus.py**

To run the import command copy it into your geonode project via:
```bash
cp load_gemet_thesaurus.py ~/path/to/geonode/geonode/base/management/commands/load_gemet_thesaurus.py
```

It then appears in your list of available commands in **python manage.py help**. Now you can get yourself an overview about the functionality with printing help:

```bash
python manage.py load_genet_thesaurus --help
usage: manage.py load_thesaurus [-h] [-d] [--name NAME] [--file FILE] [--version] [-v {0,1,2,3}] [--settings SETTINGS] [--pythonpath PYTHONPATH] [--traceback]
                                [--no-color] [--force-color] [--skip-checks]

Load a thesaurus in RDF format into DB

options:
  -h, --help            show this help message and exit
  -d, --dry-run         Only parse and print the thesaurus file, without perform insertion in the DB.
  --name NAME           Identifier name for the thesaurus in this GeoNode instance.
  --file FILE           Full path to a thesaurus in RDF format.
  --version             Show program's version number and exit.
  -v {0,1,2,3}, --verbosity {0,1,2,3}
                        Verbosity level; 0=minimal output, 1=normal output, 2=verbose output, 3=very verbose output
  --settings SETTINGS   The Python path to a settings module, e.g. "myproject.settings.main". If this isn't provided, the DJANGO_SETTINGS_MODULE environment
                        variable will be used.
  --pythonpath PYTHONPATH
                        A directory to add to the Python path, e.g. "/home/djangoprojects/myproject".
  --traceback           Raise on CommandError exceptions.
  --no-color            Don't colorize the command output.
  --force-color         Force colorization of the command output.
  --skip-checks         Skip system checks.
```

Before you run the command you have to download the gemet full version from https://www.eionet.europa.eu/gemet/en/exports/rdf/latest -> Entire GEMET thesaurus in SKOS format. After downloading and gunzipping the agrovoc RDF-File you can load the file into GeoNode via:

```bash
python manage.py load_gemet_thesaurus --name GEMET --file gemet.rdf
```
