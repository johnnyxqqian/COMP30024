"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching

This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!
"""

import sys
import json
from search.extra_utils import *
from search.minHeap import *
from search.init import *

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
    game = RoPaSciState()

    # load the initial game state into the object
    game.initialise(data=data)

    # initialise our priority queue in the form of a minheap
    queue = MinHeap(MAX_HEAP_SIZE)

    # insert initial board state into search problem
    queue.insert(game)

    # seen states:
    seen_boards = []

    state = None

    # While priority queue is not empty
    while not queue.is_empty():

        # pop min priority queue board state
        state = queue.remove()

        if state.board in seen_boards:
            continue

        if state.is_lost():
            continue

        if state.is_solved():
            break

        for

        # for each token
            # list all token possible moves

        # for each combinatoric of possible moves
            # for each move in the combinatoric
                # apply move to RoPaSci object
                # store move in RoPaSci object history
            # after all moves applied, call resolve_battles
            # state.update_cost()
            # seen_boards.append(state.board)
            #queue.insert(RoPaSci)

    # if solution found:
        # for move (move in form of hex a, hex b)
        # if move distance is greater than 1:
            # use print swing function
        # else
            # use print slide function

main('test.json')
