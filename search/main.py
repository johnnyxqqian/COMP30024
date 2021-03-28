"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching

This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!
"""

import sys
import json
# If you want to separate your code into separate files, put them
# inside the `search` directory (like this one and `util.py`) and
# then import from them like this:
from search.util import print_board, print_slide, print_swing

def main(filename):

    """
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)
    pass
    """
    try:
        with open(filename) as file:
            data = json.load(file)
    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)

    ## Convert the JSON into a board_dict
    board_dict = {}
    for hex in data['upper']:
        token, p, q = hex
        if token in ['r','p','s']:
            token = token.upper()
        board_dict[(p, q)] = token

    for hex in data['lower']:
        token, p, q = hex
        board_dict[(p, q)] = token

    print(board_dict)
    print_board(board_dict)

    # TODO:
    # Find and print a solution to the board configuration described
    # by `data`.
    # Why not start by trying to print this configuration out using the
    # `print_board` helper function? (See the `util.py` source code for
    # usage information).

main('test.json')
