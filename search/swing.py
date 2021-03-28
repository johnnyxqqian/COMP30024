# coordiante (r,q)
# token
# move #

import numpy

MOVE_DISTANCE = 1
DIRECTIONS = ((1, 0), (1, -1), (0, -1), 
    (-1, 0), (-1, 1), (0, 1),)
NUM_DIRECTIONS = 6
Q_INDEX = 1
R_INDEX = 2
T_INDEX = 0

start_coordinate = ("R",2,3)
tile = start_coordinate
t,q,r = start_coordinate
current_tile = start_coordinate

def swing_check(current_coordinate, game_state):
    for position in game_state


# identifies swingable & landable tiles
def swingable_hex_check(current_tile, game_state):
    neighbours = neighour_tiles(current_tile)
    swing_tiles = []
    land_tiles = []
    for tile in neighbours:

        # if not a block tile
        if(tile[0]):
            swing_tiles.append(tile)
            land_tiles.append(target_tile_coordinates(current_tile, tile))
            
        
    # alternatively - remove non swingable tile from neighbours


def neighour_tiles(tile):
    i=0
    neighbours = []
    while(i<NUM_DIRECTIONS):
        neighbours.append(tile+DIRECTIONS[i])
    return neighbours
    
# check for hex to swing from
# check if hex is swingable

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
    


def cube_to_axial(cube):
     q = cube.x
     r = cube.z
     return tuple(q, r)

def axial_to_cube(hex):
    x = hex[1]
    z = hex[2]
    y = -x-z
    return tuple(x, y, z)