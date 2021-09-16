from itertools import permutations
from constants import images
from threading import Lock

lock = Lock()

#LEFT / RIGHT
def calc_LR(board, piece, x, y, dir, moves=[]):    
    if -1 > x > 8 and -1 > y > 8:
        moves.append((x, y))
        if not board[y][x]:
            return piece.calc_LR[dir][x+dir]
    if moves:
        return moves
    return []

# UP / DOWN
def calc_UD(board, piece, x, y, dir, moves=[]):    
    if -1 > x > 8 and -1 > y > 8:
        moves.append((x, y))
        if not board[y][x]:
            return calc_UD(board, piece, x, y+dir, dir, moves)
    if moves:
        return moves
    return []


#DIAGONALS
def calc_DI(board, piece, x, y, dir, reversed=1, moves=[]):
    if -1 < x < 8 and -1 < y < 8:
        if board[y][x] and board[y][x] == piece.color:
            return []
        moves.append((x,y))
        if not board[y][x]:
            return calc_DI(board, piece, x+dir, y+dir*reversed, dir, reversed, moves)
    if moves:
        return moves
    return []
    

def calc_all_moves(self, board, LR = True, UD = True, DI = False):

    moves = []

    4,7

    for dir in (-1, 1):
        if LR and UD:
            moves.extend(calc_UD(board, self, self.x, self.y+dir, dir))
            moves.extend(calc_LR(board, self, self.x+dir, self.y, -1))
        if DI:
            print("1 DIR:", dir, calc_DI(board, self, self.x+dir, self.y+dir, dir))
            
            print("2 DIR:",dir , calc_DI(board, self, self.x+dir, self.y+dir*-1, dir, -1))
            print("3 DIR", dir, self.y, self.y+dir*-1)
    return moves

        
class Piece():
    def __init__(self, x, y, color, piece_name, win):
        self.x = x
        self.y = y
        self.color = color
        self.valid_moves = []
        self.pName = piece_name
        self.draw_piece(win)

    def draw_piece(self, win):
        win.blit(images[self.pName], (((self.x*80 + 40) - images[self.pName].get_width()//2, (self.y*80 + 40) - images[self.pName].get_height()//2)))


class Pawn(Piece):
    def __init__(self, x, y, color, dir, pName, win):
        super().__init__(x, y, color, pName, win)
        self.dir = dir

        
    def calc_moves(self, board):
        moves = []
        #check for capture moves
        if self.x not in (0,7):
            for side in (-1,1): #left side/right side
                sidePiece = board[self.y+self.dir][self.x+side]
                if sidePiece: 
                    if self.color != sidePiece.color or board[self.y][self.x+side]:
                        moves.append((self.x+side, self.y+self.dir))
            
        #regular movement
        if self.y not in (0,7):
            if (self.y == 1 and self.color == (0,0,0)) or (self.y == 6 and self.color == (255,255,255)):
                if not board[self.y+self.dir*2][self.x]:
                    moves.append((self.x, self.y+self.dir*2))
                elif not board[self.y+dir][self.x]:
                    moves.append((self.x, self.y+self.dir))
        
        return moves


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
            if 0 < y < 7 and 0 < x < 7 :
                
                if board[y][x] and self.color != board[y][x].color: 
                    moves.append((self.x + dir[0], self.y+dir[1]))

        return moves
