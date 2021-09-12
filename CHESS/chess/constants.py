import sys
import pygame

import os

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in %r: %s" % (cwd, files))


SQUARESIZE = 80
ROWS = 8
COLS = 8

pNAMES = ["bR", "bN", "bB", "bK", "bQ", "bP", 
         "wR", "wN", "wB", "wK", "bQ", "bP"]
images = {}

for piece in pNAMES:
    images[piece] = pygame.transform.scale(pygame.image.load('chess/assets/' + piece + ".png"), (65, 60))            

