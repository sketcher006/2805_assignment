from global_settings import *
from pygame.locals import *


def check_exit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


class Timer:
    def __init__(self, duration, repeated=False, func=None):
        self.repeated = repeated
        self.func = func
        self.duration = duration

        self.start_time = 0
        self.active = False

    def start(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def stop(self):
        self.active = False
        self.start_time = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.active:
            if current_time - self.start_time >= self.duration:
                if self.func and self.start_time != 0:
                    self.func()
                self.stop()

                if self.repeated:
                    self.start()


class Text:
    def __init__(self, text, x, y, colour, size, centered):
        self.display_surface = pygame.display.get_surface()
        font = pygame.font.SysFont(None, size)
        self.text = font.render(text, True, colour)
        self.x = x
        self.y = y
        if centered:
            text_rect = self.text.get_rect(center=(self.display_surface.get_width()/2, y))
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


class Home:
    def __init__(self):
        #self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.background_image = pygame.image.load("home.png")
        play_img = pygame.image.load('play.png').convert_alpha()
        self.play = Button(124, 296, play_img)
        score_img = pygame.image.load('score.png').convert_alpha()
        self.score = Button(378, 296, score_img)
        config_img = pygame.image.load('config.png').convert_alpha()
        self.config = Button(124, 413, config_img)
        exit_img = pygame.image.load('exit.png').convert_alpha()
        self.exit = Button(378, 413, exit_img)

    def run(self):
        # self.display_surface.blit(self.surface, (PADDING, PADDING))
        self.display_surface.blit(self.background_image, (0, 0))
        if self.play.display(self.display_surface):
            print("Play clicked")
            return 1
        if self.score.display(self.display_surface):
            print("Score clicked")
            return 2
        if self.config.display(self.display_surface):
            print("Config clicked")
            return 3
        if self.exit.display(self.display_surface):
            print("Exit clicked")
            return 4


class Score:
    def __init__(self):
        self.surface = pygame.Surface((HUD_WIDTH, HUD_HEIGHT))
        self.display_surface = pygame.display.get_surface()

    def run(self):
        self.display_surface.blit(self.surface, (2 * PADDING + GAME_WIDTH, PADDING))


class Tetros:
    def __init__(self, shape, group):
        self.block_positions = TETROS[shape]["shape"]
        self.colour = TETROS[shape]["colour"]

        self.blocks = []
        for position in self.block_positions:
            block = Block(group, position, self.colour)
            self.blocks.append(block)

    def check_horizontal_collision(self, spaces):
        collisions = []
        for block in self.blocks:
            collisions.append(block.horizontal_collide(int(block.position.x + spaces)))
        for item in collisions:
            if item:
                return True
        return False

    def check_vertical_collision(self, spaces):
        collisions = []
        for block in self.blocks:
            collisions.append(block.vertical_collide(int(block.position.y + spaces)))
        for item in collisions:
            if item:
                return True
        return False

    def move_down(self):
        if not self.check_vertical_collision(1):
            for block in self.blocks:
                block.position.y += 1
                print(block.rect.y)

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

        normal_shapes_list = ["I", "J", "L", "O", "S", "T", "Z"]
        extended_shapes_list = ["I", "J", "L", "O", "S", "T", "Z", "I_extended", "J_extended"]
        if EXTENDED:
            random_shape = random.choice(extended_shapes_list)
        else:
            random_shape = random.choice(normal_shapes_list)
        self.tetro = Tetros(random_shape, self.sprites)

        # timers
        self.vertical_timer = Timer(START_SPEED, True, self.move_down)
        self.vertical_timer.start()
        self.horizontal_timer = Timer(MAX_BUTTON_DELAY)

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

    def horizontal_collide(self, x_coord):
        return not 0 <= x_coord < COLUMNS

    def vertical_collide(self, y_coord):
        return y_coord >= ROWS

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

        self.home = Home()
        self.game = Tetris()
        self.score = Score()

    def run(self):
        while True:
            check_exit()

            self.display_surface.fill("Grey15")

            # if game has not started, show start menu
            # self.home.run()
            # elif result == 1:  # Play
            #     while True:
            #         check_exit()
            self.game.run()
            self.score.run()
            # elif result == 2:  # Score
            #     pass
            # elif result == 3:  # Config
            #     pass
            # elif result == 4:  # Exit
            #     pygame.quit()
            #     exit()




            # after game has begun
            # self.game.run()
            # self.score.run()

            pygame.display.update()
            self.clock.tick(50)


# MAIN PROGRAM
game = Main()
game.run()
