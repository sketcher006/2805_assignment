import global_settings
from os import path
from button import Button
from utility import reset_menu


class Config:
    """Class to handle the display and control of the configuration settings"""
    def __init__(self):
        """Constructor, parameters game_size (size of the game grid), game_level (current game level), normal_extended
        (boolean representing normal pieces or extended pieces), game_mode (human or AI)"""
        # self.game_size = global_settings.current_game_size
        self.surface = global_settings.pygame.display.get_surface()
        self.font = global_settings.pygame.font.Font(path.join("assets", "Arcade.ttf"), 30)

    def display_text(self, position, text):
        """method to display text in a certain font at a certain position"""
        text_surface = self.font.render(text, True, "#ffffff")
        text_rect = text_surface.get_rect(topleft=position)
        self.surface.blit(text_surface, text_rect)

    def run(self):
        """method to display the current parameters of the game"""
        text = "Extended" if global_settings.extended else "Normal"
        mode = "Human" if global_settings.human else "AI"
        self.display_text(
            (60, 200),
            f"Game size: {int(global_settings.current_game_size[0])} x "
            f"{int(global_settings.current_game_size[1])}"
        )
        self.display_text((60, 300), f"Level: {global_settings.start_level}")

        self.display_text((60, 400), f"Normal/Extended: {text}")
        self.display_text((60, 500), f"Mode: {mode}")
        self.surface.blit(self.surface, (0, 0))
