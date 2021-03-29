# coordiante (r,q)
# token
# move #

import numpy
from search.init import *


from numpy.lib.stride_tricks import as_strided
# dictionary for RPS outcomes
RPS_OUTCOMES = {
    (ROCK, PAPER): False,
    (PAPER, ROCK): True,

    (ROCK,SCISSORS): True,
    (SCISSORS, ROCK): False,

    (PAPER, SCISSORS): False,
    (SCISSORS, PAPER): True
}

start_coordinate = ("R",2,3)
hex = start_coordinate
t,q,r = start_coordinate
current_hex = start_coordinate

# def swing_check(current_coordinate, game_state):
#     for position in game_state


# identifies swingable & landable hexs
def swingable_hex_check(current_hex, board, neighbours):
    swing_hexs = []
    target_hexs = []
    for hex in neighbours:

        # if not a block hex
        if(board[hex] in UPPER_TILES):
            swing_hexs.append(hex)

            # list of 3-tuples, order is same as swing_hexs so we can trace them
            for hex in (target_hex_coordinates(current_hex, hex)):
                target_hexs.append(hex)

            # target_hexs.append(target_hex_coordinates(current_hex, hex))
            
    return target_hexs
    
# returns 3-tuple of target hexs resulting from a swing
# does not check if tuples are valid
def target_hex_coordinates(base_hex, target_hex):
    base_q = base_hex[Q_INDEX]
    base_r = base_hex[R_INDEX]
    target_q = target_hex[Q_INDEX]
    target_r = target_hex[R_INDEX]

    direction = (target_r - base_r, target_q - base_q)
    target_anchor = (target_r, target_q) + direction
    
    for i in range(NUM_DIRECTIONS):
        if(direction == NUM_DIRECTIONS[i]):
            target_clockwise = (target_r, target_q) + DIRECTIONS[i-1]
            target_anticlockwise = (target_r, target_q) + DIRECTIONS[0] if i == NUM_DIRECTIONS else (target_r, target_q)+ DIRECTIONS[i+1]

    return list(target_anchor, target_clockwise, target_anticlockwise)
    

# checks if we should move to a hex based off game rules (assumes move is valid as per Simon's definition)
def target_hex_check(base_hex, target_hex, game_state_dict):
    enemy_hex = False
    pieces_on_hex= set()

    # check if empty hex
    if game_state_dict[(target_hex[COORD_Q_INDEX], target_hex[COORD_R_INDEX])]:
        hex = game_state_dict[(target_hex[COORD_Q_INDEX], target_hex[COORD_R_INDEX])]
    else:
        return True

    # blocked
    if hex[T_INDEX]==BLOCKED:
        return False

    # hex not empty
    if len(hex[T_INDEX]) >=1:

        # storing symbols to check
        for i in range(len(hex[0])):
            
            # case sensitive in case of friendly tokens
            pieces_on_hex.add(hex[0])
            
            # occupied by enemy
            if hex[T_INDEX] in LOWER_TILES:
                enemy_hex = True

                # if enemy hex and we lose, we don't move
                if not RPS_OUTCOMES(base_hex[T_INDEX], hex[0]):
                    return False

        # >1 token with same symbol, if we move here everyone is destroyed 
        # need to update in case of friendly fire

        # if (len(hex[0])>=2) and (base_hex[T_INDEX] not in pieces_on_hex):
        #     return False

    return True

