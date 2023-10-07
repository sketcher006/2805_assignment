import global_settings

# define constants for criteria weights
WEIGHT_LINES = 1
WEIGHT_HEIGHT = -0.5
WEIGHT_HOLES = -1
WEIGHT_BUMPINESS = -0.5


# define function to get all possible moves for a shape
def get_moves(board, shape):
    moves = []
    # loop through all possible rotations
    for rotation in range(4):
        # loop through all possible columns
        for column in range(global_settings.current_game_size[global_settings.GAME_COLS]):
            # create a copy of the shape with the current rotation and column
            shape_copy = shape.copy()
            shape_copy.rotation = rotation
            shape_copy.column = column
            # check if the move is valid
            if shape_copy.is_valid_move(board):
                # add the move to the list
                moves.append((rotation, column))
    return moves

# define function to get resulting board state after applying a move
def apply_move(board, shape, move):
    # create copies of the board and the shape
    board_copy = copy.deepcopy(board)
    shape_copy = shape.copy()
    # unpack the move into rotation and column
    rotation, column = move
    # set the shape attributes to match the move
    shape_copy.rotation = rotation
    shape_copy.column = column
    # drop the shape until it hits the bottom or another piece
    while shape_copy.is_valid_move(board_copy):
        shape_copy.row += 1
    # undo the last increment
    shape_copy.row -= 1
    # add the shape to the board
    shape_copy.add_to_board(board_copy)
    # clear any full lines and update score accordingly
    score = clear_lines(board_copy)
    return board_copy, score

# define function to get heuristic value of a board state
def get_heuristic(board):
    # initialize heuristic value to zero
    heuristic = 0
    # get number of lines cleared by last move
    lines = board.last_score // global_settings.SCORE_PER_LINE
    # add lines cleared times weight to heuristic value
    heuristic += lines * WEIGHT_LINES

    # get maximum height of board (highest occupied row)
    max_height = 0
    for row in range(global_settings.current_game_size[global_settings.GAME_ROWS]):
        for col in range(global_settings.current_game_size[global_settings.GAME_COLS]):
            if board[row][col] != 0:
                max_height = max(max_height, global_settings.current_game_size[global_settings.GAME_ROWS] - row)
                break

    # add max height times weight to heuristic value
    heuristic += max_height * WEIGHT_HEIGHT

    # get number of holes in board (empty spaces with occupied spaces above them)
    holes = 0
    for col in range(global_settings.current_game_size[global_settings.GAME_COLS]):
        empty = False
        for row in range(global_settings.current_game_size[global_settings.GAME_ROWS] - 1, -1, -1):
            if board[row][col] == 0:
                empty = True
            elif empty:
                holes += 1

    # add holes times weight to heuristic value
    heuristic += holes * WEIGHT_HOLES

    # get bumpiness of board (sum of absolute differences between adjacent column heights)
    bumpiness = 0
    for col in range(global_settings.current_game_size[global_settings.GAME_COLS] - 1):
        # get height of current column
        height1 = 0
        for row in range(global_settings.current_game_size[global_settings.GAME_ROWS]):
            if board[row][col] != 0:
                height1 = global_settings.current_game_size[global_settings.GAME_ROWS] - row
                break
        # get height of next column
        height2 = 0
        for row in range(global_settings.current_game_size[global_settings.GAME_ROWS]):
            if board[row][col + 1] != 0:
                height2 = global_settings.current_game_size[global_settings.GAME_ROWS] - row
                break
        # add absolute difference between heights to bumpiness
        bumpiness += abs(height1 - height2)

    # add bumpiness times weight to heuristic value
    heuristic += bumpiness * WEIGHT_BUMPINESS

    return heuristic

# define function to get best move for a shape based on heuristic function
def get_best_move(board, shape):
    # initialize best move and best value variables
    best_move = None
    best_value = -float('inf')
    # get all possible moves for the shape
    moves = get_moves(board, shape)
    # loop through all moves
    for move in moves:
        # get resulting board state and score after applying the move
        new_board, score = apply_move(board, shape, move)
        # get heuristic value of the new board state
        value = get_heuristic(new_board)
        # check if the value is better than the current best value
        if value > best_value:
            # update best move and best value variables
            best_move = move
            best_value = value
    return best_move

# modify main game loop to use best move function instead of user input
while True:
    # handle events
    for event in global_settings.pygame.event.get():
        if event.type == global_settings.pygame.QUIT:
            global_settings.pygame.quit()
            sys.exit()
        elif event.type == global_settings.pygame.KEYDOWN:
            if event.key == global_settings.pygame.K_ESCAPE:
                global_settings.pygame.quit()
                sys.exit()
            elif event.key == global_settings.pygame.K_m:  # toggle music on/off with M key
                self.music_timer.start()
                if self.music_timer.is_finished():
                    self.music_timer.reset()
                    self.toggle_music()

    # update timers
    self.vertical_timer.update()
    self.horizontal_timer.update()
    self.rotational_timer.update()
    self.drop_timer.update()
    self.music_timer.update()

    # get best move for current shape based on heuristic function
    best_move = get_best_move(self.board_pieces, self.tetro)

    # unpack the best move into rotation and column
    rotation, column = best_move

    # set the shape attributes to match the best move
    self.tetro.rotation = rotation
    self.tetro.column = column

    # drop the shape until it hits the bottom or another piece
    while self.tetro.is_valid_move(self.board_pieces):
        self.tetro.row += 1

    # undo the last increment
    self.tetro.row -= 1

    # add the shape to the board and create a new one
    self.create_new_tetro()
