from global_settings import *
import random


# Global utility functions

def reset_menu(destination):
    for key in menu_system:
        if key == destination:
            menu_system[key] = True
        else:
            menu_system[key] = False


def get_shape():
    # return a random shape from shapes list
    print("extended:", extended)

    if extended:
        random_shape = random.choice(EXTENDED_SHAPES_LIST)
    else:
        random_shape = random.choice(NORMAL_SHAPES_LIST)
    print(random_shape)
    return random_shape
