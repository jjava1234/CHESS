from itertools import permutations

def calc_LR(board, piece, x, y, dir, valid_moves=[]):    
    if y > 7 or y < 0 or x > 7 or x < 0 or board[y][x] and board[y][x].color == piece.color:
        return valid_moves
    valid_moves.append((x, y))
    if piece.calc_LR[dir][x+dir]:
        return valid_moves

# UP / DOWN
def calc_UD(board, piece, x, y, dir, valid_moves=[]):    
    if y > 7 or y < 0 or x > 7 or x < 0 or board[y][x] and board[y][x].color == piece.color:
        return valid_moves
    valid_moves.append((x, y))
    if piece.calc_UD[y+dir][x]:
        return valid_moves

#DIAGONALS
def calc_DI(board, piece, x, y, dir, reversed=1, valid_moves=[]):
    if y > 7 or y < 0 or x > 7 or x < 0 or board[y][x] and board[y][x].color == piece.color:
        return valid_moves
    valid_moves.append((x, y))
    if piece.calc_diagonals(board, piece.x+dir, piece.y+dir*reversed, reversed):
        return valid_moves        

def calc_all_moves(self, board, LR = True, UD = True, DI = False):
        moves = []
        for dir in (-1, 1):
            if LR and UD:
                moves.append(calc_UD(board, self, self.x, self.y+dir, dir))
                moves.append(calc_LR(board, self, self.x+dir, self.y, dir))
            if DI:        
                moves.append(calc_DI(board, self, self.x+dir, self.y+dir, dir))
                moves.append(calc_DI(board, self, self.x+dir, self.y+dir*-1, dir, -1))


class Piece():
    def __init__(self, x, y, color, dir, piece_name):
        self.x = x
        self.y = y
        self.valid_moves = []
        self.color = color
        self.dir = dir
        self.pName = piece_name

class Pawn(Piece):
    def __init__(self, x, y, color, dir, pName):
        super().__init__(x, y, color, dir, pName)

    def calc_moves(self, board):
        valid_moves = []
        #check for capture moves
        if self.x not in (0,7):
            for side in (-1,1): #left side/right side
                sidePiece = board[self.y+self.dir][self.x+side]
                if sidePiece: 
                    if self.color != sidePiece.color or board[self.y][self.x+side]:
                        valid_moves.append((self.x+side, self.y+self.dir))
            
        #regular movement
        if self.y not in (0,7):
            if (self.y == 1 and self.color == (0,0,0)) or (self.y == 6 and self.color == (255,255,255)):
                if not board[self.y+self.dir*2][self.x]:
                    valid_moves.append((self.x, self.y+self.dir*2))
                elif not board[self.y+dir][self.x]:
                    valid_moves.append((self.x, self.y+self.dir))

        return valid_moves


class Rook(Piece):
    def __init__(self, x, y, color, pName):
        super().__init__(x, y, color, pName)
    
    def calc_moves(self, board):
        return (calc_all_moves(self, board, True, True, False))


class Knight(Piece):
    def __init__(self, x, y, color, pName):
        super().__init__(x, y, color, pName)
    
    
    def calc_moves(self, board):
        valid_moves = []
        dirs = [(-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1)]
        for dir in dirs:
            valid_moves.append((self.x + dir[0], self.y+dir[1]))


class Bishop(Piece):
    def __init__(self, x, y, color, pName):
        super().__init__(x, y, color, pName)
    
    def calc_moves(self, board):
        return (calc_all_moves(self, board, False, False, True))


class Queen(Piece):
    def __init__(self, x, y, color, pName):
        super().__init__(x, y, color, pName)

    def calc_moves(self, board): 
        return (calc_all_moves(self, board, True, True, True))


class King(Piece):
    def __init__(self, x, y, color, pName):
        super().__init__(x, y, color, pName)

    def calc_moves(self, board):
        valid_moves = []
        dirs = list(permutations([0, -1, 1], 2))
        for dir in dirs:
            valid_moves.append((self.x + dir[0], self.y+dir[1]))

