"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching

This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!
"""

import sys
import json
from search.extra_utils import *
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

    # initialise game object
    game = RoPaSci()

    # load the initial game state into the object
    game.initialise(data=data)

    #
    # Pseudo-ish code
    # initialise priority queue
    # input board state into search problem
    # while priority queue is not empty:
        # pop min priority queue board state
        # for each token
            # list all token possible moves
        # take
    # output each possible move, and corresponding heuristic cost
    # combine individual token moves into single moves
    # insert into priority queue

    # HEURISTIC:
    # Each token "costs" 10

    # TODO:
    # Find and print a solution to the board configuration described
    # by `data`.
    # Why not start by trying to print this configuration out using the
    # `print_board` helper function? (See the `util.py` source code for
    # usage information).

main('test.json')
