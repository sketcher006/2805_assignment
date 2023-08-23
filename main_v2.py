import pygame as pygame

from global_settings import *
from os import path

MENU = 0
SCORE = 1
CONFIG = 2
GAME = 3
PAUSE = 4


#             [menu,  score, confg, game, pause]
menu_system = [True, False, False, False, False]


def reset_menu(menu, destination):
    # clear menu option
    for i in range(len(menu)):
        menu[i] = False
    menu[destination] = True


def get_shape():
    print("extended:", EXTENDED)
    normal_shapes_list = ["I", "J", "L", "O", "S", "T", "Z"]
    extended_shapes_list = ["I", "J", "L", "O", "S", "T", "Z", "I_extend", "J_extend"]
    if EXTENDED:
        random_shape = random.choice(extended_shapes_list)
    else:
        random_shape = random.choice(normal_shapes_list)
    print(random_shape)
    return random_shape


class Timer:
    # class to manage timers for the game
    def __init__(self, duration, repeated=False, func=None):
        self.repeated = repeated
        self.func = func
        self.duration = duration

        self.start_time = 0
        self.active = False

    def start(self):
        # start the timer
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def stop(self):
        # stop the timer
        self.active = False
        self.start_time = 0

    def update(self):
        # update the time within the timer
        current_time = pygame.time.get_ticks()
        if self.active:
            if current_time - self.start_time >= self.duration:
                if self.func and self.start_time != 0:
                    self.func()
                self.stop()

                if self.repeated:
                    self.start()


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def display(self, screen):
        action = False
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                print("CLICKED")
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action


class Hud:
    def __init__(self):
        self.surface = pygame.Surface((HUD_WIDTH, HUD_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(path.join("assets", "Arcade.ttf"), 30)

        self.score = 0
        self.level = 1
        self.lines = 0

        self.shape_surfaces = {
            shape: pygame.image.load(path.join("images", f"{shape}.png")).convert_alpha() for shape in TETROS.keys()
        }

    def reset_hud_stats(self):
        self.score = 0
        self.level = 1
        self.lines = 0

    def display_text(self, position, text):
        text_surface = self.font.render(text, True, "#ffffff")
        text_rect = text_surface.get_rect(topleft=position)
        self.surface.blit(text_surface, text_rect)

    def display_pieces(self, shapes):
        for i, shape in enumerate(shapes):
            shape_surface = self.shape_surfaces[shape]
            self.surface.blit(shape_surface, (50, 140+180*i))

    def run(self, next_shapes):
        self.surface.fill("#000000")
        self.display_pieces(next_shapes)
        self.display_text((70, 20), "Group 17")
        self.display_text((50, 80), "Next pieces")
        pygame.draw.line(self.surface, "#ffffff", (10, 60), (235, 60), 3)
        self.display_text((20, 550), f"Score: {self.score}")
        self.display_text((20, 600), f"Lines: {self.lines}")
        self.display_text((20, 650), f"Level: {self.level}")
        self.display_text((20, 700), f"Extended: {EXTENDED}")
        self.display_text((20, 750), f"Mode: Human")
        self.display_surface.blit(self.surface, (2 * PADDING + GAME_WIDTH, PADDING))


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


class Config:
    def __init__(self, game_size, game_level, normal_extended, game_mode):
        self.game_size = game_size
        self.game_level = game_level
        self.normal_extended = normal_extended
        self.game_mode = game_mode
        self.surface = pygame.display.get_surface()
        self.font = pygame.font.Font(path.join("assets", "Arcade.ttf"), 30)

    def display_text(self, position, text):
        text_surface = self.font.render(text, True, "#ffffff")
        text_rect = text_surface.get_rect(topleft=position)
        self.surface.blit(text_surface, text_rect)

    def run(self):
        text = "Extended" if self.normal_extended else "Normal"
        mode = "Human" if self.game_mode else "AI"

        self.display_text((60, 200), f"Game size: {int(self.game_size[0]/GRID_SIZE)} x {int(self.game_size[1]/GRID_SIZE)}")
        self.display_text((60, 300), f"Level: {self.game_level}")

        self.display_text((60, 400), f"Normal/Extended: {text}")
        self.display_text((60, 500), f"Mode: {mode}")
        self.surface.blit(self.surface, (0,0))


class Main:
    def __init__(self):
        # initialise game
        pygame.init()
        icon = pygame.image.load(path.join("images", "icon.png"))
        pygame.display.set_icon(icon)
        pygame.display.set_caption("2805 Tetris")
        total_window_width = 3*PADDING + GAME_WIDTH + HUD_WIDTH
        total_window_height = 2*PADDING + GAME_HEIGHT
        print(total_window_width, total_window_height)
        self.display_surface = pygame.display.set_mode((total_window_width, total_window_height))
        self.clock = pygame.time.Clock()

        # get next shapes ready for game to begin
        self.next_shapes = [get_shape() for i in range(2)]

        # start game instance
        self.hud = Hud()
        self.game = Tetris(self.update_score, self.get_next_shape, self.hud.reset_hud_stats)
        self.config = Config((GAME_WIDTH, GAME_HEIGHT), self.game.current_level, EXTENDED, HUMAN)

        # load background image files
        self.home_page = pygame.image.load(path.join("images", "home.png")).convert_alpha()
        self.score_page = pygame.image.load(path.join("images", "scores.png")).convert_alpha()
        self.config_page = pygame.image.load(path.join("images", "configpage.png")).convert_alpha()
        self.pause_page = pygame.image.load(path.join("images", "pausepage.png")).convert_alpha()

        # load button images
        return_img = pygame.image.load(path.join("images", "return.png")).convert_alpha()
        play_img = pygame.image.load(path.join("images", "play.png")).convert_alpha()
        score_img = pygame.image.load(path.join("images", "score.png")).convert_alpha()
        config_img = pygame.image.load(path.join("images", "config.png")).convert_alpha()
        exit_img = pygame.image.load(path.join("images", "exit.png")).convert_alpha()
        yes_img = pygame.image.load(path.join("images", "yes.png")).convert_alpha()
        no_img = pygame.image.load(path.join("images", "no.png")).convert_alpha()

        # create buttons
        self.return_home_btn = Button(270, 700, return_img)
        self.yes_btn = Button(120, 550, yes_img)
        self.no_btn = Button(400, 550, no_img)
        self.play_btn = Button(124, 296, play_img)
        self.score_btn = Button(378, 296, score_img)
        self.config_btn = Button(124, 413, config_img)
        self.exit_btn = Button(378, 413, exit_img)

    def get_next_shape(self):
        next_piece = self.next_shapes.pop(0)

        normal_shapes_list = ["I", "J", "L", "O", "S", "T", "Z"]
        extended_shapes_list = ["I", "J", "L", "O", "S", "T", "Z", "I_extend", "J_extend"]
        if EXTENDED:
            self.next_shapes.append(random.choice(extended_shapes_list))

        else:
            self.next_shapes.append(random.choice(normal_shapes_list))

        # self.next_shapes.append(random.choice(list(TETROS.keys())))
        print(next_piece)
        return next_piece

    def update_score(self, lines, score, level):
        self.hud.lines = lines
        self.hud.score = score
        self.hud.level = level

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            if menu_system[0]:  # Menu
                self.display_surface.blit(self.home_page, (0, 0))
                if self.play_btn.display(self.display_surface):
                    print("Play clicked")
                    reset_menu(menu_system, GAME)
                if self.score_btn.display(self.display_surface):
                    print("Score clicked")
                    reset_menu(menu_system, SCORE)
                if self.config_btn.display(self.display_surface):
                    print("Config clicked")
                    reset_menu(menu_system, CONFIG)
                if self.exit_btn.display(self.display_surface):
                    print("Exit clicked")
                    reset_menu(menu_system, MENU)
                    pygame.quit()
                    exit()
                pass
            elif menu_system[SCORE]:  # Score
                self.display_surface.blit(self.score_page, (0, 0))
                if self.return_home_btn.display(self.display_surface):
                    print("Return clicked")
                    reset_menu(menu_system, MENU)
            elif menu_system[CONFIG]:  # config
                self.display_surface.blit(self.config_page, (0, 0))
                self.config.run()
                if self.return_home_btn.display(self.display_surface):
                    print("Return clicked")
                    reset_menu(menu_system, MENU)
            elif menu_system[GAME]:  # game
                self.display_surface.fill("Grey15")
                self.game.run()
                self.hud.run(self.next_shapes)
            elif menu_system[PAUSE]:  # pause menu
                self.display_surface.blit(self.pause_page, (0, 0))
                if self.yes_btn.display(self.display_surface):
                    print("Yes clicked")
                    self.game.save_high_score()
                    self.game.reset_game_stats()
                    self.hud.reset_hud_stats()
                    self.game.vertical_timer.duration = START_SPEED
                    self.game.tetro.reset = True
                    reset_menu(menu_system, MENU)
                    menu_system[MENU] = True
                    # restart the game
                if self.no_btn.display(self.display_surface):
                    print("No clicked")
                    reset_menu(menu_system, GAME)
                    menu_system[GAME] = True
                    # restart the game

            pygame.display.update()
            self.clock.tick(50)


# MAIN PROGRAM
game = Main()
game.run()
