from timer import Timer
from os import path
from utility import *


class Tetris:
    """Class to handle the main logic and gameplay controller"""
    def __init__(self, update_score, get_next_shape, reset_hud_stats):
        """Constructor, parameters include callback functions update_score, get_next_shape, and reset_hud_stats"""
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft=(PADDING, PADDING))
        self.sprites = pygame.sprite.Group()  # group for sprites
        self.update_score = update_score
        self.get_next_shape = get_next_shape
        self.reset_hud_stats = reset_hud_stats

        # initialise blank game board
        self.board_pieces = (
            [[0 for i in range(current_game_size[GAME_COLS])] for j in range(current_game_size[GAME_ROWS])]
        )
        # create initial tetromino object
        self.tetro = Tetros(get_shape(), self.sprites, self.create_new_tetro, self.board_pieces)

        # timers
        self.down_speed = start_speed  # initial game speed
        self.down_speed_fast = self.down_speed * .3  # game speed when down arrow pressed
        self.down_pressed = False
        self.vertical_timer = Timer(start_speed, True, self.move_down)  # timer to control vertical increments
        self.vertical_timer.start()
        self.horizontal_timer = Timer(MAX_BUTTON_DELAY)  # timer to control horizontal increments
        self.rotational_timer = Timer(MAX_BUTTON_DELAY)  # timer to control rotational increments
        self.drop_timer = Timer(MAX_BUTTON_DELAY)  # timer to control dropping tetros

        # score
        self.current_level = 1
        self.current_score = 0
        self.current_lines = 0

    def reset_game_stats(self):
        """reset game statistics and clear all pieces"""
        self.current_level = 1
        self.current_score = 0
        self.current_lines = 0
        self.board_pieces = [
            [0 for i in range(current_game_size[GAME_COLS])] for j in range(current_game_size[GAME_ROWS])
        ]
        self.down_speed = start_speed
        self.vertical_timer.duration = start_speed
        self.down_speed_fast = self.down_speed * .3
        self.sprites.empty()

    def save_high_score(self):
        """save high score to external file"""
        with open(path.join("assets", "high_scores.txt"), 'a') as high_scores:
            high_scores.write(str(self.current_score) + "\n")

    def check_game_over(self):
        """check if any block pieces are above game board"""
        for block in self.tetro.blocks:
            if block.position.y < 0:
                # display GAME OVER
                print("GAME OVER")

                self.save_high_score()

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

    def move_down(self):
        """move the tetromino down using move_down method from Tetros class"""
        self.tetro.move_down()

    def update_timers(self):
        # update all timers
        self.vertical_timer.update()
        self.horizontal_timer.update()
        self.rotational_timer.update()
        self.drop_timer.update()

    def draw_grid(self):
        """draw the grid on the game board"""
        for col in range(1, current_game_size[GAME_COLS]):
            pygame.draw.line(
                self.surface, (30, 30, 0), (col * current_game_size[GAME_GRID], 0),
                (col * current_game_size[GAME_GRID], HEIGHT-PADDING))
        for row in range(1, current_game_size[GAME_ROWS]):
            pygame.draw.line(
                self.surface, (30, 30, 0), (0, row * current_game_size[GAME_GRID]),
                (GAME_WIDTH, row * current_game_size[GAME_GRID]))

    def user_input(self):
        """get user input key pressed"""
        user_input = pygame.key.get_pressed()

        # check if it was left or right
        if not self.horizontal_timer.started:
            if user_input[pygame.K_LEFT]:
                self.tetro.move_horizontal(-1)
                self.horizontal_timer.start()
            if user_input[pygame.K_RIGHT]:
                self.tetro.move_horizontal(1)
                self.horizontal_timer.start()

        # check if it was up
        if not self.rotational_timer.started:
            if user_input[pygame.K_UP]:
                self.tetro.rotate()
                self.rotational_timer.start()

        # check if it was down and adjust drop speed accordingly
        if not self.down_pressed and user_input[pygame.K_DOWN]:
            self.down_pressed = True
            self.vertical_timer.duration = self.down_speed_fast
        if self.down_pressed and not user_input[pygame.K_DOWN]:
            self.down_pressed = False
            self.vertical_timer.duration = self.down_speed

        # check if it was space and drop tetro
        if not self.drop_timer.started:
            if user_input[pygame.K_SPACE]:
                self.tetro.instant_drop()
                self.drop_timer.start()

        # check if it was escape
        if user_input[pygame.K_ESCAPE]:
            print("Escape pressed")
            print("down speed", self.down_speed)
            print("vert timer", self.vertical_timer.duration)
            print("drop timer", self.drop_timer.start_time)
            reset_menu("Pause")

    def check_for_completed_row(self):
        """get index of any full row"""
        remove_rows = []
        for row in range(len(self.board_pieces)):
            if all(self.board_pieces[row]):
                remove_rows.append(row)

        # iterate through the full rows and remove the individual blocks
        if remove_rows:
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
                [0 for i in range(current_game_size[GAME_COLS])] for j in range(current_game_size[GAME_ROWS])
            ]
            for block in self.sprites:
                self.board_pieces[int(block.position.y)][int(block.position.x)] = block

            # modify the current score
            self.calculate_score(len(remove_rows))

    def calculate_score(self, cleared_lines):
        """update the total lines, level, and calculate the score based on how many lines have been removed"""
        self.current_lines += cleared_lines
        self.current_score += SCORES[cleared_lines] * self.current_level
        if self.current_lines / 10 > self.current_level:
            self.current_level += 1
            self.down_speed *= 0.8
            self.down_speed_fast = self.down_speed * .3
            self.vertical_timer.duration = self.down_speed
        self.update_score(self.current_lines, self.current_score, self.current_level)

    def run(self):
        """combine all relevant methods above and display on game surface"""
        self.user_input()
        self.update_timers()
        self.sprites.update()
        self.surface.fill('#000000')
        self.sprites.draw(self.surface)
        self.draw_grid()
        self.display_surface.blit(self.surface, (PADDING, PADDING))


class Tetros:
    """Class to handle the tetrominos (groups of individual block sprites)"""
    def __init__(self, shape, group, create_new_tetro, board_pieces):
        """Constructor, parameters shape (tetromino shape), group (of sprites), create_new_tetro (function from Tetris
        class) and board pieces (array representing the board)"""
        self.shape = shape
        self.block_positions = TETROS[shape]["shape"]  # retrieve tetromino shapes from global_settings
        self.colour = TETROS[shape]["colour"]
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

    def check_vertical_collision(self, spaces):
        """check if there is any potential collisions if tetro moves down"""
        collisions = []
        for block in self.blocks:
            collisions.append(block.vertical_collide(int(block.position.y + spaces), self.board_pieces))
        for item in collisions:
            if item:
                return True
        return False

    def instant_drop(self):
        """drop block as far as it can go until colliding with floor or tetro"""
        max_drop = 0
        while not self.check_vertical_collision(max_drop):
            max_drop += 1
        # move all blocks down until the space before collision
        for block in self.blocks:
            block.position.y += max_drop-1
        # update the board pieces array
        for block in self.blocks:
            self.board_pieces[int(block.position.y)][int(block.position.x)] = block
        self.create_new_tetro()

    def move_down(self):
        """check block is within boundary and move down if so"""
        if not self.check_vertical_collision(1):
            for block in self.blocks:
                block.position.y += 1
        # once it hits the floor or another block, set it in place and create next tetro
        else:
            for block in self.blocks:
                self.board_pieces[int(block.position.y)][int(block.position.x)] = block
            self.create_new_tetro()

    def move_horizontal(self, spaces):
        """allow the tetromino to move left or right if there are no potential horizontal collisions"""
        if not self.check_horizontal_collision(spaces):
            for block in self.blocks:
                block.position.x += spaces

    def rotate(self):
        """rotates the tetro by 90 degrees clockwise"""
        if self.shape != 'O':
            pivot_point = self.blocks[0].position  # central block that piece will pivot around
            # get new positions of individual blocks after rotation
            new_block_positions = [block.rotate(pivot_point) for block in self.blocks]
            # update block positions accordingly
            for i, block in enumerate(self.blocks):
                block.position = new_block_positions[i]


class Block(pygame.sprite.Sprite):  # inherit pygames sprite.Sprite class
    """Class to handle the individual blocks of a tetromino"""
    def __init__(self, group, position, colour):
        # Constructor, parameters group (of sprites), position (x, y) and colour
        super().__init__(group)
        self.image = pygame.Surface((current_game_size[GAME_GRID], current_game_size[GAME_GRID]))
        self.image.fill(colour)
        self.position = (pygame.Vector2(position) +
                         pygame.Vector2(current_game_size[GAME_COLS]//2-2, -2))  # set to roughly centre
        x = self.position.x * current_game_size[GAME_GRID]
        y = self.position.y * current_game_size[GAME_GRID]
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        """update position of block"""
        self.rect.topleft = self.position * current_game_size[GAME_GRID]

    def horizontal_collide(self, x_coord, board_pieces):
        """check collision with left and right walls"""
        if not 0 <= x_coord < current_game_size[GAME_COLS]:
            return True
        """check collision with other tetrominos"""
        if board_pieces[int(self.position.y)][x_coord]:
            return True

    def vertical_collide(self, y_coord, board_pieces):
        """check collision with floor"""
        if y_coord >= current_game_size[GAME_ROWS]:
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
