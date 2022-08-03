import pygame

def AddList(l1, l2):
    assert len(l1) == len(l2)
    out = list()
    for i in range(len(l1)):
        out.append(l1[i]+l2[i])
    return out

# Define some colors
class COLOR:
    black = (0,0,0)
    white = (255,255,255)
    grayBright = (200,200,200)
    gray = (150,150,150)
    grayDark = (100,100,100)
    red = (255,0,0)
    redBright = (200, 60, 60)
    redDark = (90, 0, 0)
    green = (0,255,0)
    greenBright = (60, 200, 60)
    blue = (0,0,255)
    blueBright = (60, 60, 200)
    yellow = (255, 255, 100)


class Point2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


def ArrowPoints(center, size, dir):
    if dir == "left":
        return [[center[0]-size    , center[1]         ],
                [center[0]-size/3  , center[1]-size*2/3],
                [center[0]-size/3  , center[1]-size*1/3],
                [center[0]+size    , center[1]-size*1/3],
                [center[0]+size    , center[1]+size*1/3],
                [center[0]+size/3  , center[1]+size*1/3],
                [center[0]+size/3  , center[1]+size*2/3]]


from Config import GS

def DrawText(screen, position, text, size=1, col=COLOR.black, align="lt"):
    f = pygame.font.SysFont(None, int(GS*size))
    to = f.render(text, False, col)    
    tr = to.get_rect()
    if   align[0] == "l": # Align horizontal [l, c, r]
        tr.center = (position[0] + tr.w/2, tr.center[1])
    elif align[0] == "c": 
        tr.center = (position[0]         , tr.center[1])
    elif align[0] == "r":
        tr.center = (position[0] - tr.w/2, tr.center[1])
    if   align[1] == "t": # Align vertical [t, m, b]
        tr.center = (tr.center[0], position[1] + tr.h/2)
    elif align[1] == "m":
        tr.center = (tr.center[0], position[1])
    elif align[1] == "b":
        tr.center = (tr.center[0], position[1] - tr.h/2)
    screen.blit(to,tr)


# Edit button
class UIButton:
    def __init__(self, rect, text, size = 1, colText = COLOR.black, col = COLOR.grayBright, colClicked = COLOR.gray, colDeactive = COLOR.grayDark, colHighlight = COLOR.white, colOutline = COLOR.black, outlineWidth = 2):
        # Basic
        self.active = True
        self.highlight = False
        self.clicked = False
        self.rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])
        self.text = text
        self.size = size

        # Colors
        self.colText = colText
        self.col = col
        self.colClicked = colClicked
        self.colDeactive = colDeactive
        self.colHighlight = colHighlight
        self.colOutline = colOutline

        # Others
        self.outlineWidth = outlineWidth
    
    def SetActive(self, v):
        self.active = v

    def Event(self, event):
        if self.active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.clicked = True
                else:
                    self.clicked = False
            elif event.type == pygame.MOUSEBUTTONUP:
                self.clicked = False
            elif event.type == pygame.MOUSEMOTION:
                if self.rect.collidepoint(event.pos):
                    self.highlight = True
                else:
                    self.highlight = False
        return self.clicked

    def Draw(self, screen):
        if not self.active:
            pygame.draw.rect(screen, self.colDeactive, self.rect, 0)
        elif self.clicked:
            pygame.draw.rect(screen, self.colClicked, self.rect, 0)
        elif self.highlight:
            pygame.draw.rect(screen, self.colHighlight, self.rect, 0)
        else:
            pygame.draw.rect(screen, self.col, self.rect, 0)
        pygame.draw.rect(screen, self.colOutline, self.rect, self.outlineWidth)
        DrawText(screen, AddList(self.rect[:2], [self.rect[2]/2, self.rect[3]/2]), self.text, self.size, col=COLOR.black, align="cm")
