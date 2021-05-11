

from .RoPaSciState import *
COST_LIVE_TOKEN = 10
COST_WIN_CONDITION = 10
COST_WIN = 10000
COST_DRAW = 0
COST_SING_INVIC = 10
COST_DOUB_INVIC = 1000
COST_FRIENDLY_NEIGHBOUR = 5
COST_BNEIGHBOUR = 10
COST_GNEIGHBOUR = 10


def heuristic(self, side):

    # implicity determines if we've beat an enemy token

    cost = 0

    # switch used to account for sides
    side_flag = 1 if side == UPPER else -1

    # feature 1: # our emaining tokens
    # need to check if side is upper / lower case
    cost += COST_LIVE_TOKEN * len(self.list_tokens(
        side)) * side_flag + (9-self.throws[side])

    # feature 2: # enemy tokens
    cost -= COST_LIVE_TOKEN * len(self.list_tokens(
        side)) * side_flag + (9-self.throws[side])

    up_throws = 9 - self.throws["upper"]
    lo_throws = 9 - self.throws["lower"]

    # should this just be s?
    up_tokens = [
        s.lower() for x in self.board.values() for s in x if s.isupper()
    ]

    lo_tokens = [
        s for x in self.board.values() for s in x if s.islower()
    ]
    up_symset = set(up_tokens)
    lo_symset = set(lo_tokens)

    up_invinc = [
        s for s in up_symset
        if (lo_throws == 0) and (_WHAT_BEATS[s] not in lo_symset)
    ]
    lo_invinc = [
        s for s in lo_symset
        if (up_throws == 0) and (_WHAT_BEATS[s] not in up_symset)
    ]

    up_notoks = (up_throws == 0) and (len(up_tokens) == 0)
    lo_notoks = (lo_throws == 0) and (len(lo_tokens) == 0)
    up_onetok = (up_throws == 0) and (len(up_tokens) == 1)
    lo_onetok = (lo_throws == 0) and (len(lo_tokens) == 1)

    # condition 1: one player has no remaining throws or tokens
    if up_notoks and lo_notoks:
        return COST_DRAW * side_flag
    if up_notoks:
        return COST_WIN * side_flag * (-1)
    if lo_notoks:
        return COST_WIN * side_flag

    # condition 2: both players have an invincible token
    if up_invinc and lo_invinc:
        return COST_DRAW * side_flag

    # condition 3: one player has an invincible token, the other has
    #              only one token remaining (not invincible by 2)
    if up_invinc and lo_onetok:
        return COST_WIN * side_flag
    if lo_invinc and up_onetok:
        return COST_WIN * side_flag * (-1)

    # condition 4: the same state has occurred for a 3rd time
    if self.history[state] >= 3:
        return COST_DRAW * side_flag

    # condition 5: the players have had their 360th turn without end
    if self.nturns >= _MAX_TURNS:
        return COST_DRAW * side_flag

    # feature 3: invincible tokens
    # 1 invincible token
    cost += COST_INVINC * \
        side_flag if (len(up_invinc) == 1 and lo_throws == 0) else 0
    cost += COST_INVINC * side_flag * \
        (-1) if (len(lo_invinc) == 1 and up_throws == 0) else 0

    # 2 invincible tokens
    cost += COST_DOUB_INVIC * \
        side_flag if (len(up_invinc) == 2 and lo_throws < 2) else 0
    cost += COST_DOUB_INVIC * side_flag * \
        (-1) if (len(lo_invinc) == 2 and up_throws < 2) else 0

    # if enenmy neighbour, check if beatable
    # if friendly neighbour, increase cost
    # to confirm with simon
    for token, r, q in self.board_dict_to_iterable(self.list_tokens(side)):
        neighbours = neighbour_hexes((r, q))
        for neighbour in neighbours:
            if neighbour in board_state.board.keys():

                # friendly token
                if side == UPPER and board_state.board[neighbour].isupper:
                    cost += COST_FRIENDLY_NEIGHBOUR
                elif side == LOWER and board_state.board[neighbour].islower:
                    cost += COST_FRIENDLY_NEIGHBOUR

                # enemy token
                else:
                    # enemy neighbour we can lose to
                    if _WHAT_BEATS[token] == board_state.board[neighbour].lower():
                        cost -= COST_BNEIGHBOUR * side_flag

                    # enemy neighbour we can beat
                    elif _BEATS_WHAT[token] == board.sate.board[neighbour].lower():
                        cost += COST_GNEIGHBOUR * side_flag

                    # enemy neighbour is the same token
                    else:
                        cost += 0
    return cost


def end_check(rps_state, side):

    return cost


# we want to prioritise beatable combinations of tokens

# for each of our tokens

# then safety

# ------------
