from global_settings import *
from os import path


# Class to handle the display of the HUD in the game screen
class Hud:
    def __init__(self):
        # Constructor, no parameters
        self.surface = pygame.Surface((400, HUD_HEIGHT))
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
