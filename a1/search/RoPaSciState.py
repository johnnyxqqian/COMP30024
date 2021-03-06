"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching

This module contains a RoPaSci object which contains data about the board
Simon Chen 1003925
Xue Qiang Qian 1081725
"""

from search.swing import *
from search.init import *
from search.util import *

from copy import deepcopy


class RoPaSciState(object):

    # constructor
    def __init__(self, board={}, turn=0):
        """
        Instantiates a RoPaSciState object
        """
        self.board = board
        self.turn = turn
        self.cost = self.heuristic()
        self.move_history = []
        self.board_history = []

    def is_solved(self):
        """
        Function returning all tiles that are legal board coordinates
        """
        return len(self.board_dict_to_iterable(self.list_lower_tokens())) == 0

    def is_lost(self):
        """
        Checks if a board state is lost
        """
        # a board state is lost if enemy tokens are unbeatable.
        upper_tokens = []
        lower_tokens = []

        for t, r, q in self.board_dict_to_iterable(self.list_lower_tokens()):
            lower_tokens.append(t)

        for t, r, q in self.board_dict_to_iterable(self.list_upper_tokens()):
            upper_tokens.append(t.lower())

        # determining unique lower tokens
        lower_tokens = set(lower_tokens)

        for unique_token in lower_tokens:
            if BEATEN_BY[unique_token] not in upper_tokens:
                return True

        return False

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
        Updates the tokens on a given coordinate on RoPaSciState dictionary.
        If given list of tokens is an empty list, deletes the entry from the dictionary
        """
        if tokens == []:
            del self.board[coords]
        else:
            self.board[coords] = tokens

    def list_upper_tokens(self):
        """
        Returns a dictionary with coordinates as the key, and a list of tokens as the value for upper team
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
        Returns a dictionary with coordinates as the key, and a list of tokens as the value for lower team
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

        """ 
        Takes coordinates in axial form and returns them in cube form.
        Function taken from: https://www.redblobgames.com/grids/hexagons/
        """
        # coords in the form of (r,q)
        z, x = coords
        y = -x - z
        return x, y, z

    @staticmethod
    def cube_distance(base, target):

        """ 
        Returns distance between two coordiantes in cube form
        Function taken from: https://www.redblobgames.com/grids/hexagons/
        """
        base_x, base_y, base_z = base
        target_x, target_y, target_z = target
        return (abs(base_x - target_x) + abs(base_y - target_y) + abs(base_z - target_z)) / 2

    @staticmethod
    def hex_distance(base, target):
        """ 
        Returns distance between two coordiantes in hex form
        Function taken from: https://www.redblobgames.com/grids/hexagons/
        """
        base = RoPaSciState.axial_to_cube(base)
        target = RoPaSciState.axial_to_cube(target)
        return RoPaSciState.cube_distance(base, target)

    @staticmethod
    def legal_board_coords():
        """
        Returns all tiles that are legal board coordinates
        """
        result = []
        for r in range(-4, +4 + 1):
            for q in range(-4, +4 + 1):
                if RoPaSciState.within_board((r, q)):
                    result.append((r, q))
        return result

    @staticmethod
    def within_board(coords):
        """
        Determines whether a coordinate is within the game board
        """
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
        Given a list of tokens on the hex, returns the tokens that survive on that hex
        """

        survivors = []

        # to determine which tokens are on the board
        token_set = set([t.lower() for t in tokens])

        # all 3 tokens in which case all destroyed
        if len(token_set) == len(LOWER_TILES):
            return survivors

        # only 1 token so no battle occurs
        if len(token_set) == 1:
            return tokens

        # more than 1 token in which case we determine the winning token
        winning_token = list(token_set)[0] if RPS_OUTCOMES[list(token_set)[0], list(token_set)[1]] else list(token_set)[
            1]

        # recording which tokens win
        for token in tokens:
            if (token == winning_token) or (token == winning_token.upper()):
                survivors.append(token)

        return survivors

    @staticmethod
    def neighbour_hexes(coords):
        """
        Function returning all neighbouring hexes
        """
        r, q = coords
        return [(r + r_move, q + q_move) for (r_move, q_move) in DIRECTIONS]

    def update_cost(self):
        """
        Function returning all tiles that are legal board coordinates
        """
        self.cost = self.heuristic()

    def is_blocked(self, tile):
        if tile in self.board.keys() and BLOCKED in self.board[tile]:
            return True
        return False

    def is_legal_slide(self, base, target):
        """
        Checks if a slide is legal according to 3 rules:
        1. The movement is hex distance 1
        2. The movement is within the board boundaries
        3. The target hex is not blocked
        """
        if not self.within_board(target):
            return False
        if self.hex_distance(base, target) > SLIDE_DISTANCE:
            return False
        if self.is_blocked(target):
            return False
        return True

    def apply_move(self, base, target, token):
        """
        Moves a token from hex base > hex target in the game dictionary.
        Does not check if such move is legal.
        """
        self._remove(base, token)
        self._insert(target, token)

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

        return result

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
        """
        Function returning all tiles that are legal board coordinates
        """

        # determing cost of remaining Lower tokens
        lower_token_cost = ENEMY_TOKEN_COST * len(RoPaSciState.board_dict_to_iterable(self.list_lower_tokens()))
        distances = []

        # iterating over upper tokens
        for token, r, q in RoPaSciState.board_dict_to_iterable(self.list_upper_tokens()):

            min_dist = MAX_DIST + 1

            # iterating over lower tokens
            for target_t, target_r, target_q in RoPaSciState.board_dict_to_iterable(self.list_lower_tokens()):

                # hex distance
                dist = self.hex_distance((r, q), (target_r, target_q))

                # checking if our token can beat the enemy token and if a lower distance has been found
                if RPS_OUTCOMES[token.lower(), target_t.lower()] and dist < min_dist:
                    min_dist = dist

            # no beatable lower tokens remain - we do not add into distance
            if min_dist == MAX_DIST + 1:
                continue

            distances.append(min_dist)

        return lower_token_cost + sum(distances)


def unit_test():
    board = {(1, 2): ['R'],
             (2, 2): ['P'],
             (0, 1): ['s']}
    game = RoPaSciState(board=board)

    # print(game.heuristic())

    # print("DEBUG"
