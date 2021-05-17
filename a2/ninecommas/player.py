from math import inf
from random import choice

import scipy.optimize as opt

from .RoPaSciState import *
from .consts import *


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

    def adverserial(self):
        """"
        Adversarial search using multi-stage game theory and backwards induction.

        Returns the player's best current move
        """

        optimal_move_p, exp_value = self.msgt(self._game, 0)
        print('exp = ', exp_value)
        return optimal_move_p

    def msgt(self, game=None, depth=0):
        """"
        Performs a search for player's best current move using multi-stage game theory
        and backwards induction.

        Input:
        * Game: a game state
        * Depth: the current search depth
        """

        # depth reached, begin recursion
        if depth > MAX_DEPTH:
            return None, game.evaluation(self._side)

        enemy_side = "upper" if self._side == LOWER else LOWER

        our_best_moves = []
        our_best_payoff = -inf

        e_best_moves = []
        e_best_payoff = -inf

        # identifying the player's best moves given a static board state
        for possible_move in game.possible_moves(self._side):

            new_state = deepcopy(game)
            new_state.take_turn(possible_move, None, self._side)
            val = new_state.evaluation(self._side)

            if val > our_best_payoff:
                our_best_moves = []
                our_best_moves.append(possible_move)
                our_best_payoff = val

            elif val == our_best_payoff:
                our_best_moves.append(possible_move)

        # identifying the enemy's best moves against our best moves
        for move in our_best_moves:
            for e_move in game.possible_moves(enemy_side):

                new_state = deepcopy(game)
                new_state.take_turn(move, e_move, self._side)
                val = new_state.evaluation(enemy_side)

                if val > e_best_payoff:
                    e_best_moves = []
                    e_best_moves.append(e_move)
                    e_best_payoff = val
                    # print("heur = ", val)

                elif val == e_best_payoff:
                    e_best_moves.append(e_move)

        # initialising payoff matrix
        payoff_matrix = np.zeros((len(our_best_moves), len(e_best_moves)))
        i = 0

        # tree construction & search
        for p_moves in our_best_moves:
            j = 0
            for e_moves in e_best_moves:
                new_state = deepcopy(game)
                new_state.take_turn(p_moves, e_moves, self._side)

                # recurse
                _, payoff = self.msgt(new_state, depth + 1)
                payoff_matrix[i][j] = payoff

                j += 1
            i += 1

        # determining equilibrium solution & player's best move at given state
        moves, expected_value = self.solve_game(payoff_matrix)
        move_index_p = np.where(moves == np.amax(moves))[0][0]
        bmove_player = our_best_moves[move_index_p]

        return bmove_player, expected_value

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

        # adverserial AI
        if ADVERSERIAL:
            return self.adverserial()

        # greedy AI
        max_heur = -1000000
        max_moves = []

        for possible_move in self._game.possible_moves(self._side):

            new_state = deepcopy(self._game)
            new_state.take_turn(possible_move, None, self._side)
            val = new_state.evaluation(self._side)

            if val > max_heur:
                max_moves = []
                max_moves.append(possible_move)
                max_heur = val

            elif val == max_heur:
                max_moves.append(possible_move)

        return choice(max_moves)

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
        print(self._game.evaluation(self._side))
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
