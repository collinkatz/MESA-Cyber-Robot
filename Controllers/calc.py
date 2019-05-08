# -*- coding: utf-8 -*-
"""
Method for state calculation

@author: Abhinav
"""
from __future__ import print_function
import collections

"""
Determines if we have been to the packet position before
Simple: chekcs the nodelist only

"""
def path_exists(packetPos, nodeDict):
    roundedPos = [int(packetPos[0]), int(packetPos[1])]
    if nodeDict.get(repr(roundedPos)) != None:
        return True
    else:
        return False

"""
Creates a grid from the Node dict data and runs breadth-first search
"""
def bfs(currentPos, packetPos, nodeDict):
    #Create the matrix and add values
    offset = 99
    mat = createMatrix()
    coordinates = []
    print(nodeDict)
    for index, i in nodeDict.iteritems():
        coor = eval(index)
        coordinates.append(coor)
    
    packet = [packetPos[0], packetPos[1]]
    curr_pos = [currentPos[0], currentPos[1]]
    
    print(coordinates)
    normalized_coors = transform_node_list(coordinates)
    mX = min(x[0] for x in coordinates)
    mY = min(x[1] for x in coordinates)
    packet[0] += (mX * -1)
    packet[1] += (mY * -1)
    curr_pos[0] += (mX * -1)
    curr_pos[1] += (mY * -1)
    
    
    print(normalized_coors)
    for i in normalized_coors:
        mat[offset - i[1]][i[0]] = moveEncoding.node #error is here with list index
    
   
    mat[int(offset - packet[1])][int(packet[0])] = moveEncoding.packet
    mat[offset - curr_pos[1]][curr_pos[0]] = moveEncoding.start
    
   
    for r in mat:
        for c in r:
            print(c, end=" ")
            
        print(" ")
    #Run the search algorithm
    
    path = searchForPath(mat, curr_pos, packet, nodeDict, mX, mY)
    
    if path is not None:
        return listToInstructions(path)
    return None

"""
Finds the shortest path and returns a list of coordinates
"""
def searchForPath(grid, s, p, nodeDict, xDiff, yDiff):
    start = (s[0], s[1])
    #packet = (p[0], p[1])
    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if grid[99 - y][x] == moveEncoding.packet:
            return path
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 < 100 and 0 <= y2 < 100 and grid[99 - y2][x2] != 0 and (x2, y2) not in seen and checkForWalls([x2,y2], [x,y], nodeDict, xDiff, yDiff) == True:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))

"""
Utility methods
"""

def checkForWalls(projected, current, nodeDict, xDiff, yDiff):
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
    print("Node position: " + repr(current))
    print("To " + repr(projected))
    
    if isinstance(data, str):
        if data == "Available" or data == "ParentDirection":
            print("the parent direction was available")
            possible = True
    elif isinstance(data, float):
        if data > 0:
            possible = True
        print("Steps: " + str(data))
    print("Value: ")
    print(data)
    return possible

def getNode(pos, nodeDict):
    if nodeDict.get(repr(pos)) != None:
        return nodeDict.get(repr(pos))
    else:
        return None

def transform_node_list(l):
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
    w, h = 100, 100
    mat = [[0 for x in range(w)] for y in range(h)]
    return mat

def listToInstructions(path):
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


