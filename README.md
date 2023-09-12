# 2805_assignment

List of source code files

## button.py
LOC: 30
Parameters: x, y, image
Description: x, y, and an image are passed to the constructor as parameters when creating a Button object.
x and y represent the position of the button on the screen.
image is the image file used for the button.

The object can then be displayed by calling the display method. This method also checks for interactions with the 
button. If the mouse is clicked over the button, the display method returns true, allowing for an external check to 
perform some action.

The action variable is returned at the end of the display method, indicating whether a button click action should be 
executed.

--------------------------

## config.py
LOC: 33
Parameters: game_size, game_level, normal_extended, game_mode
Description: This class is used to display the game configuration settings in the Config menu. The parameters game_size
represents the size of the game grid, game_level is the current level of the game, normal_extended is a boolean 
representing normal pieces or extended pieces, and game_mode is either human or AI.

--------------------------

## global_settings.py
LOC: 65
Parameters: NA
Description: Initialises important variables used throughout the game, including screen dimensions, game size, 
game mode, extended pieces, tetromino shapes, points awarded for line completions, timer speeds and menu control 
variables.

--------------------------
## hud.py

--------------------------
## main.py

--------------------------
## README.md

--------------------------
## tetris.py

--------------------------
## timer.py