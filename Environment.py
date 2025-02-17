import os
import pygame


class Environment:
    screen = None
    size = None

    def __init__(self):
        # Initialize the display for all platforms
        pygame.display.init()
        pygame.display.set_caption("Project 1 AI")  # Window title
        self.size = (1000, 800)  # Window size
        self.screen = pygame.display.set_mode(self.size)

        # Clear the screen to white
        self.screen.fill((255, 255, 255))
        # Initialize font support
        pygame.font.init()
        # Hide the mouse cursor
        pygame.mouse.set_visible(False)
        # Update the display
        pygame.display.update()

    def getPath(self):
        return os.path.dirname(os.path.abspath(__file__))

        # elif self.getUserInterface() == "graphics":
        # 	pygame.display.init()
        # 	pygame.display.set_caption("pySokoban")
        # 	self.size = (800,600)
        # 	self.screen = pygame.display.set_mode(self.size)
