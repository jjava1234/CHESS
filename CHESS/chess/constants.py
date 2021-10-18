import pygame
import os

def flatten(l):
    for el in l:
        if isinstance(el, list):
            yield from flatten(el)
        else:
                yield el

lineOfSight = epMOVES = []
allMOVES = {(255,255,255):{}, (0,0,0):{}}
pSQUARE = set() # protected square; invalid enemy king move
pColors = [(255,255,255), (0,0,0)]
epMOVES = ()
cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in %r: %s" % (cwd, files))


SQUARESIZE = 80
ROWS = 8
COLS = 8

pNAMES = ['bR', 'bH', 'bB', 'bK', 'bQ', 'bP', 
         'wR', 'wH', 'wB', 'wK', 'wQ', 'wP']
images = {}

for piece in pNAMES:
    images[piece] = pygame.transform.scale(pygame.image.load('chess/assets/' + piece + ".png"), (65, 60))            

