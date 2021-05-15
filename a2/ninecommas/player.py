from .RoPaSciState import *
from .consts import *
from random import choice
import sys
import numpy as np
import scipy.optimize as opt
import random
import time


class OptimisationError(Exception):
    """For if the optimiser reports failure."""


class Player:
    def __init__(self, player):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "upper" (if the instance will
        play as Upper), or the string "lower" (if the instance will play
        as Lower).
        """
        self._side = player

        if player == UPPER:
            self._opponent = LOWER
        else:
            self._opponent = UPPER

        print(f"Game passed in {player} side, we assigned {self._side} as us, and {self._opponent} as opponent ")

        self._game = RoPaSciState()
        # put your code here

    """
    def minmax(self, state, moves, depth, side):
        # iterate through (move)

        if depth == 0:
            value = state.heuristic()
            return value

        # Generate possible moves
        for possible_move in moves:

            # Pick a "Best" opposing move
            # Apply our possible and enemy "best" move
            # Get a new state

            if side == UPPER:

                # If upper, we want our heuristic to be lower
                criteria = min

                # Pick an opposing move
                #

                return

            elif side == LOWER:

                # If lower, we want our heuristic to be higher
                criteria = max

                return

        # new_state = deepcopy(self._game)
        # new_state.take_turn(possible_move, None, self._side)
        best_move = None
        return best_move

    # TODO
    # func Minimax Algorithm
    #   For each self move(combinatoric)
    #       If terminal node ( depth limit reached or game over ):
    #           return heuristic
    #       elif self.side = upper:
    #           // we want to be minimising our heuristic score
    #           return min(value, func minimax)
    #       elif self.side = lower
    #           // we want to be maximising our heuristic score
    #           return max (value, func minimax)
    """

    """
    def min(self, alpha: int = -sys.maxsize, beta: int = sys.maxsize, depth: int = 0):
        if (depth > MAX_DEPTH):
            return self._game.heuristic()

        for move in self.possible_moves():
            beta = min(beta, max(alpha, beta, depth + 1))

        if beta < alpha:
            return alpha

        return beta

    def max(self, alpha: int = -sys.maxsize, beta: int = sys.maxsize, depth: int = 0):
        # Variables

        if (depth > MAX_DEPTH):
            return self._game.heuristic()

        poss_moves = self.possible_moves()

        for move in poss_moves:
            alpha = max(alpha, min(alpha, beta, depth + 1))

        if alpha > beta:
            return alpha

        return beta

    def mini_max(self):
        best_val = 0
        best_mov = None

        # need enemy moves

        for move in self.possible_moves(self._side):
            new_state = deepcopy(self._game)

            # minimax of our move
            val = self.minimax_value(new_state.take_turn(move, None, self._side), 0)

            if val > best_val:
                best_val = val
                best_mov = move

        return best_mov

    def minimax_value(self, move, depth, side):
        max_cost = 0
        min_cost = 0

        # cut-off
        if depth > MAX_DEPTH:
            return self._game.heurisitc()

        # max = upper
        # not sure if this makes sense
        # not sure if this makes sense

        elif self._side == UPPER:
            for move in self.possible_moves():
                cost = self.minimax_value(move, depth + 1)
                if cost > max_cost:
                    max_cost = cost
            return max_cost

        else:
            for move in self.possible_moves():
                cost = self.minimax_value(move, depth + 1)
                if cost < min_cost:
                    min_cost = cost
            return min_cost
    """

    def adverserial(self):

        optimal_move_p, exp_value = self.backprop(self._game, 0)
        print('optimal = ', optimal_move_p)
        return optimal_move_p

    def backprop(self, game=None, depth=0):

        if depth > MAX_DEPTH:
            temp = 1 if self._side == UPPER else -1
            return None, self._game.heuristic(self._side) * temp

        enemy_side = "upper" if self._side == LOWER else LOWER
        # possible moves for player & enemy
        # player_moves = random.sample(game.possible_moves(self._side), 5)
        possible_player_moves = game.possible_moves(self._side)
        # player_moves = random.sample(possible_player_moves, len(possible_player_moves))
        player_moves = possible_player_moves
        random.shuffle(player_moves)

        # print("moves = ", player_moves)
        possible_enemy_moves = game.possible_moves(enemy_side)
        enemy_moves = random.sample(possible_enemy_moves, min(len(possible_enemy_moves), 5))

        payoff_matrix = np.zeros((len(player_moves), len(enemy_moves)))

        i = 0
        for p_moves in player_moves:
            j = 0
            if i < 10:
                # replace with limiting branching factor
                for e_moves in enemy_moves:

                    if j < 10:
                        new_state = deepcopy(game)
                        new_state.take_turn(p_moves, e_moves, self._side)
                        a, payoff = self.backprop(new_state, depth + 1)
                        payoff_matrix[i][j] = payoff

                        j += 1
                    else:
                        break

                i += 1

        moves, expected_value = self.solve_game(payoff_matrix)

        move_index_p = np.where(moves == np.amax(moves))[0][0]
        bmove_player = player_moves[move_index_p]
        # move_index_e = np.where(payoff_matrix == np.amin(payoff_matrix[move_index_p]))[0][0]
        # bmove_enemy = enemy_moves[move_index_e]

        # print("player best = ", bmove_player, "exp = ", expected_value, "depth = ", depth, "pmoves = ",
        #   len(player_moves), "emoves = ", len(enemy_moves))
        # print("Shape = ", payoff_matrix.shape)

        return bmove_player, expected_value

    """

    def select_move(self):
        payoff_matrix = np.zeros((self._game.turn, self._game.turn))
        enemy_side = "upper" if self._side == LOWER else LOWER

        # possible moves for player & enemy
        player_moves = self.possible_moves(self._side)
        enemy_moves = self.possible_moves(enemy_side)

        # (n,m) matrix of moves
        i = 0
        for p_moves in player_moves:
            j = 0
            for e_moves in enemy_moves:
                new_state = deepcopy(self._game)
                new_state.take_turn(p_moves, e_moves, self._side)
                payoff = new_state.heuristic()
                payoff_matrix[i][j] = payoff
                j += 1
            i += 1

        moves, expected_value = self.solve_game(payoff_matrix)

        move_index_p = np.amax(moves)
        bmove_player = player_moves[move_index_p]
        move_index_e = np.amin(payoff_matrix[move_index_p])
        bmove_enemy = enemy_moves[move_index_e]

        return bmove_player, bmove_enemy, expected_value

    """

    def solve_game(self, V, maximiser=True, rowplayer=True):
        """
        Given a utility matrix V for a zero-sum game, compute a mixed-strategy
        security strategy/Nash equilibrium solution along with the bound on the
        expected value of the game to the player.
        By default, assume the player is the MAXIMISER and chooses the ROW of V,
        and the opponent is the MINIMISER choosing the COLUMN. Use the flags to
        change this behaviour.

        Parameters
        ----------
        * V: (n, m)-array or array-like; utility/payoff matrix;
        * maximiser: bool (default True); compute strategy for the maximiser.
            Set False to play as the minimiser.
        * rowplayer: bool (default True); compute strategy for the row-chooser.
            Set False to play as the column-chooser.

        Returns
        -------
        * s: (n,)-array; probability vector; an equilibrium mixed strategy over
            the rows (or columns) ensuring expected value v.
        * v: float; mixed security level / guaranteed minimum (or maximum)
            expected value of the equilibrium mixed strategy.

        Exceptions
        ----------
        * OptimisationError: If the optimisation reports failure. The message
            from the optimiser will accompany this exception.
        """
        V = np.asarray(V)
        # lprog will solve for the column-maximiser
        if rowplayer:
            V = V.T
        if not maximiser:
            V = -V
        m, n = V.shape
        # ensure positive
        c = -V.min() + 1
        Vpos = V + c
        # solve linear program
        res = opt.linprog(
            np.ones(n),
            A_ub=-Vpos,
            b_ub=-np.ones(m),
        )
        if res.status:
            raise OptimisationError(res.message)  # TODO: propagate whole result
        # compute strategy and value
        v = 1 / res.x.sum()
        s = res.x * v
        v = v - c  # re-scale
        if not maximiser:
            v = -v
        return s, v

    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """

        ### Generate all possible moves
        # Generate all swings and slides
        max_heur = -1000000
        max_moves = []
        for possible_move in self._game.possible_moves(self._side):
            new_state = deepcopy(self._game)
            new_state.take_turn(possible_move, None, self._side)
            val = new_state.heuristic(self._side)
            if val > max_heur:
                max_moves = []
                max_moves.append(possible_move)
                max_heur = val

            elif val == max_heur:
                max_moves.append(possible_move)


        return choice(max_moves)

        #return self.adverserial()

    """
    def possible_moves(self, side):
        possible_moves = []
        for t, r, q in self._game.board_dict_to_iterable(self._game.list_tokens(self._side)):
            legal_moves = self._game.list_legal_moves((r, q), self._side)
            for legal_move in legal_moves:
                move = (legal_move[0], (r, q), legal_move[1])
                possible_moves.append(move)

        if side == UPPER:
            token_set = UPPER_TILES
        else:
            token_set = LOWER_TILES

        for t in token_set:
            for tile in self._game.possible_throws(self._side):
                move = ("THROW", t.lower(), tile)
                possible_moves.append(move)

        return

    """

    def update(self, opponent_action, player_action):
        """
        Called at the end of each turn to inform this player of both
        players' chosen actions. Update your internal representation
        of the game state.
        The parameter opponent_action is the opponent's chosen action,
        and player_action is this instance's latest chosen action.
        """
        # put your code here
        # player actions in the form:

        self._game.take_turn(player_action, opponent_action, self._side)
        print(self._game.heuristic(self._side))
        # print("board: ")
        # self.print_board()
        # self.print_board(self._game.list_tokens(UPPER))
        # self.print_board(self._game.list_tokens(LOWER))

    def print_board(self, board_dict=None, message="", compact=True, ansi=False, **kwargs):
        """
        For help with visualisation and debugging: output a board diagram with
        any information you like (tokens, heuristic values, distances, etc.).

        Arguments:

        board_dict -- A dictionary with (r, q) tuples as keys (following axial
            coordinate system from specification) and printable objects (e.g.
            strings, numbers) as values.
            This function will arrange these printable values on a hex grid
            and output the result.
            Note: At most the first 5 characters will be printed from the string
            representation of each value.
        message -- A printable object (e.g. string, number) that will be placed
            above the board in the visualisation. Default is "" (no message).
        ansi -- True if you want to use ANSI control codes to enrich the output.
            Compatible with terminals supporting ANSI control codes. Default
            False.
        compact -- True if you want to use a compact board visualisation,
            False to use a bigger one including axial coordinates along with
            the printable information in each hex. Default True (small board).

        Any other keyword arguments are passed through to the print function.

        Example:

            >>> board_dict = {
            ...     ( 0, 0): "hello",
            ...     ( 0, 2): "world",
            ...     ( 3,-2): "(p)",
            ...     ( 2,-1): "(S)",
            ...     (-4, 0): "(R)",
            ... }
            >>> print_board(board_dict, "message goes here", ansi=False)
            # message goes here
            #              .-'-._.-'-._.-'-._.-'-._.-'-.
            #             |     |     |     |     |     |
            #           .-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
            #          |     |     | (p) |     |     |     |
            #        .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
            #       |     |     |     | (S) |     |     |     |
            #     .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
            #    |     |     |     |     |     |     |     |     |
            #  .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
            # |     |     |     |     |hello|     |world|     |     |
            # '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
            #    |     |     |     |     |     |     |     |     |
            #    '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
            #       |     |     |     |     |     |     |     |
            #       '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
            #          |     |     |     |     |     |     |
            #          '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
            #             | (R) |     |     |     |     |
            #             '-._.-'-._.-'-._.-'-._.-'-._.-'
        """
        if compact:
            template = """# {00:}
    #              .-'-._.-'-._.-'-._.-'-._.-'-.
    #             |{57:}|{58:}|{59:}|{60:}|{61:}|
    #           .-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
    #          |{51:}|{52:}|{53:}|{54:}|{55:}|{56:}|
    #        .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
    #       |{44:}|{45:}|{46:}|{47:}|{48:}|{49:}|{50:}|
    #     .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
    #    |{36:}|{37:}|{38:}|{39:}|{40:}|{41:}|{42:}|{43:}|
    #  .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
    # |{27:}|{28:}|{29:}|{30:}|{31:}|{32:}|{33:}|{34:}|{35:}|
    # '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
    #    |{19:}|{20:}|{21:}|{22:}|{23:}|{24:}|{25:}|{26:}|
    #    '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
    #       |{12:}|{13:}|{14:}|{15:}|{16:}|{17:}|{18:}|
    #       '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
    #          |{06:}|{07:}|{08:}|{09:}|{10:}|{11:}|
    #          '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
    #             |{01:}|{02:}|{03:}|{04:}|{05:}|
    #             '-._.-'-._.-'-._.-'-._.-'-._.-'"""
        else:
            template = """# {00:}
    #                  ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
    #                 | {57:} | {58:} | {59:} | {60:} | {61:} |
    #                 |  4,-4 |  4,-3 |  4,-2 |  4,-1 |  4, 0 |
    #              ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
    #             | {51:} | {52:} | {53:} | {54:} | {55:} | {56:} |
    #             |  3,-4 |  3,-3 |  3,-2 |  3,-1 |  3, 0 |  3, 1 |
    #          ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
    #         | {44:} | {45:} | {46:} | {47:} | {48:} | {49:} | {50:} |
    #         |  2,-4 |  2,-3 |  2,-2 |  2,-1 |  2, 0 |  2, 1 |  2, 2 |
    #      ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
    #     | {36:} | {37:} | {38:} | {39:} | {40:} | {41:} | {42:} | {43:} |
    #     |  1,-4 |  1,-3 |  1,-2 |  1,-1 |  1, 0 |  1, 1 |  1, 2 |  1, 3 |
    #  ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
    # | {27:} | {28:} | {29:} | {30:} | {31:} | {32:} | {33:} | {34:} | {35:} |
    # |  0,-4 |  0,-3 |  0,-2 |  0,-1 |  0, 0 |  0, 1 |  0, 2 |  0, 3 |  0, 4 |
    #  `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-'
    #     | {19:} | {20:} | {21:} | {22:} | {23:} | {24:} | {25:} | {26:} |
    #     | -1,-3 | -1,-2 | -1,-1 | -1, 0 | -1, 1 | -1, 2 | -1, 3 | -1, 4 |
    #      `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-'
    #         | {12:} | {13:} | {14:} | {15:} | {16:} | {17:} | {18:} |
    #         | -2,-2 | -2,-1 | -2, 0 | -2, 1 | -2, 2 | -2, 3 | -2, 4 |
    #          `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-'
    #             | {06:} | {07:} | {08:} | {09:} | {10:} | {11:} |
    #             | -3,-1 | -3, 0 | -3, 1 | -3, 2 | -3, 3 | -3, 4 |   key:
    #              `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-'     ,-' `-.
    #                 | {01:} | {02:} | {03:} | {04:} | {05:} |       | input |
    #                 | -4, 0 | -4, 1 | -4, 2 | -4, 3 | -4, 4 |       |  r, q |
    #                  `-._,-' `-._,-' `-._,-' `-._,-' `-._,-'         `-._,-'"""
        # prepare the provided board contents as strings, formatted to size.
        if not board_dict:
            board_dict = self._game.board
        ran = range(-4, +4 + 1)
        cells = []
        for rq in [(r, q) for r in ran for q in ran if -r - q in ran]:
            if rq in board_dict:
                cell = str(board_dict[rq]).center(5)
                if ansi:
                    # put contents in bold
                    cell = f"\033[1m{cell}\033[0m"
            else:
                cell = "     "  # 5 spaces will fill a cell
            cells.append(cell)
        # prepare the message, formatted across multiple lines
        multiline_message = "\n# ".join(message.splitlines())
        # fill in the template to create the board drawing, then print!
        board = template.format(multiline_message, *cells)
        print(board, **kwargs)
