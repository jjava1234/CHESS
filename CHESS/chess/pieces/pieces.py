import itertools
import config

#LEFT / RIGHT
def calc_LR(board, piece, movesList, check, x, y, dir):    
    if -1 < x < 8 and -1 < y < 8:
        if board[y][x] and board[y][x].pName[1] == "K":
            if board[y][x].color != piece.color and not check:
                config.pSQUARE.add((x+dir,y))
                config.lineOfSight.extend(calc_LR(board, piece, [], True, x+dir*-1, y, dir*-1))
            else:
                return movesList
        movesList.append((x, y))
        if not board[y][x]:
            return calc_LR(board, piece, movesList, check, x+dir, y, dir)
    return movesList

# UP / DOWN
def calc_UD(board, piece, movesList, check, x, y, dir): 
    if -1 < x < 8 and -1 < y < 8:
        if board[y][x] and board[y][x].pName[1] == "K":
            if board[y][x].color != piece.color and not check:
                config.pSQUARE.add((x,y+dir))
                config.lineOfSight.extend(calc_UD(board, piece, [], True, x, y+dir*-1, dir*-1))
            else:
                return movesList
        movesList.append((x, y))
        if not board[y][x]:
            return calc_UD(board, piece, movesList, check, x, y+dir, dir)
    return movesList


#DIAGONALS
def calc_DI(board, piece, movesList, check, x, y, dir, reversed = 1):
    if -1 < x < 8 and -1 < y < 8:
        if board[y][x] and board[y][x].pName[1] == "K":
            if board[y][x].color != piece.color and not check:
                config.pSQUARE.add((x+dir,y+dir))
                config.lineOfSight.extend(calc_DI(board, piece, [], True, x+dir*-1, y+dir*reversed*-1, dir*-1, reversed))       
            else:
                return movesList
        movesList.append((x,y))
        if not board[y][x]:
            return calc_DI(board, piece, movesList, check, x+dir, y+dir*reversed, dir, reversed)
    return movesList
    

def calc_all_moves(self, board, check, LR = False, UD = False, DI = False):
    moves = []
    for dir in (-1, 1):
        if LR and UD:
            moves.extend(calc_UD(board, self, [], check, self.x, self.y+dir, dir))
            moves.extend(calc_LR(board, self, [], check, self.x+dir, self.y, dir))
        if DI:
            moves.extend(calc_DI(board, self, [], check, self.x+dir, self.y+dir, dir))
            moves.extend(calc_DI(board, self, [], check, self.x+dir, self.y+dir*-1, dir, -1))

    return moves

        
class Piece():
    def __init__(self, x, y, color, piece_name, win):
        self.x = x
        self.y = y
        self.color = color
        self.valid_moves = []
        self.pName = piece_name
        self.drawPIECE(win)

    def drawPIECE(self, win, check = False):
        if self.pName[1] == "K" and check:
            config.pygame.draw.rect(win, (245, 64, 41), (self.x*80, self.y*80, 80, 80))
        win.blit(config.images[self.pName], (((self.x*80 + 40) - config.images[self.pName].get_width()//2, (self.y*80 + 40) - config.images[self.pName].get_height()//2)))


    def updatePIECE(self, win, newPOS):
        self.x, self.y = newPOS[0], newPOS[1]        
        self.drawPIECE(win)                

class Pawn(Piece):
    def __init__(self, x, y, color, dir, pName, win):
        super().__init__(x, y, color, pName, win)
        self.dir = dir

    def valid_DJ(self, board): #double jump
        moves = []
        color = {1:(0,0,0), 6:(255,255,255)}
        if self.y in (1,6) and self.color == color[self.y] and not board[self.y+self.dir*2][self.x]:
            moves.append((self.x, self.y+self.dir*2))
        return moves

    def captureMoves(self, board):
        moves = []
        for side in (-1, 1):
            if self.x+side not in (-1,7):
                if board[self.y+self.dir][self.x+side] and board[self.y+self.dir][self.x+side].color != self.color:   
                    moves.append((self.x+side, self.y+self.dir))
        return moves


    def enPASSANT(self):
        moves = []
        for side in (-1,1):
            if (self.x+side, self.y) == config.epMOVES:
                moves.append((self.x+side, self.y+self.dir))
        return moves

    def forward(self, board, check):
        moves = []
        newY= self.y + self.dir
        if not board[newY][self.x]:
            moves.append((self.x, newY))
        return moves

    def calc_moves(self, board, check):
        moves = []
        return list(config.flatten([self.forward(board, check), self.valid_DJ(board), self.captureMoves(board), self.enPASSANT()]))


class Rook(Piece):
    def __init__(self, x, y, color, pName, win):
        super().__init__(x, y, color, pName, win)
    
    def calc_moves(self, board, check = False):
        return calc_all_moves(self, board, check, True, True, False)

#King and Knight starts with same letter
class Horse(Piece):     
    def __init__(self, x, y, color, pName, win):
        super().__init__(x, y, color, pName, win)
    
    
    def calc_moves(self, board, check = False):
        moves = []
        dirs = [(-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1)]
        for dir in dirs:
            if -1 < (y := self.y+dir[1]) < 8 and -1 < (x := self.x+dir[0]) < 8:
                if board[y][x]:
                    if self.color != board[y][x].color:
                        moves.append((x, y))
                else:
                    moves.append((x,y))
        return moves

class Bishop(Piece):
    def __init__(self, x, y, color, pName, win):
        super().__init__(x, y, color, pName, win)
    
    def calc_moves(self, board, check = False):
        return calc_all_moves(self, board, check, False, False, True)


class Queen(Piece):
    def __init__(self, x, y, color, pName, win):
        super().__init__(x, y, color, pName, win)

    def calc_moves(self, board, check = False): 
        return calc_all_moves(self, board, check, True, True, True)
            

class King(Piece):
    def __init__(self, x, y, color, pName, win):
        super().__init__(x, y, color, pName, win)

    def calc_safety(self, board, check):
        for pos in calc_all_moves(self, board, False, True, True, True):
            x = pos[0]
            y = pos[1]
            if board[y][x] and (self.x, self.y) in board[y][x].calc_moves(board, check):
                check.append((x, y))
            

    def calc_moves(self, board, check = False):
        moves = []
        dirs = list(set(itertools.permutations([0, -1, -1, 1, 1], 2)))
        for dir in dirs:
            x = self.x+dir[0]
            y = self.y+dir[1]
            if -1 < y < 8 and -1 < x < 8:
                if not board[y][x] or self.color != board[y][x].color:
                    moves.append((self.x + dir[0], self.y+dir[1]))                        
    
        #need to find a way to differentiate them
        if check and len(moves) == 0:
            return False
        eMOVES = list(itertools.chain.from_iterable(list(config.allMOVES[config.pColors[(config.pColors.index(self.color)+1)%2]].values())))
        return list(set(moves).difference(config.pSQUARE, eMOVES))

