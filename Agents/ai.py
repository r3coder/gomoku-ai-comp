
# Test Agent
# Written by Seunghyun Lee : coder@dgist.ac.kr
# Somewhat place stones randomly on the board, but in reasonable manner

from ctypes import c_int
from dataclasses import asdict
from typing_extensions import assert_never, assert_type
from Utils import Point2d
from Gomoku import *
import random

class ai:
    def __init__(self):
        pass
    
    # Code exectued every time the game is reset
    def Initialize(self):
        
        pass
        
    # Code executed every move
    def Move(self, GG, color):
        a=0
        b=0
        c=0
        d=0
        p = GG.GetBoardDimension()
        if GG.GetNumberOfPlacedStones() == 0:
            return Point2d(p.x//2, p.y//2)
        for i in range (p.x):
            for j in range (p.y):
                    h,v,dl,dr=GG.GetLines(Point2d(i,j),3)
                    if GG.GetTurnText()=='black':
                        for k in range (7):
                            if h[k]==2:
                                a+=1
                        if a==3:
                            for l in range (7):
                                if h[l]==0:
                                    return Point2d(i,j+3)
                        for k in range (7):
                            if v[k]==2:
                                b+=1
                        if a==3:
                            for l in range (7):
                                if v[l]==0:
                                    return Point2d(i+3,j)
                        
                        for k in range (7):
                            if dl[k]==2:
                                c+=1
                        if a==3:
                            for l in range (7):
                                if dl[l]==0:
                                    return Point2d(i-3,j-3)
                        for k in range (7):
                            if dr[k]==2:
                                d+=1
                        if a==3:
                            for l in range (7):
                                if dr[l]==0:
                                    return Point2d(i+3,j+3)
                    elif GG.GetTurnText()=='white':
                        for k in range (7):
                            if h[k]==1:
                                a+=1
                        if a==3:
                            for l in range (7):
                                if h[l]==0:
                                    return Point2d(i+3,j)
                        for k in range (7):
                            if v[k]==1:
                                b+=1
                        if a==3:
                            for l in range (7):
                                if v[l]==0:
                                    return Point2d(i,j+3)
                        for k in range (7):
                            if dl[k]==1:
                                c+=1
                        if a==3:
                            for l in range (7):
                                if dl[l]==0:
                                    return Point2d(i-3,j-3)
                        for k in range (7):
                            if dr[k]==1:
                                d+=1
                        if a==3:
                            for l in range (7):
                                if dr[l]==0:
                                    return Point2d(i+3,j+3)
                        



                    


        if GG.board[p.x//2, p.y//2] == 0:
            return Point2d(p.x//2,p.y//2)
        
        for i in range (0,p.x):
            for j in range (0,p.y):
                if GG.IsPositionIsWinning(Point2d(i,j)) == True:
                    return Point2d(i,j)
        
                

        for i in range(p.y):
            lista=list()
            for j in range(p.x):
                lista.append(GG.board[j,i])
            if(GetConsecutiveStonesInLine(lista, j))==2:
                if(GG.board(j+2,i))==0:
                      return Point2d(j+2,i)
                elif(GG.board(j-2,i))==0:
                    return Point2d(j-2,i)
            if(GetConsecutiveStonesInLine(lista, j))==3:
                if(GG.board(j+3,i))==0:
                    return Point2d(j+3,i)
                elif(GG.board(j-3,i))==0:
                    return Point2d(j-3,i)   

        for j in range(p.x):
            listb=list()
            for i in range(p.y):
                listb.append(GG.board[j,i])
            if(GetConsecutiveStonesInLine(listb, i))==2:
                if(GG.board(j,i+2))==0:
                    return Point2d(j,i+2)
                elif(GG.board(j,i-2))==0:
                    return Point2d(j,i-2)
            if(GetConsecutiveStonesInLine(listb, i))==3:
                if(GG.board(j,i+3))==0:
                    return Point2d(j,i+3)
                elif(GG.board(j,i-3))==0:
                    return Point2d(j,i-3)
        


        v = GG.GetAllValidMovesInRange(1) 
        return random.choice(v)