
SLIDE_DISTANCE = 1

DIRECTIONS = ((1, 0), (1, -1), (0, -1), 
    (-1, 0), (-1, 1), (0, 1),)

NUM_DIRECTIONS = 6
Q_INDEX = 1
R_INDEX = 0

ROCK = 'r'
PAPER ='p'
SCISSORS ='s'
BLOCKED = ""

COORD_Q_INDEX = 1
COORD_R_INDEX = 0

LOWER_TILES = ["r", "p", "s"]
UPPER_TILES = ["R", "P", "S"]

# dictionary for RPS outcomes
RPS_OUTCOMES = {
    (ROCK, PAPER): False,
    (PAPER, ROCK): True,

    (ROCK, SCISSORS): True,
    (SCISSORS, ROCK): False,

    (PAPER, SCISSORS): False,
    (SCISSORS, PAPER): True
}

MAX_HEAP_SIZE = 1000000