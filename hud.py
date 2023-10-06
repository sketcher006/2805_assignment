import global_settings
from os import path


class Hud:
    """Class to handle the display of the HUD in the game screen"""
    def __init__(self):
        """Constructor, no parameters"""
        self.surface = global_settings.pygame.Surface((global_settings.HUD_WIDTH, global_settings.HUD_HEIGHT))
        self.display_surface = global_settings.pygame.display.get_surface()
        self.font = global_settings.pygame.font.Font(path.join("assets", "Arcade.ttf"), 30)

        # game statistics
        self.score = 0
        self.level = 1
        self.lines = 0

        # create dictionary to store shape image previews
        self.shape_surfaces = {}
        shape_names = global_settings.TETROS.keys()
        for shape in shape_names:
            image_path = path.join("images", f"{shape}.png")
            shape_surface = global_settings.pygame.image.load(image_path).convert_alpha()
            self.shape_surfaces[shape] = shape_surface

    def reset_hud_stats(self):
        """initialise game statistics"""
        self.score = 0
        self.level = 1
        self.lines = 0

    def display_text(self, position, text):
        """display custom text at certain location"""
        text_surface = self.font.render(text, True, "#ffffff")
        text_rect = text_surface.get_rect(topleft=position)
        self.surface.blit(text_surface, text_rect)

    def display_pieces(self, shapes):
        """loops through the 2 preview shapes and draws them onto the surface"""
        for i, shape in enumerate(shapes):
            shape_surface = self.shape_surfaces[shape]
            self.surface.blit(shape_surface, (50, 140+180*i))

    def run(self, next_shapes):
        """runs and displays all elements of the HUD"""
        self.surface.fill("#000000")
        self.display_pieces(next_shapes)
        self.display_text((70, 20), "Group 17")
        self.display_text((50, 80), "Next pieces")
        global_settings.pygame.draw.line(self.surface, "#ffffff", (10, 60), (235, 60), 3)
        self.display_text((20, 550), f"Score: {self.score}")
        self.display_text((20, 600), f"Lines: {self.lines}")
        self.display_text((20, 650), f"Level: {self.level}")
        self.display_text((20, 700), f"Extended: {global_settings.extended}")
        mode = "Human" if global_settings.human else "AI"
        self.display_text((20, 750), f"Mode: {mode}")
        self.display_surface.blit(
            self.surface, (2 * global_settings.PADDING + global_settings.GAME_WIDTH, global_settings.PADDING)
        )
