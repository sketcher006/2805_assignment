from global_settings import *
from os import path


# !!! NEED TO ADD ABILITY TO CHANGE THESE SETTINGS !!! #

# Class to handle the display and control of the configuration settings
class Config:
    # Constructor, parameters game_size (size of the game grid), game_level (current game level), normal_extended
    # (boolean representing normal pieces or extended pieces), game_mode (human or AI)
    def __init__(self, game_size, game_level, normal_extended, game_mode):
        self.game_size = game_size
        self.game_level = game_level
        self.normal_extended = normal_extended
        self.game_mode = game_mode
        self.surface = pygame.display.get_surface()
        self.font = pygame.font.Font(path.join("assets", "Arcade.ttf"), 30)

    def display_text(self, position, text):
        # method to display text in a certain font at a certain position
        text_surface = self.font.render(text, True, "#ffffff")
        text_rect = text_surface.get_rect(topleft=position)
        self.surface.blit(text_surface, text_rect)

    def run(self):
        # method to display the current parameters of the game
        text = "Extended" if self.normal_extended else "Normal"
        mode = "Human" if self.game_mode else "AI"

        self.display_text((60, 200), f"Game size: {int(self.game_size[0]/GRID_SIZE)} x {int(self.game_size[1]/GRID_SIZE)}")
        self.display_text((60, 300), f"Level: {self.game_level}")

        self.display_text((60, 400), f"Normal/Extended: {text}")
        self.display_text((60, 500), f"Mode: {mode}")
        self.surface.blit(self.surface, (0, 0))
