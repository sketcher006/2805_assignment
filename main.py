from global_settings import *
from os import path
from tetris import Tetris
from hud import Hud
from button import Button
from config import Config


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