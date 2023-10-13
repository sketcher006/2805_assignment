from os import path
from tetris import Tetris
from hud import Hud
from button import Button
from config import Config
from utility import *
from global_settings import pygame
import global_settings



class Main:
    """Main class to handle the game in its entirety"""
    def __init__(self):
        """initialise game"""
        pygame.init()
        icon = pygame.image.load(path.join("images", "icon.png"))
        pygame.display.set_icon(icon)
        pygame.display.set_caption("2805 Tetris")
        total_window_width = 3*global_settings.PADDING + global_settings.GAME_WIDTH + global_settings.HUD_WIDTH
        total_window_height = 2*global_settings.PADDING + global_settings.GAME_HEIGHT
        self.display_surface = pygame.display.set_mode((total_window_width, total_window_height))
        self.clock = pygame.time.Clock()
        self.config = Config()
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
        self.pause_page2 = pygame.image.load(path.join("images", "PAUSED.png")).convert_alpha()

        # load button images
        return_img = pygame.image.load(path.join("images", "return.png")).convert_alpha()
        play_img = pygame.image.load(path.join("images", "play.png")).convert_alpha()
        score_img = pygame.image.load(path.join("images", "score.png")).convert_alpha()
        config_img = pygame.image.load(path.join("images", "config.png")).convert_alpha()
        exit_img = pygame.image.load(path.join("images", "exit.png")).convert_alpha()
        yes_img = pygame.image.load(path.join("images", "yes.png")).convert_alpha()
        no_img = pygame.image.load(path.join("images", "no.png")).convert_alpha()
        btn_small_img = pygame.image.load(path.join("images", "btn_small.png")).convert_alpha()
        btn_normal_img = pygame.image.load(path.join("images", "btn_normal.png")).convert_alpha()
        btn_large_img = pygame.image.load(path.join("images", "btn_large.png")).convert_alpha()

        btn_1_img = pygame.image.load(path.join("images", "btn_1.png")).convert_alpha()
        btn_2_img = pygame.image.load(path.join("images", "btn_2.png")).convert_alpha()
        btn_3_img = pygame.image.load(path.join("images", "btn_3.png")).convert_alpha()
        btn_4_img = pygame.image.load(path.join("images", "btn_4.png")).convert_alpha()
        btn_5_img = pygame.image.load(path.join("images", "btn_5.png")).convert_alpha()
        btn_6_img = pygame.image.load(path.join("images", "btn_6.png")).convert_alpha()

        btn_normal2_img = pygame.image.load(path.join("images", "btn_normal.png")).convert_alpha()
        btn_extended_img = pygame.image.load(path.join("images", "btn_extended.png")).convert_alpha()

        btn_human_img = pygame.image.load(path.join("images", "btn_human.png")).convert_alpha()
        btn_ai_img = pygame.image.load(path.join("images", "btn_ai.png")).convert_alpha()

        # create buttons
        self.return_home_btn = Button(270, 700, return_img)
        self.yes_btn = Button(120, 550, yes_img)
        self.no_btn = Button(400, 550, no_img)
        self.play_btn = Button(124, 296, play_img)
        self.score_btn = Button(378, 296, score_img)
        self.config_btn = Button(124, 413, config_img)
        self.exit_btn = Button(378, 413, exit_img)
        self.small_btn = Button(120, 240, btn_small_img)
        self.normal_btn = Button(270, 240, btn_normal_img)
        self.large_btn = Button(420, 240, btn_large_img)
        self.n1_btn = Button(130, 340, btn_1_img)
        self.n2_btn = Button(200, 340, btn_2_img)
        self.n3_btn = Button(270, 340, btn_3_img)
        self.n4_btn = Button(340, 340, btn_4_img)
        self.n5_btn = Button(410, 340, btn_5_img)
        self.n6_btn = Button(480, 340, btn_6_img)
        self.normal2_btn = Button(130, 440, btn_normal2_img)
        self.extended_btn = Button(400, 440, btn_extended_img)
        self.human_btn = Button(130, 540, btn_human_img)
        self.ai_btn = Button(410, 540, btn_ai_img)

    def get_next_shape(self):
        """retrieve the first shape from the list of next shapes"""
        next_piece = self.next_shapes.pop(0)
        # replace popped piece for new random piece
        if global_settings.extended:
            self.next_shapes.append(random.choice(global_settings.EXTENDED_SHAPES_LIST))
        else:
            self.next_shapes.append(random.choice(global_settings.NORMAL_SHAPES_LIST))
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
            # Left-align i and name, and right-align score
            formatted_text = f"{i + 1:<3}{name:<10}{score:>6}"
            text = font.render(formatted_text, True, (255, 255, 255))
            text_rect = text.get_rect(center=(global_settings.WIDTH / 2, y_offset))
            self.display_surface.blit(text, text_rect)
            y_offset += 50

    def run(self):
        """Main loop to refresh screen"""
        if global_settings.extended:
            print("Extro yes")
        while True:
            # check for X pressed
            for event in global_settings.pygame.event.get():
                if event.type == global_settings.pygame.QUIT:
                    global_settings.pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        if self.game.pause:

                            reset_menu("Game")

            if global_settings.menu_system["Menu"]:  # display Menu screen
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

            elif global_settings.menu_system["Score"]:  # display Score screen
                # display the score background image
                self.display_surface.blit(self.score_page, (0, 0))
                self.display_top_scores()
                # check for button click to return to the main menu
                if self.return_home_btn.display(self.display_surface):
                    reset_menu("Menu")

            elif global_settings.menu_system["Config"]:  # display Config screen
                # display the config background image
                self.display_surface.blit(self.config_page, (0, 0))
                # create and run the config menu with current settings

                self.config.run()
                # check for button clicks to perform action
                if self.return_home_btn.display(self.display_surface):
                    reset_menu("Menu")
                if self.small_btn.display(self.display_surface):
                    print("small pressed")
                    global_settings.current_game_size = global_settings.GAME_SIZE_SMALL
                    update_game_size()
                    self.game = Tetris(self.update_score, self.get_next_shape, self.hud.reset_hud_stats)
                if self.normal_btn.display(self.display_surface):
                    print("normal pressed")
                    global_settings.current_game_size = global_settings.GAME_SIZE_NORMAL
                    update_game_size()
                    self.game = Tetris(self.update_score, self.get_next_shape, self.hud.reset_hud_stats)
                if self.large_btn.display(self.display_surface):
                    print("large pressed")
                    global_settings.current_game_size = global_settings.GAME_SIZE_LARGE
                    update_game_size()
                    self.game = Tetris(self.update_score, self.get_next_shape, self.hud.reset_hud_stats)
                if self.n1_btn.display(self.display_surface):
                    print("1 pressed")
                    global_settings.start_level = 1
                    global_settings.start_speed = global_settings.start_speed_1
                    self.hud = Hud()
                    self.game = Tetris(self.update_score, self.get_next_shape, self.hud.reset_hud_stats)
                if self.n2_btn.display(self.display_surface):
                    print("2 pressed")
                    global_settings.start_level = 2
                    global_settings.start_speed = global_settings.start_speed_2
                    self.hud = Hud()
                    self.game = Tetris(self.update_score, self.get_next_shape, self.hud.reset_hud_stats)
                if self.n3_btn.display(self.display_surface):
                    print("3 pressed")
                    global_settings.start_level = 3
                    global_settings.start_speed = global_settings.start_speed_3
                    self.hud = Hud()
                    self.game = Tetris(self.update_score, self.get_next_shape, self.hud.reset_hud_stats)
                if self.n4_btn.display(self.display_surface):
                    print("4 pressed")
                    global_settings.start_level = 4
                    global_settings.start_speed = global_settings.start_speed_4
                    self.hud = Hud()
                    self.game = Tetris(self.update_score, self.get_next_shape, self.hud.reset_hud_stats)
                if self.n5_btn.display(self.display_surface):
                    print("5 pressed")
                    global_settings.start_level = 5
                    global_settings.start_speed = global_settings.start_speed_5
                    self.hud = Hud()
                    self.game = Tetris(self.update_score, self.get_next_shape, self.hud.reset_hud_stats)
                if self.n6_btn.display(self.display_surface):
                    print("6 pressed")
                    global_settings.start_level = 6
                    global_settings.start_speed = global_settings.start_speed_6
                    self.hud = Hud()
                    self.game = Tetris(self.update_score, self.get_next_shape, self.hud.reset_hud_stats)
                if self.normal2_btn.display(self.display_surface):
                    print("normal pressed")
                    global_settings.extended = False
                    print("extended:", global_settings.extended)
                if self.extended_btn.display(self.display_surface):
                    print("extended pressed")
                    global_settings.extended = True
                    print("extended:", global_settings.extended)
                if self.human_btn.display(self.display_surface):
                    print("human pressed")
                    global_settings.human = True
                    print("human mode:", global_settings.human)
                if self.ai_btn.display(self.display_surface):
                    print("ai pressed")
                    global_settings.human = False
                    print("human mode:", global_settings.human)

            elif global_settings.menu_system["Game"]:  # Display Game screen
                # display grey background and run game and hud
                self.display_surface.fill("Grey15")
                self.game.run()
                self.hud.run(self.next_shapes)

            elif global_settings.menu_system["Pause"]:  # display pause menu
                # display the pause menu background image
                self.display_surface.blit(self.pause_page, (0, 0))
                # check for yes/no button clicks
                if self.yes_btn.display(self.display_surface):
                    # self.game.save_high_score() # if they quit, no high score
                    self.game.reset_game_stats()
                    self.hud.reset_hud_stats()
                    self.game.bg_music.stop()
                    self.game.music_playing = False
                    self.hud = Hud()
                    self.game = Tetris(self.update_score, self.get_next_shape, self.hud.reset_hud_stats)
                    reset_menu("Menu")
                if self.no_btn.display(self.display_surface):
                    reset_menu("Game")

            elif global_settings.menu_system["Pause2"]:  # display pause2 menu
                self.display_surface.blit(self.pause_page2, (0, 0))



            global_settings.pygame.display.update()
            self.clock.tick(50)


# MAIN PROGRAM
game = Main()
game.run()
