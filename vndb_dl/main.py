# -*- coding: utf-8 -*-
import argparse
import os 

from .arg_parser import parse_ids, parse_urls
from .vn import VN
        
def main():
    parser = argparse.ArgumentParser(
        description="Download visual novel information from vndb.org.",
        allow_abbrev=True
    )
    parser.add_argument(
        '-j', '--json',
        help="Parse the visual novel metadata as a JSON file in the visual \
            novel folder ([True]/False)",
        type=bool,
        default=True
    )
    parser.add_argument(
        '-p', '--plain',
        help="Parse the visual novel metadata as a plain text file in the visual \
        novel folder ([True]/False)",
        type=bool,
        default=True
    )
    parser.add_argument(
        # The --id switch accepts two syntaxes:
        '-i', '--id',
        nargs="+",
        help="vndb id of the visual novel; where in vndb.org/v###, \
        the ### is the vn's id. --id accepts both list of numbers (eg. 5 6 7) \
        and ranges (eg. 5-7) as well as both (eg. 5-7 9 11). \
        Commas and spaces are accepted (eg 5-7, 40 49, 51), as long as each \
        character is separated by a space (57,59 will give you vn n.5759).",
        type=str # Stringly-typed list of ints for further processing
                 # There is most likely a better way to do this
    )
    parser.add_argument(
        '-u', '--url',
        nargs="+",
        help="vndb url of the visual novel",
        type=str
    )
    parser.add_argument(
        '-d', '--directory',
        help="Source directory where the data for each visual novel will \
        be stored",
        type=str,
        default=os.getcwd()
    )
    args = parser.parse_args()

    # The command is only correct if either id, url, or both id and url
    # are specified.
    if not (args.id or args.url):
        parser.error("At least one of --id or --url is required.")

    # We parse --id and --url into a single set of ids:
    # This avoids duplicates if both an id and an url refer to the same id
    # eg. --url https://vndb.org/v7 --id 7
    id_set = set()

    # Get the list of ids from the parser into our set.
    # argpaste does the job of separating based on whitespace:
    # we only have to account for commas and ranges.
    # The parse_ids() function takes care of that job.
    if args.id:
        for id in parse_ids(args.id):
            id_set.add(id)

    # From the list of urls, make them ids, then add them into
    # our set.
    if args.url:
        try:
            for id in parse_urls(args.url):
                id_set.add(id)
        except ValueError:
            raise parser.error("Invalid URL. \n\
        Check that the url is of this form: https://vndb.org/v###, where ### is a number.")

    # For each ID, create an VN object,
    # then extract it into directory.
    # --directory changes the directory each VN is extracted to.
    for id in id_set:
        vn = VN(id)
        print(str(vn.id), "-", vn.metadata["Title"], "; extracting screenshots...")
        vn.extract(args.directory)

if __name__ == '__main__':
    main()