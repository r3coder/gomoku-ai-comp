

import numpy as np
from Utils import Point2d

# Get number of "possible" consecutive stones in a single line starting from pos
# It ignores the gap once to check if it is open 3 or open 4.
## line(list): list of stones. 0: empty, 1: black, 2: white
## pos(int): position of stone to start from. usually len(line)//2
## return(int, int): number of posible consecutive stones on left, right
def GetPossibleConsecutiveStonesInLine(line, pos):
    if len(line)<pos: # line is too short, error
        return -1
    if line[pos] == 0:
        return 0
    # Check left side
    lineLeft, lineRight, lineCenter = line.copy(), line.copy(), line.copy()
    switch = False
    for i in range(0, pos):
        if not (line[pos-i-1] == 0 or line[pos-i-1] == line[pos]):
            break
        if line[pos-i-1] == 0:
            switch = True
        if switch:
            if line[pos-i-1] != 0:
                break
            else:
                lineLeft[pos-i-1] = line[pos]
                lineCenter[pos-i-1] = line[pos]
    switch = False
    for i in range(pos+1, len(line)):
        if not(line[i] == 0 or line[i] == line[pos]):
            break
        if line[i] == 0:
            switch = True
        if switch:
            if line[i] != 0:
                break
            else:
                lineRight[i] = line[pos]
                lineCenter[i] = line[pos]
    rl = GetConsecutiveStonesInLine(lineLeft, pos)
    rc = GetConsecutiveStonesInLine(lineCenter, pos)
    rr = GetConsecutiveStonesInLine(lineRight, pos)
    # print(lineLeft, lineCenter, lineRight, rl, rc, rr)
    return rl, rc, rr

# Get number of consecutive stones in a single line starting from pos
## line(list): list of stones. 0: empty, 1: black, 2: white
## pos(int): position of stone to start from. usually len(line)//2
## return(int): number of consecutive stones. If it is 5, it can be a win
def GetConsecutiveStonesInLine(line, pos):
    if len(line)<pos:
        return -1
    if line[pos] == 0:
        return 0
    res = 1
    for i in range(0, pos):
        if line[pos-i-1] != line[pos]:
            break
        res += 1
    for j in range(pos+1, len(line)):
        if line[j] != line[pos]:
            break
        res += 1
    return res

class GomokuGame:
    def __init__(self, boardDim = Point2d(15, 15)):
        self.boardDim = boardDim

        self.board = None
        self.state = None
        self.stoneCount = 0
        self.winner = -1
        self.InitializeBoard()

    def InitializeBoard(self, slient = True):
        self.board = np.zeros((self.boardDim.x, self.boardDim.y))
        self.stoneCount = 0
        self.winner = -1
        self.state = "playing"

        if not slient:
            print("Board initialized")

    # Place a stone to the board
    ## pos(Point2d): position to place stone
    ## stone(int): stone to place. 1: black, 2: white, if it is not provided, it will be determined by the turn
    def PlaceStone(self, pos, stone = -1, slient = True):
        if self.state != "playing":
            return False, "Game is not playing"
        if self.board[pos.x, pos.y] != 0:
            return False, "Position is not empty"
        if stone == -1:
            stone = self.stoneCount % 2 + 1
        if not slient:
            print("Placing stone at", pos, "with stone", stone)


        if self.IsPositionIsWinning(pos):
            self.board[pos.x, pos.y] = stone
            self.state = "over"
            self.winner = stone
            if not slient:
                print("Player {} wins".format(stone))
            return True

        v = self.IsValidMove(pos)
        if v:
            self.board[pos.x, pos.y] = stone
            self.stoneCount += 1
            if not slient:
                print("Placed stone at", pos, "with stone", stone)
            return True
        
        if self.stoneCount == self.boardDim.x * self.boardDim.y:
            self.state = "over"
            if not slient:
                print("Game is over")
            return True
    
    # Get horizontal, vertical, diagonal lines for a position
    ## pos(Point2d): position to get lines for
    ## neigh(int) : length of line. If you set 6, it will contain 6+1+6=13 elements
    ## return(list): list of lines, -1 if the position is out of range
    def GetLines(self, pos, neigh=6):
        lineh, linev, linedl, linedr = np.zeros(neigh*2+1, dtype = np.int), np.zeros(neigh*2+1, dtype = np.int), np.zeros(neigh*2+1, dtype = np.int), np.zeros(neigh*2+1, dtype = np.int)
        for i in range(-neigh,neigh+1):
            lineh[i+neigh]  = -1 if pos.y + i < 0 or pos.y + i >= self.boardDim.y else self.board[pos.x, pos.y + i]
            linev[i+neigh]  = -1 if pos.x + i < 0 or pos.x + i >= self.boardDim.x else self.board[pos.x + i, pos.y] 
            linedl[i+neigh] = -1 if pos.x + i < 0 or pos.x + i >= self.boardDim.x or pos.y + i < 0 or pos.y + i >= self.boardDim.y else self.board[pos.x + i, pos.y + i] 
            linedr[i+neigh] = -1 if pos.x - i < 0 or pos.x - i >= self.boardDim.x or pos.y + i < 0 or pos.y + i >= self.boardDim.y else self.board[pos.x - i, pos.y + i]
        return lineh, linev, linedl, linedr

    # Check if the position makes a 3-3
    ## pos(Point2d): position to check
    ## return(bool): True if it makes a 4-4
    def IsPositionMakes33(self, pos, slient = True):
        if self.board[pos.x, pos.y] != 0:
            if not slient:
                print("%s is not a winning position, because it is not empty" % str(pos))
            return False
        
        stone_color = self.stoneCount % 2 + 1
        # temporary place a stone and get lines, and remove placed stone
        self.board[pos.x, pos.y] = stone_color
        lineh, linev, linedl, linedr = self.GetLines(pos, 6)
        self.board[pos.x, pos.y] = 0

        v = GetPossibleConsecutiveStonesInLine(lineh, 6)
        v = GetPossibleConsecutiveStonesInLine(linev, 6)
        v = GetPossibleConsecutiveStonesInLine(linedl, 6)
        v = GetPossibleConsecutiveStonesInLine(linedr, 6)

        self.board[pos.x, pos.y] = 0
        return False
    
    # Check if the position makes a 4-4
    ## pos(Point2d): position to check
    ## return(bool): True if it makes a 4-4
    def IsPositionMakes44(self, pos, slient = True):
        if self.board[pos.x, pos.y] != 0:
            if not slient:
                print("%s is not a winning position, because it is not empty" % str(pos))
            return False
        
        if not slient:
            print("Check if %s makes a 4-4" % str(pos))
        stone_color = self.stoneCount % 2 + 1
        # Temporary place a stone and get lines, and remove placed stone
        self.board[pos.x, pos.y] = stone_color
        lineh, linev, linedl, linedr = self.GetLines(pos, 6)
        self.board[pos.x, pos.y] = 0

        # Get Consecutive Stones in each line
        vh = GetConsecutiveStonesInLine(lineh, 6)
        vv = GetConsecutiveStonesInLine(linev, 6)
        vdl = GetConsecutiveStonesInLine(linedl, 6)
        vdr = GetConsecutiveStonesInLine(linedr, 6)

        # if two among [vh, vv, vdl and vdr] are 4, it's 4-4
        v = 0
        v += 1 if vh == 4 else 0
        v += 1 if vv == 4 else 0
        v += 1 if vdl == 4 else 0
        v += 1 if vdr == 4 else 0
        if v >= 2:
            if not slient:
                print("%s makes a 4-4" % str(pos))
            return True
        else:
            if not slient:
                print("%s does not make a 4-4" % str(pos))
            return False
    
    # Check if the position is makes more than 5 stones
    ## pos(Point2d): position to check
    ## return(bool): True if it makes more than 5 stones, False otherwise (including it makes 5 stones, gomoku completes)
    def IsPositionMakesMorestones(self, pos, slient = True):
        if self.board[pos.x, pos.y] != 0:
            if not slient:
                print("%s is not a winning position, because it is not empty" % str(pos))
            return False
        
        if not slient:
            print("Check if %s makes more than 5 stones" % str(pos))
        stone_color = self.stoneCount % 2 + 1
        # Temporary place a stone and get lines, and remove placed stone
        self.board[pos.x, pos.y] = stone_color
        lineh, linev, linedl, linedr = self.GetLines(pos, 6)
        self.board[pos.x, pos.y] = 0

        # Get Consecutive Stones in each line
        vh = GetConsecutiveStonesInLine(lineh, 6)
        vv = GetConsecutiveStonesInLine(linev, 6)
        vdl = GetConsecutiveStonesInLine(linedl, 6)
        vdr = GetConsecutiveStonesInLine(linedr, 6)
        if vh >= 6 or vv >= 6 or vdl >= 6 or vdr >= 6:
            if vh == 5 or vv == 5 or vdl == 5 or vdr == 5:
                if not slient:
                    print("%s makes more than 6 stones, but Gomoku completes, return False" % str(pos))
                return False
            else:
                if not slient:
                    print("%s makes more than 6 stones" % str(pos))
                return True
        else:
            if not slient:
                print("%s does not make more than 6 stones" % str(pos))
            return False

    # Check if the position is a winning position
    ## pos(Point2d): position to check
    ## return(bool): True if it is a winning position, False otherwise
    def IsPositionIsWinning(self, pos, slient = True):
        if self.board[pos.x, pos.y] != 0:
            if not slient:
                print("%s is not a winning position, because it is not empty" % str(pos))
            return False
        
        if not slient:
            print("Check if %s makes a winning move"%str(pos))
        stone_color = self.stoneCount % 2 + 1
        # temporary place a stone and get lines, and remove placed stone
        self.board[pos.x, pos.y] = stone_color
        lineh, linev, linedl, linedr = self.GetLines(pos, 4)
        self.board[pos.x, pos.y] = 0

        vh = GetConsecutiveStonesInLine(lineh, 4)
        vv = GetConsecutiveStonesInLine(linev, 4)
        vdl = GetConsecutiveStonesInLine(linedl, 4)
        vdr = GetConsecutiveStonesInLine(linedr, 4)
        if not slient:
            print(lineh, vh, linev, vv, linedl, vdl, linedr, vdr)
        if vh == 5 or vv == 5 or vdl == 5 or vdr == 5:
            if not slient:
                print("Placing stone at %s makes gomoku, Return True"%str(pos))
            return True
        else:
            if not slient:
                print("Placing stone at %s does not make gomoku, Return False"%str(pos))
            return False
    
    # Get Current Turn
    def GetTurnText(self):
        if self.state == "playing":
            if self.stoneCount % 2 + 1 == 1:
                return "black"
            else:
                return "white"
        else:
            return "none"
    
    # Return number of placed stones
    def GetNumberOfPlacedStones(self):
        return self.stoneCount
    
    # Return dimension of board
    def GetBoardDimension(self):
        return self.boardDim

    # Check if position is valid move
    ## pos(Point2d): position to check
    ## return(bool): True if it is a valid move, False otherwise
    def IsValidMove(self, pos, silent = True):
        # check if pos is in the grid
        if pos.x < 0 or pos.x >= self.boardDim.x or pos.y < 0 or pos.y >= self.boardDim.y:
            if not silent:
                print("%s is not in the grid" % str(pos))
            return False
        # check if pos is empty
        if self.board[pos.x, pos.y] != 0:
            if not silent:
                print("%s is not empty" % str(pos))
            return False

        if self.IsPositionIsWinning(pos):
            if not silent:
                print("%s is a winning move" % str(pos))
            return True
        # check if black player played 3-3 or 4-4 or 6 stones
        if self.stoneCount % 2 == 0:
            if self.IsPositionMakes33(pos):
                if not silent:
                    print("%s makes a 3-3" % str(pos))
                return False
            if self.IsPositionMakes44(pos):
                if not silent:
                    print("%s makes a 4-4" % str(pos))
                return False
            if self.IsPositionMakesMorestones(pos):
                if not silent:
                    print("%s makes more than 5 stones" % str(pos))
                return False
        
        if not silent:
            print("%s is a valid move" % str(pos))
        return True

    # Return all valid moves can play
    ## return(list): list of valid moves
    def GetAllValidMoves(self):
        validMoves = []
        for x in range(self.boardDim.x):
            for y in range(self.boardDim.y):
                p = Point2d(x, y)
                if self.IsValidMove(p):
                    validMoves.append(p)
        return validMoves

    def GetAllInvalidMoves(self, excludeEmpty = False):
        invalidMoves = []
        for x in range(self.boardDim.x):
            for y in range(self.boardDim.y):
                if excludeEmpty and self.board[x, y] != 0:
                    continue
                p = Point2d(x, y)
                if not self.IsValidMove(p):
                    invalidMoves.append(p)
        return invalidMoves

    # Get all valid moves within a certain distance from placed stone
    ## r(int): range of distance
    def GetAllValidMovesInRange(self, r=2):
        validMoves = []
        for x in range(self.boardDim.x):
            for y in range(self.boardDim.y):
                pos = Point2d(x, y)
                if self.board[pos.x, pos.y] != 0:
                    for i in range(-r, r+1):
                        for j in range(-r, r+1):
                            p = Point2d(pos.x + i, pos.y + j)
                            if p not in validMoves and self.IsValidMove(p):
                                validMoves.append(p)
        return list(set(validMoves))