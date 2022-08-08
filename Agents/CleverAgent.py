from Utils import Point2d
from Gomoku import *
import random



class CleverAgent:
    def __init__(self):
        pass

    def Initialize(self):
        num = True

    def Move(self, GG, color):
        if GG.GetNumberOfPlacedStones()==0:
            p = GG.GetBoardDimension()
            return Point2d(p.x//2, p.y//2)
        #v = GG.GetAllValidMovesInRange(2)
        #return random.choice(v)

        if GG.GetNumberOfPlacedStones()%2==1 :
            mycolor=2
            othercolor=1
        else:
            mycolor=1
            othercolor=2

        listA = GG.GetAllValidMoves()

        for i in range(len(listA)):
            c = listA[i]
            a = c.x
            b = c.y
            if GG.IsPositionIsWinning(Point2d(a,b)) == True:
                return Point2d(a,b)
                
            else:
                continue

        for i in range(len(listA)):
            c = listA[i]
            a = c.x
            b = c.y
            da, db, dc, dd = GG.GetLines(Point2d(a,b),3)
            if da[0] == da[1] == da[2] == othercolor or da[4] == da[5] == da[6] == othercolor:
                return Point2d(a,b)
                
            elif db[0] == db[1] == db[2] == othercolor or db[4] == db[5] == db[6] == othercolor:
                return Point2d(a,b)
                
            elif dc[0] == dc[1] == dc[2] == othercolor or dc[4] == dc[5] == dc[6] == othercolor:
                return Point2d(a,b)
               
            elif dd[0] == dd[1] == dd[2] == othercolor or dd[4] == dd[5] == dd[6] == othercolor:
                return Point2d(a,b)
                
            else:
                continue

        for i in range(len(listA)):
            c = listA[i]
            a = c.x
            b = c.y
            da, db, dc, dd = GG.GetLines(Point2d(a,b),3)
            if da[0] == da[1] == da[2] == mycolor or da[4] == da[5] == da[6] == mycolor:
                return Point2d(a,b)
           
            elif db[0] == db[1] == db[2] == mycolor or db[4] == db[5] == db[6] == mycolor:
                return Point2d(a,b)
             
            elif dc[0] == dc[1] == dc[2] == mycolor or dc[4] == dc[5] == dc[6] == mycolor:
                return Point2d(a,b)
              
            elif dd[0] == dd[1] == dd[2] == mycolor or dd[4] == dd[5] == dd[6] == mycolor:
                return Point2d(a,b)
               
            else:
                continue

       
        
                     
        for j in range(15):
            for k in range(15):
                if GG.board[j,k] == mycolor :
                    listC, listD, listE, listF = GG.GetLines(Point2d(j,k), 1)
                    if listC[0] == 0:
                        if GG.board[j-1,k] == 0 :
                            return Point2d(j-1,k)
                       
                    elif listC[2] == 0:
                        if GG.board[j+1,k] == 0 :
                            return Point2d(j+1,k)
                        
                    elif listD[0] == 0:
                        if GG.board[j,k+1] == 0 :
                            return Point2d(j,k+1)
                      
                    elif listD[2] == 0:
                        if GG.board[j,k-1] == 0 :
                            return Point2d(j,k-1)
                       
                    elif listE[0] == 0:
                        if GG.board[j-1,k+1] == 0 :
                            return Point2d(j-1,k+1)
                        
                    elif listE[2] == 0:
                        if GG.board[j+1,k-1] == 0 :
                            return Point2d(j+1,k-1)
                       
                    elif listF[0] == 0:
                        if GG.board[j+1,k+1] == 0 :
                            return Point2d(j+1,k+1)
                       
                    elif listF[2] == 0:
                        if GG.board[j-1,k-1] == 0 :
                            return Point2d(j-1,k-1)
                      
                    else:
                        continue
                else:
                    continue

        for j in range(15):
            for k in range(15):
                if GG.board[j,k] == othercolor :
                    listC, listD, listE, listF = GG.GetLines(Point2d(j,k), 1)
                    if listC[0] == 0:
                        if GG.board[j-1,k] == 0 :
                            return Point2d(j-1,k)
                       
                    elif listC[2] == 0:
                        if GG.board[j+1,k] == 0 :
                            return Point2d(j+1,k)
                        
                    elif listD[0] == 0:
                        if GG.board[j,k+1] == 0 :
                            return Point2d(j,k+1)
                      
                    elif listD[2] == 0:
                        if GG.board[j,k-1] == 0 :
                            return Point2d(j,k-1)
                       
                    elif listE[0] == 0:
                        if GG.board[j-1,k+1] == 0 :
                            return Point2d(j-1,k+1)
                        
                    elif listE[2] == 0:
                        if GG.board[j+1,k-1] == 0 :
                            return Point2d(j+1,k-1)
                       
                    elif listF[0] == 0:
                        if GG.board[j+1,k+1] == 0 :
                            return Point2d(j+1,k+1)
                       
                    elif listF[2] == 0:
                        if GG.board[j-1,k-1] == 0 :
                            return Point2d(j-1,k-1)
                      
                    else:
                        continue
                else:
                    continue

        for i in range(len(listA)):
            c = listA[i]
            a = c.x
            b = c.y
            da, db, dc, dd = GG.GetLines(Point2d(a,b),2)
            if da[0] == da[1] == othercolor or da[3] == da[4] == othercolor:
                return Point2d(a,b)
               
            elif db[0] == db[1] == othercolor or db[3] == db[4] == othercolor:
                return Point2d(a,b)
              
            elif dc[0] == dc[1] == othercolor or dc[3] == dc[4] == othercolor:
                return Point2d(a,b)
              
            elif dd[0] == dd[1] == othercolor or dd[3] == dd[4] == othercolor:
                return Point2d(a,b)
            
            else:
                continue

        for i in range(len(listA)):
            c = listA[i]
            a = c.x
            b = c.y
            da, db, dc, dd = GG.GetLines(Point2d(a,b),2)
            if da[0] == da[1] == mycolor or da[4] == da[3] == mycolor:
                return Point2d(a,b)
         
            elif db[0] == db[1] == mycolor or db[4] == db[3] == mycolor:
                return Point2d(a,b)
               
            elif dc[0] == dc[1] == mycolor or dc[4] == dc[3] == mycolor:
                return Point2d(a,b)
                
            elif dd[0] == dd[1] == mycolor or dd[4] == dd[3] == mycolor:
                return Point2d(a,b)
              
            else:
                continue

        v = GG.GetAllValidMovesInRange(2)
        return random.choice(v)
           
        