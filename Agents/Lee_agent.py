from secrets import choice
from Utils import Point2d
from Gomoku import *
import random
import copy



class Lee_agent:
    def Initialize(self):
        pass

    def ifposmake(self,GG,point,color): 
            self.point = point
            h,v,dl,dr = GG.GetLines(point, 3)
            ah, av, adl, adr = 0,0,0,0
            if GetConsecutiveStonesInLine(h, h[3]) == 4:
                ah += 4 
            elif GetConsecutiveStonesInLine(h, h[3]) == 3:
                ah += 3
            elif GetConsecutiveStonesInLine(h, h[3]) == 2:
                ah += 2
            elif GetConsecutiveStonesInLine(h, h[3]) == 1:
                ah += 1
            else:
                ah = 0


            if GetConsecutiveStonesInLine(v, v[3]) == 4:
                av += 4 
            elif GetConsecutiveStonesInLine(v, v[3]) == 3:
                av += 3
            elif GetConsecutiveStonesInLine(v, v[3]) == 2:
                av += 2
            elif GetConsecutiveStonesInLine(v, v[3]) == 1:
                av += 1
            else:
                av = 0

            if GetConsecutiveStonesInLine(dr, dr[3]) == 4:
                adr += 4 
            elif GetConsecutiveStonesInLine(dr, dr[3]) == 3:
                adr += 3
            elif GetConsecutiveStonesInLine(dr, dr[3]) == 2:
                adr += 2
            elif GetConsecutiveStonesInLine(dr, dr[3]) == 1:
                adr += 1
            else:
                adr = 0

            if GetConsecutiveStonesInLine(dl, dl[3]) == 4:
                adl += 4 
            elif GetConsecutiveStonesInLine(dl, dl[3]) == 3:
                adl += 3
            elif GetConsecutiveStonesInLine(dl, dl[3]) == 2:
                adl += 2
            elif GetConsecutiveStonesInLine(dl, dl[3]) == 1:
                adl += 1
            else:
                adl = 0
            
            s = [ah, av, adl, adr]
            if s.count(4) >= 2:
                return 0
            elif s.count(3) >=2:
                return 0
            elif s.count(4) and s.count(3) == 1:
                return 100
            elif s.count(3) == 1 and s.count(4) == 0:
                return 50
            elif s.count(4) ==1 and s.count(3) == 1:
                return 70
            elif s.count(2) >=1:
                return 30
            elif s.count(1) >=1:
                return 10
            else: return 0

    def Move(self,GG,color):
        
        if GG.GetNumberOfPlacedStones() == 0:
            a = GG.GetBoardDimension()
            return Point2d(a.x//2,a.y//2)
        else:
            s = GG.GetAllValidMovesInRange(2)
            l = copy.deepcopy(s)
            print(type(s[0]))
            for i in range(0, len(s)):
                 s[i] = self.ifposmake(GG, Point2d(s[i].x,s[i].y),color)
            k = sorted(s)
            b = k[-1]
                   
            c = s.index(b)
            v = l[c]
            return v
