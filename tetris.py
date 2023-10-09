from timer import Timer
from os import path
from utility import *
import pygame.locals as pg_locals
from os.path import join
import copy


class Tetris:
    """Class to handle the main logic and gameplay controller"""
    def __init__(self, update_score, get_next_shape, reset_hud_stats):
        """Constructor, parameters include callback functions update_score, get_next_shape, and reset_hud_stats"""
        self.surface = global_settings.pygame.Surface((global_settings.GAME_WIDTH, global_settings.GAME_HEIGHT))
        self.display_surface = global_settings.pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft=(global_settings.PADDING, global_settings.PADDING))
        self.sprites = global_settings.pygame.sprite.Group()  # group for sprites
        self.update_score = update_score
        self.get_next_shape = get_next_shape
        self.reset_hud_stats = reset_hud_stats

        # initialise blank game board
        self.board_pieces = (
            [[0 for i in range(global_settings.current_game_size[global_settings.GAME_COLS])]
             for j in range(global_settings.current_game_size[global_settings.GAME_ROWS])]
        )
        # create initial tetromino object
        self.tetro = Tetros(get_shape(), self.sprites, self.create_new_tetro, self.board_pieces)

        # timers
        self.down_speed = global_settings.start_speed  # initial game speed
        self.down_speed_fast = self.down_speed * .3  # game speed when down arrow pressed
        self.down_pressed = False

        self.vertical_timer = Timer(global_settings.start_speed, True, self.move_down)  # timer to control vert incremen
        self.vertical_timer.start()
        self.horizontal_timer = Timer(global_settings.MAX_BUTTON_DELAY)  # timer to control horizontal increments
        self.rotational_timer = Timer(global_settings.MAX_BUTTON_DELAY)  # timer to control rotational increments
        self.drop_timer = Timer(global_settings.MAX_BUTTON_DELAY)  # timer to control dropping tetros
        self.music_timer = Timer(global_settings.MAX_BUTTON_DELAY)  # timer to control music toggle
        self.ai_timer = Timer(1000)
        self.ai_timer_horizontal = Timer(20)

        # score
        self.current_level = global_settings.start_level
        self.current_score = 0
        self.current_lines = 0

        # load sounds
        self.bg_music = global_settings.pygame.mixer.Sound(join('audio', 'bg_music.mp3'))
        self.bg_music.set_volume(0.05)
        self.sfx_thump = global_settings.pygame.mixer.Sound(join('audio', 'thud.mp3'))
        self.sfx_thump.set_volume(0.5)
        self.sfx_tick = global_settings.pygame.mixer.Sound(join('audio', 'tick.mp3'))
        self.sfx_tick.set_volume(0.5)
        self.sfx_line_clear = global_settings.pygame.mixer.Sound(join('audio', 'line_clear.mp3'))
        self.sfx_line_clear.set_volume(0.5)
        self.sfx_tetris = global_settings.pygame.mixer.Sound(join('audio', 'tetris.mp3'))
        self.sfx_tetris.set_volume(0.5)
        self.music_playing = False

    def reset_game_stats(self):
        """reset game statistics and clear all pieces"""
        self.current_level = global_settings.start_level
        self.current_score = 0
        self.current_lines = 0
        self.board_pieces = [
            [0 for i in range(global_settings.current_game_size[global_settings.GAME_COLS])]
            for j in range(global_settings.current_game_size[global_settings.GAME_ROWS])
        ]
        self.down_speed = global_settings.start_speed
        self.vertical_timer.duration = global_settings.start_speed
        self.down_speed_fast = self.down_speed * .3
        self.sprites.empty()

    def save_high_score(self, name):
        """Save high score to an external file."""
        with open(path.join("assets", "high_scores.txt"), 'a') as high_scores:
            high_scores.write(name + ":" + str(self.current_score) + "\n")

        with open("assets/high_scores.txt", "r") as high_scores_file:
            high_scores_data = [line.strip().split(":") for line in high_scores_file]

        # Convert scores to integers
        high_scores_data = [(name, int(score)) for name, score in high_scores_data]

        # Sort the list based on scores in descending order
        high_scores_data.sort(key=lambda x: x[1], reverse=True)

        with open("assets/high_scores.txt", "w") as high_scores_file:
            for name, score in high_scores_data:
                high_scores_file.write(f"{name}:{score}\n")

    def get_users_name(self):
        user_input = ""
        input_active = True

        if not global_settings.human:
            return "ai"

        while input_active:
            for event in global_settings.pygame.event.get():
                if event.type == pg_locals.KEYDOWN:
                    if event.key == pg_locals.K_RETURN:  # User pressed Enter to submit the name
                        input_active = False
                    elif event.key == pg_locals.K_BACKSPACE:  # User pressed Backspace to delete a character
                        user_input = user_input[:-1]
                    else:
                        user_input += event.unicode  # Add the typed character to the input field

            # Clear the screen
            self.display_surface.fill((0, 0, 0))

            # Display the input field
            font = global_settings.pygame.font.Font(None, 36)
            input_text = font.render("Enter your name: " + user_input, True, (255, 255, 255))
            text_rect = input_text.get_rect(center=(global_settings.WIDTH / 2, global_settings.HEIGHT / 2))
            self.display_surface.blit(input_text, text_rect)

            global_settings.pygame.display.flip()

        return user_input

    def check_game_over(self):
        """check if any block pieces are above game board"""
        for block in self.tetro.blocks:
            if block.position.y < 0:
                # display GAME OVER
                print("GAME OVER")
                self.bg_music.stop()
                self.music_playing = False
                # ask for users name
                name = self.get_users_name()
                if name:
                    self.save_high_score(name)

                # reset stats ready for new game
                self.reset_game_stats()
                self.reset_hud_stats()

                # return to main menu
                reset_menu("Menu")
                break

    def create_new_tetro(self):
        """generate new tetromino piece"""
        self.check_game_over()
        self.check_for_completed_row()  # remove completed rows
        self.tetro = Tetros(self.get_next_shape(), self.sprites, self.create_new_tetro, self.board_pieces)

    def print_game_board(self, board, current_piece, print_piece):
        current_block_positions = []

        for lil_block in current_piece.blocks:
            current_block_positions.append((int(lil_block.position.y), int(lil_block.position.x)))
        print(current_block_positions)

        for row in range(len(board)):
            for col in range(len(board[row])):
                if (row, col) in current_block_positions and print_piece:
                    print("*", end="")
                elif board[row][col]:
                    print("X", end="")
                else:
                    print("O", end="")
            print()

    def calculate_unwanted_spaces(self, board):
        unwanted_spaces = 0
        for row in range(1, len(board)):
            for col in range(len(board[0])):
                if board[row][col] == 0:
                    if board[row - 1][col] != 0:
                        unwanted_spaces += 1
        return unwanted_spaces

    def check_potential_rows(self, board):
        potential_completed_rows = []
        for row in range(len(board)):
            if all(board[row]):
                potential_completed_rows.append(row)
        return potential_completed_rows

    def calculate_max_height_penalty(self, board):
        found_top = False
        top = None
        for row in range(len(board)):
            if found_top:
                break
            for col in range(len(board[0])):
                if board[row][col] != 0:
                    top = row
                    found_top = True
                    break
        if top is not None:
            return global_settings.current_game_size[1] - top
        else:
            return 0

    def move_down(self):
        """move the tetromino down using move_down method from Tetros class"""
        self.tetro.move_down(self.board_pieces)
        # self.print_game_board()

    def update_timers(self):
        # update all timers
        self.vertical_timer.update()
        self.horizontal_timer.update()
        self.rotational_timer.update()
        self.ai_timer.update()
        self.drop_timer.update()
        self.music_timer.update()

    def draw_grid(self):
        """draw the grid on the game board"""
        for col in range(1, global_settings.current_game_size[global_settings.GAME_COLS]):
            global_settings.pygame.draw.line(
                self.surface, (30, 30, 0), (col * global_settings.current_game_size[global_settings.GAME_GRID], 0),
                (col * global_settings.current_game_size[global_settings.GAME_GRID],
                 global_settings.HEIGHT-global_settings.PADDING))
        for row in range(1, global_settings.current_game_size[global_settings.GAME_ROWS]):
            global_settings.pygame.draw.line(
                self.surface, (30, 30, 0), (0, row * global_settings.current_game_size[global_settings.GAME_GRID]),
                (global_settings.GAME_WIDTH, row * global_settings.current_game_size[global_settings.GAME_GRID]))

    def run_ai(self):
        if not self.ai_timer.started:
            best_x_coord = None
            best_rotate = None
            best_metric = float('inf')
            best_x_coords = []
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
                tetro_clone.print_tetro_shape()
                self.print_game_board(board_clone, tetro_clone, True)

                # rotate the piece rotation times
                for i in range(rotation):
                    tetro_clone.rotate()
                tetro_clone.print_tetro_shape()
                tetro_clone.print_data()

                # analyse every possible x position
                for x_pos in range(global_settings.current_game_size[0]):
                    # Clone the cloned tetro and board to reset its attributes
                    new_tetro_clone = tetro_clone.clone()
                    new_board_clone = [[cell for cell in row] for row in board_clone]

                    new_tetro_clone.print_tetro_shape()
                    new_tetro_clone.print_data()

                    # Move cloned tetro to new x pos
                    for j in range(len(new_tetro_clone.blocks)):
                        new_tetro_clone.blocks[j].position.x += x_pos

                    new_tetro_clone.print_tetro_shape()
                    new_tetro_clone.print_data()

                    # check if position is within bounds
                    if new_tetro_clone.in_bounds():
                        # place tetro in this x coord
                        new_tetro_clone.instant_drop(new_board_clone, False)
                        self.print_game_board(new_board_clone, new_tetro_clone, True)
                        # calculate metric data
                        unwanted_spaces = self.calculate_unwanted_spaces(new_board_clone)
                        height_penalty = self.calculate_max_height_penalty(new_board_clone)
                        potential_completed_rows = self.check_potential_rows(new_board_clone)
                        highest_point_of_current_tetro = new_tetro_clone.get_tetros_height()

                        # Weights for the penalties
                        height_weight = .2
                        unwanted_spaces_weight = 1
                        potential_rows_weight = -1
                        highest_point_weight = 2

                        # Calculate the metric
                        this_rotations_penalty = (
                                height_weight * height_penalty +
                                unwanted_spaces_weight * unwanted_spaces +
                                potential_rows_weight * len(potential_completed_rows) +
                                highest_point_weight * highest_point_of_current_tetro
                        )
                        print("boards score like this ^:", this_rotations_penalty)
                        if this_rotations_penalty < best_metric:
                            best_metric = this_rotations_penalty
                            best_rotate = rotation
                            best_x_coords = []
                            for block in new_tetro_clone.blocks:
                                best_x_coords.append(block.position.x)
                            best_x_coord = x_pos
                    else:
                        print("block cant be here:", x_pos)

            print("best rotation:", best_rotate)
            print("best x-co:", best_x_coord)
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

    def user_input(self):
        """get user input key pressed"""
        user_input = global_settings.pygame.key.get_pressed()

        if global_settings.human:
            # check if it was left or right
            if not self.horizontal_timer.started:
                if user_input[global_settings.pygame.K_LEFT]:
                    if self.music_playing:
                        self.sfx_tick.play()
                    self.tetro.move_horizontal(-1)
                    self.horizontal_timer.start()
                if user_input[global_settings.pygame.K_RIGHT]:
                    if self.music_playing:
                        self.sfx_tick.play()
                    self.tetro.move_horizontal(1)
                    self.horizontal_timer.start()

            # check if it was up
            if not self.rotational_timer.started:
                if user_input[global_settings.pygame.K_UP]:
                    if self.music_playing:
                        self.sfx_tick.play()
                    self.tetro.rotate()
                    self.rotational_timer.start()

            # check if it was down and adjust drop speed accordingly
            if not self.down_pressed and user_input[global_settings.pygame.K_DOWN]:
                self.down_pressed = True
                self.vertical_timer.duration = self.down_speed_fast
            if self.down_pressed and not user_input[global_settings.pygame.K_DOWN]:
                self.down_pressed = False
                self.vertical_timer.duration = self.down_speed

            # check if it was space and drop tetro
            if not self.drop_timer.started:
                if user_input[global_settings.pygame.K_SPACE]:
                    if self.music_playing:
                        self.sfx_thump.play()
                    self.tetro.instant_drop(self.board_pieces, True)
                    self.drop_timer.start()

        # check if it was escape
        if user_input[global_settings.pygame.K_ESCAPE]:
            print("Escape pressed")
            self.tetro.print_tetro_shape()
            self.tetro.print_data()
            print("down speed", self.down_speed)
            print("vert timer", self.vertical_timer.duration)
            print("drop timer", self.drop_timer.start_time)
            reset_menu("Pause")

        # Check if the "m" key is pressed and toggle the music
        if user_input[global_settings.pygame.K_m] and not self.music_timer.started:
            print("m pressed")
            if self.music_playing:
                print("music is playing, stopping music")
                self.bg_music.stop()
                self.music_playing = False
            else:
                print("music is not playing, starting music")
                self.bg_music.play(-1)
                self.music_playing = True
            self.music_timer.start()

    def check_for_completed_row(self):
        """get index of any full row"""
        remove_rows = []
        for row in range(len(self.board_pieces)):
            if all(self.board_pieces[row]):
                remove_rows.append(row)

        # iterate through the full rows and remove the individual blocks
        if remove_rows:
            if self.music_playing:
                if len(remove_rows) == 4:
                    self.sfx_tetris.play()
                else:
                    self.sfx_line_clear.play()
            for remove_row in remove_rows:
                # remove the completed row from board
                for block in self.board_pieces[remove_row]:
                    block.kill()
                # move the remaining blocks down
                for row in self.board_pieces:
                    for block in row:
                        if block and block.position.y < remove_row:
                            block.position.y += 1
            # rebuild the board_pieces array
            self.board_pieces = [
                [0 for i in range(global_settings.current_game_size[global_settings.GAME_COLS])]
                for j in range(global_settings.current_game_size[global_settings.GAME_ROWS])
            ]
            for block in self.sprites:
                self.board_pieces[int(block.position.y)][int(block.position.x)] = block

            # modify the current score
            self.calculate_score(len(remove_rows))

    def calculate_score(self, cleared_lines):
        """update the total lines, level, and calculate the score based on how many lines have been removed"""
        self.current_lines += cleared_lines
        self.current_score += global_settings.SCORES[cleared_lines] * self.current_level
        if self.current_lines / 10 > self.current_level:
            self.current_level += 1
            self.down_speed *= 0.8
            self.down_speed_fast = self.down_speed * .3
            self.vertical_timer.duration = self.down_speed
        self.update_score(self.current_lines, self.current_score, self.current_level)

    def run(self):
        """combine all relevant methods above and display on game surface"""
        self.user_input()
        if not global_settings.human:
            self.run_ai()
        self.update_timers()
        self.sprites.update()
        self.surface.fill('#000000')
        self.sprites.draw(self.surface)
        self.draw_grid()
        self.display_surface.blit(self.surface, (global_settings.PADDING, global_settings.PADDING))


class Tetros:
    """Class to handle the tetrominos (groups of individual block sprites)"""
    def __init__(self, shape, group, create_new_tetro, board_pieces):
        """Constructor, parameters shape (tetromino shape), group (of sprites), create_new_tetro (function from Tetris
        class) and board pieces (array representing the board)"""
        self.shape = shape
        self.group = group
        self.block_positions = global_settings.TETROS[shape]["shape"]  # retrieve tetromino shapes from global_settings
        self.colour = global_settings.TETROS[shape]["colour"]
        self.create_new_tetro = create_new_tetro
        self.board_pieces = board_pieces

        self.blocks = []
        for position in self.block_positions:
            block = Block(group, position, self.colour)
            self.blocks.append(block)

    def check_horizontal_collision(self, spaces):
        """check if there is any potential collisions if tetro moves left or right"""
        collisions = []
        for block in self.blocks:
            collisions.append(block.horizontal_collide(int(block.position.x + spaces), self.board_pieces))
        for item in collisions:
            if item:
                return True
        return False

    def check_vertical_collision(self, spaces, game_board):
        """check if there is any potential collisions if tetro moves down"""
        collisions = []
        for block in self.blocks:
            collisions.append(block.vertical_collide(int(block.position.y + spaces), game_board))
        for item in collisions:
            if item:
                return True
        return False

    def instant_drop(self, game_board, create_new):
        """drop block as far as it can go until colliding with floor or tetro"""
        max_drop = 0
        while not self.check_vertical_collision(max_drop, game_board):
            max_drop += 1
        # move all blocks down until the space before collision
        for block in self.blocks:
            block.position.y += max_drop-1
        # update the board pieces array
        for block in self.blocks:
            game_board[int(block.position.y)][int(block.position.x)] = block
        if create_new:
            self.create_new_tetro()

    def move_down(self, game_board):
        """check block is within boundary and move down if so"""
        if not self.check_vertical_collision(1, game_board):
            for block in self.blocks:
                block.position.y += 1
        # once it hits the floor or another block, set it in place and create next tetro
        else:
            for block in self.blocks:
                game_board[int(block.position.y)][int(block.position.x)] = block
            if global_settings.human:
                self.create_new_tetro()

    def move_horizontal(self, spaces):
        """allow the tetromino to move left or right if there are no potential horizontal collisions"""
        if not self.check_horizontal_collision(spaces):
            for block in self.blocks:
                block.position.x += spaces
            return 0
        else:
            print("collision")
            return 1

    def rotate(self):
        """rotates the tetro by 90 degrees clockwise"""
        if self.shape != 'O':
            pivot_point = self.blocks[0].position  # central block that piece will pivot around
            # get new positions of individual blocks after rotation
            new_block_positions = [block.rotate(pivot_point) for block in self.blocks]
            # update block positions accordingly
            for i, block in enumerate(self.blocks):
                block.position = new_block_positions[i]

    def clone(self):
        """Return a copy of the current Tetros object"""
        new_shape = copy.copy(self.shape)
        new_group = global_settings.pygame.sprite.Group()

        # create a new Tetros object with the same attributes as the original one
        new_tetro = Tetros(new_shape, new_group, self.create_new_tetro, self.board_pieces)

        new_tetro.colour = self.colour
        for i in range(len(self.blocks)):
            new_tetro.blocks[i].position.x = copy.copy(self.blocks[i].position.x)
            new_tetro.blocks[i].position.y = copy.copy(self.blocks[i].position.y)

        # return the new Tetros object
        return new_tetro

    def print_data(self):
        print("shape:", self.shape)
        print("group", self.group)
        print("positions:", self.block_positions)
        print("colour:", self.colour)
        print("blocks:", self.blocks)
        for block in self.blocks:
            print(block.print_data())

    def print_tetro_shape(self):
        grid = [['.' for _ in range(4)] for _ in range(4)]

        min_x = min(block.position.x for block in self.blocks)
        min_y = min(block.position.y for block in self.blocks)

        for block in self.blocks:
            x = block.position.x - min_x
            y = block.position.y - min_y

            if 0 <= x < 4 and 0 <= y < 4:
                grid[int(y)][int(x)] = 'X'

        for row in grid:
            print(' '.join(row))

    def in_bounds(self):
        for block in self.blocks:
            if block.position.x < 0 or block.position.x >= global_settings.current_game_size[0]:
                return False
        return True

    def get_tetros_height(self):
        highest_y = float('inf')
        for block in self.blocks:
            if block.position.y < highest_y:
                highest_y = block.position.y
        return global_settings.current_game_size[1] - highest_y


class Block(global_settings.pygame.sprite.Sprite):  # inherit pygames sprite.Sprite class
    """Class to handle the individual blocks of a tetromino"""
    def __init__(self, group, position, colour):
        # Constructor, parameters group (of sprites), position (x, y) and colour
        super().__init__(group)
        self.colour = colour
        self.image = (global_settings.pygame.Surface((global_settings.current_game_size[global_settings.GAME_GRID],
                                                      global_settings.current_game_size[global_settings.GAME_GRID])))
        self.image.fill(colour)
        self.position = (global_settings.pygame.Vector2(position) +
                         global_settings.pygame.Vector2(
                             global_settings.current_game_size[global_settings.GAME_COLS]//2-1, -2)
                         )  # set to roughly centre
        x = self.position.x * global_settings.current_game_size[global_settings.GAME_GRID]
        y = self.position.y * global_settings.current_game_size[global_settings.GAME_GRID]
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        """update position of block"""
        self.rect.topleft = self.position * global_settings.current_game_size[global_settings.GAME_GRID]

    def horizontal_collide(self, x_coord, board_pieces):
        """check collision with left and right walls"""
        if not 0 <= x_coord < global_settings.current_game_size[global_settings.GAME_COLS]:
            return True
        """check collision with other tetrominos"""
        if global_settings.human:
            if board_pieces[int(self.position.y)][x_coord]:
                return True

    def vertical_collide(self, y_coord, board_pieces):
        """check collision with floor"""
        if y_coord >= global_settings.current_game_size[global_settings.GAME_ROWS]:
            return True
        """check collision with other tetrominos"""
        if y_coord >= 0 and board_pieces[y_coord][int(self.position.x)]:
            return True

    def rotate(self, pivot_point):
        """find new positions for individual blocks around pivot point"""
        distance = self.position - pivot_point
        rotated = distance.rotate(90)
        new_position = pivot_point + rotated
        return new_position

    def print_data(self):
        print("pos:", self.position.x, self.position.y, end=", ")
