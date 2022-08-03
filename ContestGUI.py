
from re import T
import timeit
import pygame
from Config import GAMEMODE, GRID_X, GRID_Y, BOARD_X, BOARD_Y
from Config import GS
from Gomoku import GomokuGame
from Utils import COLOR, Point2d, UIButton


#############################################################################################
# Add Your Agent Here
from Agents import Test, CleverAgent
AgentList = [Test.Test(), CleverAgent.CleverAgent()]
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

        self.UIElements = dict()
        # UI Elements
        ui_start = (BOARD_X+GS*(GRID_X+1), BOARD_Y)
        self.UIElements["S"] = UIButton((ui_start[0], ui_start[1], GS*3.8, GS*1.8), "Start", size=1.5, col=COLOR.green)
        self.UIElements["X"] = UIButton((ui_start[0]+GS*4, ui_start[1], GS*3.8, GS*1.8), "Start x 50", size=1, col=COLOR.green)
        self.UIElements["R"] = UIButton((ui_start[0], ui_start[1]+GS*2, GS*3.8, GS*1.8), "Reset", size=1.5, col=COLOR.red)
        self.UIElements["BX"] = UIButton((ui_start[0]+GS*4, ui_start[1]+GS*2, GS*3.8, GS*0.8), "Black:Human", size=0.8)
        self.UIElements["WX"] = UIButton((ui_start[0]+GS*4, ui_start[1]+GS*3, GS*3.8, GS*0.8), "White:Human", size=0.8)
        list_start = (BOARD_X+GS*(GRID_X+1), BOARD_Y+GS*4)
        for i in range(len(AgentList)):
            self.UIElements["B%s"%i] = UIButton((list_start[0] + GS*4, list_start[1]+GS*(i+7/4), GS*3/4, GS*3/4), "B", size=3/4)
            self.UIElements["W%s"%i] = UIButton((list_start[0] + GS*5, list_start[1]+GS*(i+7/4), GS*3/4, GS*3/4), "W", size=3/4)
    
    def Draw(self, screen):
        for key, value in self.UIElements.items():
            value.Draw(screen)

    def Event(self, event):
        for key, value in self.UIElements.items():
            clicked = value.Event(event)
            if clicked:
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
                elif key[0] == "X":
                    self.Execute(50)
                elif key[0] == "R":
                    self.Reset()

    def Reset(self):
        print("Resetting...")
        self.blackTime = 300
        self.whiteTime = 300
        GG.InitializeBoard()
        self.state = "idle"
        self.lastPoint = Point2d(-1, -1)
        pass

    def Execute(self, times):
        if self.state == "idle":
            self.state = "executing"
            print("Executing...")
            # Execute the game for times times
            pass

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
                    pass
                else:
                    pnt = self.blackPlayer.Move(GG, "black")
                    GG.PlaceStone(pnt)
                    self.lastPoint = pnt
            elif GG.GetTurnText() == "white":
                if self.whitePlayer is None:
                    pass
                else:
                    pnt = self.whitePlayer.Move(GG, "white")
                    GG.PlaceStone(pnt)
                    self.lastPoint = pnt

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
    pygame.draw.rect(screen, COLOR.black, [info_start[0], info_start[1], GS*(GRID_X), GS*3],2)

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

    # Draw Current Player Arrow
    size = GS*3/4
    center = [info_start[0]+GS*GRID_X/2, info_start[1]+GS*3/4]
    if GG.GetTurnText() == "black":
        pygame.draw.polygon(screen, COLOR.black, [[center[0]-size, center[1]],[center[0]-size/3, center[1]-size*2/3],[center[0]-size/3, center[1]+size*2/3]], 0)
        pygame.draw.rect(screen, COLOR.black, [center[0]-size/3, center[1]-size*1/3, size*2/3, size*2/3], 0)
    if GG.GetTurnText() == "white":
        pygame.draw.polygon(screen, COLOR.black, [[center[0]+size, center[1]],[center[0]+size/3, center[1]-size*2/3],[center[0]+size/3, center[1]+size*2/3]], 0)
        pygame.draw.rect(screen, COLOR.black, [center[0]-size/3, center[1]-size*1/3, size*2/3, size*2/3], 0)

    # Draw list of agents
    list_start = (BOARD_X+GS*(GRID_X+1), BOARD_Y+GS*4)
    t = fontLarge.render("Agent List", True, COLOR.black)
    screen.blit(t, [list_start[0]+GS/4, list_start[1]+GS/2])
    for i in range(len(AgentList)):
        # draw text
        t = fontMiddle.render(AgentList[i].__class__.__name__, True, COLOR.black)
        screen.blit(t, [list_start[0]+GS/4, list_start[1]+GS*1.8+i*GS])
        # draw line
        pygame.draw.line(screen, COLOR.black, [list_start[0]+GS/4, list_start[1]+GS*2.1+i*GS+GS/2], [list_start[0]+GS/4+GS*15, list_start[1]+GS*2.1+i*GS+GS/2], 2)


    GM.Draw(screen)


    pygame.display.flip()
    return 0



def MouseDown(pos):
    clickPos = Point2d((int)((pos[1]-BOARD_Y)/GS), (int)((pos[0]-BOARD_X)/GS))
    if clickPos.x < GRID_X and clickPos.y < GRID_Y and clickPos.x >= 0 and clickPos.y >= 0:
        print(clickPos)
        GG.PlaceStone(clickPos)
    return 0

GG.IsPositionMakesMorestones()

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