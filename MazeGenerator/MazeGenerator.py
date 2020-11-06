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

#outOfRange and visited check
def invalidCoord(visited, connections, i, j):
    return i < 0 or i >= len(connections) or j < 0 or j >= len(connections[i]) or visited[i][j] == True

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
  
    #taking width and height of maze
    width = int(input())
    height = int(input())

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
            connections[i].append([])
            visited[i].append(False)
    
    #i, j are current coords
    #appending starting point to stack
    i, j = rnd.randint(0, len(connections) - 1), 0
    stack.append((i, j))
    #fromDir contains direction in which we would come back to previous node
    fromDir = dir.LEFT

    #while there is possible traceback
    while not len(stack) == 0:
        #we mark node as visited and make connection to the previous node
        if not visited[i][j] == True:
            connections[i][j].append(fromDir)
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
            connections[i][j].append(chosenDir)
            #change current node to chosen and update fromDir
            i, j = goNext(i, j, chosenDir)
            fromDir = opposite(chosenDir)
        #if we have no choice go back          
        else:
            i, j = stack.pop()
    
    #return size and shape of maze
    return width, height, connections


def runGame(width, height, maze):
    screen = pygame.display.set_mode((width, height))
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False



runGame(makeMaze())



