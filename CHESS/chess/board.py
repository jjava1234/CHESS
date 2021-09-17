from pieces import *
from constants import *

bPieces = [Rook, Horse, Bishop, Queen, King, Bishop, Horse, Rook]
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
                        board[row].append(bPieces[col](col, row, (0,0,0), f"b{bPieces[col].__name__[0]}", self.win))
                    else:
                        board[row].append(0)

            #            board[row].append(Pawn(col, row, (0,0,0), 1, "bP", self.win))
                elif row > 5:
                    if row == 7:
                        board[row].append(wPieces[col](col, row, (255,255,255), f"w{wPieces[col].__name__[0]}", self.win))
                    else: 
                          board[row].append(0)

         #               board[row].append(Pawn(col, row, (255,255,255), -1, "wP", self.win))
                else:
                    board[row].append(0)
        self.draw_pieces()


    def draw_pieces(self):
        pass
    
    def draw_moves(self, valid_moves):
        for move in valid_moves:
            pygame.draw.circle(self.win, (0,0,255), (move[0]*80+40, move[1]*80+40), 15)
        return valid_moves

    def undraw_moves(self, board, valid_moves):
        colors = [(210,180,140), (111,78,55)]
        for move in valid_moves:
            pygame.draw.rect(self.win, colors[(move[0]+move[1])%2], (move[0]*80, move[1]*80, 80, 80))     
            if piece := board[move[1]][move[0]]:
                piece.draw_piece(self.win)

    def select(self, x, y):
        if piece := self.board_layout[y//80][x//80]:
            if self.selected != piece:
                if select := self.selected:
                    self.undraw_moves(self.board_layout, self.selected.valid_moves)            
                    self.selected.valid_moves.clear()
                self.selected = piece
                self.selected.valid_moves = self.draw_moves(self.selected.calc_moves(self.board_layout))

                    
        #else:


#move function: see if opponent piece's new pos puts enemy's king in danger 


