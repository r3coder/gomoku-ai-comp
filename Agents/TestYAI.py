# Test Agent
# Written by Seunghyun Lee : coder@dgist.ac.kr
# Somewhat place stones randomly on the board, but in reasonable manner

from Utils import Point2d
from Gomoku import *
import random

iii = 1
jjj = 1
class TestYAI:
    def __init__(self):
        pass
    
    # Code exectued every time the game is reset
    def Initialize(self):
        pass
        
    # 반대 돌이 이길지 판단
    def Anotherstone(self, GG, decolor):
        e = 0
        anj = 1
        ani = 1
        for ani in range(15):
            anj = 1
            for anj in range(15):
                if GG.IsPositionIsWinning(Point2d(ani, anj)) == 1:
                    e = 1
                    break
                else:
                    continue
            if e == 1:
                iii = ani
                jjj = anj
                break
            else :
                continue
        if e == 1:
            return 1
        else :
            return 0
        
    # Code executed every move
    def Move(self, GG, color):      #color = 1 or 2
        if GG.GetNumberOfPlacedStones() == 0:
            p = GG.GetBoardDimension()
            return Point2d(p.x//2, p.y//2)
        v = [0]*225
        v = GG.GetAllValidMovesInRange(1)
        print(v)
        if color == 1:
            decolor = 2
        else :
            decolor = 1
        i = 1
        j = 1
        d = 0
        #내 돌이 이기는지 판단
        for i in range(15):
            j = 1
            for j in range(15):
                if GG.IsPositionIsWinning(Point2d(i, j)) == 1:
                    d = 1
                    break
                else :
                    continue    
            if d == 1:
                break
            else :
                continue   
        #연속된 돌 판단
        i3 = 1
        j3 = 1
        garoc = 0
        seroc = 0
        leftdaec = 0
        rightdaec =0
        for i3 in range(15):
            j3 = 1
            for j3 in range(15):
                garo, sero, leftdae, rightdae = GG.GetLines(Point2d(i3,j3), 4)
                if GetConsecutiveStonesInLine(garo, 4) == 3 & garo[4] == color:
                    if garo[5] == 0 :
                        garoc = 1
                        break
                    elif garo[6] == 0 :
                        garoc = 2
                        break
                    elif garo[7] == 0 :
                        garoc = 3
                        break
                    elif garo[3] == 0:
                        garoc = -1
                        break
                    elif garoc[2] == 0:
                        garoc = -2
                        break
                    elif garoc[1] == 0:
                        garoc = -3
                        break
                    else:
                        garoc = 0
                elif GetConsecutiveStonesInLine(garo, 4) == 3 & garo[4] == decolor:
                    if garo[5] == 0 :
                        garoc = 1
                        break
                    elif garo[6] == 0 :
                        garoc = 2
                        break
                    elif garo[7] == 0 :
                        garoc = 3
                        break
                    elif garo[3] == 0:
                        garoc = -1
                        break
                    elif garoc[2] == 0:
                        garoc = -2
                        break
                    elif garoc[1] == 0:
                        garoc = -3
                        break
                    else:
                        garoc = 0
                elif GetConsecutiveStonesInLine(sero, 4) == 3 & sero[4] == color:
                    if sero[5] == 0 :
                        seroc = 1
                        break
                    elif sero[6] == 0 :
                        seroc = 2
                        break
                    elif sero[7] == 0 :
                        seroc = 3
                        break
                    elif sero[3] == 0:
                        seroc = -1
                        break
                    elif seroc[2] == 0:
                        seroc = -2
                        break
                    elif seroc[1] == 0:
                        seroc = -3
                        break
                    else:
                        seroc = 0
                elif GetConsecutiveStonesInLine(sero, 4) == 3 & sero[4] == decolor:
                    if sero[5] == 0 :
                        seroc = 1
                        break
                    elif sero[6] == 0 :
                        seroc = 2
                        break
                    elif sero[7] == 0 :
                        seroc = 3
                        break
                    elif sero[3] == 0:
                        seroc = -1
                        break
                    elif seroc[2] == 0:
                        seroc = -2
                        break
                    elif seroc[1] == 0:
                        seroc = -3
                        break
                    else:
                        seroc = 0
                elif GetConsecutiveStonesInLine(leftdae, 4) == 3 & leftdae[4] == color:
                    if leftdae[5] == 0 :
                        leftdaec = 1
                        break
                    elif leftdae[6] == 0 :
                        leftdaec = 2
                        break
                    elif leftdae[7] == 0 :
                        leftdaec = 3
                        break
                    elif leftdae[3] == 0:
                        leftdaec = -1
                        break
                    elif leftdae[2] == 0:
                        leftdaec = -2
                        break
                    elif leftdae[1] == 0:
                        leftdaec = -3
                        break
                    else:
                        leftdaec = 0
                elif GetConsecutiveStonesInLine(leftdae, 4) == 3 & leftdae[4] == decolor:
                    if leftdae[5] == 0 :
                        leftdaec = 1
                        break
                    elif leftdae[6] == 0 :
                        leftdaec = 2
                        break
                    elif leftdae[7] == 0 :
                        leftdaec = 3
                        break
                    elif leftdae[3] == 0:
                        leftdaec = -1
                        break
                    elif leftdae[2] == 0:
                        leftdaec = -2
                        break
                    elif leftdae[1] == 0:
                        leftdaec = -3
                        break
                    else:
                        leftdaec = 0
                elif GetConsecutiveStonesInLine(rightdae, 4) == 3 & rightdae[4] == color:
                    if rightdae[5] == 0 :
                        rightdaec = 1
                        break
                    elif rightdae[6] == 0 :
                        rightdaec = 2
                        break
                    elif  rightdae[7] == 0 :
                        rightdaec = 3
                        break
                    elif rightdae[3] == 0:
                        rightdaec = -1
                        break
                    elif rightdae[2] == 0:
                        rightdaec = -2
                        break
                    elif rightdae[1] == 0:
                        rightdaec = -3
                        break
                    else:
                        rightdaec = 0
                elif GetConsecutiveStonesInLine(rightdae, 4) == 3 & rightdae[4] == decolor:
                    if rightdae[5] == 0 :
                        rightdaec = 1
                        break
                    elif rightdae[6] == 0 :
                        rightdaec = 2
                        break
                    elif  rightdae[7] == 0 :
                        rightdaec = 3
                        break
                    elif rightdae[3] == 0:
                        rightdaec = -1
                        break
                    elif rightdae[2] == 0:
                        rightdaec = -2
                        break
                    elif rightdae[1] == 0:
                        rightdaec = -3
                        break
                    else:
                        rightdaec = 0
                else:
                    continue
            if garoc + seroc + leftdaec + rightdaec != 0:
                break
        f = 0
        ik = 1
        jk = 1
        for ik in range(15):
            for jk in range(15):
                if color != 1 & GG.IsPositionMakes33(Point2d(i3,j3)) != 1 & GG.IsPositionMakes44(Point2d(i3,j3)) != 1:
                    f = 1
        if f == 0:            
            if d == 1:                              #내 돌이 무조건 이기는지 판단
                return Point2d(i,j)
        #    elif TestYAI.Anotherstone(self, GG, decolor) == 1:      #상대 돌이 무조건 이기는지 판단
        #        return Point2d(iii, jjj)
        #    elif seroc != 0:                            #돌이 세로로 3칸 연속으로 되어 있는지 판단
        #        return Point2d(i3, j3 - seroc)
        #    elif garoc != 0:                            #돌이 가로로 3칸 연속으로 되어 있는지 판단
        #        return Point2d(i3+garoc, j3)
        #    elif leftdaec != 0:                              #돌이 왼쪽 대각선으로 3칸 연속으로 되어 있는지 판단
        #        return Point2d(i3+leftdaec, j3 - leftdaec)
        #    elif rightdaec != 0:                              #돌이 오른쪽 대각선으로 3칸 연속으로 되어 있는지 판단
        #        return Point2d(i3 +rightdaec, j3 + rightdaec)
            else:
                return random.choice(v)
        elif f == 1:
            return random.choice(v)
