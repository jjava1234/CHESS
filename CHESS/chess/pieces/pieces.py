from itertools import permutations
from constants import *

enPASSANT = False
pPIECE = {} #protected piece; i.e invalid enemy king move

#LEFT / RIGHT
def calc_LR(board, piece, movesList, x, y, dir):    
    if -1 < x < 8 and -1 < y < 8:
        if board[y][x] and board[y][x].color == piece.color:
            pPIECE[piece] = (board[y][x].x, board[y][x].x)
            return movesList        
        movesList.append((x, y))
        if not board[y][x]:
            return calc_LR(board, piece, movesList, x+dir, y, dir)
    return movesList

# UP / DOWN
def calc_UD(board, piece, movesList, x, y, dir): 
    if -1 < x < 8 and -1 < y < 8:
        if board[y][x] and board[y][x].color == piece.color:
            pPIECE[piece] = (board[y][x].x, board[y][x].x) 
            return movesList
        movesList.append((x, y))
        if not board[y][x]:
            return calc_UD(board, piece, movesList, x, y+dir, dir)
    return movesList


#DIAGONALS
def calc_DI(board, piece, movesList, x, y, dir, reversed=1):
    if -1 < x < 8 and -1 < y < 8:
        if board[y][x] and board[y][x].color == piece.color:
            pPIECE[piece] = (board[y][x].x, board[y][x].x)
            return movesList
        movesList.append((x,y))
        if not board[y][x]:
            return calc_DI(board, piece, movesList, x+dir, y+dir*reversed, dir, reversed)
    return movesList
    

def calc_all_moves(self, board, LR = False, UD = False, DI = False):
    moves = []
    for dir in (-1, 1):
        if LR and UD:
            moves.extend(calc_UD(board, self, [], self.x, self.y+dir, dir))
            moves.extend(calc_LR(board, self, [], self.x+dir, self.y, dir))
        if DI:
            moves.extend(calc_DI(board, self, [], self.x+dir, self.y+dir, dir))
            moves.extend(calc_DI(board, self, [], self.x+dir, self.y+dir*-1, dir, -1))
    
    return moves

        
class Piece():
    def __init__(self, x, y, color, piece_name, win):
        self.x = x
        self.y = y
        self.color = color
        self.valid_moves = []
        self.pName = piece_name
        self.drawPIECE(win)

    def drawPIECE(self, win):
        win.blit(images[self.pName], (((self.x*80 + 40) - images[self.pName].get_width()//2, (self.y*80 + 40) - images[self.pName].get_height()//2)))


    def updatePIECE(self, win, newPOS):
        self.x, self.y = newPOS[0], newPOS[1]        
        self.drawPIECE(win)

class Pawn(Piece):
    def __init__(self, x, y, color, dir, pName, win):
        super().__init__(x, y, color, pName, win)
        self.dir = dir

    def valid_DJ(self, moves): #double jump
        if (self.y == 1 and self.color == (0,0,0)) or (self.y == 6 and self.color == (255,255,255)):
            return (self.x, self.y+self.dir*2)
    
    def captureMoves(self, board, moves):
        if not board[self.y+self.dir][self.x] and board[self.y+self.dir][self.x].color == self.color and self.y in (0,7):   
            return (self.x, self.y+self.dir)
 
    def enPASSANT(self, board, moves):
        for side in (-1,1):
            if self.y in (3,4) and enPASSANT and board[self.y][self.x+side]:
                return (self.x, self.y)

    def calc_moves(self, board):
        return [self.valid_DJ(), self.captureMoves, self.enPASSANT()]


class Rook(Piece):
    def __init__(self, x, y, color, pName, win):
        super().__init__(x, y, color, pName, win)
    
    def calc_moves(self, board):
        return calc_all_moves(self, board, True, True, False)

#King and Knight starts with same letter
class Horse(Piece):     
    def __init__(self, x, y, color, pName, win):
        super().__init__(x, y, color, pName, win)
    
    
    def calc_moves(self, board, moves=[]):
        dirs = [(-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]
        for dir in dirs:
            if -1 < (y := self.y+dir[1]) < 8 and -1 < (x := self.x+dir[0]) < 8:
                if board[y][x]:
                    if self.color != board[y][x].color:
                        moves.append((x, y))
                    else:
                        pPIECE[self] = (x,y)
                else:
                    moves.append((x,y))

        return moves

class Bishop(Piece):
    def __init__(self, x, y, color, pName, win):
        super().__init__(x, y, color, pName, win)
    
    def calc_moves(self, board):
        return calc_all_moves(self, board, False, False, True)


class Queen(Piece):
    def __init__(self, x, y, color, pName, win):
        super().__init__(x, y, color, pName, win)

    def calc_moves(self, board): 
        return calc_all_moves(self, board, True, True, True)
            

class King(Piece):
    def __init__(self, x, y, color, pName, win):
        super().__init__(x, y, color, pName, win)

    def calc_moves(self, board, moves=[]):
        dirs = list(permutations([0, -1, -1, 1, 1], 2))
        for dir in dirs:
            x = self.x+dir[0]
            y = self.y+dir[1]
            if -1 < y < 8 and -1 < x < 8:
                if not board[y][x] or self.color != board[y][x].color:
                    moves.append((self.x + dir[0], self.y+dir[1]))                        
                elif board[y][x]:
                    pPIECE[self] = (board[y][x].x, board[y][x].x) 

        return moves
