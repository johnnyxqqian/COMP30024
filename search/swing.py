# coordiante (r,q)
# token
# move #

import numpy
from search.init import all


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
tile = start_coordinate
t,q,r = start_coordinate
current_tile = start_coordinate

# def swing_check(current_coordinate, game_state):
#     for position in game_state


# identifies swingable & landable tiles
def swingable_hex_check(current_tile, game_state):
    neighbours = neighour_tiles(current_tile)
    swing_tiles = []
    target_tiles = []
    for tile in neighbours:

        # if not a block tile
        if(tile[0] in UPPER_TILES):
            swing_tiles.append(tile)

            # list of 3-tuples, order is same as swing_tiles so we can trace them
            target_tiles.append(target_tile_coordinates(current_tile, tile))
            

# unused but kept so other code won't give errors
def neighour_tiles(tile):
    i=0
    neighbours = []
    while(i<NUM_DIRECTIONS):
        neighbours.append(tile+DIRECTIONS[i])
        i+=1
    return neighbours
    
# returns 3-tuple of target tiles resulting from a swing
# does not check if tuples are valid
def target_tile_coordinates(base_tile, target_tile):
    base_q = base_tile[Q_INDEX]
    base_r = base_tile[R_INDEX]
    target_q = target_tile[Q_INDEX]
    target_r = target_tile[R_INDEX]

    direction = (target_q - base_q, target_r - base_r)
    target_anchor = (target_q, target_r) + direction
    
    for i in range(NUM_DIRECTIONS):
        if(direction == NUM_DIRECTIONS[i]):
            target_clockwise = (target_q, target_r) + DIRECTIONS[i-1]
            target_anticlockwise = (target_q, target_r) + DIRECTIONS[0] if i == NUM_DIRECTIONS else (target_q, target_r)+ DIRECTIONS[i+1]

    return list(target_anchor, target_clockwise, target_anticlockwise)
    

# checks if we should move to a tile based off game rules (assumes move is valid as per Simon's definition)
def target_tile_check(base_tile, target_tile, game_state_dict):
    enemy_tile = False
    pieces_on_tile= set()

    # check if empty tile
    if game_state_dict[(target_tile[COORD_Q_INDEX], target_tile[COORD_R_INDEX])]:
        tile = game_state_dict[(target_tile[COORD_Q_INDEX], target_tile[COORD_R_INDEX])]
    else:
        return True

    # blocked
    if tile[T_INDEX]==BLOCKED:
        return False

    # tile not empty
    if len(tile[T_INDEX]) >=1:

        # storing symbols to check
        for i in range(len(tile[0])):
            
            # case sensitive in case of friendly tokens
            pieces_on_tile.add(tile[0])
            
            # occupied by enemy
            if tile[T_INDEX] in LOWER_TILES:
                enemy_tile = True

                # if enemy tile and we lose, we don't move
                if not RPS_OUTCOMES(base_tile[T_INDEX], tile[0]):
                    return False

        # >1 token with same symbol, if we move here everyone is destroyed 
        # need to update in case of friendly fire

        # if (len(tile[0])>=2) and (base_tile[T_INDEX] not in pieces_on_tile):
        #     return False

    return True

