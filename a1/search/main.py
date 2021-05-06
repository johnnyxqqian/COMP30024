"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching

This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!
"""

import json

# Simons imports

from search.RoPaSciState import *
from search.util import *
from search.minHeap import *
from search.init import *

import time

from itertools import product
from copy import deepcopy

# Johnnys imports
"""
from extra_utils import *
from util import *
from minHeap import *
from init import *
"""

# If you want to separate your code into separate files, put them
# inside the `search` directory (like this one and `util.py`) and
# then import from them like this:


def main():

    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)

    """
    try:
        with open(filename) as file:
            data = json.load(file)
    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)
    """

    start = time.time()

    # initialise game object
    game = RoPaSciState()

    # load the initial game state into the object
    game.initialise(data=data)

    print_board(game.board)

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

        seen_boards.append(state.board)

        if state.is_lost():
            continue

        if state.is_solved():
            break

        # for each token
            # list all token possible moves

        tokens_moves_list = []
        for t, r, q in state.board_dict_to_iterable(state.list_upper_tokens()):
            token_possible_moves = []
            legal_moves = state.list_legal_moves((r,q))
            for legal_move in legal_moves:
                move = ((r,q), legal_move, t)
                token_possible_moves.append(move)

            tokens_moves_list.append(token_possible_moves)

        for moves in product(*tokens_moves_list):
            new_state = deepcopy(state)
            new_state.take_turn(moves)
            queue.insert(new_state)

    if state.is_solved():
        print("# Solution Found")
        for move in state.move_history:

            # move in the form (hex1, hex2, token, turn number)
            base_hex, target_hex, token, turn = move

            # Filter into swings and slides
            if state.hex_distance(base_hex, target_hex) == 2:
                # print("# Token: ", token)
                print_swing(turn, *base_hex, *target_hex)

            elif state.hex_distance(base_hex, target_hex) == 1:
                # print("# Token: ", token)
                print_slide(turn, *base_hex, *target_hex)

        #for board in state.board_history:
        #    print_board(board)
        #    time.sleep(0.1)
        print_board(state.board)

    else:
        print("# unable to find solution")

    end = time.time()
    print("# Search completed in time: ", round(end - start, 2), " seconds")

