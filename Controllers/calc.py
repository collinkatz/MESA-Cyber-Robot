
###############################################################################
# Team Name:      Viking 1 Veterans                                           #
#                                                                             #
# Contributors:   Collin Katz, Ayana Monroe, Abhinav Modugula, and David Huh  #
#                                                                             #
# Email:          collin.katz@gmail.com                                       #
# School:         Long Reach High School                                      #
# Date Created:   Wednesday February 16, 2019, 10:18 AM                       #
###############################################################################

"""
Pathing Methods
"""

import collections

def path_exists(packetPos, nodeDict):
    """
     Function:       path_exists

     Description:    Determines if it is possible to calculate a path
                     to the next target location
            
     Parameters:     packetPos    -   the target position
                     nodeDict     -   a dictionary of node positions and node objects

     Returns:        True or False: whether a path can be calulated or not
    """
    roundedPos = [int(packetPos[0]), int(packetPos[1])]
    if nodeDict.get(repr(roundedPos)) != None:
        return True
    else:
        return False

def bfs(currentPos, packetPos, nodeDict):
    """
     Function:       bfs

     Description:    Uses the node information to contruct a partial grid
                     representing the maze and then runs breadth-first search
                     on that grid to find the exact path to the target packet
                     or virus location
            
     Parameters:     currentPos   -   the robot's current location
                     packetPos    -   the target position
                     nodeDict     -   a dictionary of node positions and node objects

     Returns:        A path that the robot can take to the next target location
    """
    #Creates the matrix
    offset = 99
    mat = createMatrix()
    coordinates = []
    
    for index, i in nodeDict.iteritems():
        coor = eval(index)
        coordinates.append(coor)
    
    packet = [packetPos[0], packetPos[1]]
    curr_pos = [currentPos[0], currentPos[1]]
    
    #Normalizes all the coordinates to positive values
    #so that they can be added to the matrix
    normalized_coors = transform_node_list(coordinates)
    mX = min(x[0] for x in coordinates)
    mY = min(x[1] for x in coordinates)
    packet[0] += (mX * -1)
    packet[1] += (mY * -1)
    curr_pos[0] += (mX * -1)
    curr_pos[1] += (mY * -1)
    
    #Adds the node, packet, and current position coordinates to the matrix
    for i in normalized_coors:
        mat[offset - i[1]][i[0]] = moveEncoding.node #error is here with list index
    mat[int(offset - packet[1])][int(packet[0])] = moveEncoding.packet
    mat[offset - curr_pos[1]][curr_pos[0]] = moveEncoding.start
    
   
    
    #Runs the search algorithm
    path = searchForPath(mat, curr_pos, nodeDict, mX, mY)
    
    if path is not None:
        return listToInstructions(path)
    return None


def searchForPath(grid, startCoor, nodeDict, xDiff, yDiff):
    """
     Function:       searchForPath

     Description:    Uses the breadth-first search algorithm to find a path
                     from start to the target location
            
     Parameters:     grid        - a 2D python matrix that represents the information
                                   we know about the maze
                     startCoor   - the positon that the search on the maze should start from 
                     nodeDict    - a dictionary of node positions and node objects
                     xDiff       - a constant to convert matrix coordinates to actual maze positions
                     yDiff       - a constant to convert matrix coordinates to actual maze positions

     Returns:        True or False: whether a path can be calulated or not
    """
    start = (startCoor[0], startCoor[1])
    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if grid[99 - y][x] == moveEncoding.packet: #destination reached
            return path
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 < 100 and 0 <= y2 < 100 and grid[99 - y2][x2] != 0 and (x2, y2) not in seen and checkForWalls([x2,y2], [x,y], nodeDict, xDiff, yDiff) == True:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))

"""
Utility Methods
"""

def checkForWalls(projected, current, nodeDict, xDiff, yDiff):
    """
     Function:       checkForWalls

     Description:    makes sure that a wall is not blocking the path
                     between two maze locations
            
     Parameters:     projected   -   the robot's current location
                     current     -   the target position
                     nodeDict    -   a dictionary of node positions and node objects
                     xDiff       -   a constant to convert matrix coordinates to actual maze positions
                     yDiff       -   a constant to convert matrix coordinates to actual maze positions

     Returns:        True or False: whether or not there is a wall inbetween two node positions
    """
    possible = False
    projectedPos = [0, 0]
    currentPos = [0, 0]
    projectedPos[0] = projected[0] + xDiff
    projectedPos[1] = projected[1] + yDiff
    currentPos[0] = current[0] + xDiff
    currentPos[1] = current[1] + yDiff
    
    node = getNode(currentPos, nodeDict)
    data = None
    if projectedPos[0] == currentPos[0] + 1 and projectedPos[1] == currentPos[1]:
        data = node.paths["East"]
    elif projectedPos[0] == currentPos[0] - 1 and projectedPos[1] == currentPos[1]:
        data = node.paths["West"]
    elif projectedPos[0] == currentPos[0] and projectedPos[1] == currentPos[1] + 1:
        data = node.paths["North"]
    elif projectedPos[0] == currentPos[0] and projectedPos[1] == currentPos[1] - 1:
        data = node.paths["South"]
    #DIAGNOSTIC
    
    
    if isinstance(data, str):
        if data == "Available" or data == "ParentDirection":
            
            possible = True
    elif isinstance(data, float):
        if data > 0:
            possible = True
        
    
    return possible

def getNode(pos, nodeDict):
    """
    Returns a node object that is at a certain pos,
    or None if there is no node there
    
    """
    if nodeDict.get(repr(pos)) != None:
        return nodeDict.get(repr(pos))
    else:
        return None

def transform_node_list(l):
    """
    Shifts a list of coordinates so that there are
    no negative values
    """
    mX = min(x[0] for x in l)
    mY = min(x[1] for x in l)
    ln = []
    for x in l:
        coor = [0, 0]
        coor[0] = x[0] + (mX * -1)
        coor[1] = x[1] + (mY * -1)
        ln.append(coor)
    return ln

class moveEncoding:
    """
    A class to represent different constants that are
    referred to throghout the path calculation algorithm
    """
    up = "up"
    right = "right"
    left = "left"
    down = "down"
    rowNum = [0, 1, 0, -1] #offsets up, right, down, left by changing the x and y values
    colNum = [1, 0, -1, 0]
    start = 1
    packet = 3
    node = 2
    inferredNode = 4
    empty = 0
    
def createMatrix():
    """
    Creates a 100 by 100 2D matrix of zeroes
    """
    w, h = 100, 100
    mat = [[0 for x in range(w)] for y in range(h)]
    return mat

def listToInstructions(path):
    """
    Converts a list of coordinates representing a path into
    a list of instructions that the robot can follow
    """
    j = []
    for index, coor in enumerate(path):
        if (index == len(path) - 1):
            break
        x_orig = coor[0]
        y_orig = coor[1]
        x_fin = path[index+1][0]
        y_fin = path[index+1][1]
        if (x_orig == x_fin):
            if (y_orig < y_fin):
                j.append(moveEncoding.up)
            elif (y_orig > y_fin):
                j.append(moveEncoding.down)
        elif (y_orig == y_fin):
            if (x_orig > x_fin):
                j.append(moveEncoding.left)
            elif (x_orig < x_fin):
                j.append(moveEncoding.right)
    return j


