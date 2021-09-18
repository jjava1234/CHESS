from itertools import permutations
from constants import images

#LEFT / RIGHT
def calc_LR(board, piece, movesList, x, y, dir):    
    if -1 < x < 8 and -1 < y < 8:
        if board[y][x] and board[y][x].color == piece.color:
            return movesList        
        movesList.append((x, y))
        if not board[y][x]:
            return calc_LR(board, piece, movesList, x+dir, y, dir)
    return movesList

# UP / DOWN
def calc_UD(board, piece, movesList, x, y, dir): 
    if -1 < x < 8 and -1 < y < 8:
        if board[y][x] and board[y][x].color == piece.color:
            return movesList
        movesList.append((x, y))
        if not board[y][x]:
            return calc_UD(board, piece, movesList, x, y+dir, dir)
    return movesList


#DIAGONALS
def calc_DI(board, piece, movesList, x, y, dir, reversed=1):
    if -1 < x < 8 and -1 < y < 8:
        if board[y][x] and board[y][x].color == piece.color:
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

    def ENEMEYPawnDJ(): #double jump
        pass
        #if self.ENEMYlastMove:
            # or check it in move function

    def calc_moves(self, board):
        moves = []
        #check for en passant moves 
        if self.x not in (0,7):
            for side in (-1,1): #left side/right side
                sidePiece = board[self.y+self.dir][self.x+side]
                if sidePiece and self.color != sidePiece.color and self.ENEMYpawnDJ(): 
                        moves.append((self.x+side, self.y+self.dir))
            
        #check for captures moves
        if self.y not in (0,7):
            if (self.y == 1 and self.color == (0,0,0)) or (self.y == 6 and self.color == (255,255,255)):
                if not board[self.y+self.dir*2][self.x]:
                    moves.append((self.x, self.y+self.dir*2))
            if not board[self.y+self.dir][self.x]:
                moves.append((self.x, self.y+self.dir))
        return moves


class Rook(Piece):
    def __init__(self, x, y, color, pName, win):
        super().__init__(x, y, color, pName, win)
    
    def calc_moves(self, board):
        print("hello?")
        return calc_all_moves(self, board, True, True, False)

#King and Knight starts with same letter
class Horse(Piece):     
    def __init__(self, x, y, color, pName, win):
        super().__init__(x, y, color, pName, win)
    
    
    def calc_moves(self, board, moves=[]):
        dirs = [(-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]
        for dir in dirs:
            if -1 < (y := self.y+dir[1]) < 8 and -1 < (x := self.x+dir[0]) < 8:
                if not board[y][x] or self.color != board[y][x].color:     
                    moves.append((x, y))
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
            if -1 < y < 8 and -1 < x < 8 :
                
                if board[y][x] and self.color != board[y][x].color: 
                    moves.append((self.x + dir[0], self.y+dir[1]))
        print(moves)
        return moves

#move function: see if opponent piece's new pos puts enemy's king in danger 

