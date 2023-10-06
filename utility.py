import global_settings
import random


# Global utility functions

def reset_menu(destination):
    """set current visible page to destination"""
    for key in global_settings.menu_system:
        if key == destination:
            global_settings.menu_system[key] = True
        else:
            global_settings.menu_system[key] = False


def get_shape():
    """return a random shape from shapes list"""
    print("extended:", global_settings.extended)

    if global_settings.extended:
        random_shape = random.choice(global_settings.EXTENDED_SHAPES_LIST)
    else:
        random_shape = random.choice(global_settings.NORMAL_SHAPES_LIST)
    print(random_shape)
    return random_shape
