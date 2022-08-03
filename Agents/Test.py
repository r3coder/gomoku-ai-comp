
# Test Agent
# Written by Seunghyun Lee : coder@dgist.ac.kr
# Somewhat place stones randomly on the board, but in reasonable manner

from Utils import Point2d
from Gomoku import *
import random

class Test:
    def __init__(self):
        pass
    
    # Code exectued every time the game is reset
    def Initialize(self):
        pass
    
    # Code executed every move
    def Move(self, GG, color):
        if GG.GetNumberOfPlacedStones() == 0:
            p = GG.GetBoardDimension()
            return Point2d(p.x//2, p.y//2)
        v = GG.GetAllValidMovesInRange(2)
        return random.choice(v)
