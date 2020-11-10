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

###############################################################################

############################# DRAWING FUNCTIONS ###############################
#drawing given maze on screen
def drawMaze(screen, maze, CELL_SIZE, WALL_THICKNESS, CONNECTION_COLOR):
    #thickness of walls, size of filling rectangles 
    FILL_SIZE = CELL_SIZE - 2 * WALL_THICKNESS
    LINE_COLOR = (200, 50, 100)
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
def drawPlayer(screen, playerPos, previous, CELL_SIZE, WALL_THICKNESS, CONNECTION_COLOR):
    FILL_SIZE = CELL_SIZE - 2 * WALL_THICKNESS
    PLAYER_COLOR = (255, 120, 0)
    pygame.draw.rect(screen, CONNECTION_COLOR, (WALL_THICKNESS + CELL_SIZE * previous[1], WALL_THICKNESS + CELL_SIZE * previous[0], FILL_SIZE, FILL_SIZE))
    pygame.draw.rect(screen, PLAYER_COLOR, (WALL_THICKNESS + CELL_SIZE * playerPos[1], WALL_THICKNESS + CELL_SIZE * playerPos[0], FILL_SIZE, FILL_SIZE))
   

###############################################################################################

################################# INTERACTIVE FUNCTIONS ####################################
#checking if move is viable
def validMove(i, j, maze, dir):
    return not outOfRange(i, j) and opposite(dir) in maze[i][j]

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
    #some constants
    #we fetch screen height
    SCREEN_H = pygame.display.Info().current_h
    #if height of the maze is less than 50 then half the screen is enough on 1920x1080 screen (more responsive design later)
    if height < 50:
        SCREEN_H = SCREEN_H // 2
    #we choose height as our scaling factor (// to avoid grid tearing )
    CELL_SIZE = SCREEN_H // height
    print(CELL_SIZE)
    #
    WINDOW_HEIGHT = int(CELL_SIZE * height)
    print(WINDOW_HEIGHT)
    WINDOW_WIDTH = int(CELL_SIZE * width) 
    print(WINDOW_WIDTH)
    #no more fps (and by that input events) are needed
    FPS_MAX = 30
    #it needs to be at least 1 but then we scale it to fit smaller mazes
    WALL_THICKNESS = int(CELL_SIZE * 0.05) + 1
    print(WALL_THICKNESS)
    #ground color, personal preference (can add interactive color choice later)
    CONNECTION_COLOR = (0, 100, 200)

    #used for framerate limit
    fpsClock = pygame.time.Clock()
    #playerPos init at the opening
    playerPos = [startPos[0], startPos[1]]
    previous = [startPos[0], startPos[1]]

    #start window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.flip()

    #we only need to draw maze once, then we need only to update player and his previous square
    drawMaze(screen, maze, CELL_SIZE, WALL_THICKNESS, CONNECTION_COLOR)
    drawPlayer(screen, playerPos, previous, CELL_SIZE, WALL_THICKNESS, CONNECTION_COLOR)

    #main game loop
    running = True
    while running:
        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                playerMovement(event, playerPos, previous, maze)
        
        #rest of logic 
        drawPlayer(screen, playerPos, previous, CELL_SIZE, WALL_THICKNESS, CONNECTION_COLOR)
        pygame.display.update()
        fpsClock.tick(FPS_MAX)

#################################################################################################
startPos, endPos, connections = makeMaze()
pygame.init()
runGame(startPos, endPos, connections)



#TODO:
# ADD RESTRAINS TO MAZE SIZE
# MAKE INTERACTIVE START SCREEN WHERE YOU CAN CHOOSE SIZE AND COLOR OF THE MAZE
# PATHFINDING ALGORITHM (DIJKSTRA AND A* MAYBE DFS)
# MORE RESPONSIVE WINDOW
# BUG: YOU CAN GO DIAGONALLY GIVEN THE RIGHT INPUT (LEAVE IT OR FLUSH EVENTS AFTER MOVEMENT ACTION)
# REFACTOR MAYBE
#
#
#
#
#