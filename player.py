import pygame
from settings import *
from utils import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group) # As soon as Player is instanced the object will be inside of this group

        # SETUP
        self.import_assets() # Animations
        self.status = "down_idle" # Status of player
        self.frameIndex = 0 # Animation reference
        self.image = self.animations[self.status][self.frameIndex] # Gets 
        # OLD CODE self.image.fill("green") 
        self.rect = self.image.get_rect(center = pos)

        # MOVEMENT
        # The direction that the sprite should move: -1, 1
        # If y is -ve 1, move up
        self.direction = pygame.math.Vector2() #x, y default: 0, 0 
        self.pos = pygame.math.Vector2(self.rect.center) # to be frame-rate independent vector 2 is needed
        self.speed = 200
    
    def import_assets(self):
        # Allows for dynamic loading of images without hardcoding paths directly
        self.animations = {'up': [],'down': [],'left': [],'right': [],
						   'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
						   'right_hoe':[],'left_hoe':[],'up_hoe':[],'down_hoe':[],
						   'right_axe':[],'left_axe':[],'up_axe':[],'down_axe':[],
						   'right_water':[],'left_water':[],'up_water':[],'down_water':[]}
        
        for animation in self.animations.keys(): # Itterates over the key value pairs for the surfaces as the values
            fullPath = "graphics/character/" + animation
            self.animations[animation] = import_path(fullPath)
        
        print(self.animations)
    
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
        # Normalised vector: the vector should always be 1
        if self.direction.magnitude() > 0: # For a vector to be normalised it should be greater than 0 length
            self.direction = self.direction.normalize() # Without this going diagonal is root 2 speed instead of a single unit, therefore, faster.
        
        # For collision management the movements need to split into their components
        # HORIZONTAL
        self.pos.x += self.direction.x * self.speed * delta_time
        self.rect.centerx = self.pos.x
        # VERTICAL
        self.pos.y += self.direction.y * self.speed * delta_time
        self.rect.centery = self.pos.y
        
    
    def update(self, delta_time):
        self.input()
        self.move(delta_time)