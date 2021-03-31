# contains logic related to swing actions

from search.init import *

def has_friendly_tile(neighbours):
    for tiles in neighbours:
        if tiles in UPPER_TILES:
            return True
    return False

# identifies swingable & landable tiles
def swingable_hex_check(current_tile, board, neighbours):
    target_tiles = []

    for neighbour in neighbours:
        if neighbour in board.keys():
            for token in board[neighbour]:
                if token in UPPER_TILES:

                    # list of 3-tuples, order is same as swing_tiles so we can trace them
                    for tile in (target_hex_coordinates(current_tile, neighbour)):
                        target_tiles.append(tile)
                        break

    return list(set(target_tiles))
    
# returns 3-tuple of target tiles resulting from a swing
# does not check if tuples are valid
def target_hex_coordinates(base_tile, target_tile):
    base_q = base_tile[Q_INDEX]
    base_r = base_tile[R_INDEX]
    target_q = target_tile[Q_INDEX]
    target_r = target_tile[R_INDEX]
    
    direction = (target_r - base_r, target_q - base_q)
    dir_r, dir_q = direction
    target_anchor = (target_r + dir_r, target_q + dir_q)
    
    for i in range(NUM_DIRECTIONS):
        if(direction == DIRECTIONS[i]):
            target_clockwise = (target_r+DIRECTIONS[i-1][R_INDEX], target_q+DIRECTIONS[i-1][R_INDEX])
            target_anticlockwise = (target_r+ DIRECTIONS[0][R_INDEX], target_q+ DIRECTIONS[0][Q_INDEX])  if i >= NUM_DIRECTIONS-1 else (target_r + DIRECTIONS[i+1][R_INDEX]
    , target_q + DIRECTIONS[i+1][Q_INDEX]
    )

    if target_anchor == target_tile:   
        return [target_clockwise, target_anticlockwise]
    
    else:
        return [target_anchor, target_clockwise, target_anticlockwise]
    

            
        