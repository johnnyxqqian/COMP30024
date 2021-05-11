"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching

This module contains a RoPaSci object which contains data about the board
Simon Chen 1003925
Xue Qiang Qian 1081725
"""

from copy import deepcopy

from .consts import *


class RoPaSciState(object):

    # constructor
    def __init__(self, board={}, turn=0):
        """
        Instantiates a RoPaSciState object
        """
        self.board = board
        self.turn = turn
        self.throws = {UPPER: 9, LOWER: 9}

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

    def list_tokens(self, side):
        """
        Returns a dictionary with coordinates as the key, and a list of tokens as the value for the given team/
        side = {'upper', 'lower'}
        """
        result = {}

        # whats the str?
        if side == UPPER:
            is_side = str.isupper
        else:
            is_side = str.islower

        for coords, tokens in self.board.items():
            for t in tokens:
                if is_side(t):
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

    def is_legal_slide(self, base, target):
        """
        Checks if a slide is legal according to 3 rules:
        1. The movement is hex distance 1
        2. The movement is within the board boundaries
        """
        if not self.within_board(target):
            return False
        if self.hex_distance(base, target) > SLIDE_DISTANCE:
            return False
        return True

    def apply_move(self, base, target, token):
        """
        Moves a token from hex base > hex target in the game dictionary.
        Does not check if such move is legal.
        For a throw, pass base=None
        """
        if base:
            self._remove(base, token)
        self._insert(target, token)

    def take_turn(self, player_move, opponent_move, player_side):
        """
        applies the moves, increments the turn, and records all moves.
        Returns the resulting new board state.
        """

        # throws in the form ("THROW", s, (r, q))
        # slide/swings in the form (atype, (ra, qa), (rb, qb))
        self.turn += 1
        #self.board_history.append(deepcopy(self.board))

        # process player move
        if player_side == UPPER:
            to_player_case = str.upper
            to_opp_case = str.lower
            opp_side = LOWER
        else:
            to_player_case = str.lower
            to_opp_case = str.upper
            opp_side = UPPER

        if player_move:
            if player_move[0] == 'THROW':
                self.throws[player_side] -= 1
                self.apply_move(
                    None, player_move[2], to_player_case(player_move[1]))
            else:
                self.apply_move(player_move[1],
                                player_move[2],
                                self.board[player_move[1]][0])

        if opponent_move:
            if opponent_move[0] == 'THROW':
                self.throws[opp_side] -= 1
                self.apply_move(None,
                                opponent_move[2],
                                to_opp_case(opponent_move[1]))
            else:
                self.apply_move(opponent_move[1],
                                opponent_move[2],
                                self.board[opponent_move[1]][0])

        self.resolve_battles()

    def list_legal_moves(self, base_hex, side):
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
                result.append(("SLIDE", neighbour))

        for tile in self.swingable_hex_check(base_hex, self.board, neighbours, side):
            if self.within_board(tile):
                result.append(("SWING", tile))

        return result

    def resolve_battles(self):
        """
        Looks at board state and calls play_rps on all hexes which have two or more tokens on them
        """
        updates = []
        for coords, tokens in self.board.items():
            if len(tokens) > 1:
                survivors = self.play_rps(tokens)
                updates.append((coords, survivors))

        if updates:
            for update in updates:
                coords, survivors = update
                self._update(coords, survivors)

    def heuristic(self):
        """
        Calculates the heuristic. Currently takes 2 factors:
        1. absolute hex distance (minimum hex distance) from each
        """

        # determining cost of remaining Lower tokens
        lower_token_cost = ENEMY_TOKEN_COST * \
            len(self.board_dict_to_iterable(self.list_lower_tokens()))
        distances = []

        # iterating over upper tokens
        for token, r, q in self.board_dict_to_iterable(self.list_upper_tokens()):

            min_dist = MAX_DIST + 1

            # iterating over lower tokens
            for target_t, target_r, target_q in self.board_dict_to_iterable(self.list_lower_tokens()):

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

    @staticmethod
    def has_friendly_tile(neighbours, side):
        tile_set = UPPER_TILES if side == UPPER else LOWER_TILES
        for tiles in neighbours:
            if tiles in tile_set:
                return True
        return False

    # identifies swingable & landable tiles
    def swingable_hex_check(self, current_tile, board, neighbours, side):
        target_tiles = []
        tile_set = UPPER_TILES if side == UPPER else LOWER_TILES

        for neighbour in neighbours:
            if neighbour in board.keys():
                for token in board[neighbour]:
                    if token in tile_set:

                        # list of 3-tuples, order is same as swing_tiles so we can trace them
                        for tile in (self.target_hex_coordinates(current_tile, neighbour)):
                            target_tiles.append(tile)
                            break

        return list(set(target_tiles))

    # returns 3-tuple of target tiles resulting from a swing
    # does not check if tuples are valid
    @staticmethod
    def target_hex_coordinates(base_tile, target_tile):
        base_q = base_tile[Q_INDEX]
        base_r = base_tile[R_INDEX]
        target_q = target_tile[Q_INDEX]
        target_r = target_tile[R_INDEX]

        direction = (target_r - base_r, target_q - base_q)
        dir_r, dir_q = direction
        target_anchor = (target_r + dir_r, target_q + dir_q)

        for i in range(NUM_DIRECTIONS):
            if direction == DIRECTIONS[i]:
                target_clockwise = (
                    target_r + DIRECTIONS[i - 1][R_INDEX], target_q + DIRECTIONS[i - 1][R_INDEX])
                target_anticlockwise = (
                    target_r + DIRECTIONS[0][R_INDEX],
                    target_q + DIRECTIONS[0][Q_INDEX]) if i >= NUM_DIRECTIONS - 1 else (
                    target_r +
                    DIRECTIONS[i + 1][R_INDEX], target_q +
                    DIRECTIONS[i + 1][Q_INDEX]
                )

        if target_anchor == target_tile:
            return [target_clockwise, target_anticlockwise]

        else:
            return [target_anchor, target_clockwise, target_anticlockwise]

    def possible_throws(self, side):

        if side == UPPER:
            throw_range = range(4-9+self.throws[UPPER], +4+1)

        else: # Side is lower
            throw_range = range(-4, -4+10-self.throws[LOWER])

        hex_range = range(-4, +4+1)
        possible_hexes = [
            (r, q) for r in throw_range for q in hex_range if -r - q in hex_range]

        return possible_hexes


def unit_test():
    board = {(1, 2): ['R'],
             (2, 2): ['P'],
             (0, 1): ['s']}
    game = RoPaSciState(board=board)

    # print(game.heuristic())

    # print("DEBUG"
