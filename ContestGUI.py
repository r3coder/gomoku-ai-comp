
import random
from re import T
import timeit
import pygame
from Config import GAMEMODE, GRID_X, GRID_Y, BOARD_X, BOARD_Y, ROUNDS
from Config import GS
from Gomoku import GomokuGame
from Utils import COLOR, Point2d, UIButton


#############################################################################################
# Add Your Agent Here
from Agents import RandomDrop
AgentList = [RandomDrop.RandomDrop()]
#############################################################################################

GG = GomokuGame(Point2d(GRID_X, GRID_Y))

class GameManager:
    def __init__(self):
        self.blackPlayer = None
        self.whitePlayer = None
        self.blackTime = 300
        self.whiteTime = 300

        self.state = "idle"
        self.lastPoint = Point2d(-1, -1)

        self.currentRound = 0
        self.totalRound = ROUNDS

        self.time_limit = 1.0
        self.UIElements = dict()

        self.roundTotal = [0] * (len(AgentList) + 1)
        self.roundWin = [0] * (len(AgentList) + 1)
        self.moveTotal = [0] * (len(AgentList))
        self.moveFail = [0] * (len(AgentList))
        self.log = ""

        self.stepPause = 0

        # log file
        self.logFile = open("log.txt", "w")
        self.logFile.write("Log\n")
        # UI Elements
        ui_start = (BOARD_X+GS*(GRID_X+1), BOARD_Y)
        self.UIElements["S"] = UIButton((ui_start[0], ui_start[1], GS*3.8, GS*1.8), "Start", size=1.5, col=COLOR.green)
        self.UIElements["X"] = UIButton((ui_start[0]+GS*4, ui_start[1], GS*3.8, GS*1.8), "Start x %d"%ROUNDS, size=1, col=COLOR.green)
        self.UIElements["R"] = UIButton((ui_start[0], ui_start[1]+GS*2, GS*3.8, GS*1.8), "Reset", size=1.5, col=COLOR.red)
        self.UIElements["BX"] = UIButton((ui_start[0]+GS*4, ui_start[1]+GS*2, GS*3.8, GS*0.8), "Black:Human", size=0.8)
        self.UIElements["WX"] = UIButton((ui_start[0]+GS*4, ui_start[1]+GS*3, GS*3.8, GS*0.8), "White:Human", size=0.8)
        list_start = (BOARD_X+GS*(GRID_X+1), BOARD_Y+GS*4)
        for i in range(len(AgentList)):
            self.UIElements["B%s"%i] = UIButton((list_start[0] + GS*6, list_start[1]+GS*(i+11/4), GS*3/4, GS*3/4), "B", size=3/4)
            self.UIElements["W%s"%i] = UIButton((list_start[0] + GS*7, list_start[1]+GS*(i+11/4), GS*3/4, GS*3/4), "W", size=3/4)
    
    def Draw(self, screen):
        for key, value in self.UIElements.items():
            value.Draw(screen)

    def Event(self, event):
        for key, value in self.UIElements.items():
            clicked = value.Event(event)
            if event.type == pygame.MOUSEBUTTONDOWN and value.rect.collidepoint(event.pos):
                if key[0] == "B":
                    if key[1] == "X":
                        self.blackPlayer = None
                    else:
                        self.blackPlayer = AgentList[int(key[1])]
                elif key[0] == "W":
                    if key[1] == "X":
                        self.whitePlayer = None
                    else:
                        self.whitePlayer = AgentList[int(key[1])]
                elif key[0] == "S":
                    self.Execute(1)
                    print("executing")

                elif key[0] == "X":
                    self.Execute(ROUNDS)
                elif key[0] == "R":
                    self.Reset()

    def Reset(self):
        print("Resetting...")
        self.blackTime = 300
        self.whiteTime = 300
        GG.InitializeBoard()
        self.state = "idle"
        self.lastPoint = Point2d(-1, -1)
        
        self.log = ""
        self.currentRound = 0
        self.totalRound = ROUNDS
        pass

    def StartRound(self):
        self.state = "executing"
        self.currentRound += 1
        self.stepPause = 180
        print("Round %s"%self.currentRound)
        GG.InitializeBoard()
        self.logFile.write("Black '%s', White '%s':"%(self.GetPlayerName("black"), self.GetPlayerName("white")))
        self.lastPoint = Point2d(-1, -1)
        if self.blackPlayer != None:
            self.blackPlayer.Initialize()
        if self.whitePlayer != None:
            self.whitePlayer.Initialize()

    def Execute(self, times):
        self.totalRound = times
        self.currentRound = 0
        self.log = ""
        if self.state == "idle":
            if self.currentRound < self.totalRound:
                self.StartRound()

    def GetPlayerName(self, user):
        if user == "black":
            if self.blackPlayer is None:
                return "Human"
            else:
                return self.blackPlayer.__class__.__name__
        elif user == "white":
            if self.whitePlayer is None:
                return "Human"
            else:
                return self.whitePlayer.__class__.__name__
        else:
            return None

    def Step(self):
        if self.state == "idle":
            for key, value in self.UIElements.items():
                if key[0] == "B" or key[0] == "W" or key[0] == "S" or key[0] == "X":
                    value.SetActive(True)
        elif self.state == "executing":
            for key, value in self.UIElements.items():
                if key[0] == "B" or key[0] == "W" or key[0] == "S" or key[0] == "X":
                    value.SetActive(False)

            if GG.GetTurnText() == "black":
                if self.blackPlayer is None:
                    pnt = None
                else:
                    flag = False
                    try:
                        pnt = self.blackPlayer.Move(GG, "black")
                        print("Black Player %s Played %s"%(self.blackPlayer.__class__.__name__, str(pnt)))
                    except Exception as e:
                        print(str(e))
                        pnt = None
                        flag = True
                    v, m = GG.PlaceStone(pnt)
                    if flag or not v:
                        print("Black Player Tried to play invalid move!, placing stone at random")
                        self.moveFail[AgentList.index(self.blackPlayer)] += 1
                        pnt = random.choice(GG.GetAllValidMoves())
                        GG.PlaceStone(pnt)
                    self.moveTotal[AgentList.index(self.blackPlayer)] += 1
                            
            elif GG.GetTurnText() == "white":
                if self.whitePlayer is None:
                    pnt = None
                else:
                    flag = False
                    try:
                        pnt = self.whitePlayer.Move(GG, "white")
                        print("White Player %s Played %s"%(self.whitePlayer.__class__.__name__, str(pnt)))
                    except Exception as e:
                        print(str(e))
                        pnt = None
                        flag = True
                    v, m = GG.PlaceStone(pnt)
                    if flag or not v:
                        print("White Player Tried to play invalid move!, placing stone at random position")
                        self.moveFail[AgentList.index(self.whitePlayer)] += 1
                        pnt = random.choice(GG.GetAllValidMoves())
                        GG.PlaceStone(pnt)
                    self.moveTotal[AgentList.index(self.whitePlayer)] += 1
            if pnt != None:
                self.logFile.write("%s, "%str(pnt))
                self.lastPoint = pnt
            
            # Check if end of game
            if GG.state == "over":
                # add winner
                if self.blackPlayer != None:
                    ind_b = AgentList.index(self.blackPlayer)
                else:
                    ind_b = -1
                if self.whitePlayer != None:
                    ind_w = AgentList.index(self.whitePlayer)
                else:
                    ind_w = -1

                if GG.winner == 1:
                    self.roundWin[ind_b] += 1
                    self.log += "B"
                    self.logFile.write(" Black Win\n")
                elif GG.winner == 2:
                    self.log += "W"
                    self.roundWin[ind_w] += 1
                    self.logFile.write(" White Win\n")
                else:
                    self.logFile.write(" Draw\n")

                
                self.roundTotal[ind_b] += 1
                self.roundTotal[ind_w] += 1
                self.state = "ready"
        elif self.state == "ready":
            self.stepPause -= 1
            if self.stepPause <= 0:
                if self.currentRound == self.totalRound:
                    self.state = "idle"
                else:
                    self.StartRound()
                    

    def SetAgent(self, user, index):
        if user == "black":
            self.blackPlayer = AgentList[index]
        elif user == "white":
            self.whitePlayer = AgentList[index]
        else:
            print("Agent set!")
            return False
        print("Agent set!")
        return True

GM = GameManager()
from Gomoku import *
lst = [0, 0, 1, 1, 1, 0, 1, 1, 0]
GetConsecutiveStonesInLine(lst, 4)
# Draw everything
def Draw(screen):
    screen.fill(COLOR.white)

    # Draw gomoku board
    board_start = (BOARD_X, BOARD_Y)
    pygame.draw.rect(screen, (249,224,146), [board_start[0], board_start[1], GS*(GRID_X), GS*(GRID_Y)],0)
    pygame.draw.rect(screen, COLOR.black, [board_start[0], board_start[1], GS*(GRID_X), GS*(GRID_Y)],2)
    pygame.draw.rect(screen, COLOR.black, [board_start[0]+GS/2, board_start[1]+GS/2, GS*(GRID_X-1), GS*(GRID_Y-1)],4)
    for ix in range(GRID_X-1):
        for iy in range(GRID_Y-1):
            pygame.draw.rect(screen, COLOR.black, [board_start[0]+GS/2+iy*GS, board_start[1]+GS/2+ix*GS, GS, GS],2)

    # Draw center point
    pygame.draw.circle(screen, COLOR.black, [board_start[0]+GS*GRID_X/2, board_start[0]+GS*GRID_Y/2], 5)
    pygame.draw.circle(screen, COLOR.black, [board_start[0]+GS*(3+1/2), board_start[0]+GS*(3+1/2)], 5)
    pygame.draw.circle(screen, COLOR.black, [board_start[0]+GS*(3+1/2), board_start[0]+GS*(GRID_Y-3-1/2)], 5)
    pygame.draw.circle(screen, COLOR.black, [board_start[0]+GS*(GRID_X-3-1/2), board_start[0]+GS*(3+1/2)], 5)
    pygame.draw.circle(screen, COLOR.black, [board_start[0]+GS*(GRID_X-3-1/2), board_start[0]+GS*(GRID_Y-3-1/2)], 5)


    if GM.lastPoint.x != -1:
        pygame.draw.circle(screen, COLOR.red, [board_start[0]+GS*(1/2+GM.lastPoint.y), board_start[0]+GS*(1/2+GM.lastPoint.x)], GS/2)

    # Draw stones
    for i in range(GRID_X):
        for j in range(GRID_Y):
            if GG.board[j,i] == 1:
                pygame.draw.circle(screen, COLOR.black, [board_start[0]+GS*i+GS/2, board_start[1]+GS*j+GS/2], GS/2-4)
                pygame.draw.circle(screen, COLOR.black, [board_start[0]+GS*i+GS/2, board_start[1]+GS*j+GS/2], GS/2-6)
            elif GG.board[j,i] == 2:
                pygame.draw.circle(screen, COLOR.black, [board_start[0]+GS*i+GS/2, board_start[1]+GS*j+GS/2], GS/2-4)
                pygame.draw.circle(screen, COLOR.white, [board_start[0]+GS*i+GS/2, board_start[1]+GS*j+GS/2], GS/2-6)

    # Draw Game Information
    info_start = (BOARD_X, BOARD_Y+GS*GRID_Y+GS/4)
    pygame.draw.rect(screen, COLOR.black, [info_start[0], info_start[1], GS*(GRID_X), GS*4],2)

    fontMiddle = pygame.font.SysFont(None, GS)
    fontSmall = pygame.font.SysFont(None, int(GS*3/4))
    fontLarge = pygame.font.SysFont(None, int(GS*3/2))
    # Draw Information
    # textState = fontMiddle.render("State : " + str(GG.state), True, COLOR.black)
    # screen.blit(textState, [info_start[0]+GS/4, info_start[1]+GS/4])
    screen.blit(fontSmall.render("Black", True, COLOR.black)
        , [info_start[0]+GS/4, info_start[1]+GS/4])
    screen.blit(fontMiddle.render(GM.GetPlayerName("black"), True, COLOR.black)
        , [info_start[0]+GS/4, info_start[1]+GS/4+GS*3/4])
    # t = fontSmall.render("%2d:%2d.%3d"%(GM.blackTime/60,GM.blackTime%60,GM.blackTime/1000), True, COLOR.black)
    # screen.blit(t
    #     , [info_start[0]+GS/4, info_start[1]+GS/4+GS*6/4])
    t = fontSmall.render("White", True, COLOR.black)
    screen.blit(t
        , [info_start[0]+GS*GRID_X-GS/4 - t.get_rect().w, info_start[1]+GS/4], )
    t = fontMiddle.render(GM.GetPlayerName("white"), True, COLOR.black)
    screen.blit(t
        , [info_start[0]+GS*GRID_X-GS/4 - t.get_rect().w, info_start[1]+GS/4+GS*2/4], )

    t = fontSmall.render("%d/%d"%(GM.currentRound, GM.totalRound), True, COLOR.black)
    screen.blit(t
        , [info_start[0]+GS*GRID_X/2 - t.get_rect().w/2, info_start[1]+GS*5/4], )


    # Draw log
    if len(GM.log) > 0:
        # draw circle
        for i in range(len(GM.log)):
            if GM.log[i] == "B":
                color = COLOR.black
            elif GM.log[i] == "W":
                color = COLOR.white
            pos = [info_start[0]+GS*3/4+(i%20)*GS*0.7, info_start[1]+(i//20)*GS*0.7+GS*2.2]
            pygame.draw.circle(screen, COLOR.black, pos, GS/4+2, 0)
            pygame.draw.circle(screen, color, pos, GS/4, 0)


    # Draw Current Player Arrow
    size = GS*3/4
    center = [info_start[0]+GS*GRID_X/2, info_start[1]+GS*3/4]
    if GG.GetTurnText() == "black":
        pygame.draw.polygon(screen, COLOR.black, [[center[0]-size, center[1]],[center[0]-size/3, center[1]-size*2/3],[center[0]-size/3, center[1]+size*2/3]], 0)
        pygame.draw.rect(screen, COLOR.black, [center[0]-size/3, center[1]-size*1/3, size*2/3, size*2/3], 0)
    if GG.GetTurnText() == "white":
        pygame.draw.polygon(screen, COLOR.black, [[center[0]+size, center[1]],[center[0]+size/3, center[1]-size*2/3],[center[0]+size/3, center[1]+size*2/3]], 0)
        pygame.draw.rect(screen, COLOR.black, [center[0]-size/3, center[1]-size*1/3, size*2/3, size*2/3], 0)

    fontMono = pygame.font.SysFont("Consolas", GS//2)
    # Draw list of agents
    list_start = (BOARD_X+GS*(GRID_X+1), BOARD_Y+GS*4)
    t = fontLarge.render("Agent List", True, COLOR.black)
    screen.blit(t, [list_start[0]+GS/4, list_start[1]+GS/2])

    # Human Player
    
    if GM.roundWin[-1] == 0:
        v = 0.0
    else:
        v = float(GM.roundWin[-1])*100/float(GM.roundTotal[-1])
    t = fontMiddle.render("Human", True, COLOR.black)
    screen.blit(t, [list_start[0]+GS/4, list_start[1]+GS*1.8])
    pygame.draw.line(screen, COLOR.black, [list_start[0]+GS/4, list_start[1]+GS*2.1+GS/2], [list_start[0]+GS/4+GS*18, list_start[1]+GS*2.1+GS/2], 2)
    t = fontMono.render("%3d/%3d %5.1f%%"%(GM.roundWin[-1], GM.roundTotal[-1], v), True, COLOR.black)
    screen.blit(t, [list_start[0]+GS/4+GS*8, list_start[1]+GS*2])

    t = fontSmall.render("Win Rate", True, COLOR.black)
    screen.blit(t, [list_start[0]+GS*9, list_start[1]+GS*1.2])
    t = fontSmall.render("Move Invalid rate", True, COLOR.black)
    screen.blit(t, [list_start[0]+GS*14, list_start[1]+GS*1.2])

    for i in range(len(AgentList)):
        # draw text
        t = fontMiddle.render(AgentList[i].__class__.__name__, True, COLOR.black)
        screen.blit(t, [list_start[0]+GS/4, list_start[1]+GS*2.8+i*GS])
        # draw line
        pygame.draw.line(screen, COLOR.black, [list_start[0]+GS/4, list_start[1]+GS*3.1+i*GS+GS/2], [list_start[0]+GS/4+GS*18, list_start[1]+GS*3.1+i*GS+GS/2], 2)
        # draw stat
        
        if GM.roundTotal[i] == 0:
            v = 0.0
        else:
            v = float(GM.roundWin[i])*100/float(GM.roundTotal[i])
        if GM.moveTotal[i] == 0:
            m = 0.0
        else:
            m = float(GM.moveFail[i])*100/float(GM.moveTotal[i])
        t = fontMono.render("%3d/%3d %5.1f%%   %4d/%4d %5.1f%%"%(GM.roundWin[i], GM.roundTotal[i], v, GM.moveFail[i], GM.moveTotal[i], m), True, COLOR.black)
        screen.blit(t, [list_start[0]+GS/4+GS*8, list_start[1]+GS*3+i*GS])

    GM.Draw(screen)



    pygame.display.flip()
    return 0



def MouseDown(pos):
    clickPos = Point2d((int)((pos[1]-BOARD_Y)/GS), (int)((pos[0]-BOARD_X)/GS))
    if clickPos.x < GRID_X and clickPos.y < GRID_Y and clickPos.x >= 0 and clickPos.y >= 0:
        print("Human player placed at ",clickPos)
        if GG.GetTurnText() == "black" and GM.blackPlayer == None:
            GG.PlaceStone(clickPos)
        elif GG.GetTurnText() == "white" and GM.whitePlayer == None:
            GG.PlaceStone(clickPos)
    return 0


def Main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))

    pygame.display.set_caption("Gomoku Contest GUI")

    running = True
    while running:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                MouseDown(pygame.mouse.get_pos())
            GM.Event(event)
        
        GM.Step()
        Draw(screen)

    pygame.quit()
    return 0




if __name__=="__main__":
    Main()