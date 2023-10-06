from os import path
from tetris import Tetris
from hud import Hud
from button import Button
from config import Config
from utility import *


class Main:
    """Main class to handle the game in its entirety"""
    def __init__(self):
        """initialise game"""
        pygame.init()
        icon = pygame.image.load(path.join("images", "icon.png"))
        pygame.display.set_icon(icon)
        pygame.display.set_caption("2805 Tetris")
        total_window_width = 3*PADDING + GAME_WIDTH + HUD_WIDTH
        total_window_height = 2*PADDING + GAME_HEIGHT
        self.display_surface = pygame.display.set_mode((total_window_width, total_window_height))
        self.clock = pygame.time.Clock()

        # get next shapes loaded ready for game to begin
        self.next_shapes = [get_shape() for i in range(2)]

        # create hud and game objects
        self.hud = Hud()
        self.game = Tetris(self.update_score, self.get_next_shape, self.hud.reset_hud_stats)

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
        """retrieve the first shape from the list of next shapes"""
        next_piece = self.next_shapes.pop(0)
        # replace popped piece for new random piece
        if extended:
            self.next_shapes.append(random.choice(EXTENDED_SHAPES_LIST))
        else:
            self.next_shapes.append(random.choice(NORMAL_SHAPES_LIST))
        return next_piece

    def update_score(self, lines, score, level):
        """update current score, lines and level"""
        self.hud.lines = lines
        self.hud.score = score
        self.hud.level = level

    def display_top_scores(self):
        # Read the data from the file into a list of tuples
        with open("assets/high_scores.txt", "r") as high_scores_file:
            high_scores_data = [line.strip().split(":") for line in high_scores_file]

        # Display the top ten scores on the screen
        font = pygame.font.Font(path.join("assets", "Arcade.ttf"), 50)
        y_offset = 170
        for i, (name, score) in enumerate(high_scores_data[:10]):
            text = font.render(f"{i + 1}. {name}: {score}", True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH / 2, y_offset))
            self.display_surface.blit(text, text_rect)
            y_offset += 50

    def run(self):
        """Main loop to refresh screen"""
        while True:
            # check for X pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            if menu_system["Menu"]:  # display Menu screen
                # display menu background image
                self.display_surface.blit(self.home_page, (0, 0))
                # check for button clicks and perform actions
                if self.play_btn.display(self.display_surface):
                    reset_menu("Game")
                if self.score_btn.display(self.display_surface):
                    reset_menu("Score")
                if self.config_btn.display(self.display_surface):
                    reset_menu("Config")
                if self.exit_btn.display(self.display_surface):
                    reset_menu("Menu")
                    pygame.quit()
                    exit()

            elif menu_system["Score"]:  # display Score screen
                # display the score background image
                self.display_surface.blit(self.score_page, (0, 0))
                self.display_top_scores()
                # check for button click to return to the main menu
                if self.return_home_btn.display(self.display_surface):
                    reset_menu("Menu")

            elif menu_system["Config"]:  # display Config screen
                # display the config background image
                self.display_surface.blit(self.config_page, (0, 0))
                # create and run the config menu with current settings
                config = Config(self.game.current_level, extended, human)
                config.run()
                # check for button clicks to perform action
                if self.return_home_btn.display(self.display_surface):
                    reset_menu("Menu")

            elif menu_system["Game"]:  # Display Game screen
                # display grey background and run game and hud
                self.display_surface.fill("Grey15")
                self.game.run()
                self.hud.run(self.next_shapes)

            elif menu_system["Pause"]:  # display pause menu
                # display the pause menu background image
                self.display_surface.blit(self.pause_page, (0, 0))
                # check for yes/no button clicks
                if self.yes_btn.display(self.display_surface):
                    # self.game.save_high_score() # if they quit, no high score
                    self.game.reset_game_stats()
                    self.hud.reset_hud_stats()

                    reset_menu("Menu")
                if self.no_btn.display(self.display_surface):
                    reset_menu("Game")

            pygame.display.update()
            self.clock.tick(50)


# MAIN PROGRAM
game = Main()
game.run()
