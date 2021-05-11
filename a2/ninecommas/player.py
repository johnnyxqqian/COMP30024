from a2.ninecommas.RoPaSciState import *
from a2.ninecommas.consts import *


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
            legal_moves = self._game.list_legal_moves((r, q),)
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

        return possible_moves[0]

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
