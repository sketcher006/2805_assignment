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
    print("extended:", EXTENDED)
    normal_shapes_list = ["I", "J", "L", "O", "S", "T", "Z"]
    extended_shapes_list = ["I", "J", "L", "O", "S", "T", "Z", "I_extend", "J_extend"]
    if EXTENDED:
        random_shape = random.choice(extended_shapes_list)
    else:
        random_shape = random.choice(normal_shapes_list)
    print(random_shape)
    return random_shape
