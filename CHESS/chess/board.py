import config
from pieces import *

bPieces = [Rook, Horse, Bishop, Queen, King, Bishop, Horse, Rook]
wPieces = bPieces[::-1]

class Board():
    def __init__(self, window, game):
        self.board_layout = pPIECE = []
        self.selected = None
        self.game = game
        self.KingsPOS = [(3,7), (4,0)] 
        self.win = window
        self.old_checks = {}
        self.check = []
        self.create_board()
 

    def create_board(self):
        self.win.fill((111,78,55))
        for row in range(config.ROWS):
            for col in range(row%2, config.COLS, 2):
                config.pygame.draw.rect(self.win, (210,180,140), (col*80, row*80, 80, 80))
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
                        board[row].append(Pawn(col, row, (0,0,0), 1, "bP", self.win))
                elif row > 5:
                    if row == 7:
                        board[row].append(wPieces[col](col, row, (255,255,255), f"w{wPieces[col].__name__[0]}", self.win))
                    else: 
                        board[row].append(Pawn(col, row, (255,255,255), -1, "wP", self.win))
                else:
                    board[row].append(0)


    def capture(self, move):
        if (piece := self.board_layout[move[1]][move[0]]):
            if piece in (pMOVES:= config.allMOVES[self.game.pColors[(self.game.pColors.index(self.game.turn)+1)%2]]):
                del pMOVES[piece]            
            self.board_layout[move[1]][move[0]] = 0

    def record_eMOVES(self, piece):
        if piece.pName[1] != "K":
            config.allMOVES[self.game.turn][piece] = piece.calc_moves(self.board_layout, self.check)

    def nextTurn(self, game):
        game.turn = game.pColors[(game.pColors.index(game.turn)+1)%2]
    
    def stuck(self, piece):
        #check if piece is protecting king
        if (piece.x, piece.y) in self.old_checks:
            oldCHECK = self.old_checks[(piece.x, piece.y)]
            x = oldCHECK[0]
            y = oldCHECK[1]
            if self.board_layout[y][x]:
                return True
            else:
                del oldCHECK
                return False


    def movePiece(self, piece, oldIMAGES, move):
        if self.check:
            allEnemyMOVES = config.allMOVES[self.game.pColors[(self.game.pColors.index(self.game.turn)+1)%2]]
            for eMOVES in allEnemyMOVES.items():
                if piece.pName[1] == "K":                     
                    #TODO: calc king's remaining moves; if none, call checkmate
                    if piece.calc_moves(self.board_layout):
                        pass

                    if move in eMOVES:
                        return
                    config.pSQUARE.clear()
                    self.check = []

                else:      
                    if move not in list(config.flatten([self.check, config.lineOfSight])):
                        return
                    allEnemyMOVES[eMOVES[0]] = eMOVES[0].calc_moves(self.board_layout, self.check)
                    self.old_checks[move] = list(self.check)[0]
                    self.check = []
                    config.lineOfSight.clear()
                    

                    #if move not in self.check or len(self.check) > 1: 
                    #    pass
        
        if piece.pName[1] == "K":
            self.KingsPOS[self.game.pColors.index(self.game.turn)] = move

        if piece.pName[1] == "P":  
            if piece.y - move[1] in (-2, 2) and move[1] in (3,4):
                config.epMOVES = move #enPassant move
            elif piece.x - move[0] not in (-1, 1):
                config.epMOVES = ()
            elif piece.y - move[1] in (-1, 1) and piece.x - move[0] in (-1, 1):
                config.epMOVES = () 
        else:
            config.epMOVES = ()


        if self.stuck(piece):
            return
                 
        oldIMAGES.append((piece.x, piece.y))
        newX, newY = move[0], move[1]
        
        # pawn enPassant
        if config.epMOVES:
            capturedPIECE = (move[0], move[1] + piece.dir*-1)
            self.capture(capturedPIECE)
            oldIMAGES.append(capturedPIECE)
            print()
        else:
            self.capture(move)

        self.board_layout[newY][newX], self.board_layout[piece.y][piece.x] = piece, self.board_layout[newY][newX]        
        piece = self.board_layout[newY][newX] 
        self.undraw(self.board_layout, oldIMAGES)
        piece.updatePIECE(self.win, (newX, newY))
        
        # self.validCheck(piece)

        # see if move opened up a check
        eKingPOS = self.KingsPOS[(self.game.pColors.index(self.game.turn)+1)%2]
        x = eKingPOS[0]
        y = eKingPOS[1]
        config.lineOfSight.clear()
        self.board_layout[y][x].calc_safety(self.board_layout, self.check)
        
        self.record_eMOVES(piece)

        self.nextTurn(self.game)
        
        
    def drawMOVES(self, piece, valid_moves):
        if self.stuck(piece):
            return
        for move in valid_moves:
            if self.check and move not in list(config.flatten([self.check, config.lineOfSight])) and piece.pName[1] != "K":
                continue
            if not self.board_layout[move[1]][move[0]] or self.board_layout[move[1]][move[0]].color != self.game.turn:
                config.pygame.draw.circle(self.win, (0,0,255), (move[0]*80+40, move[1]*80+40), 15)
        return valid_moves

    def undraw(self, board, positions):
        colors = [(210,180,140), (111,78,55)]
        if positions:
            for pos in positions:
                config.pygame.draw.rect(self.win, colors[(pos[0]+pos[1])%2], (pos[0]*80, pos[1]*80, 80, 80))     
                if (piece := board[pos[1]][pos[0]]):
                    piece.drawPIECE(self.win)
            self.selected.valid_moves.clear()


    def select(self, x, y):
        
        print()
        for row in self.board_layout:
            for col in row:
                if col:
                    print(col.pName, end=" ")
                else:
                    print("0", end="  ")
            print()

        if (piece := self.board_layout[y//80][x//80]) and self.board_layout[y//80][x//80].color == self.game.turn:
            if self.selected != piece:
                if self.selected:
                    self.undraw(self.board_layout, self.selected.valid_moves) 
                self.selected = piece
                self.selected.valid_moves = self.drawMOVES(self.selected, self.selected.calc_moves(self.board_layout, self.check))
                
        elif self.selected and (validMOVES := self.selected.valid_moves):
            if (x//80, y//80) in validMOVES:
                self.movePiece(self.selected, validMOVES, (x//80, y//80))
        #else:


#move function: see if opponent piece's new pos puts enemy's king in danger 
