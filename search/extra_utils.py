"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching

This module contains self-written helper functions for calculating board states and action legitimacy.
Simon Chen 1003925
Xue Qiang Qian
"""

from search.swing import *
from search.init import *
from search.util import *
from copy import deepcopy


# import importlib
# importlib.import_module("extra_utils")
# importlib.import_module("util")
# importlib.import_module("swing")
# importlib.import_module("minHeap")
# importlib.import_module("init")

class RoPaSciState(object):

    def __init__(self, board={}, turn=0):
        self.board = board
        self.turn = turn
        self.cost = self.heuristic()
        self.move_history = []
        self.board_history = []

    def is_solved(self):
        return len(self.board_dict_to_iterable(self.list_lower_tokens())) == 0

    def is_lost(self):
        # a board state is lost if enemy tokens are unbeatable.
        # for enemy token, append token to a set
        upper_tokens = []
        lower_tokens = []

        for t, r, q in self.board_dict_to_iterable(self.list_lower_tokens()):
            lower_tokens.append(t)

        for t, r, q in self.board_dict_to_iterable(self.list_upper_tokens()):
            upper_tokens.append(t.lower())
        lower_tokens = set(lower_tokens)

        for unique_token in lower_tokens:
            if BEATEN_BY[unique_token] not in upper_tokens:
                return True

        return False

        # checks if for every unique enemy token type, there is the corresponding token on the other team

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

        self.update_cost()

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
            # if len(tokens)>1:
            
            for t in tokens:
                if t in LOWER_TILES:
                    if coords in result.keys():
                        result[coords].append(t)
                    else:
                        result[coords] = [t]
            # else:
            #     if tokens in LOWER_TILES:
            #         if coords in result.keys():
            #             result[coords].append(tokens)
            #         else:
            #             result[coords] = [tokens]
                
                
        return result

    @staticmethod
    def board_dict_to_iterable(board_dict):
        """
        Given a RoPaSci Board dict, converts it into an iterable in the form of a tuple.
        Result is of the form (t, r, q) where:
        t: token in character format
        r: axial row
        q: axial column
        """
        result = []
        for coords, tokens in board_dict.items():
            r, q = coords
            for token in tokens:
                result.append((token, r, q))
        return result

    # Hex and movement related functions

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
        if abs(r + q) > 4:
            return False
        if abs(r) > 4:
            return False
        if abs(q) > 4:
            return False
        return True

    @staticmethod
    def play_rps(tokens):
        """
        given a list of tokens on the hex, returns the tokens that survive on that hex
        """

        survivors = []

        # to determine which tokens are on the board
        token_set = set([t.lower() for t in tokens])

        # all 3 tokens in which case all destroyed
        if (len(token_set) == len(LOWER_TILES)):
            return survivors

        # only 1 token
        if len(token_set) == 1:
            return tokens

        # more than 1 token in which case we determine the winning token

        winning_token = list(token_set)[0] if RPS_OUTCOMES[list(token_set)[0], list(token_set)[1]] else list(token_set)[
            1]

        for token in tokens:
            if (token == winning_token) or (token == winning_token.upper()):
                survivors.append(token)

        return survivors

    @staticmethod
    def neighbour_hexes(coords):
        r, q = coords
        return [(r + r_move, q + q_move) for (r_move, q_move) in DIRECTIONS]

    def update_cost(self):
        self.cost = self.heuristic()

    def is_blocked(self, b):
        if b in self.board.keys() and BLOCKED in self.board[b]:
            return True
        return False

    def is_legal_slide(self, a, b):
        """
        Checks if a slide is legal according to 3 rules:
        1. The movement is hex distance 1
        2. The movement is within the board boundaries
        3. The target hex is not blocked
        """
        if not self.within_board(b):
            return False
        if self.hex_distance(a, b) > SLIDE_DISTANCE:
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
        """
        applies the moves, increments the turn, and records all moves.
        Returns the resulting new board state.
        """
        self.turn += 1
        self.board_history.append(deepcopy(self.board))
        for a, b, t in moves:
            self.apply_move(a, b, t)
            self.move_history.append((a, b, t, self.turn))
        self.resolve_battles()
        self.update_cost()

    def list_legal_moves(self, base_hex):
        """
        Given the current board state, returns a list of all possible moves that can be made from hex a
        1. iterates through all neighbouring hexes and checks legality. If legal, append to result
        2. if there is a friendly token on a neighbouring hex, checks the legality of swing movements and appends
        """
        result = []
        # r, q = a
        # checks neighbouring hexes and if a slide is legal
        
        neighbours = self.neighbour_hexes(base_hex)
        
        for neighbour in neighbours:
            if self.is_legal_slide(base_hex, neighbour):
                result.append(neighbour)

        
        for hex in swingable_hex_check(base_hex, self.board, neighbours):
            if self.within_board(hex) and not self.is_blocked(hex):
                result.append(hex)
        
        return tuple(result)

    def resolve_battles(self):
        """
        Looks at board state and calls play_rps on all hexes which have two or more tokens on them
        """
        updates = []
        for coords, tokens in self.board.items():
            # print("coords = ", coords , "tokens =", tokens)
            if len(tokens) > 1:
                survivors = self.play_rps(tokens)
                updates.append((coords, survivors))

        if updates:
            for update in updates:
                coords, survivors = update
                self._update(coords, survivors)

    def heuristic(self):

        lower_token_cost = ENEMY_TOKEN_COST * len(RoPaSciState.board_dict_to_iterable(self.list_lower_tokens()))
        distances = []

        # iterating over upper tokens
        for token, r, q in RoPaSciState.board_dict_to_iterable(self.list_upper_tokens()):

            least_dist = MAX_DIST + 1

            # iterating over enemy tokens
            for target_t, target_r, target_q in RoPaSciState.board_dict_to_iterable(self.list_lower_tokens()):

                # increase cost to account for prioritisation of eating enemy tokens

                dist = self.hex_distance((r, q), (target_r, target_q))

                # checking if our token can beat the enemy token and the distance has reduced
                if RPS_OUTCOMES[token.lower(), target_t.lower()] and dist < least_dist:
                    least_dist = dist
                    distances.append(least_dist)

            if least_dist == MAX_DIST + 1:
                continue

            distances.append(least_dist)

        return (lower_token_cost + sum(distances))

        # for each our token:
        # calculate distance to every other ENEMY token
        # for each of our tokens that can beat an enemy token (i.e. max(#lowerTokens))
        # have each token move closer to its assigned enemy token based off next least distance
        # if move involves suicide -> go next best / ignore this move

        # for each of our tokens:
        # calculate distance to every other ENEMY token our token can beat
        # return sum of distances


## Move
# Given piece position, move from hex 1 to 2

# Coordinate template (r, q)
# Token is "R", "P", "S", "r", "p", "s"

def unit_test():
    board = {(1, 2): ['R'],
             (2, 2): ['P'],
             (0, 1): ['s']}
    game = RoPaSciState(board=board)

    print(game.heuristic())

    print("DEBUG")
