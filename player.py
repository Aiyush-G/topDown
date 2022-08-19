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
        

        # TOOLS
        self.tools = ["hoe", "axe", "water"]
        self.toolIndex = 0
        self.selectedTool = self.tools[self.toolIndex]

        # TIMERS
        self.timers = {
            "toolUse" : Timer(350, self.use_tool), 
            "toolSwitch" : Timer(250)
        }
    
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
        
        #print(self.animations)
    
    def animate(self, deltaTime):
        # Loops over the individual sprites surfaces smoothly and returns back to first sprite image at the end
        self.frameIndex += 4 * deltaTime
        if self.frameIndex >= len(self.animations[self.status]):
            self.frameIndex = 0
        self.image = self.animations[self.status][int(self.frameIndex)]
    
    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers["toolUse"].active:
            # MOVEMENT  
            if keys[pygame.K_UP]:       #print("up")
                self.direction.y = -1
                self.status = "up"      # Animation
            elif keys[pygame.K_DOWN]:   #print("down")    
                self.direction.y = 1
                self.status = "down"
            else:                       # Refreshes every cycle so on nokey sprite shouldn't move
                self.direction.y = 0
                #self.status = "down_idle"

            if keys[pygame.K_RIGHT]:    #print("right")
                self.direction.x = 1
                self.status = "right"
            elif keys[pygame.K_LEFT]:   #print("left")
                self.direction.x = -1
                self.status = "left"
            else:
                self.direction.x = 0
                #self.status = "down_idle"
            # print(self.direction) >>> [0,0]

        # TOOLS
        if keys[pygame.K_SPACE]:
            # If player clicks space then the tool is actice for a certain amount of time
            self.timers["toolUse"].activate()
            self.direction = pygame.math.Vector2() # Stops the player from moving when the tool animation is in use
            self.frameIndex = 0 # Restarts animation from beginning FIXED BUG
        
        # CHANGE TOOL
        # If the "t" key is held down for multiple inputs then the index keeps changing, to solve this an additional timer 
        # is implemented here
        if keys[pygame.K_t] and not self.timers["toolSwitch"].active:
            self.timers["toolSwitch"].activate()
            print(self.toolIndex)
            self.toolIndex += 1
            self.toolIndex = self.toolIndex if self.toolIndex < len(self.tools) else 0 
            self.selectedTool = self.tools[self.toolIndex]

    def use_tool(self):
        pass
        #print(self.selectedTool)

    def get_status(self):
        # IDLE
        # If player isn't moving then transfer to idle state
        if self.direction.magnitude() == 0:
            self.status = f"{self.status.split('_')[0]}_idle" # Look at the naming of the animations: left_idle, down_idle, up_idle, right_idle

        if self.timers["toolUse"].active:
            self.status = f"{self.status.split('_')[0]}_{self.selectedTool}"
            
    
    def update_timers(self):
        for timer in self.timers.values(): # Itterates over each individual timer
            timer.update()

    def move(self, deltaTime):
        # Framerate independence is achieved here
        # Normalised vector: the vector should always be 1
        if self.direction.magnitude() > 0: # For a vector to be normalised it should be greater than 0 length
            self.direction = self.direction.normalize() # Without this going diagonal is root 2 speed instead of a single unit, therefore, faster.
        
        # For collision management the movements need to split into their components
        # HORIZONTAL
        self.pos.x += self.direction.x * self.speed * deltaTime
        self.rect.centerx = self.pos.x
        # VERTICAL
        self.pos.y += self.direction.y * self.speed * deltaTime
        self.rect.centery = self.pos.y
        
    
    def update(self, deltaTime):
        self.input()
        self.update_timers()
        self.get_status()
        self.move(deltaTime)
        self.animate(deltaTime)