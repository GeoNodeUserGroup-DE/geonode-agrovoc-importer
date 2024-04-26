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

 Before you run the command you have to download the agrovoc. You can do so from https://www.fao.org/agrovoc/releases. After downloading and unziping the agrovoc RDF-File you can load the file into GeoNode via:

```bash
python manage.py load_agrovoc_thesaurus --name AGROVOC --file agrovoc_2022-07-01_core.nt
```

**Please notice: running this script will require a big amount of memory (~12.5GB)**
