# -*- coding: utf-8 -*-

from itertools import chain

def parse_range_list(rl):
    """
    Given a string with either an stringly-typed int
    or a string in the form "(int)-(int)" separated by
    commas, return a list of all ints.

    For example, for this string:
        "5,7,9,11-14"
    this function would return
        [5, 7, 9, 11, 12, 13, 14].
    """

    def parse_range(r):
        """ Given a string of form "(int1)-(int2)", return range(int1, int2). """
        if len(r) == 0:
            return []
        parts = r.split("-")
        if len(parts) > 2:
            raise ValueError("Invalid range: {}".format(r))

        return range(int(parts[0]), int(parts[-1])+1)

    return sorted(set(chain.from_iterable(map(parse_range, rl.split(",")))))

def parse_ids(args):
    """ 
    Parse the ids from --id into a list of ints, then return that list.
    Each one is a vn id. 

    The format for args is a list of strings. Each string can be:
    - a stringly-typed int: "4"
    - a stringly-typed int with commas: "4,"
    - a range: "4-7"
    - a range with commas: "4-7,"
    Each string is a different element of the list.

    If the string is a 'range', eg. "4-7", this function will return all
    numbers in that range ([4, 5, 6, 7]).
    """
    def parse_range_list_pack(args):
        """ Pack the list into the correct format. """
        for i, string in enumerate(args):
            string = string.replace(",", "")
            args[i] = string
        args = ",".join(args)
        return args

    def find_char(letter, lst):
        """ Helper that returns a boolean value if letter is in lst. """
        return any(letter in word for word in lst)

    if find_char("-", args):
        # Pack in format for parse_range_list()…
        args = parse_range_list_pack(args)
        # …then parse the format.
        # Implementation is found in format_list_numbers.py.
        args = parse_range_list(args)
    else:
        args = list(map(int, args))
    
    return args

def parse_urls(args):
    """ 
    Parse the urls from --url into a list of ints, then return that list.
    Each one is a vn id. 
    """
    id_list = []

    for url in args:
        url_start = "https://vndb.org/v"
        if url.startswith(url_start):
            id = url[len(url_start):]
            # Make sure the end of the string is well-formed
            # Raises ValueError otherwhise
            id = int(id)
            id_list.append(id)

    return id_list