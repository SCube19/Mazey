import random as rnd
from dir import dir

############################# FUNCTIONS GENERATING MAZE #####################################
#outOfRange and visited check
def invalidCoord(visited, i, j, height, width):
    return outOfRange(i, j, width, height) or visited[i][j] == True

def outOfRange(i, j, height, width):
    return i < 0 or i >= height or j < 0 or j >= width 

#opposite directions
def opposite(direction):
    if direction == dir.UP:
        return dir.DOWN
    if direction == dir.DOWN:
        return dir.UP
    if direction == dir.RIGHT:
        return dir.LEFT
    if direction == dir.LEFT:
        return dir.RIGHT

#change coords to next node depending on dir
def goNext(i, j, direction):
    if direction == dir.UP:
       return i - 1, j
    elif direction == dir.DOWN:
       return i + 1, j
    elif direction == dir.RIGHT:
       return i, j + 1
    elif direction == dir.LEFT:
       return i, j - 1

#making maze
def makeMaze(height, width):
  
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
        if not invalidCoord(visited, i + 1, j, width, height):
            possibleDirs.append(dir.DOWN)
        if not invalidCoord(visited, i - 1, j, width, height):
            possibleDirs.append(dir.UP)
        if not invalidCoord(visited, i, j + 1, width, height):
            possibleDirs.append(dir.RIGHT)
        if not invalidCoord(visited, i, j - 1, width, height):
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