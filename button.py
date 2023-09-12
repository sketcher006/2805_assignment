from global_settings import *


# Class to handle button objects
class Button:
    def __init__(self, x, y, image):
        # Constructor, parameters x, y (coords) and image (file location)
        self.image = image
        self.rect = image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def display(self, screen):
        # method to display the button and check for interaction
        action = False
        mouse_pos = pygame.mouse.get_pos()

        # trigger action if button is clicked
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        # reset button if mouse is not clicked
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action
