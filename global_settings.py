import pygame


# GLOBALS

## SCREEN
WIDTH = 710
HEIGHT = 840
PADDING = 20

## GAME
GAME_WIDTH = 400
GAME_HEIGHT = 800

GAME_COLS = 0
GAME_ROWS = 1
GAME_GRID = 2
# cols, rows, grid_size
GAME_SIZE_NORMAL = (10, 20, 40)
GAME_SIZE_SMALL = (8, 16, 50)
GAME_SIZE_LARGE = (16, 32, 25)
current_game_size = GAME_SIZE_NORMAL

## HUD
HUD_WIDTH = 250
HUD_HEIGHT = 800

## EXTENDED (extended == True uses additional pieces)
extended = False

## HUMAN or AI (human == True means the human controls the game, otherwise the ai will control it)
human = True

## TETRO SHAPES
TETROS = {
    # Standard
    #               PIVOT
    # "I": {"shape": [(1, 0), (0, 0), (2, 0), (3, 0)], "colour": (0, 240, 240)},  # aqua
    # "J": {"shape": [(1, 1), (0, 0), (0, 1), (2, 1)], "colour": (0, 0, 240)},  # blue
    # "L": {"shape": [(1, 1), (0, 1), (2, 0), (2, 1)], "colour": (240, 160, 0)},  # orange
    # "O": {"shape": [(0, 0), (1, 0), (0, 1), (1, 1)], "colour": (240, 240, 0)},  # yellow
    # "S": {"shape": [(1, 1), (0, 1), (1, 0), (2, 0)], "colour": (0, 240, 0)},  # green
    # "T": {"shape": [(1, 1), (1, 0), (0, 1), (2, 1)], "colour": (160, 0, 240)},  # purple
    # "Z": {"shape": [(1, 1), (0, 0), (1, 0), (2, 1)], "colour": (240, 0, 0)},  # red
    #
    # # Extended
    # "I_extend": {"shape": [(1, 0), (0, 0), (2, 0)], "colour": (0, 240, 240)},  # aqua
    # "J_extend": {"shape": [(0, 1), (0, 0), (1, 1)], "colour": (0, 0, 240)}  # blue

    "I": {"shape": [(0, 0), (-1, 0), (1, 0), (2, 0)], "colour": (0, 240, 240)},  # aqua
    "J": {"shape": [(0, 1), (-1, 0), (-1, 1), (1, 1)], "colour": (0, 0, 240)},  # blue
    "L": {"shape": [(0, 1), (-1, 1), (1, 0), (1, 1)], "colour": (240, 160, 0)},  # orange
    "O": {"shape": [(-1, 0), (0, 0), (-1, 1), (0, 1)], "colour": (240, 240, 0)},  # yellow
    "S": {"shape": [(0, 1), (-1, 1), (0, 0), (1, 0)], "colour": (0, 240, 0)},  # green
    "T": {"shape": [(0, 1), (0, 0), (-1, 1), (1, 1)], "colour": (160, 0, 240)},  # purple
    "Z": {"shape": [(0, 1), (-1, 0), (0, 0), (1, 1)], "colour": (240, 0, 0)},  # red

    # Extended
    "I_extend": {"shape": [(0, 0), (-1, 0), (1, 0)], "colour": (0, 240, 240)},  # aqua
    "J_extend": {"shape": [(-1, 1), (-1, 0), (0, 1)], "colour": (0, 0, 240)}  # blue
}

NORMAL_SHAPES_LIST = ["I", "J", "L", "O", "S", "T", "Z"]
EXTENDED_SHAPES_LIST = ["I", "J", "L", "O", "S", "T", "Z", "I_extend", "J_extend"]

## SCORE PER LINES
SCORES = {
    1: 100,
    2: 300,
    3: 600,
    4: 1000
}

## START SETTINGS
speed_increment_multiplier = 0.8
start_speed_1 = 200
start_speed_2 = start_speed_1 * speed_increment_multiplier
start_speed_3 = start_speed_2 * speed_increment_multiplier
start_speed_4 = start_speed_3 * speed_increment_multiplier
start_speed_5 = start_speed_4 * speed_increment_multiplier
start_speed_6 = start_speed_5 * speed_increment_multiplier

start_speed = start_speed_1  # milliseconds between vertical drop time
MAX_BUTTON_DELAY = 130  # milliseconds between the fastest time allowed between key presses
start_level = 1

menu_system = {  # Dictionary to control which page is displayed
    "Menu": True,
    "Score": False,
    "Config": False,
    "Game": False,
    "Pause": False
}
