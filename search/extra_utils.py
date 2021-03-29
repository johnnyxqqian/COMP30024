"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching

This module contains self-written helper functions for calculating board states and action legitimacy.
Simon Chen 1003925
Xue Qiang Qian
"""

from search.swing import *

class RoPaSciState(object):

    def __init__(self, board={}, turn=0):
        self.board = board
        self.turn = turn

    # Game board related functions
    def initialise(self, data):
        """
        Function for first initialisation, using the given JSON data object to create the initial state
        """
        for token, r, q in data['upper']:
            self._insert((r, q), token.upper())

        for token, r, q in data['lower']:
            self._insert((r, q), token)

        for token, r, q in data['block']:
            self._insert((r, q), token)

    def _insert(self, coords, token):
        """
        Inserts token with coords into the RoPaSciState dictionary
        """
        if coords not in self.board.keys():
            self.board[coords] = [token]
        else:
            self.board[coords].append(token)

    def _remove(self, coords, token):
        """
        Removes token with coords out of the RoPaSciState dictionary
        """
        self.board[coords].remove(token)
        if self.board[coords] == []:
            del self.board[coords]

    def _update(self, coords, tokens):
        """
        updates the tokens on a given coordinate on RoPaSciState dictionary.
        If given list of tokens is an empty list, deletes the entry from the dictionary
        """
        if tokens == []:
            del self.board[coords]
        else:
            self.board[coords] = tokens

    def list_upper_tokens(self):
        """
        returns a dictionary with coordinates as the key, and a list of tokens as the value for upper team
        """
        result = {}
        for coords, tokens in self.board.items():
            for t in tokens:
                if t in UPPER_TILES:
                    if coords in result.keys():
                        result[coords].append(t)
                    else:
                        result[coords] = [t]
        return result

    def list_lower_tokens(self):
        """
        returns a dictionary with coordinates as the key, and a list of tokens as the value for lower team
        """
        result = {}
        for coords, tokens in self.board.items():
            for t in tokens:
                if t in LOWER_TILES:
                    if coords in result.keys():
                        result[coords].append(t)
                    else:
                        result[coords] = [t]
        return result

    # Hex and movement related functions
    @staticmethod
    def return_neighbouring_hexes(input_coords):
        neighbour_hexes = []
        r_in, q_in = input_coords
        for direction in DIRECTIONS:
            r_add, q_add = direction
            r_new = r_in + r_add
            q_new = q_in + q_add
            neighbour_hexes.append((r_new, q_new))
        return tuple(neighbour_hexes)

    @staticmethod
    def axial_to_cube(coords):
        # coords in the form of (r,q)
        z, x = coords
        y = -x - z
        return x, y, z

    @staticmethod
    def cube_distance(a, b):
        ax, ay, az = a
        bx, by, bz = b
        return (abs(ax - bx) + abs(ay - by) + abs(az - bz)) / 2

    @staticmethod
    def hex_distance(a, b):
        a = RoPaSciState.axial_to_cube(a)
        b = RoPaSciState.axial_to_cube(b)
        return RoPaSciState.cube_distance(a, b)

    @staticmethod
    def legal_board_coords():
        """
        Function returning all hexes that are legal board coordinates
        """
        result = []
        for r in range(-4, +4 + 1):
            for q in range(-4, +4 + 1):
                if RoPaSciState.within_board((r, q)):
                    result.append((r, q))
        return result

    @staticmethod
    def within_board(coords):
        r, q = coords
        if abs(r + q) <= 4:
            return True
        return False

    @staticmethod
    def play_rps(tokens):
        """
        given a list of tokens on the hex, returns the tokens that survive on that hex
        """

        survivors = []

        # tracking unique tokens
        unique_tokens = 0
        unique_token_set = set()

        # if we have more than 2 tokens
        if len(tokens) > 2:
            for token in tokens:

                # check if we come across a new token
                if token.lower() not in unique_token_set:
                    unique_token_set.add(token).lower()
                    unique_tokens+=1
               
                # if we R,P and S, no tokens survive
                if unique_tokens == len(LOWER_TILES):
                    return []

        for i in range(len(tokens)-1):
            if RPS_OUTCOMES(tokens[i], tokens[i+1]):
                survivors.append(tokens[i])
            
        return survivors

    @staticmethod
    def neighbour_hexes(coords):
        r, q = coords
        return [(r + r_move, q + q_move) for (r_move, q_move) in DIRECTIONS]

    def is_blocked(self, b):
        if BLOCKED in self.board[b]:
            return True
        return False

    def is_legal_slide(self, a, b):
        """
        Checks if a slide is legal according to 3 rules:
        1. The movement is hex distance 1
        2. The movement is within the board boundaries
        3. The target hex is not blocked
        """
        if self.hex_distance(a, b) == SLIDE_DISTANCE:
            return False
        if not self.within_board(b):
            return False
        if self.is_blocked(b):
            return False
        return True

    def apply_move(self, a, b, token):
        """
        Moves a token from hex a > hex b in the game dictionary.
        Does not check if such move is legal.
        """
        self._remove(a, token)
        self._insert(b, token)

    def take_turn(self, moves):
        new_state = RoPaSciState(board=self.board, turn=self.turn + 1)
        for a, b, t in moves:
            new_state.apply_move(a, b, t)
        new_state.resolve_battles()
        return new_state

    def list_legal_moves(self, base_hex):
        """
        Given the current board state, returns a list of all possible moves that can be made from hex a
        1. iterates through all neighbouring hexes and checks legality. If legal, append to result
        2. if there is a friendly token on a neighbouring hex, checks the legality of swing movements and appends
        """
        result = []
        # r, q = a
        # checks neighbouring hexes and if a slide is legal
        for neighbour in self.neighbour_hexes((r, q)):
            if self.is_legal_slide((r, q), neighbour):
                result.append(neighbour)

        neighbours = self.return_neighbouring_hexes(base_hex)
        for hex in swingable_hex_check(base_hex, self.board, neighbours):
            if self.within_board(hex) and not self.is_blocked(hex):
                result.append(hex)

        return tuple(result)

    def resolve_battles(self):
        """
        Looks at board state and calls play_rps on all hexes which have two or more tokens on them
        """
        for coords, tokens in self.board.items():
            if len(tokens) > 1:
                survivors = self.play_rps(tokens)
            self._update(coords, survivors)

    def heuristic(self):
        pass


## Move
# Given piece position, move from hex 1 to 2

# Coordinate template (r, q)
# Token is "R", "P", "S", "r", "p", "s"

### TODO:


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
