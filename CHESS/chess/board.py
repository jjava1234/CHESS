from pieces import *
from constants import *

bPieces = [Rook, Horse, Bishop, Queen, King, Bishop, Horse, Rook]
wPieces = bPieces[::-1]


class Board():
    def __init__(self, window, game):
        self.board_layout = []
        self.selected = None
        self.game = game
        self.win = window
        self.bK_pos = (4,0)
        self.wK_pos = (3,7)
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

                        #board[row].append(Pawn(col, row, (0,0,0), 1, "bP", self.win))
                elif row > 5:
                    if row == 7:
                        board[row].append(wPieces[col](col, row, (255,255,255), f"w{wPieces[col].__name__[0]}", self.win))
                    else: 
                          board[row].append(0)

                        #board[row].append(Pawn(col, row, (255,255,255), -1, "wP", self.win))
                else:
                    board[row].append(0)


    def captureCheck(self, move):
        x, y = move[0], move[1]
        if piece := self.board_layout[y][x]:
            piece = 0
    
    def switchTurn(self, game):
        game.turn = game.pColors[(game.pColors.index(game.turn)+1)%2]

    def movePiece(self, piece, oldIMAGES, move):
        oldIMAGES.append((piece.x, piece.y))
        
        self.captureCheck(move)

        if piece.pName[1] == "K":
            pass
        newX, newY = move[0], move[1]
        self.board_layout[newY][newX], piece = piece, self.board_layout[newY][newX]
        
            #see if king's move gets him checked or 

        piece = self.board_layout[newY][newX] 
        self.undraw(self.board_layout, oldIMAGES)
        piece.updatePIECE(self.win, (newX, newY))
        

        #self.kingCheck()
        self.switchTurn(self.game)
        

    def drawMOVES(self, valid_moves):
        for move in valid_moves:
            pygame.draw.circle(self.win, (0,0,255), (move[0]*80+40, move[1]*80+40), 15)
        return valid_moves

    def undraw(self, board, positions, undrawMoves=False):
        print(positions)
        colors = [(210,180,140), (111,78,55)]
        for pos in positions:
            pygame.draw.rect(self.win, colors[(pos[0]+pos[1])%2], (pos[0]*80, pos[1]*80, 80, 80))     
            
            if undrawMoves and (piece := board[pos[1]][pos[0]]):
                piece.drawPIECE(self.win)
        self.selected.valid_moves.clear()

    def captureCheck(self, piece):
        pass

    def select(self, x, y):
        print(x//80,y//80)
        if (piece := self.board_layout[y//80][x//80]) and self.board_layout[y//80][x//80].color == self.game.turn:
            if self.selected != piece:
                if self.selected:
                    self.undraw(self.board_layout, self.selected.valid_moves, True) #undraw moves           
                self.selected = piece
                self.selected.valid_moves = self.drawMOVES(self.selected.calc_moves(self.board_layout))
                
        elif validMOVES := self.selected.valid_moves:
            if (x//80, y//80) in validMOVES:
                self.movePiece(self.selected, self.selected.valid_moves, (x//80, y//80))

                    
        #else:


#move function: see if opponent piece's new pos puts enemy's king in danger 

