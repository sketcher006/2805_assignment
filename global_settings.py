import pygame
import random

# GLOBALS

## SCREEN
WIDTH = 710
HEIGHT = 840
PADDING = 20

## GAME
COLUMNS = 10
ROWS = 20
GRID_SIZE = 40
GAME_WIDTH = COLUMNS * GRID_SIZE
GAME_HEIGHT = ROWS * GRID_SIZE

## HUD
HUD_WIDTH = 250
HUD_HEIGHT = GAME_HEIGHT

## EXTENDED
EXTENDED = False

## HUMAN or AI
HUMAN = True

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

## SCORE PER LINES
SCORES = {
    1: 100,
    2: 300,
    3: 600,
    4: 1000
}

## START SETTINGS
START_SPEED = 200
MAX_BUTTON_DELAY = 150

MENU = 0
SCORE = 1
CONFIG = 2
GAME = 3
PAUSE = 4


#             [menu,  score, confg, game, pause]
menu_system = [True, False, False, False, False]


def reset_menu(menu, destination):
    # clear menu option
    for i in range(len(menu)):
        menu[i] = False
    menu[destination] = True


def get_shape():
    print("extended:", EXTENDED)
    normal_shapes_list = ["I", "J", "L", "O", "S", "T", "Z"]
    extended_shapes_list = ["I", "J", "L", "O", "S", "T", "Z", "I_extend", "J_extend"]
    if EXTENDED:
        random_shape = random.choice(extended_shapes_list)
    else:
        random_shape = random.choice(normal_shapes_list)
    print(random_shape)
    return random_shape