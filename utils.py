from os import walk # Traverse through directories
import pygame

def import_path(path):
    surfaceList = []

    for folderName, subfolders, imageFiles in walk(path): # only need image files
        # # Returns list with contents of the folder
        # #     PATH               NO SUBFOLDER         FILES
        # # ('graphics/character/up', [], ['2.png', '3.png', '1.png', '0.png'])
        
        for image in imageFiles:
            # Path to folder + image name itself
            fullPath = f"{path}/{image}"
            imageSurface = pygame.image.load(fullPath).convert_alpha() # Makes image transparent and optimises
            surfaceList.append(imageSurface)

    return surfaceList

class Timer:
    # Starts at default of 0 start time, the time is continously checked for a certain duration
    # if the time is after a certain furation then run a function

    def __init__(self, duration, function = None): # function runs when the timer has run out
        self.duration = duration
        self.function = function
        self.startTime = 0 
        self.active = False
    
    def activate(self):
        self.active = True
        self.startTime = pygame.time.get_ticks() # This allows the timer to be started at any point within the game and not just the start
    
    def deactivate(self):
        self.active = False
        self.startTime = 0

    def update(self):
        currentTime = pygame.time.get_ticks() # Holds current time
        if currentTime - self.startTime >= self.duration:
            # Timer has run out
            self.deactivate()
            if self.function: self.function() # run function at the end of the timer if defined by user