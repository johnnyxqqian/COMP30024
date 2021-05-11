from .RoPaSciState import *
from .consts import *
from random import choice


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

    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """

        ### Generate all possible moves
        # Generate all swings and slides
        possible_moves = []
        for t, r, q in self._game.board_dict_to_iterable(self._game.list_tokens(self._side)):
            legal_moves = self._game.list_legal_moves((r, q),self._side)
            for legal_move in legal_moves:
                move = (legal_move[0], (r, q), legal_move[1])
                possible_moves.append(move)

        if self._side == UPPER:
            token_set = UPPER_TILES
        else:
            token_set = LOWER_TILES

        for t in token_set:
            for tile in self._game.possible_throws(self._side):
                move = ("THROW", t.lower(), tile)
                possible_moves.append(move)

        return choice(possible_moves)

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
        print(self._game.heuristic())
        #print("board: ")
        #self.print_board()
        #self.print_board(self._game.list_tokens(UPPER))
        #self.print_board(self._game.list_tokens(LOWER))

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
