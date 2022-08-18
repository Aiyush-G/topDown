import pygame
from settings import *
from player import Player

class Level:
    def __init__(self):
        
        # Surface shown to player
        self.display_surface = pygame.display.get_surface()

        # Sprite groups
        self.all_sprites = pygame.sprite.Group() # helper to update sprites

        self.setup()

    def setup(self):
        self.player = Player((640, 360), self.all_sprites) # pos, group

    def run(self, delta_time):
        # print("Running Game")
        self.display_surface.fill("#000000") # black
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(delta_time) # calls update on all children, and passes dt