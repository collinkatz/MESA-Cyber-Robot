import logging
import datetime
import math
import random
import time

#--Depricated--#
# Setup a timestamped logfile for this run in the logs directory
#timestamp = datetime.datetime.now().strftime('%Y-%m-%d--%H-%M-%S')
#logfilename = 'D:\\Collin\\Documents\\Python\\MESA Cyber Robot\\Repository\\Logs\\robot_logfile_' + timestamp + '.txt'
#logging.basicConfig(filename=logfilename,level=logging.DEBUG)
###########

# Seting up variables for absolute coordinate system || Robot will be keeping track of its own coordinates as well as coordinates of packets and viruses relative to the starting point/origin
class robotInheritence: # a class used once which defines the properties that the robot will inherit at the begining of the program
    CurrentFacingDirection = 1 # Direction is represented in a number from 1 to 4 || 1 is North, 2 is East, 3 is South, and 4 is West
    currentPosition = [0, 0] # The robots position represented as an Array with index 0 as the X value and index 1 as the Y value
    CurrentNode = None # The node instance that the robot currently has the same position as
    nodeDict = {} # A dictionary of node instances with each node being indexed at a position represented as [X, Y]

class node:

    def __init__(self, position, retreatNode, pathData): # Called when instance of packet created
        """ Create a new node at position """
        self.nodePosition = position # [x, y] will be a table
        self.retreatDirection = "" # The direction that the robot will retreat away from the node
        self.numdeadpaths = 0 # Number of unavailable directions to move at a node ie. if node in open = 0 if node surrounded by walls = 4
        self.numlivepaths = 0 # Number of available directions to move at a node
        self.NumberofAdjacentExistingNodes = 0 # Number of nodes that currently exist adjacently from a node
        self.Paths = {"North": False, "South": False, "West": False, "East": False} # The status in all cardinal directions of potential movements
        self.AdjacentNodes = {"North": [self.nodePosition[0], self.nodePosition[1] + 1], "South": [self.nodePosition[0], self.nodePosition[1] - 1], "West": [self.nodePosition[0] - 1, self.nodePosition[1]], "East": [self.nodePosition[0] + 1, self.nodePosition[1]]} # The positions of all nodes adjacent of this node instance

        #--This sets up all values in self.Paths--#
        for i in range(0, len(pathData)):
            if isinstance(pathData[i], str):
                print("The passed value is Parent Direction")
                self.numlivepaths = self.numlivepaths + 1
                if i == 0:
                    self.retreatDirection = "North"
                elif i == 1:
                    self.retreatDirection = "South"
                elif i == 2:
                    self.retreatDirection = "West"
                elif i == 3:
                    self.retreatDirection = "East"
            elif isinstance(pathData[i], float):
                if pathData[i] > 0:
                    print(str(i) + "\t" + str(pathData[i]))
                    pathData[i] = "Available"
                    self.numlivepaths = self.numlivepaths + 1
                elif pathData[i] == 0:
                    print(str(i) + "\t" + str(pathData[i]))
                    pathData[i] = "NoPath"
                    self.numdeadpaths = self.numdeadpaths + 1
                else:
                    print("node: why so negative?")
            else:
                print("Look man, I don't know who you are or how you got here, but you need to leave")
            
        self.Paths["North"] = pathData[0]
        self.Paths["South"] = pathData[1]
        self.Paths["West"] = pathData[2]
        self.Paths["East"] = pathData[3]

        self.parentNode = retreatNode

def control_robot(robot):

    robotProperties = robotInheritence

    #--Setting up movement functions--# A movement function will turn the robot towards the cardinal direction and make it step a specified distance in that direction

    def step_north(distance):
        if robotProperties.CurrentFacingDirection == 3: # if the direction it is facing is South
            robot.turn_left()
            robot.turn_left()
        elif robotProperties.CurrentFacingDirection == 4: # if the direction it is facing is West
            robot.turn_right()
        elif robotProperties.CurrentFacingDirection == 2: # if the direction it is facing is East
            robot.turn_left()
        elif robotProperties.CurrentFacingDirection == 1: # if the direction it is facing is North
            #Do nothing
            pass
        robot.step_forward(distance) # Step forward after now facing North
        robotProperties.currentPosition[1] = robotProperties.currentPosition[1] + distance # Change the current Y position by 1
        robotProperties.CurrentFacingDirection = 1

    def step_south(distance):
        if robotProperties.CurrentFacingDirection == 1: # if the direction it is facing is North
            robot.turn_left()
            robot.turn_left()
        elif robotProperties.CurrentFacingDirection == 4: # if the direction it is facing is West
            robot.turn_left()
        elif robotProperties.CurrentFacingDirection == 2: # if the direction it is facing is East
            robot.turn_right()
        elif robotProperties.CurrentFacingDirection == 3: # if the direction it is facing is South
            #Do nothing
            pass
        robot.step_forward(distance) # Step forward after now facing South
        robotProperties.currentPosition[1] = robotProperties.currentPosition[1] - distance # Change the current Y position by -1
        robotProperties.CurrentFacingDirection = 3

    def step_west(distance):
        if robotProperties.CurrentFacingDirection == 1: # if the direction it is facing is North
            robot.turn_left()
        elif robotProperties.CurrentFacingDirection == 3: # if the direction it is facing is South
            robot.turn_right()
        elif robotProperties.CurrentFacingDirection == 2: # if the direction it is facing is East
            robot.turn_left()
            robot.turn_left()
        elif robotProperties.CurrentFacingDirection == 4: # if the direction it is facing is West
            #Do nothing
            pass
        robot.step_forward(distance) # Step forward after now facing West
        robotProperties.currentPosition[0] = robotProperties.currentPosition[0] - distance # Change the current X position by -1
        robotProperties.CurrentFacingDirection = 4

    def step_east(distance):
        if robotProperties.CurrentFacingDirection == 1: # if the direction it is facing is North
            robot.turn_right()
        elif robotProperties.CurrentFacingDirection == 3: # if the direction it is facing is South
            robot.turn_left()
        elif robotProperties.CurrentFacingDirection == 4: # if the direction it is facing is West
            robot.turn_left()
            robot.turn_left()
        elif robotProperties.CurrentFacingDirection == 2: # if the direction it is facing is East
            #Do nothing
            pass
        robot.step_forward(distance) # Step forward after now facing East
        robotProperties.currentPosition[0] = robotProperties.currentPosition[0] + distance # Change the current X position by 1
        robotProperties.CurrentFacingDirection = 2

    ###########

    def make_node(position, facingDirection, retreatNode, distancefromWalls): # Function that decides how to create a node based on info it is given
        if facingDirection == 1: # if the direction it is facing is North
            Northdistance = distancefromWalls[0]
            Southdistance = "ParentDirection"
            Westdistance = distancefromWalls[2]
            Eastdistance = distancefromWalls[1]
        elif facingDirection == 3: # if the direction it is facing is South
            Northdistance = "ParentDirection"
            Southdistance = distancefromWalls[0]
            Westdistance = distancefromWalls[1]
            Eastdistance = distancefromWalls[2]
        elif facingDirection == 4: # if the direction it is facing is West
            Northdistance = distancefromWalls[1]
            Southdistance = distancefromWalls[2]
            Westdistance = distancefromWalls[0]
            Eastdistance = "ParentDirection"
        elif facingDirection == 2: # if the direction it is facing is East
            Northdistance = distancefromWalls[2]
            Southdistance = distancefromWalls[1]
            Westdistance = "ParentDirection"
            Eastdistance = distancefromWalls[0]
        robotNode = node(position, retreatNode, [Northdistance, Southdistance, Westdistance, Eastdistance]) # Creating a node using the filtered information
        robotProperties.nodeDict[repr(position)] = robotNode # Adding the new node to the robots node dictionary

    def Retreat(): # Moves robot back to the previous node
        if robotProperties.CurrentNode.retreatDirection == "North":
            print("Retreating North")
            step_north(1)
        elif robotProperties.CurrentNode.retreatDirection == "South":
            print("Retreating South")
            step_south(1)
        elif robotProperties.CurrentNode.retreatDirection == "West":
            print("Retreating West")
            step_west(1)
        elif robotProperties.CurrentNode.retreatDirection == "East":
            print("Retreating East")
            step_east(1)

    # Getting basic information about the current maze and where everything that involves the actual robot goes ##############################################################################################
    packets = robot.sense_packets()
    print(packets)

    #--Initilization of robot node system--#
    make_node(robotProperties.currentPosition, robotProperties.CurrentFacingDirection, robotProperties.CurrentNode, [robot.sense_steps(robot.SENSOR_FORWARD), robot.sense_steps(robot.SENSOR_RIGHT), robot.sense_steps(robot.SENSOR_LEFT)])
    robotProperties.CurrentNode = robotProperties.nodeDict[repr(robotProperties.currentPosition)]
    ###########

    #--Real depth first search--#

    while True:
        print("#####################")

        #--Decides whether or not to make a node in the current location and update the robots current node--#
        if robotProperties.nodeDict.get(repr(robotProperties.currentPosition)) != None:
            print("Already a node here: " + repr(robotProperties.currentPosition))
            robotProperties.CurrentNode = robotProperties.nodeDict[repr(robotProperties.currentPosition)]
        else:
            print("Make node here: " + repr(robotProperties.currentPosition))
            make_node(robotProperties.currentPosition, robotProperties.CurrentFacingDirection, robotProperties.CurrentNode, [robot.sense_steps(robot.SENSOR_FORWARD), robot.sense_steps(robot.SENSOR_RIGHT), robot.sense_steps(robot.SENSOR_LEFT)])
            robotProperties.CurrentNode = robotProperties.nodeDict[repr(robotProperties.currentPosition)]
        ###########

        robotProperties.CurrentNode.NumberofAdjacentExistingNodes = 0 # Updates the number of adjacent nodes the current node has each time the robot enters a node

        #--This decides what direction the robot will step in to explore a position without a node--#
        for i in robotProperties.CurrentNode.AdjacentNodes:
            print("i = " + str(i))
            if robotProperties.nodeDict.get(repr(robotProperties.CurrentNode.AdjacentNodes[i])) == None: # If the robot does not find a node at an adjacent position
                if i == "North":
                    if robotProperties.CurrentNode.Paths[i] == "Available":
                        step_north(1)
                        print("Step North")
                        break
                    else:
                        pass
                elif i == "South":
                    if robotProperties.CurrentNode.Paths[i] == "Available":
                        step_south(1)
                        print("Step South")
                        break
                    else:
                        pass
                elif i == "West":
                    if robotProperties.CurrentNode.Paths[i] == "Available":
                        step_west(1)
                        print("Step West")
                        break
                    else:
                        pass
                elif i == "East":
                    if robotProperties.CurrentNode.Paths[i] == "Available":
                        step_east(1)
                        print("Step East")
                        break
                    else:
                        pass
            elif robotProperties.nodeDict.get(repr(robotProperties.CurrentNode.AdjacentNodes[i])) != None and (robotProperties.CurrentNode.Paths[i] == "Available" or robotProperties.CurrentNode.Paths[i] == "ParentDirection"):
                robotProperties.CurrentNode.NumberofAdjacentExistingNodes = robotProperties.CurrentNode.NumberofAdjacentExistingNodes + 1
        ###########

        print("Adjacent nodes to live paths: " + str(robotProperties.CurrentNode.NumberofAdjacentExistingNodes) + "\t" + str(robotProperties.CurrentNode.numlivepaths))
        
        if robotProperties.CurrentNode.NumberofAdjacentExistingNodes == robotProperties.CurrentNode.numlivepaths: # Conditions for retreating
            print("Trying retreat: " + robotProperties.CurrentNode.retreatDirection)
            Retreat()    
        

    ###########