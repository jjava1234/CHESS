import sys
import pygame

import os

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in %r: %s" % (cwd, files))


SQUARESIZE = 80
ROWS = 8
COLS = 8

pNAMES = ["bR", "bH", "bB", "bK", "bQ", "bP", 
         "wR", "wH", "wB", "wK", "wQ", "wP"]
images = {}

for piece in pNAMES:
    print(piece)
    images[piece] = pygame.transform.scale(pygame.image.load('chess/assets/' + piece + ".png"), (65, 60))            
