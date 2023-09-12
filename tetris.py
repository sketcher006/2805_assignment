from global_settings import *
from timer import Timer
from os import path


class Tetris:
    def __init__(self, update_score, get_next_shape, reset_hud_stats):
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft=(PADDING, PADDING))
        self.sprites = pygame.sprite.Group()
        self.update_score = update_score
        self.get_next_shape = get_next_shape
        self.reset_hud_stats = reset_hud_stats

        self.board_pieces = [[0 for i in range(COLUMNS)] for j in range(ROWS)]
        self.tetro = Tetros(get_shape(), self.sprites, self.create_new_tetro, self.board_pieces)

        # timers
        self.down_speed = START_SPEED
        self.down_speed_fast = self.down_speed * .3
        self.down_pressed = False
        self.vertical_timer = Timer(START_SPEED, True, self.move_down)
        self.vertical_timer.start()
        self.horizontal_timer = Timer(MAX_BUTTON_DELAY)
        self.rotational_timer = Timer(MAX_BUTTON_DELAY)

        # score
        self.current_level = 1
        self.current_score = 0
        self.current_lines = 0

    def reset_game_stats(self):
        self.current_level = 1
        self.current_score = 0
        self.current_lines = 0
        self.board_pieces = [[0 for i in range(COLUMNS)] for j in range(ROWS)]
        self.down_speed = START_SPEED
        self.down_speed_fast = self.down_speed * .3
        # self.vertical_timer = Timer(START_SPEED, True, self.move_down)
        self.sprites.empty()

    def save_high_score(self):
        # save high score to external file
        with open(path.join("assets", "high_scores.txt"), 'a') as high_scores:
            high_scores.write(str(self.current_score) + "\n")

    def check_game_over(self):
        for block in self.tetro.blocks:
            if block.position.y < 0:
                # display GAME OVER
                print("GAME OVER")

                self.save_high_score()

                # reset stats ready for new game
                self.reset_game_stats()
                self.reset_hud_stats()

                reset_menu(menu_system, MENU)
                break

    def create_new_tetro(self):
        self.check_game_over()
        self.check_for_completed_row()
        self.tetro = Tetros(self.get_next_shape(), self.sprites, self.create_new_tetro, self.board_pieces)

    def move_down(self):
        # print("time tick")
        self.tetro.move_down()

    def update_timers(self):
        self.vertical_timer.update()
        self.horizontal_timer.update()
        self.rotational_timer.update()

    def draw_grid(self):
        for col in range(1, COLUMNS):
            pygame.draw.line(self.surface, (30, 30, 0), (col * GRID_SIZE, 0), (col * GRID_SIZE, HEIGHT-PADDING))

        for row in range(1, ROWS):
            pygame.draw.line(self.surface, (30, 30, 0), (0, row * GRID_SIZE), (GAME_WIDTH, row * GRID_SIZE))

    def user_input(self):
        # get user input key pressed
        user_input = pygame.key.get_pressed()

        # check if it was left or right
        if not self.horizontal_timer.active:
            if user_input[pygame.K_LEFT]:
                self.tetro.move_horizontal(-1)
                self.horizontal_timer.start()
            if user_input[pygame.K_RIGHT]:
                self.tetro.move_horizontal(1)
                self.horizontal_timer.start()

        # check if it was up
        if not self.rotational_timer.active:
            if user_input[pygame.K_UP]:
                self.tetro.rotate()
                self.rotational_timer.start()

        if not self.down_pressed and user_input[pygame.K_DOWN]:
            self.down_pressed = True
            self.vertical_timer.duration = self.down_speed_fast

        if self.down_pressed and not user_input[pygame.K_DOWN]:
            self.down_pressed = False
            self.vertical_timer.duration = self.down_speed

        # check if it was escape
        if user_input[pygame.K_ESCAPE]:
            print("Escape pressed")
            print("down speed", self.down_speed)
            print("vert timer", self.vertical_timer.duration)
            reset_menu(menu_system, PAUSE)

    def check_for_completed_row(self):
        # get index of any full row
        remove_rows = []
        for row in range(len(self.board_pieces)):
            if all(self.board_pieces[row]):
                remove_rows.append(row)

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
            self.board_pieces = [[0 for i in range(COLUMNS)] for j in range(ROWS)]
            for block in self.sprites:
                self.board_pieces[int(block.position.y)][int(block.position.x)] = block

            self.calculate_score(len(remove_rows))

    def calculate_score(self, cleared_lines):
        self.current_lines += cleared_lines
        self.current_score += SCORES[cleared_lines] * self.current_level
        if self.current_lines / 10 > self.current_level:
            self.current_level += 1
            self.down_speed *= 0.8
            self.down_speed_fast = self.down_speed * .3
            self.vertical_timer.duration = self.down_speed
        self.update_score(self.current_lines, self.current_score, self.current_level)

    def run(self):
        self.user_input()
        self.update_timers()
        self.sprites.update()
        self.surface.fill('#000000')
        self.sprites.draw(self.surface)
        self.draw_grid()
        self.display_surface.blit(self.surface, (PADDING, PADDING))


class Tetros:
    def __init__(self, shape, group, create_new_tetro, board_pieces):
        self.shape = shape
        self.block_positions = TETROS[shape]["shape"]
        self.colour = TETROS[shape]["colour"]
        self.create_new_tetro = create_new_tetro
        self.board_pieces = board_pieces
        self.reset = False

        self.blocks = []
        for position in self.block_positions:
            block = Block(group, position, self.colour)
            self.blocks.append(block)

    def check_horizontal_collision(self, spaces):
        collisions = []
        for block in self.blocks:
            collisions.append(block.horizontal_collide(int(block.position.x + spaces), self.board_pieces))
        for item in collisions:
            if item:
                return True
        return False

    def check_vertical_collision(self, spaces):
        collisions = []
        for block in self.blocks:
            collisions.append(block.vertical_collide(int(block.position.y + spaces), self.board_pieces))
        for item in collisions:
            if item:
                return True
        return False

    def move_down(self):
        # check block is within boundary
        if not self.check_vertical_collision(1) and not self.reset:
            for block in self.blocks:
                block.position.y += 1
                # print(block.rect.y)
            # print("move down")
        else:
            self.reset = False
            for block in self.blocks:
                self.board_pieces[int(block.position.y)][int(block.position.x)] = block
            self.create_new_tetro()

    def move_horizontal(self, spaces):
        if not self.check_horizontal_collision(spaces):
            for block in self.blocks:
                block.position.x += spaces

    def rotate(self):
        # print("rotate")
        if self.shape != 'O':
            pivot_point = self.blocks[0].position

            # new block positions
            new_block_positions = [block.rotate(pivot_point) for block in self.blocks]

            for i, block in enumerate(self.blocks):
                block.position = new_block_positions[i]


class Block(pygame.sprite.Sprite):
    def __init__(self, group, position, colour):
        super().__init__(group)
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(colour)

        self.position = pygame.Vector2(position) + pygame.Vector2(COLUMNS//2-2, -2)  # set to roughly centre
        x = self.position.x * GRID_SIZE
        y = self.position.y * GRID_SIZE
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        # get pos to update rect
        # self.rect = self.image.get_rect(topleft=self.position * GRID_SIZE)
        self.rect.topleft = self.position * GRID_SIZE

    def horizontal_collide(self, x_coord, board_pieces):
        if not 0 <= x_coord < COLUMNS:
            return True

        if board_pieces[int(self.position.y)][x_coord]:
            return True

    def vertical_collide(self, y_coord, board_pieces):
        if y_coord >= ROWS:
            return True

        if y_coord >= 0 and board_pieces[y_coord][int(self.position.x)]:
            return True

    def rotate(self, pivot_point):
        distance = self.position - pivot_point
        rotated = distance.rotate(90)
        new_position = pivot_point + rotated
        return new_position