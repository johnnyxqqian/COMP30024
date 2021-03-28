"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching

This module contains self-written helper functions for calculating board states and action legitimacy.
Simon Chen 1003925
Xue Qiang Qian
"""

# Movement
directions = (
    (1, 0),
    (1, 0),
    (0, 1),
    (0, -1),
    (-1, 1),
    (-1, 0)
)


def return_neighbouring_hexes(input_coords):
    neighbour_hexes = []
    r_in, q_in = input_coords
    for direction in directions:
        r_add, q_add = direction
        r_new = r_in + r_add
        q_new = q_in + q_add
        neighbour_tiles.append((r_new, q_new))
    return tuple(neighbour_hexes)


def axial_to_cube(coords):
    # coords in the form of (r,q)
    z, x = coords
    y = -x - z
    return x, y, z


def cube_distance(a, b):
    ax, ay, az = a
    bx, by, bz = b
    return (abs(ax - bx) + abs(ay - by) + abs(az - bz)) / 2


def hex_distance(a, b):
    a = axial_to_cube(a)
    b = axial_to_cube(b)
    return cube_distance(a, b)


def legal_board_coords():
    """
    Function returning all hexes that are legal board coordinates
    """
    result = []
    for r in range(-4, 5):
        for q in range(-4, 5):
            if within_board((r, q)):
                result.append((r, q))
    return result


def within_board(coords):
    r, q = coords
    if abs(r + q) <= 4:
        return True
    return False


## Move
# Given piece position, move from hex 1 to 2

# Coordinate template (r, q)
# Token is "R", "P", "S", "r", "p", "s"

### TODO:

### Swing Function (Check)
# Is there an adjacent friendly token?
# Look at opposite hexes that are not adjacent
# Are they legal hexes?
# If so, it is legal

def legal_slide(a, b):
    if hex_distance(a, b) > 1:
        return False
    if not within_board(b):
        return False
    # Todo implement block checking
    return True


from heapq import heappush, heappop, heapify


# Todo
# add credit for this code
# Convert this class to account for board state and their cost values
# A class for Min Heap
class MinHeap:

    # Constructor to initialize a heap
    def __init__(self):
        self.heap = []

    def parent(self, i):
        return (i - 1) / 2

    # Inserts a new key 'k'
    def insertKey(self, k):
        heappush(self.heap, k)

        # Decrease value of key at index 'i' to new_val

    # It is assumed that new_val is smaller than heap[i]
    def decreaseKey(self, i, new_val):
        self.heap[i] = new_val
        while (i != 0 and self.heap[self.parent(i)] > self.heap[i]):
            # Swap heap[i] with heap[parent(i)]
            self.heap[i], self.heap[self.parent(i)] = (
                self.heap[self.parent(i)], self.heap[i])

    # Method to remove minium element from min heap
    def extractMin(self):
        return heappop(self.heap)

    # This functon deletes key at index i. It first reduces
    # value to minus infinite and then calls extractMin()
    def deleteKey(self, i):
        self.decreaseKey(i, float("-inf"))
        self.extractMin()

### Win/Lose Condition State Checking
