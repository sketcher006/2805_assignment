# 2805_assignment

----------------------------------------------------
----------------------------------------------------

## List of files:

### button.py
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

### config.py
LOC: 33
Parameters: game_size, game_level, normal_extended, game_mode
Description: This class is used to display the game configuration settings in the Config menu. The parameters game_size
represents the size of the game grid, game_level is the current level of the game, normal_extended is a boolean 
representing normal pieces or extended pieces, and game_mode is either human or AI.

--------------------------

### global_settings.py
LOC: 65
Parameters: NA
Description: Initialises important variables used throughout the game, including screen dimensions, game size, 
game mode, extended pieces, tetromino shapes, points awarded for line completions, timer speeds and menu control 
variables.

--------------------------

### hud.py
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

### main.py
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

### README.md
This file

--------------------------

### tetris.py
LOC: 296
Contains three classes: Tetris, Tetro, Block. A block is a single square of a tetromino, a tetromino is a group of 
blocks arranged in a certain way, and tetris is a group of tetrominos controllable by the user.


#### Block
Parameters: group, position, colour
Description: A simple class to handle the behaviour of individual pieces of a tetromino. The constructor requires a 
group, position and colour. The group parameter is required for the Sprite parent class. The position is an x, y 
coordinate that represents the location in the grid. The colour is the colour of the tetromino group. 

The Block class has four methods: update, horizontal_collide, vertical_collide, and rotate. update refreshes the 
location of the block based on the new position coordinates after user input or timer action. horizontal_collide returns
true if the block will move into a wall or another piece. vertical_collide returns true if the block will hit the floor
or another piece below. rotate calculates the new position of the individual blocks around a pivot point.


#### Tetro
Parameters: shape, group, create_new_tetro, board_pieces

Description: This class represents a tetromino; a group of Blocks. Tetro has six methods that are designed to handle 
various aspects of tetrominos in the game, including their movement, rotation, collision detection, and creation. The 
constructor requires a shape of the tetromino to be created, a sprite group, the create_new_tetro method from the Tetris
class, and the board_pieces array repsresenting the game board.

Methods:

check_horizontal_collision:
Checks if there would be any potential collisions if the tetromino moves left or right by the specified number of 
spaces. It returns True if a collision is detected, and False otherwise.

check_vertical_collision:
Checks if there would be any potential collisions if the tetromino moves down by the specified number of spaces.
It returns True if a collision is detected, and False otherwise.

instant_drop:
Drops the tetromino as far as it can go until it collides with the floor or another tetromino. It updates the position 
of the blocks, the board_pieces array, and then creates a new tetromino using the create_new_tetro function.

move_down:
Checks if the tetromino can move down by one space and, if so, moves it down. If the tetromino cannot move down further,
it sets the blocks in place on the game board (board_pieces) and creates a new tetromino.

move_horizontal:
Allows the tetromino to move left or right by the specified number of spaces if there are no potential horizontal 
collisions.

rotate:
Rotates the tetromino by using a pivot point around which the tetromino will rotate. It computes new positions for the 
individual blocks after rotation and updates their positions accordingly.


#### Tetris
Parameters: update_score, get_next_shape, reset_hud_stats

Description: The Tetris class is responsible for managing the main logic and gameplay control of the Tetris game. It 
includes various methods and attributes that handle game state, user input, scoring, timers, and more. The constructor 
requires three parameters, update_score which is a callback function to adjust the score, get_next_shape which is 
another callback function to get a new tetromino shape, and another callback function reset_hud_stats which resets the 
HUD display. 

Methods:

reset_game_stats:
Resets game statistics and clears the game board. Resets the game speed and clears the sprite group.

save_high_score:
Saves the current score to an external file.

check_game_over:
Checks if any block pieces of the current tetromino are above the game board indicating a game over condition.If the 
game is over, the high score is saved, game statistics are reset, and the user is returned to the main menu.

create_new_tetro:
Generates a new tetromino piece. Also checks for game over, removes completed rows, and creates the next tetromino.

move_down:
Moves the current tetromino down using the move_down method from the Tetros class.

update_timers:
Updates all timers used in the game (vertical, horizontal, rotational, and drop).

draw_grid:
Draws the grid on the game board.

user_input:
Handles user input, including left, right, up (rotate) and down (drop speed) arrows, space bar (instant drop), and the 
escape key. Also adjusts various timers to prevent accidental rapid key presses.

check_for_completed_row:
Identifies and removes any full rows on the game board. Moves the remaining blocks down and rebuilds the 
board_pieces array. Calculates and updates the score based on the number of cleared lines.

calculate_score:
Updates the total lines, level, and score based on the number of lines cleared. Adjusts vertical drop speed based on the
current level.

run:
Combines various methods to run the game logic in a single game loop iteration. Handles user input, updates timers, 
updates sprite positions, clears and draws the game board, and displays it on the screen.

--------------------------

### timer.py
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

### utility.py
LOC: 23
Parameters: menu, destination
Description: Two global functions are contained here, reset_menu and get_shape. reset_menu is used to clear the menu and
re-assign a new menu option. get_shape is used to randomly choose a new tetromino shape from the available selection. 

--------------------------

Total LOC: 678

--------------------------

## File tree:

Main directory
|-- assets
|   |-- Arcade.ttf  # font used for rendering
|   |-- high_scores.txt  # saved high scores data
|-- images  # images used for sprites, buttons and menus
|   |-- config.png
|   |-- configpage.png
|   |-- exit.png
|   |-- exit_btn.png
|   |-- home.png
|   |-- I.png
|   |-- I_extended.png
|   |-- icon.png
|   |-- J.png
|   |-- J_extended.png
|   |-- L.png
|   |-- no.png
|   |-- O.png
|   |-- pausepage.png
|   |-- play.png
|   |-- return.png
|   |-- S.png
|   |-- score.png
|   |-- scores.png
|   |-- star_btn.png
|   |-- T.png
|   |-- yes.png
|   |-- Z.png
|-- button.py
|-- config.py
|-- global_settings.py
|-- hud.py
|-- main.py
|-- README.md
|-- tetris.py
|-- timer.py
|-- utility.py

----------------------------------------------------
----------------------------------------------------

## Naming Conventions
Classes: Use CamelCase for class names. For example, MyClass.
Objects: Use snake_case for object names. For example, my_object.
Functions: Use snake_case for function names. For example, my_function.
Constants: Use UPPER_CASE for constant names. For example MY_CONSTANT.
Variables: Use snake_case for variable names. For example, my_variable.

----------------------------------------------------
----------------------------------------------------

## Usage
Ensure pygame is installed
Ensure project is unzipped and all files are included in directory as per file tree above
Run main.py (program tested using Python 3.9.2 and Pygame 2.5.0)

----------------------------------------------------
----------------------------------------------------

## Contributors
Daniel Jacobsen
Jack Brighton
Patrick Rukera

----------------------------------------------------
----------------------------------------------------

## Acknowledgements
Many thanks to the Youtube tutorial creators:
- freeCodeCamp
- Tech with Tim
- Chris Honselaar
- Programming with Nick

Pygame documentation:
- https://www.pygame.org/docs/

ChatGPT for debugging and providing unit tests:
- https://chat.openai.com