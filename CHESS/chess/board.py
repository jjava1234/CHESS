from chess.pieces import bishop, king
from .pieces import *
from .constants import *

bPieces = [rook.Rook, knight.Knight, bishop.Bishop, queen.Queen, king.King, bishop.Bishop, knight.Knight, rook.Rook]
wPieces = bPieces[::-1]


class Board():
    def __init__(self, window, game):
        self.board_layout = []
        self.game = game
        self.win = window
        self.selected = None
        self.create_board()
        

    def create_board(self):
        self.win.fill((111,78,55))
        for row in range(ROWS):
            for col in range(row%2, COLS, 2):
                pygame.draw.rect(self.win, (210,180,140), (col*80, row*80, 80, 80))
        self.create_pieces()

    def create_pieces(self):
        board = self.board_layout
        for row in range(8):
            board.append([])
            for col in range(8):
                if row < 2:
                    if row == 0:
                        board[row].append(bPieces[col](col, row, (0,0,0)))
                    else:
                        board[row].append(pawn.Pawn(col, row, (0,0,0), 1))
                elif row > 5:
                    if row == 7:
                        board[row].append(wPieces[col](col, row, (255,255,255)))
                    else: 
                        board[row].append(pawn.Pawn(col, row, (255,255,255), -1))
                else:
                    board[row].append(0)
        self.draw_pieces()


    def draw_pieces(self):
        board = self.board_layout
        for row in board:
            for piece in row:
                if piece:
                    if piece.color == (0,0,0):
                        for bPiece in bP_images:
                            if bPiece == piece.pName:
                                self.win.blit(bP_images[bPiece], (((piece.x*80 + 40) - bP_images[bPiece].get_width()//2, (piece.y*80 + 40) - bP_images[bPiece].get_height()//2)))
                    else:
                        for wPiece in wP_images:
                            if wPiece == piece.pName:
                                self.win.blit(wP_images[wPiece], (((piece.x*80 + 40) - bP_images[bPiece].get_width()//2, (piece.y*80 + 40) - bP_images[bPiece].get_height()//2)))
    
    
    def draw_moves(self, valid_moves):
        print(valid_moves)
        for move in valid_moves:
            pygame.draw.circle(self.win, (0,0,255), (move[0]*80+40, move[1]*80+40), 15)

    def undraw_moves(self, valid_moves):
        for move in valid_moves:
            if move[0]%2 == move[1]%2:
                print(move[0], move[1])
                pygame.draw.rect(self.win, (210,180,140), (move[0]*80, move[1]*80, 80, 80))
            else:
                pygame.draw.rect(self.win, (111,78,55), (move[0]*80, move[1]*80, 80, 80))


    def select(self, x, y):
        if piece := self.board_layout[y//80][x//80]:
            if self.selected != piece:
                if self.selected:
                    self.undraw_moves(self.selected.valid_moves)            
                    self.selected.valid_moves.clear()
                self.selected = piece
                self.draw_moves(self.selected.calc_moves(self.board_layout))

                    
        #else:


#move function: see if opponent piece's new pos puts enemy's king in danger 
