WORKING:


def run_ai(self):
    """AI logic to control gameplay"""
    if not self.ai_timer.started:
        best_rotate = None
        best_metric = float('inf')
        best_x_coords = []

        # Weights for the penalties
        height_weight = .5
        unwanted_spaces_weight = 2
        potential_rows_weight = -2
        highest_point_weight = 1

        # generate raw shape at far left
        master_tetro = self.tetro.clone()
        for block_no in range(len(master_tetro.blocks)):
            master_tetro.blocks[block_no].position.x = (
                global_settings.TETROS[master_tetro.shape]["shape"][block_no][0]
            )
        master_tetro.print_data()

        # iterate through all rotations
        for rotation in range(4):
            # clone tetro and board
            tetro_clone = master_tetro.clone()
            board_clone = [[cell for cell in row] for row in self.board_pieces]
            # tetro_clone.print_tetro_shape()
            # self.print_game_board(board_clone, tetro_clone, True)

            # rotate the piece rotation times
            for i in range(rotation):
                tetro_clone.rotate()
            # tetro_clone.print_tetro_shape()
            # tetro_clone.print_data()

            # analyse every possible x position
            for x_pos in range(global_settings.current_game_size[0]):
                # Clone the cloned tetro and board to reset its attributes
                new_tetro_clone = tetro_clone.clone()
                new_board_clone = [[cell for cell in row] for row in board_clone]

                # new_tetro_clone.print_tetro_shape()
                # new_tetro_clone.print_data()

                # Move cloned tetro to new x pos
                for j in range(len(new_tetro_clone.blocks)):
                    new_tetro_clone.blocks[j].position.x += x_pos

                # new_tetro_clone.print_tetro_shape()
                # new_tetro_clone.print_data()

                # check if position is within bounds
                if new_tetro_clone.in_bounds():
                    # place tetro in this x coord
                    new_tetro_clone.instant_drop(new_board_clone, False)
                    # self.print_game_board(new_board_clone, new_tetro_clone, True)
                    # calculate metric data
                    unwanted_spaces = self.calculate_unwanted_spaces(new_board_clone)
                    height_penalty = self.calculate_max_height_penalty(new_board_clone)
                    potential_completed_rows = self.check_potential_rows(new_board_clone)
                    highest_point_of_current_tetro = new_tetro_clone.get_tetros_height()

                    # Calculate the metric
                    this_rotations_penalty = (
                            height_weight * height_penalty +
                            unwanted_spaces_weight * unwanted_spaces +
                            potential_rows_weight * len(potential_completed_rows) +
                            highest_point_weight * highest_point_of_current_tetro
                    )
                    print(f"boards score for {rotation} and {x_pos}: {this_rotations_penalty}")
                    self.print_game_board(new_board_clone, new_tetro_clone, True)
                    if this_rotations_penalty < best_metric:
                        best_metric = this_rotations_penalty
                        best_rotate = rotation
                        best_x_coords = []
                        for block in new_tetro_clone.blocks:
                            best_x_coords.append(block.position.x)
                        # best_x_coord = x_pos
                # else:
                #     print("block cant be here:", x_pos)

        print("best rotation:", best_rotate)
        # print("best x-co:", best_x_coord)
        print("best metric:", best_metric)

        # do the best move found here
        # rotate best_rotate

        for k in range(best_rotate):
            self.tetro.rotate()
        # move to best coordinate
        for l in range(len(self.tetro.blocks)):
            self.tetro.blocks[l].position.x = best_x_coords[l]

        self.ai_timer.start()

    else:
        self.ai_timer.update()

        current_time = global_settings.pygame.time.get_ticks()
        elapsed_time = current_time - self.ai_timer.start_time
        if elapsed_time >= self.ai_timer.duration:
            self.tetro.instant_drop(self.board_pieces, True)
            if self.music_playing:
                self.sfx_thump.play()


# RANDOM ai
else:
ai_is_moving = True
ai_is_moving_horizontal = False

if ai_is_moving:
    if not self.ai_timer.started:
        # pick left or right
        left_or_right = random.randint(0, 1)  # 0 = left, 1 = right
        print("leftorfright:", left_or_right)

        # pick spaces to move
        distance = random.randint(0, global_settings.current_game_size[0] / 2 + 1)
        # distance = round(random.uniform(0, global_settings.current_game_size[0]/2+1))
        print("distance", distance)

        # rotate up to 3 times
        rotate = random.randint(0, 3)
        print("rotate", rotate)

        rotate_count = 0
        while rotate_count < rotate:
            self.tetro.rotate()
            rotate_count += 1

        current_distance = 0

        while current_distance < distance:
            if not self.ai_timer_horizontal.started:
                if left_or_right:
                    print("right:", self.tetro.blocks[0].position.x)
                    if self.tetro.move_horizontal(1):
                        self.print_game_board()

                else:
                    print("left:", self.tetro.blocks[0].position.x)
                    if self.tetro.move_horizontal(-1):
                        self.print_game_board()

                current_distance += 1
                self.ai_timer_horizontal.start()
            else:
                self.ai_timer_horizontal.update()

        self.ai_timer.start()

    else:
        self.ai_timer.update()

        current_time = global_settings.pygame.time.get_ticks()
        elapsed_time = current_time - self.ai_timer.start_time
        if elapsed_time >= self.ai_timer.duration:
            self.tetro.instant_drop(self.board_pieces, True)
            ai_is_moving = False




import global_settings

# for all possible x positions
for x_pos in range(global_settings.current_game_size[0]):
    # clone board and tetro
    cloned_board_pieces = [[cell for cell in row] for row in self.board_pieces]
    current_tetro_clone = self.tetro.clone()

    # move cloned tetro to far left
    print("before shift on iter:", x_pos)
    current_tetro_clone.print_data()
    for i in range(len(current_tetro_clone.blocks)):
        current_tetro_clone.blocks[i].position.x = (
                global_settings.TETROS[current_tetro_clone.shape]["shape"][i][0] - 1 + x_pos
        )
    print("after shift on iter:", x_pos)
    current_tetro_clone.print_data()
    self.print_game_board(cloned_board_pieces, current_tetro_clone, True)

    # check if position is within bounds
    # block_is_in_bounds = True
    # for block in current_tetro_clone.blocks:
    #     if block.position.x < 0 or block.position.x > global_settings.current_game_size[0]:
    #         block_is_in_bounds = False
    #         break

    if current_tetro_clone.in_bounds():
        print("entire tetro is in bounds")
        # iterate through all rotations
        for rotation in range(4):
            print("Rotation:", rotation)
            current_new_pos_tetro_clone = current_tetro_clone.clone()
            new_cloned_board_pieces = [[cell for cell in row] for row in self.board_pieces]
            # # DEBUG ----------------------------------------
            # print("\norig: ", end="")
            # for block in self.tetro.blocks:
            #     block.print_data()
            # print("\ncopy: ", end="")
            # for block in current_tetro_clone.blocks:
            #     block.print_data()
            # # DEBUG ----------------------------------------

            # rotate the piece rotation times
            for i in range(rotation):
                current_new_pos_tetro_clone.rotate()

            # check the new rotation is in bounds
            if current_new_pos_tetro_clone.in_bounds():

                current_new_pos_tetro_clone.instant_drop(new_cloned_board_pieces, False)

                self.print_game_board(new_cloned_board_pieces, current_new_pos_tetro_clone, True)
                self.print_game_board(new_cloned_board_pieces, current_new_pos_tetro_clone, False)

                # calculate metric
                unwanted_spaces = 0
                for row in range(1, len(new_cloned_board_pieces)):
                    for col in range(len(new_cloned_board_pieces[0])):
                        if new_cloned_board_pieces[row][col] == 0:
                            if new_cloned_board_pieces[row - 1][col] != 0:
                                unwanted_spaces += 1
                print("unwanted spaces:", unwanted_spaces)

                # calculate maximum height
                found_top = False
                top = None
                penalty = 0
                for row in range(len(new_cloned_board_pieces)):
                    if found_top:
                        break

                    for col in range(len(new_cloned_board_pieces[0])):
                        if new_cloned_board_pieces[row][col] != 0:
                            top = row
                            found_top = True
                            break
                if top is not None:
                    print("top", top)
                    penalty = global_settings.current_game_size[1] - top
                    print("penalty", penalty)
                else:
                    print("board is empty")
                this_rotations_penalty = penalty + unwanted_spaces
                print("this_rotation_penalty:", this_rotations_penalty)
                if this_rotations_penalty < best_metric:
                    best_metric = this_rotations_penalty
                    best_rotate = rotation
                    best_x_coord = x_pos
            else:
                print("block cant rotate here")
    else:
        print("block cant go here on x")
        continue


#
# # Iterate through all possible x positions (horizontal positions)
# for x_coord in range(global_settings.current_game_size[global_settings.GAME_COLS]):
#     print("x_coord", x_coord)
#     # Clone the current tetromino's blocks
#     current_tetro_clone = self.tetro.clone()
#
#     # Calculate the offset to maintain the shape's relative positions
#     x_offset = x_coord - current_tetro_clone.blocks[0].position.x
#
#     # Move the entire tetromino to the current x position
#     for block in current_tetro_clone.blocks:
#         block.position.x += x_offset
#
#     # check the entire tetromino is still within bounds
#     for block in current_tetro_clone.blocks:
#         print("'", block.position.x, block.position.y, "'")
#         if block.position.x < 0:
#             print("block is out of bounds left")
#             continue
#         if block.position.x > global_settings.current_game_size[0]-1:
#             print("block is out of bounds right")
#             continue
#
#     # Simulate dropping the blocks down until collision
#     max_drop = 0
#     while not current_tetro_clone.check_vertical_collision(max_drop):
#         max_drop += 1
#     # move all blocks down until the space before collision
#     # for block in current_tetro_clone.blocks:
#     #     block.position.y += max_drop - 1
#     print("block can move down", max_drop-1, "positions")
#
#     # Calculate a metric to evaluate the current position (e.g., number of completed lines)
#     # I need to put the piece in the new x coordinates that renders the highest metric score
#     metric = self.calculate_metric(cloned_board_pieces)









class TetrisAI:
    def __init__(self, tetris_game):
        self.tetris = tetris_game

    def find_best_position(self, tetromino):
        best_position = None
        best_score = float('-inf')

        for row in range(self.tetris.rows):
            for col in range(self.tetris.cols):
                for rotation in range(4):
                    # Try placing the tetromino at the current position and rotation
                    if self.tetris.is_valid_position(tetromino, row, col, rotation):
                        # Create a copy of the board to simulate the placement
                        simulated_board = [row[:] for row in self.tetris.board_pieces]
                        self.tetris.place_tetromino(simulated_board, tetromino, row, col, rotation)

                        # Evaluate the position based on your chosen metrics
                        score = self.evaluate_position(simulated_board)

                        # Update the best position if this one has a higher score
                        if score > best_score:
                            best_score = score
                            best_position = (row, col, rotation)

        return best_position

    def evaluate_position(self, simulated_board):
        # Implement your evaluation metrics here
        # Example: Calculate the height of the highest block in the board
        max_height = max([sum(row) for row in simulated_board])
        return max_height

    def play(self):
        while not self.tetris.is_game_over():
            next_tetromino = self.tetris.get_next_shape()
            best_position = self.find_best_position(next_tetromino)
            if best_position:
                row, col, rotation = best_position
                self.tetris.move_tetromino(row, col, rotation)
            else:
                # Game over condition
                break



#
# # define constants for criteria weights
# WEIGHT_LINES = 1
# WEIGHT_HEIGHT = -0.5
# WEIGHT_HOLES = -1
# WEIGHT_BUMPINESS = -0.5
#
#
# # define function to get all possible moves for a shape
# def get_moves(board, shape):
#     moves = []
#     # loop through all possible rotations
#     for rotation in range(4):
#         # loop through all possible columns
#         for column in range(global_settings.current_game_size[global_settings.GAME_COLS]):
#             # create a copy of the shape with the current rotation and column
#             shape_copy = shape.copy()
#             shape_copy.rotation = rotation
#             shape_copy.column = column
#             # check if the move is valid
#             if shape_copy.is_valid_move(board):
#                 # add the move to the list
#                 moves.append((rotation, column))
#     return moves
#
# # define function to get resulting board state after applying a move
# def apply_move(board, shape, move):
#     # create copies of the board and the shape
#     board_copy = copy.deepcopy(board)
#     shape_copy = shape.copy()
#     # unpack the move into rotation and column
#     rotation, column = move
#     # set the shape attributes to match the move
#     shape_copy.rotation = rotation
#     shape_copy.column = column
#     # drop the shape until it hits the bottom or another piece
#     while shape_copy.is_valid_move(board_copy):
#         shape_copy.row += 1
#     # undo the last increment
#     shape_copy.row -= 1
#     # add the shape to the board
#     shape_copy.add_to_board(board_copy)
#     # clear any full lines and update score accordingly
#     score = clear_lines(board_copy)
#     return board_copy, score
#
# # define function to get heuristic value of a board state
# def get_heuristic(board):
#     # initialize heuristic value to zero
#     heuristic = 0
#     # get number of lines cleared by last move
#     lines = board.last_score // global_settings.SCORE_PER_LINE
#     # add lines cleared times weight to heuristic value
#     heuristic += lines * WEIGHT_LINES
#
#     # get maximum height of board (highest occupied row)
#     max_height = 0
#     for row in range(global_settings.current_game_size[global_settings.GAME_ROWS]):
#         for col in range(global_settings.current_game_size[global_settings.GAME_COLS]):
#             if board[row][col] != 0:
#                 max_height = max(max_height, global_settings.current_game_size[global_settings.GAME_ROWS] - row)
#                 break
#
#     # add max height times weight to heuristic value
#     heuristic += max_height * WEIGHT_HEIGHT
#
#     # get number of holes in board (empty spaces with occupied spaces above them)
#     holes = 0
#     for col in range(global_settings.current_game_size[global_settings.GAME_COLS]):
#         empty = False
#         for row in range(global_settings.current_game_size[global_settings.GAME_ROWS] - 1, -1, -1):
#             if board[row][col] == 0:
#                 empty = True
#             elif empty:
#                 holes += 1
#
#     # add holes times weight to heuristic value
#     heuristic += holes * WEIGHT_HOLES
#
#     # get bumpiness of board (sum of absolute differences between adjacent column heights)
#     bumpiness = 0
#     for col in range(global_settings.current_game_size[global_settings.GAME_COLS] - 1):
#         # get height of current column
#         height1 = 0
#         for row in range(global_settings.current_game_size[global_settings.GAME_ROWS]):
#             if board[row][col] != 0:
#                 height1 = global_settings.current_game_size[global_settings.GAME_ROWS] - row
#                 break
#         # get height of next column
#         height2 = 0
#         for row in range(global_settings.current_game_size[global_settings.GAME_ROWS]):
#             if board[row][col + 1] != 0:
#                 height2 = global_settings.current_game_size[global_settings.GAME_ROWS] - row
#                 break
#         # add absolute difference between heights to bumpiness
#         bumpiness += abs(height1 - height2)
#
#     # add bumpiness times weight to heuristic value
#     heuristic += bumpiness * WEIGHT_BUMPINESS
#
#     return heuristic
#
# # define function to get best move for a shape based on heuristic function
# def get_best_move(board, shape):
#     # initialize best move and best value variables
#     best_move = None
#     best_value = -float('inf')
#     # get all possible moves for the shape
#     moves = get_moves(board, shape)
#     # loop through all moves
#     for move in moves:
#         # get resulting board state and score after applying the move
#         new_board, score = apply_move(board, shape, move)
#         # get heuristic value of the new board state
#         value = get_heuristic(new_board)
#         # check if the value is better than the current best value
#         if value > best_value:
#             # update best move and best value variables
#             best_move = move
#             best_value = value
#     return best_move
#
# # modify main game loop to use best move function instead of user input
# while True:
#     # handle events
#     for event in global_settings.pygame.event.get():
#         if event.type == global_settings.pygame.QUIT:
#             global_settings.pygame.quit()
#             sys.exit()
#         elif event.type == global_settings.pygame.KEYDOWN:
#             if event.key == global_settings.pygame.K_ESCAPE:
#                 global_settings.pygame.quit()
#                 sys.exit()
#             elif event.key == global_settings.pygame.K_m:  # toggle music on/off with M key
#                 self.music_timer.start()
#                 if self.music_timer.is_finished():
#                     self.music_timer.reset()
#                     self.toggle_music()
#
#     # update timers
#     self.vertical_timer.update()
#     self.horizontal_timer.update()
#     self.rotational_timer.update()
#     self.drop_timer.update()
#     self.music_timer.update()
#
#     # get best move for current shape based on heuristic function
#     best_move = get_best_move(self.board_pieces, self.tetro)
#
#     # unpack the best move into rotation and column
#     rotation, column = best_move
#
#     # set the shape attributes to match the best move
#     self.tetro.rotation = rotation
#     self.tetro.column = column
#
#     # drop the shape until it hits the bottom or another piece
#     while self.tetro.is_valid_move(self.board_pieces):
#         self.tetro.row += 1
#
#     # undo the last increment
#     self.tetro.row -= 1
#
#     # add the shape to the board and create a new one
#     self.create_new_tetro()
