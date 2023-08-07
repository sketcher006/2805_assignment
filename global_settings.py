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

## TETRO SHAPES
TETROS = {
    # Standard
    "I": {"shape": [(0, 0), (1, 0), (2, 0), (3, 0)], "colour": (0, 240, 240)},  # aqua
    "J": {"shape": [(0, 0), (0, 1), (1, 1), (2, 1)], "colour": (0, 0, 240)},  # blue
    "L": {"shape": [(0, 1), (1, 1), (2, 0), (2, 1)], "colour": (240, 160, 0)},  # orange
    "O": {"shape": [(0, 0), (1, 0), (0, 1), (1, 1)], "colour": (240, 240, 0)},  # yellow
    "S": {"shape": [(0, 1), (1, 1), (1, 0), (2, 0)], "colour": (0, 240, 0)},  # green
    "T": {"shape": [(1, 0), (0, 1), (1, 1), (2, 1)], "colour": (160, 0, 240)},  # purple
    "Z": {"shape": [(0, 0), (1, 0), (1, 1), (2, 1)], "colour": (240, 0, 0)},  # red

    # Extended
    "I_extend": {"shape": [(0, 0), (1, 0), (2, 0)], "colour": (0, 240, 240)},  # aqua
    "J_extend": {"shape": [(0, 0), (0, 1), (1, 1)], "colour": (0, 0, 240)}  # blue
}

## SCORE PER LINES
SCORES = {
    1: 100,
    2: 300,
    3: 600,
    4: 1000
}

## START SETTINGS
START_SPEED = 500
MAX_BUTTON_DELAY = 200