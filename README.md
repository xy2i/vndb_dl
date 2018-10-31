# vndb_dl

vndb_dl is a command-line utility that allows to download VN metadata and screenshots from vndb.org.

[Download from PyPi](https://pypi.org/project/vndb-dl/)

Disclaimer: this is a simple web scrapper, done as a learning project. If you want to fetch data from vndb, [use their official API.](https://vndb.org/d11)

## Usage

vndb_dl can be used from the command line. You can either specify an id to use with the -i option:

```shell
$ vndb_dl -i 7
```

or an vndb.org url:

```shell
$ vndb_dl -u https://vndb.org/v7
```

Bulk downloading is supported with ranges:

```shell
$ vndb_dl -i 7-12, 14 # Will download vns with id [7; 12] and vn with id 14
```

By default, vn_dl will output metadata about each vn in a metadata.txt and metadata.json file. To disable either or both of these, set their flags to false:

```shell
$ vndb_dl -i 7 -j False -p False
```

By default, vndb_dl will output into the working directory. You can change the directory with the directory flag:
```shell
$ vndb_dl -i 7-12 -d download_folder
```

This covers full usage of vndb_dl.

```shell
$ vndb_dl --help
usage: vndb_dl [-h] [-j JSON] [-p PLAIN] [-i ID [ID ...]] [-u URL [URL ...]]
               [-d DIRECTORY]

Download visual novel information from vndb.org.

optional arguments:
  -h, --help            show this help message and exit
  -j JSON, --json JSON  Parse the visual novel metadata as a JSON file in the
                        visual novel folder ([True]/False)
  -p PLAIN, --plain PLAIN
                        Parse the visual novel metadata as a plain text file
                        in the visual novel folder ([True]/False)
  -i ID [ID ...], --id ID [ID ...]
                        vndb id of the visual novel; where in vndb.org/v###,
                        the ### is the vn's id. --id accepts both list of
                        numbers (eg. 5 6 7) and ranges (eg. 5-7) as well as
                        both (eg. 5-7 9 11). Commas and spaces are accepted
                        (eg 5-7, 40 49, 51), as long as each character is
                        separated by a space (57,59 will give you vn n.5759).
  -u URL [URL ...], --url URL [URL ...]
                        vndb url of the visual novel
  -d DIRECTORY, --directory DIRECTORY
                        Source directory where the data for each visual novel
                        will be stored
```

## For developers

Any contributions are very appreciated. Please submit a pull request if you find improvements.

### Documentation

All documentation can be found in sphinx format under the `docs` folder.

### Unit tests

Tests are located in the `tests` folder.
