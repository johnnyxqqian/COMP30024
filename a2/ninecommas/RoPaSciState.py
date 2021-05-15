"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching

This module contains a RoPaSci object which contains data about the board
Simon Chen 1003925
Xue Qiang Qian 1081725
"""

from copy import deepcopy
from .consts import *
import numpy as np


class RoPaSciState(object):

    # constructor
    def __init__(self, board={}, turn=0):
        """
        Instantiates a RoPaSciState object
        """
        self.board = board
        self.turn = turn
        self.throws = {UPPER: 9, LOWER: 9}
        self.board_history = {}

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

        # boardkey = hash(frozenset(self.board.items()))

        # if boardkey in self.board_history.keys():
        #    self.board_history[boardkey] += 1
        # else:
        #    self.board_history[boardkey] = 1

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
                                self.list_tokens(player_side)[player_move[1]][0])

        if opponent_move:
            if opponent_move[0] == 'THROW':
                self.throws[opp_side] -= 1
                self.apply_move(None,
                                opponent_move[2],
                                to_opp_case(opponent_move[1]))
            else:
                self.apply_move(opponent_move[1],
                                opponent_move[2],
                                self.list_tokens(opp_side)[opponent_move[1]][0])

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

    def heuristic(self, side):
        """
        Gives us the heuristic value for the given side. Higher = Better for the passed in side, Lower = Worse
        """

        enemy = LOWER if side == UPPER else UPPER
        payoff = 0

        # feature 1: # our remaining tokens

        # A throw is more valuable than a token on board
        payoff += COST_SELF_TOKEN * len(self.list_tokens(side))
        payoff += COST_THROW_TOKEN * self.throws[side]

        # feature 2: # enemy tokens
        payoff -= COST_ENEMY_TOKEN * len(self.list_tokens(enemy))
        payoff -= COST_THROW_TOKEN * self.throws[enemy]

        # print("cost pre-matrix = ", payoff)
        # feature 3: distance of tokens from prey / predator
        pred = np.zeros((9, 9))
        i = j = 0

        for token, r, q in self.board_dict_to_iterable(self.list_tokens(side)):
            j = 0
            min_lose_dist = min_dist = 100000
            e_token_index = lose_e_token_index = 0

            for target_t, target_r, target_q in self.board_dict_to_iterable(self.list_tokens(enemy)):

                # least distance to beatable enemy token
                dist = self.hex_distance((r, q), (target_r, target_q))

                if BEATS_WHAT[token.lower()] == target_t.lower():

                    if dist < min_dist:
                        min_dist = dist
                        e_token_index = j


                elif token.lower() == target_t.lower():
                    pred[i][j] == 0

                else:

                    if dist < min_lose_dist:
                        min_lose_dist = dist
                        lose_e_token_index = j

                j += 1

            pred[i][e_token_index] = 1 * (1 / min_dist)
            pred[i][lose_e_token_index] = (-1) * (1 / min_lose_dist)
            i += 1

        #print(pred)
        print(np.sum(pred * 5))
        # need to factor in throws increaing the cost
        payoff += np.sum(pred * 5)

        return payoff

        # print("payoff post matrix - ", payoff)


        p_throws = 9 - self.throws[side]
        lo_throws = 9 - self.throws[enemy]

        # should this just be s?
        p_tokens = [
            s.lower() for x in self.board.values() for s in x if s.isupper()
        ]

        e_tokens = [
            s for x in self.board.values() for s in x if s.islower()
        ]

        p_symset = set(p_tokens)
        e_symset = set(e_tokens)

        p_invinc = [
            s for s in p_symset
            if (lo_throws == 0) and (WHAT_BEATS[s] not in e_symset)
        ]
        e_invinc = [
            s for s in e_symset
            if (p_throws == 0) and (WHAT_BEATS[s] not in p_symset)
        ]

        p_notoks = (p_throws == 0) and (len(p_tokens) == 0)
        e_notoks = (lo_throws == 0) and (len(e_tokens) == 0)
        p_onetok = (p_throws == 0) and (len(p_tokens) == 1)
        e_onetok = (lo_throws == 0) and (len(e_tokens) == 1)

        # condition 1: one player has no remaining throws or tokens
        if p_notoks and e_notoks:
            return COST_DRAW
        if p_notoks:
            return COST_WIN * (-1)
        if e_notoks:
            return COST_WIN

        # condition 2: both players have an invincible token
        if p_invinc and e_invinc:
            return COST_DRAW

        # condition 3: one player has an invincible token, the other has
        #              only one token remaining (not invincible by 2)
        if p_invinc and e_onetok:
            return COST_WIN
        if e_invinc and p_onetok:
            return COST_WIN * (-1)

        # condition 4: the same state has occurred for a 3rd time
        #         if self.history[state] >= 3:
        #             return COST_DRAW

        # condition 5: the players have had their 360th turn without end
        if self.turn >= MAX_TURNS:
            return COST_DRAW

        """
        # feature 3: invincible tokens
        for side in ["upper", "lower"]:
            invinc = p_invinc if side == UPPER else e_invinc
            throws = lo_throws if side == UPPER else p_throws
            side_flag = 1 if side == UPPER else -1

            # 1 invincible token
            payoff += COST_INVINC * \
                    side_flag if (len(p_invinc) == 1 and lo_throws == 0) else 0

            # 2 invincible tokens
            payoff += COST_DOUB_INVIC * \
                    side_flag if (len(invinc) == 2 and throws < 2) else 0

        # if enenmy neighbour, check if beatable
        # if friendly neighbour, increase cost
        # to confirm with simon

        """

        """
        visited=set()
        for token, r, q in self.board_dict_to_iterable(self.list_tokens(side)):
            neighbours = neighbour_hexes((r, q))
            neighbourset = set()
            for neighbour in neighbours:
                if neighbour in board_state.board.keys() and neighbour not in visited:

                    # friendly token
                    if token.isupper() and self.board[neighbour].isupper():
                        cost += COST_FRIENDLY_NEIGHBOUR
                    elif token.islower() and self.board[neighbour].islower():
                        cost -= COST_FRIENDLY_NEIGHBOUR

                    # enemy token
                    else:
                        # enemy neighbour we can lose to
                        if _WHAT_BEATS[token] == self.board[neighbour].lower():
                            cost -= COST_BNEIGHBOUR * side_flag

                        # enemy neighbour we can beat
                        elif _BEATS_WHAT[token] == self.sate.board[neighbour].lower():
                            cost += COST_GNEIGHBOUR * side_flag

                        # enemy neighbour is the same token
                        else:
                            cost += 0
                    visited.add(neighbour)
            """
        # print("cost at end", payoff)
        return payoff

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
        if self.throws[side] == 0:
            return []

        if side == UPPER:
            throw_range = range(4 - 9 + self.throws[UPPER], +4 + 1)

        else:  # Side is lower
            throw_range = range(-4, -4 + 10 - self.throws[LOWER])

        hex_range = range(-4, +4 + 1)
        possible_hexes = [
            (r, q) for r in throw_range for q in hex_range if self.within_board((r,q))]

        return possible_hexes

    def possible_moves(self, side):
        possible_moves = []
        for t, r, q in self.board_dict_to_iterable(self.list_tokens(side)):
            legal_moves = self.list_legal_moves((r, q), side)
            for legal_move in legal_moves:
                move = (legal_move[0], (r, q), legal_move[1])
                possible_moves.append(move)

        if side == UPPER:
            token_set = UPPER_TILES
        else:
            token_set = LOWER_TILES

        for t in token_set:
            for tile in self.possible_throws(side):
                move = ("THROW", t.lower(), tile)
                possible_moves.append(move)

        return possible_moves


def unit_test():
    board = {(1, 2): ['R'],
             (2, 2): ['P'],
             (0, 1): ['s']}
    game = RoPaSciState(board=board)

    # print(game.heuristic())

    # print("DEBUG"
