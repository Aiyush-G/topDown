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