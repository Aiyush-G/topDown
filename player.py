import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group) # As soon as Player is instanced the object will be inside of this group
        
        # SETUP
        self.image = pygame.Surface((32, 64)) 
        self.image.fill("green")
        self.rect = self.image.get_rect(center = pos)

        # MOVEMENT
        # The direction that the sprite should move: -1, 1
        # If y is -ve 1, move up
        self.direction = pygame.math.Vector2() #x, y default: 0, 0 
        self.pos = pygame.math.Vector2(self.rect.center) # to be frame-rate independent vector 2 is needed
        self.speed = 200
    
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:       #print("up")
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:   #print("down")    
            self.direction.y = 1
        else:                       # Refreshes every cycle so on nokey sprite shouldn't move
            self.direction.y = 0 

        if keys[pygame.K_RIGHT]:    #print("right")
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:   #print("left")
            self.direction.x = -1
        else:
            self.direction.x = 0
        
        # print(self.direction) >>> [0,0]
    
    def move(self, delta_time):
        # Framerate independence is achieved here
        self.pos += self.direction * self.speed * delta_time
        self.rect.center = self.pos
    
    def update(self, delta_time):
        self.input()
        self.move(delta_time)