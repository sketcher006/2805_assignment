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
LOC: 56
Parameters: None
Description: The Hud class does not take any parameters when creating an object. It uses the pygame module to create and
display a heads-up display on the game screen.

The objects main attributes include score, level, lines, and shape_surfaces. The score, level, and lines are integers
that represent the current game statistics. The shape_surfaces is a dictionary initialised in global_settings.py that 
maps each shape name to an image that represents the shape.

The object has methods such as reset_hud_stats, display_text, display_pieces, and run. The reset_hud_stats method resets
the score, level, and lines attributes. The display_text method takes a position and text as parameters and renders the 
text on the HUD surface at the given position. The display_pieces method takes a list of shapes as a parameter and 
displays them on the HUD surface using the shape_surfaces dictionary. The run method takes a list of next_shapes as a 
parameter and updates the HUD surface with the current game statistics and the next shapes. It also blits the HUD 
surface on the display_surface at a certain position.

--------------------------
## main.py
LOC: 139
Parameters: None
Description: The Main class uses the pygame module to initialise and run the game.

The objects main attributes include next_shapes, hud, game, various background images and buttons. The next_shapes is a 
list of shapes that are generated randomly for the next pieces. The hud is a Hud object that displays the game 
statistics on the screen. The game is a Tetris object that handles the logic and display of the game grid.

The Main object has 3 methods: get_next_shape, update_score, and run. The get_next_shape method returns the first shape 
from the next_shapes list and appends a new random shape to the list. The update_score method takes lines, score, and 
level as parameters and updates the hud attributes with these values. The run method is the main game loop that handles 
the events and updates the game. It controls the displaying of the different pages and buttons depending on the game 
state. It also uses a menu_system list to keep track of which page is active.

--------------------------
## README.md
This file

--------------------------
## tetris.py

--------------------------
## timer.py
LOC: 36
Parameters: duration, repeated, func
Description: This is a simple timer class to handle cases pertinent to time. The duration parameter determines how long 
the time will run before something can happen, repeated is whether the timer starts itself again after the specified 
duration and if a function has been included in the parameter, it can be called at the end of the duration. The timer 
class has been used to control vertical speed, horizontal keypress speed, and rotational keypress speed. The vertical 
timer repeats itself continuously and performs the function move_down after each duration, controlling the gameplay 
speed.

The Timer class has three methods, start, stop and update. Start and stop are self-explanatory, update however is called 
on each new frame and checks if the duration has been served. If so, the timer will be stopped, a function may be run, 
and the timer may be repeated.

--------------------------
## utility.py
LOC: 23
Parameters: menu, destination
Description: Two global functions are contained here, reset_menu and get_shape. reset_menu is used to clear the menu and
re-assign a new menu option. get_shape is used to randomly choose a new tetromino shape from the available selection. 
