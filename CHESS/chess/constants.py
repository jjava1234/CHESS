import pygame

SQUARESIZE = 80
ROWS = 8
COLS = 8

bP_images = {"rook": pygame.transform.scale(pygame.image.load('./assets/bR.png'), (65, 60)), 
              "knight": pygame.transform.scale(pygame.image.load('./assets/bN.png'), (65,60)),
              "bishop": pygame.transform.scale(pygame.image.load('./assets/bB.png'), (65,60)),
              "queen" :pygame.transform.scale(pygame.image.load('./assets/bQ.png'), (65,60)),
              "king": pygame.transform.scale(pygame.image.load('./assets/bK.png'), (65,60)),
              "pawn": pygame.transform.scale(pygame.image.load('./assets/bP.png'), (65,60))}

wP_images = {"rook": pygame.transform.scale(pygame.image.load('./assets/wR.png'), (65, 60)), 
              "knight": pygame.transform.scale(pygame.image.load('./assets/wN.png'), (65,60)),
              "bishop": pygame.transform.scale(pygame.image.load('./assets/wB.png'), (65,60)),
              "queen" :pygame.transform.scale(pygame.image.load('./assets/wQ.png'), (65,60)),
              "king": pygame.transform.scale(pygame.image.load('./assets/wK.png'), (65,60)),
              "pawn": pygame.transform.scale(pygame.image.load('./assets/wP.png'), (65,60))}  

