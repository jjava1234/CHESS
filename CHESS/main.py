from chess.board import Board
from chess.game import Game
import pygame

win = pygame.display.set_mode((640,640))
pygame.display.set_caption("Chess")
game = Game()
board = Board(win, game)
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()  
            board.select(pos[0], pos[1])

    pygame.display.update()

