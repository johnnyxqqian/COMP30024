
from a2.ninecommas.RoPaSciState import *

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
        self._board = Board()
        # put your code here

    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """

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
    
    def update(self, opponent_action, player_action):
        """
        Called at the end of each turn to inform this player of both
        players' chosen actions. Update your internal representation
        of the game state.
        The parameter opponent_action is the opponent's chosen action,
        and player_action is this instance's latest chosen action.
        """
        # put your code here