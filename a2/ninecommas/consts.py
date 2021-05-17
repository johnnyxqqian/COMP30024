SLIDE_DISTANCE = 1

DIRECTIONS = ((1, 0), (1, -1), (0, -1),
              (-1, 0), (-1, 1), (0, 1),)

NUM_DIRECTIONS = 6
Q_INDEX = 1
R_INDEX = 0

ROCK = 'r'
PAPER = 'p'
SCISSORS = 's'
BLOCKED = ""


LOWER_TILES = ["r", "p", "s"]
UPPER_TILES = ["R", "P", "S"]

LOWER = 'lower'
UPPER = 'upper'

# dictionary for RPS outcomes
RPS_OUTCOMES = {
    (ROCK, PAPER): False,
    (PAPER, ROCK): True,

    (ROCK, SCISSORS): True,
    (SCISSORS, ROCK): False,

    (PAPER, SCISSORS): False,
    (SCISSORS, PAPER): True,

    (ROCK, ROCK): True,
    (PAPER, PAPER): True,
    (SCISSORS, SCISSORS): True,
}

MAX_HEAP_SIZE = 1000000
MAX_DIST = 9

ENEMY_TOKEN_COST = 10
COST_SELF_TOKEN = 10
COST_THROW_TOKEN = 15
COST_ENEMY_TOKEN = 10


COST_WIN_CONDITION = 10

COST_WIN = 10000
COST_DRAW = -10
COST_INVINC = 30

MAX_TURNS = 360

# rock-paper-scissors mechanic
BEATS_WHAT = {"r": "s", "p": "r", "s": "p"}
WHAT_BEATS = {"r": "p", "p": "s", "s": "r"}

MAX_DEPTH = 1
ADVERSERIAL = False
