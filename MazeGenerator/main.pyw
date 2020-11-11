import pygame 
import time
import sys
import generator as gnr
from dir import dir 
import os
from  forms import form as f
from forms import button as butt

pygame.init()

#some consts
height = 0                                  #num of rows
width = 0                                   #num of cols
SCREEN_H = pygame.display.Info().current_h  #monitor height
LINE_COLOR = None                           #color of walls
PLAYER_COLOR = None                         #color of player
CONNECTION_COLOR = None                     #color of maze
CELL_SIZE = None                            #size of cell (all 4 walls  + center)
WINDOW_HEIGHT = None                        #created window height
WINDOW_WIDTH = None                         #created window width
FPS_MAX = None                              #max fps
WALL_THICKNESS = None                       #thickness of walls
startImg = None                             #image of start point
endImg = None                               #image of end point

#initializing before runGame
def initConsts(w, h):
    global height
    global width
    global SCREEN_H
    global LINE_COLOR
    global PLAYER_COLOR
    global CONNECTION_COLOR
    global CELL_SIZE
    global WINDOW_HEIGHT
    global WINDOW_WIDTH
    global FPS_MAX
    global WALL_THICKNESS
    global startImg
    global endImg

    width = int(w)
    height = int(h)
    LINE_COLOR = (200, 50, 100)
    PLAYER_COLOR = (255, 120, 0)
    CONNECTION_COLOR = (0, 100, 200)
    #if height of the maze is less than 50 then half the screen is enough on 1920x1080 screen (more responsive design later)
    if height < 50:
       SCREEN_H = SCREEN_H // 2
    #to not obscure window borders
    else:
        SCREEN_H = int(SCREEN_H * 0.9)
    #we choose height as our scaling factor (// to avoid grid tearing)
    CELL_SIZE = SCREEN_H // height
    WINDOW_HEIGHT = int(CELL_SIZE * height)
    WINDOW_WIDTH = int(CELL_SIZE * width) 
    #no more fps (and by that input events) are needed
    FPS_MAX = 30
    #it needs to be at least 1 but then we scale it to fit smaller mazes
    WALL_THICKNESS = int(CELL_SIZE * 0.05) + 1
    #loading imgs
    startImg = pygame.transform.scale(pygame.image.load("start.png"), (CELL_SIZE - 2 * WALL_THICKNESS, CELL_SIZE - 2 * WALL_THICKNESS))
    endImg = pygame.transform.scale(pygame.image.load("exit.png"), (CELL_SIZE - 2 * WALL_THICKNESS, CELL_SIZE - 2 * WALL_THICKNESS))
 


############################# DRAWING FUNCTIONS ###############################
#drawing given maze on screen
def drawMaze(screen, maze):
    #thickness of walls, size of filling rectangles 
    FILL_SIZE = CELL_SIZE - 2 * WALL_THICKNESS
    #filling screen with white so we can fill connections with CONNECTION_COLOR
    screen.fill(LINE_COLOR)
    for i in range(height):
        for j in range(width):
            #positions of filling rectangles
            FILL_CENTER_POS_X = WALL_THICKNESS + CELL_SIZE * j
            FILL_CENTER_POS_Y = WALL_THICKNESS + CELL_SIZE * i
            #drawing filling rectangles (basically making grid)
            pygame.draw.rect(screen, CONNECTION_COLOR, (FILL_CENTER_POS_X, FILL_CENTER_POS_Y, FILL_SIZE, FILL_SIZE))
            #adding connectors to grid to make a maze
            
            if dir.DOWN in maze[i][j]:
                pygame.draw.rect(screen, CONNECTION_COLOR, (FILL_CENTER_POS_X, FILL_CENTER_POS_Y + FILL_SIZE, FILL_SIZE, WALL_THICKNESS))
            if dir.UP in maze[i][j]:
                pygame.draw.rect(screen, CONNECTION_COLOR, (FILL_CENTER_POS_X, FILL_CENTER_POS_Y - WALL_THICKNESS, FILL_SIZE, WALL_THICKNESS))
            if dir.RIGHT in maze[i][j]:
                pygame.draw.rect(screen, CONNECTION_COLOR, (FILL_CENTER_POS_X + FILL_SIZE, FILL_CENTER_POS_Y, WALL_THICKNESS, FILL_SIZE))
            if dir.LEFT in maze[i][j]:
                pygame.draw.rect(screen, CONNECTION_COLOR, (FILL_CENTER_POS_X - WALL_THICKNESS, FILL_CENTER_POS_Y, WALL_THICKNESS, FILL_SIZE))

#drawing player rect
def drawPlayer(screen, playerPos):
    FILL_SIZE = CELL_SIZE - 2 * WALL_THICKNESS
    pygame.draw.rect(screen, PLAYER_COLOR, (WALL_THICKNESS + CELL_SIZE * playerPos[1], WALL_THICKNESS + CELL_SIZE * playerPos[0], FILL_SIZE, FILL_SIZE))

def erasePlayer(screen, previous):
    FILL_SIZE = CELL_SIZE - 2 * WALL_THICKNESS
    pygame.draw.rect(screen, CONNECTION_COLOR, (WALL_THICKNESS + CELL_SIZE * previous[1], WALL_THICKNESS + CELL_SIZE * previous[0], FILL_SIZE, FILL_SIZE))
   
#drawing end and start points
def drawExits(screen, startPos, endPos):
    screen.blit(startImg, (WALL_THICKNESS + CELL_SIZE * startPos[1], WALL_THICKNESS + CELL_SIZE * startPos[0]))
    screen.blit(endImg, (WALL_THICKNESS + CELL_SIZE * endPos[1], WALL_THICKNESS + CELL_SIZE * endPos[0]))

###############################################################################################

################################# INTERACTIVE FUNCTIONS ####################################
#checking if move is viable
def validMove(i, j, maze, dir):
    return not gnr.outOfRange(i, j, height, width) and gnr.opposite(dir) in maze[i][j]

#updating player according to an input
def playerMovement(event, playerPos, previous, maze):
   #for some reason when updating previous y coord we need to also change previous x coord and vice versa
   previous[0] = playerPos[0]
   previous[1] = playerPos[1]
   if event.key == pygame.K_LEFT and validMove(playerPos[0], playerPos[1] - 1, maze, dir.LEFT):
       playerPos[1] -= 1
   elif event.key == pygame.K_RIGHT and validMove(playerPos[0], playerPos[1] + 1, maze, dir.RIGHT):
       playerPos[1] += 1
   elif event.key == pygame.K_UP and validMove(playerPos[0] - 1, playerPos[1], maze, dir.UP):
       playerPos[0] -= 1
   elif event.key == pygame.K_DOWN and validMove(playerPos[0] + 1, playerPos[1], maze, dir.DOWN):
       playerPos[0] += 1

#############################################################################################

############################### MAIN GAME FUNCTION ########################################## 
#main game loop function
def runGame(startPos, endPos, maze):
    #used for framerate limit
    fpsClock = pygame.time.Clock()
    #playerPos init at the opening
    playerPos = [startPos[0], startPos[1]]
    previous = [startPos[0], startPos[1]]

    #start window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.flip()

    #we only need to draw maze once, then we need only to update player and his previous square
    drawMaze(screen, maze)

    #main game loop
    running = True
    while running:
        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                playerMovement(event, playerPos, previous, maze)
        
        if playerPos[0] == endPos[0] and playerPos[1] == endPos[1]:
            running = False

        #draw
        erasePlayer(screen, previous)
        drawExits(screen, startPos, endPos) 
        drawPlayer(screen, playerPos)
        #update
        pygame.display.update()
        fpsClock.tick(FPS_MAX)

#################################################################################################
#initial window
def run():
    screen = pygame.display.set_mode((500, 500))
    pygame.display.flip()
    screen.fill((50, 50, 200))

    #forms for maze size input
    wForm = f(100, 50, 300, 50, (255,255,255))
    hForm = f(100, 175, 300, 50, (255,255,255))
    #button for applying settings
    button = butt(50, 400, 400, 50, (100, 100, 100), "GENERATE")
    #text above forms
    wText = pygame.font.SysFont('Arial', 30).render("WIDTH", True, (0, 0, 0))
    hText = pygame.font.SysFont('Arial', 30).render("HEIGHT", True, (0, 0, 0))
    #position of text
    wTextRect = wText.get_rect(center = (250, 30))
    hTextRect = hText.get_rect(center = (250, 150))

    while True:
        for event in pygame.event.get():
            wForm.capture(event)
            hForm.capture(event)
            generation = button.checkClick(event)
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
        
        #we want maximum size of maze to be 100 because of readability
        if  len(wForm.getInput()) != 0 and int(wForm.getInput()) > 100:
            wForm.changeInput("100")
        if  len(hForm.getInput()) != 0 and int(hForm.getInput()) > 100:
            hForm.changeInput("100")

        #after applying settings we go to maze visualization
        if generation:
            initConsts(wForm.getInput(), hForm.getInput())
            startPos, endPos, maze = gnr.makeMaze(height, width)
            runGame(startPos, endPos, maze)
            pygame.quit()
            exit()

        button.draw(screen)
        wForm.draw(screen)
        hForm.draw(screen)
        screen.blit(wText, wTextRect)
        screen.blit(hText, hTextRect)
        pygame.display.update()

    pygame.quit()
    exit()

######################################################################################################
run()



#TODO:
# ADD RESTRAINS TO MAZE SIZE
# MAKE INTERACTIVE START SCREEN WHERE YOU CAN CHOOSE SIZE AND COLOR OF THE MAZE
# PATHFINDING ALGORITHM (DIJKSTRA AND A* MAYBE DFS)
# MORE RESPONSIVE WINDOW
# BUG: YOU CAN GO DIAGONALLY GIVEN THE RIGHT INPUT (LEAVE IT OR FLUSH EVENTS AFTER MOVEMENT ACTION)
# REFACTOR MAYBE
# MAZEBUILDING ANIMATION
# FIND A WAY TO CENTER GAME WINDOW
#
#
#