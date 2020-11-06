import pygame 
import random as rnd
from enum import Enum
import time

#direction enum
class dir(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

global height 
global width 
height = int(input())
width = int(input())

def outOfRange(i, j):
    return i < 0 or i >= height or j < 0 or j >= width 

############################# FUNCTIONS GENERATING MAZE #####################################
#outOfRange and visited check
def invalidCoord(visited, connections, i, j):
    return outOfRange(i, j) or visited[i][j] == True

#opposite directions
def opposite(dir):
    if dir == dir.UP:
        return dir.DOWN
    if dir == dir.DOWN:
        return dir.UP
    if dir == dir.RIGHT:
        return dir.LEFT
    if dir == dir.LEFT:
        return dir.RIGHT

#change coords to next node depending on dir
def goNext(i, j, dir):
    if dir == dir.UP:
       return i - 1, j
    elif dir == dir.DOWN:
       return i + 1, j
    elif dir == dir.RIGHT:
       return i, j + 1
    elif dir == dir.LEFT:
       return i, j - 1

#making maze
def makeMaze():
  
    #connections = possible moves taken from point i, j for every i, j
    #visited = nodes already generated
    #stack = traceback for backtracking 
    connections = []
    visited = []
    stack = []

    #init lists
    for i in range(height):
        connections.append([])
        visited.append([])
        for j in range(width):
            connections[i].append(set())
            visited[i].append(False)
    
    #i, j are current coords
    #appending starting point to stack
    i, j = rnd.randint(0, height - 1), 0
    startPos = (i, j)

    stack.append((i, j))
    #fromDir contains direction in which we would come back to previous node
    fromDir = dir.LEFT

    #while there is possible traceback
    while not len(stack) == 0:
        #we mark node as visited and make connection to the previous node
        if not visited[i][j] == True:
            connections[i][j].add(fromDir)
            visited[i][j] = True
        
        #we determine possible generations for random choice
        possibleDirs = []
        if not invalidCoord(visited, connections, i + 1, j):
            possibleDirs.append(dir.DOWN)
        if not invalidCoord(visited, connections, i - 1, j):
            possibleDirs.append(dir.UP)
        if not invalidCoord(visited, connections, i, j + 1):
            possibleDirs.append(dir.RIGHT)
        if not invalidCoord(visited, connections, i, j - 1):
            possibleDirs.append(dir.LEFT)

        #if we have any choice
        if not len(possibleDirs) == 0:
            #append to traceback stack
            stack.append((i, j))
            #choose at random and connect to it
            chosenDir = possibleDirs[rnd.randint(0, len(possibleDirs) - 1)]
            connections[i][j].add(chosenDir)
            #change current node to chosen and update fromDir
            i, j = goNext(i, j, chosenDir)
            fromDir = opposite(chosenDir)
        #if we have no choice go back          
        else:
            i, j = stack.pop()
    
    #exit coords
    endI, endJ = rnd.randint(0, height - 1), width - 1
    connections[endI][endJ].add(dir.RIGHT)
    
    #return startPos, endPos, shape of maze
    return startPos, (endI, endJ), connections

#################################################

############################# DRAWING FUNCTIONS ###############################
#drawing given maze on screen
def drawMaze(screen, maze, CELL_SIZE, WALL_THICKNESS, ):
    #thickness of walls, size and color of filling rectangles 
    FILL_SIZE = CELL_SIZE - 2 * WALL_THICKNESS
    CONNECTION_COLOR = (0, 40, 100)
    LINE_COLOR = (32, 165, 55)
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
def drawPlayer(screen, playerPos, CELL_SIZE, WALL_THICKNESS):
    FILL_SIZE = CELL_SIZE - 2 * WALL_THICKNESS
    PLAYER_COLOR = (255, 120, 0)
    pygame.draw.rect(screen, PLAYER_COLOR, (WALL_THICKNESS + CELL_SIZE * playerPos[1], WALL_THICKNESS + CELL_SIZE * playerPos[0], FILL_SIZE, FILL_SIZE))

#######################################################################

################################# INTERACTIVE FUNCTIONS ####################################
#checking if move is viable
def validMove(i, j, maze, dir):
    return not outOfRange(i, j) and opposite(dir) in maze[i][j]

#updating player according to an input
def playerMovement(event, playerPos, maze):
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
    #some constants
    FPS_MAX = 15
    CELL_SIZE = 30
    WALL_THICKNESS = 2

    #used for framerate limit
    fpsClock = pygame.time.Clock()
    #start window
    screen = pygame.display.set_mode((CELL_SIZE * width, CELL_SIZE * height))
    pygame.display.flip()

    playerPos = [startPos[0], startPos[1]]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                playerMovement(event, playerPos, maze)
        
        drawMaze(screen, maze, CELL_SIZE, WALL_THICKNESS)
        drawPlayer(screen, playerPos, CELL_SIZE, WALL_THICKNESS)

        pygame.display.update()

        fpsClock.tick(FPS_MAX)

#####################################################################################
startPos, endPos, connections = makeMaze()
runGame(startPos, endPos, connections)



