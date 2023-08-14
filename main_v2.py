from global_settings import *
from pygame.locals import *

MENU = 0
SCORE = 1
CONFIG = 2
GAME = 3

#             [menu,  score, confg, game]
menu_system = [True, False, False, False]


def reset_menu(menu):
    # clear menu option
    for i in range(4):
        menu[i] = False


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


class Text:
    # class to manage the display of text within pygame
    def __init__(self, text, x, y, colour, size, centered):
        self.centered = centered
        self.display_surface = pygame.display.get_surface()
        font = pygame.font.Font("Arcade.ttf", size)
        self.text = font.render(text, True, colour)
        self.x = x
        self.y = y

    def display_text(self):
        if self.centered:
            text_rect = self.text.get_rect(center=(self.display_surface.get_width()/2, self.y))
            self.display_surface.blit(self.text, text_rect)
        else:
            self.display_surface.blit(self.text, (self.x, self.y))


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


class Score:
    def __init__(self):
        self.surface = pygame.Surface((HUD_WIDTH, HUD_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.group_txt = Text("Group 17", 500, 30, "#ffffff", 30, False)
        self.score_txt = Text("Score:", 460, 500, "#ffffff", 30, False)
        self.lines_txt = Text("Lines:", 460, 550, "#ffffff", 30, False)
        self.level_txt = Text("Level:", 460, 600, "#ffffff", 30, False)
        self.extend_txt = Text("Extended:", 460, 650, "#ffffff", 30, False)
        self.mode_txt = Text("Mode:", 460, 700, "#ffffff", 30, False)



    def run(self):
        self.surface.fill("#000000")

        self.display_surface.blit(self.surface, (2 * PADDING + GAME_WIDTH, PADDING))
        self.group_txt.display_text()
        self.score_txt.display_text()
        self.lines_txt.display_text()
        self.level_txt.display_text()
        self.extend_txt.display_text()
        self.mode_txt.display_text()


class Tetros:
    def __init__(self, shape, group, create_new_tetro, board_pieces):
        self.block_positions = TETROS[shape]["shape"]
        self.colour = TETROS[shape]["colour"]
        self.create_new_tetro = create_new_tetro
        self.board_pieces = board_pieces

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
        if not self.check_vertical_collision(1):
            for block in self.blocks:
                block.position.y += 1
                # print(block.rect.y)
        else:
            for block in self.blocks:
                self.board_pieces[int(block.position.y)][int(block.position.x)] = block
            self.create_new_tetro()

    def move_horizontal(self, spaces):
        if not self.check_horizontal_collision(spaces):
            for block in self.blocks:
                block.position.x += spaces


class Tetris:
    def __init__(self):
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft=(PADDING, PADDING))
        self.sprites = pygame.sprite.Group()

        # normal_shapes_list = ["I", "J", "L", "O", "S", "T", "Z"]
        # extended_shapes_list = ["I", "J", "L", "O", "S", "T", "Z", "I_extended", "J_extended"]
        # if EXTENDED:
        #     random_shape = random.choice(extended_shapes_list)
        # else:
        #     random_shape = random.choice(normal_shapes_list)

        self.board_pieces = [[0 for i in range(COLUMNS)] for j in range(ROWS)]
        self.tetro = Tetros(self.get_shape(), self.sprites, self.create_new_tetro, self.board_pieces)

        # timers
        self.vertical_timer = Timer(START_SPEED, True, self.move_down)
        self.vertical_timer.start()
        self.horizontal_timer = Timer(MAX_BUTTON_DELAY)

    def get_shape(self):
        normal_shapes_list = ["I", "J", "L", "O", "S", "T", "Z"]
        extended_shapes_list = ["I", "J", "L", "O", "S", "T", "Z", "I_extended", "J_extended"]
        if EXTENDED:
            random_shape = random.choice(extended_shapes_list)
        else:
            random_shape = random.choice(normal_shapes_list)
        return random_shape

    def create_new_tetro(self):
        self.check_for_completed_row()
        self.tetro = Tetros(self.get_shape(), self.sprites, self.create_new_tetro, self.board_pieces)

    def move_down(self):
        print("time tick")
        self.tetro.move_down()

    def update_timers(self):
        self.vertical_timer.update()
        self.horizontal_timer.update()

    def draw_grid(self):
        for col in range(1, COLUMNS):
            pygame.draw.line(self.surface, (30, 30, 0), (col * GRID_SIZE, 0), (col * GRID_SIZE, HEIGHT-PADDING))

        for row in range(1, ROWS):
            pygame.draw.line(self.surface, (30, 30, 0), (0, row * GRID_SIZE), (GAME_WIDTH, row * GRID_SIZE))

    def user_input(self):
        user_input = pygame.key.get_pressed()

        if not self.horizontal_timer.active:
            if user_input[pygame.K_LEFT]:
                self.tetro.move_horizontal(-1)
                self.horizontal_timer.start()
            if user_input[pygame.K_RIGHT]:
                self.tetro.move_horizontal(1)
                self.horizontal_timer.start()
            if user_input[pygame.K_UP]:
                pass
            if user_input[pygame.K_DOWN]:
                pass
        if user_input[pygame.K_ESCAPE]:
            print("Escape pressed")
            print(menu_system)
            reset_menu(menu_system)
            print(menu_system)
            menu_system[MENU] = True
            print(menu_system)
            # show pause game menu

    def check_for_completed_row(self):
        # get index of any full row
        remove_rows = []
        # for i, row in enumerate(self.board_pieces):
        #     if all(row):
        #         remove_rows.append(i)
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


class Main:
    def __init__(self):
        pygame.init()
        icon = pygame.image.load("icon.png")
        pygame.display.set_icon(icon)
        pygame.display.set_caption("2805 Tetris")
        total_window_width = 3*PADDING + GAME_WIDTH + HUD_WIDTH
        total_window_height = 2*PADDING + GAME_HEIGHT
        print(total_window_width, total_window_height)
        self.display_surface = pygame.display.set_mode((total_window_width, total_window_height))
        self.clock = pygame.time.Clock()

        self.game = Tetris()
        self.score = Score()

        # self.display_surface = pygame.display.get_surface()
        self.home_page = pygame.image.load("home.png")
        self.score_page = pygame.image.load("scores.png")
        self.config_page = pygame.image.load("configpage.png")

        return_img = pygame.image.load('return.png').convert_alpha()
        self.returnbtn = Button(270, 700, return_img)
        self.returnbtn_game = Button(470, 750, return_img)

        play_img = pygame.image.load('play.png').convert_alpha()
        self.play = Button(124, 296, play_img)
        score_img = pygame.image.load('score.png').convert_alpha()
        self.score_btn = Button(378, 296, score_img)
        config_img = pygame.image.load('config.png').convert_alpha()
        self.config = Button(124, 413, config_img)
        exit_img = pygame.image.load('exit.png').convert_alpha()
        self.exit = Button(378, 413, exit_img)

    def run(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            if menu_system[0]:  # Menu
                self.display_surface.blit(self.home_page, (0, 0))
                if self.play.display(self.display_surface):
                    print("Play clicked")
                    reset_menu(menu_system)
                    menu_system[GAME] = True
                    print(menu_system)
                if self.score_btn.display(self.display_surface):
                    print("Score clicked")
                    reset_menu(menu_system)
                    menu_system[SCORE] = True
                    print(menu_system)
                if self.config.display(self.display_surface):
                    print("Config clicked")
                    reset_menu(menu_system)
                    menu_system[CONFIG] = True
                    print(menu_system)
                if self.exit.display(self.display_surface):
                    print("Exit clicked")
                    reset_menu(menu_system)
                    pygame.quit()
                    exit()
                pass
            elif menu_system[SCORE]:  # Score
                self.display_surface.blit(self.score_page, (0, 0))
                if self.returnbtn.display(self.display_surface):
                    print("Return clicked")
                    reset_menu(menu_system)
                    menu_system[MENU] = True
                    print(menu_system)
            elif menu_system[CONFIG]:  # config
                self.display_surface.blit(self.config_page, (0, 0))
                if self.returnbtn.display(self.display_surface):
                    print("Return clicked")
                    reset_menu(menu_system)
                    menu_system[MENU] = True
                    print(menu_system)
            elif menu_system[GAME]: # game
                self.display_surface.fill("Grey15")
                self.game.run()
                self.score.run()




                if self.returnbtn_game.display(self.display_surface):
                    print("Return clicked")
                    reset_menu(menu_system)
                    menu_system[MENU] = True
                    print(menu_system)
            # print("menu:", self.running, "play", self.playing)


            pygame.display.update()
            self.clock.tick(50)


# MAIN PROGRAM


game = Main()
game.run()










