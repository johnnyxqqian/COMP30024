"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching

This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!
"""

import sys
import json
from search.extra_utils import *
from search.util import *
from search.minHeap import *
from search.init import *
from itertools import product
from copy import deepcopy

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
    boards_checked = 0
    boards_popped = 0
    # While priority queue is not empty
    while not queue.is_empty():

        ## KEEP WHILE PROGRAMMING TO HELP AUTOFINISH
        #state = RoPaSciState()

        # pop min priority queue board state
        state = queue.remove()

        boards_popped+=1
        print("popped: ",boards_popped)

        if state.board in seen_boards:
            continue

        seen_boards.append(state.board)

        boards_checked += 1
        print("checked: ",boards_checked)

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

        # for each combinatoric of possible moves
            # for each move in the combinatoric
                # apply move to RoPaSci object
                # store move in RoPaSci object history
            # after all moves applied, call resolve_battles
            # state.update_cost()
            # seen_boards.append(state.board)
            #queue.insert(RoPaSci)

        for moves in product(*tokens_moves_list):
            new_state = deepcopy(state)
            new_state.take_turn(moves)
            queue.insert(new_state)

    if state.is_solved():
        for move in state.move_history:

            # move in the form (hex1, hex2, token, turn number)
            base_hex, target_hex, token, turn = move

            if state.hex_distance(base_hex, target_hex) == 2:
                print_swing(token, *base_hex, *target_hex)
            elif state.hex_distance(base_hex, target_hex) == 1:
                print_slide(token, *base_hex, *target_hex)
            else:
                print("something has gone wrong")

    else:
        print("unable to find solution")

main('testsimple.json')
