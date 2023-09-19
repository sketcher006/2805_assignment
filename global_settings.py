import pygame


# GLOBALS

## SCREEN
WIDTH = 710
HEIGHT = 840
PADDING = 20

## GAME
GAME_WIDTH = 400
GAME_HEIGHT = 800
                #cols, rows, grid_size
game_size_normal = (10, 20, 40)
game_size_small = (8, 16, 50)
game_size_large = (16, 32, 25)
current_game_size = game_size_small
GAME_COLS = 0
GAME_ROWS = 1
GAME_GRID = 2

## HUD
HUD_WIDTH = 250
HUD_HEIGHT = 800

## EXTENDED
extended = False

## HUMAN or AI
human = True

## TETRO SHAPES
TETROS = {
    # Standard
    #               PIVOT
    "I": {"shape": [(1, 0), (0, 0), (2, 0), (3, 0)], "colour": (0, 240, 240)},  # aqua
    "J": {"shape": [(1, 1), (0, 0), (0, 1), (2, 1)], "colour": (0, 0, 240)},  # blue
    "L": {"shape": [(1, 1), (0, 1), (2, 0), (2, 1)], "colour": (240, 160, 0)},  # orange
    "O": {"shape": [(0, 0), (1, 0), (0, 1), (1, 1)], "colour": (240, 240, 0)},  # yellow
    "S": {"shape": [(1, 1), (0, 1), (1, 0), (2, 0)], "colour": (0, 240, 0)},  # green
    "T": {"shape": [(1, 1), (1, 0), (0, 1), (2, 1)], "colour": (160, 0, 240)},  # purple
    "Z": {"shape": [(1, 1), (0, 0), (1, 0), (2, 1)], "colour": (240, 0, 0)},  # red

    # Extended
    "I_extend": {"shape": [(1, 0), (0, 0), (2, 0)], "colour": (0, 240, 240)},  # aqua
    "J_extend": {"shape": [(0, 1), (0, 0), (1, 1)], "colour": (0, 0, 240)}  # blue
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
start_speed = 200
MAX_BUTTON_DELAY = 150

MENU = 0
SCORE = 1
CONFIG = 2
GAME = 3
PAUSE = 4

#             [menu, score, confg, game, pause]
menu_system = [True, False, False, False, False]
