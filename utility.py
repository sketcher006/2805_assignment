from global_settings import *
import random


# Global utility functions

def reset_menu(menu, destination):
    # clear menu option
    for i in range(len(menu)):
        menu[i] = False
    menu[destination] = True


def get_shape():
    # return a random shape from shapes list
    print("extended:", extended)

    if extended:
        random_shape = random.choice(EXTENDED_SHAPES_LIST)
    else:
        random_shape = random.choice(NORMAL_SHAPES_LIST)
    print(random_shape)
    return random_shape
