import logging
import os
import datetime
import math
import random
import time

# Setup a timestamped logfile for this run in the logs directory
#timestamp = datetime.datetime.now().strftime('%Y-%m-%d--%H-%M-%S')
#logfilename = 'D:\\Collin\\Documents\\Python\\MESA Cyber Robot\\Repository\\Logs\\robot_logfile_' + timestamp + '.txt'
#logging.basicConfig(filename=logfilename,level=logging.DEBUG)

# Seting up variables for absolute coordinate system || Robot will be keeping track of its own coordinates as well as coordinates of packets and viruses relative to the starting point/origin
class robotInheritence:
    CurrentFacingDirection = 1 # Direction is represented in a number from 1 to 4 || 1 is North, 2 is East, 3 is South, and 4 is West
    currentPosition = [0, 0]
    CurrentNode = None
    nodeDict = {}
    seekingdirection = 1

class node:

    def __init__(self, position, retreatNode, pathData):
        """ Create a new node at position """
        self.nodePosition = position # [x, y] will be a table
        self.numdeadpaths = 0
        self.retreatDirection = ""
        self.Paths = {"North": False, "South": False, "West": False, "East": False}

        for i in range(0, len(pathData)):
            if pathData[i] > 0:
                pathData[i] = "Available"
            elif pathData[i] == 0:
                pathData[i] = "NoPath"
                self.numdeadpaths = self.numdeadpaths + 1
            else:
                if i == 0:
                    self.retreatDirection = "North"
                elif i == 1:
                    self.retreatDirection = "South"
                elif i == 2:
                    self.retreatDirection = "West"
                elif i == 3:
                    self.retreatDirection = "East"
                pass # Keep pathdata as what it was when it was passed
            
        self.Paths["North"] = pathData[0]
        self.Paths["1"] = pathData[0]
        self.Paths["South"] = pathData[1]
        self.Paths["3"] = pathData[1]
        self.Paths["West"] = pathData[2]
        self.Paths["4"] = pathData[2]
        self.Paths["East"] = pathData[3]
        self.Paths["2"] = pathData[3]

        self.parentNode = None
        self.parentNode = retreatNode

def control_robot(robot):

    robotProperties = robotInheritence

    # Setting up movement functions
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
        robotProperties.currentPosition[1] = robotProperties.currentPosition[1] + 1 # Change the current Y position by 1

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
        robotProperties.currentPosition[1] = robotProperties.currentPosition[1] - 1 # Change the current Y position by -1

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
        robotProperties.currentPosition[0] = robotProperties.currentPosition[0] - 1 # Change the current X position by -1

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
        robotProperties.currentPosition[0] = robotProperties.currentPosition[0] + 1 # Change the current X position by 1

    def make_node(position, facingDirection, retreatNode, distancefromWalls):
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
        robotNode = node(position, retreatNode, [Northdistance, Southdistance, Westdistance, Eastdistance])
        robotProperties.nodeDict[repr(position)] = robotNode





    # Getting basic information about the current maze and where everything that involves the actual robot goes ##############################################################################################
    packets = robot.sense_packets()
    print(packets)

    #--Initilization of robot node system--#
    make_node(robotProperties.currentPosition, robotProperties.CurrentFacingDirection, robotProperties.CurrentNode, [robot.sense_steps(robot.SENSOR_FORWARD), robot.sense_steps(robot.SENSOR_RIGHT), robot.sense_steps(robot.SENSOR_LEFT)])
    robotProperties.CurrentNode = robotProperties.nodeDict[repr(robotProperties.currentPosition)]
    ###########

    #--Depth first search logic--#
    while True:
        print(len(robotProperties.nodeDict))
        if robotProperties.nodeDict.get(repr(robotProperties.currentPosition)) != None:
            print("node here")
            robotProperties.CurrentNode = robotProperties.nodeDict[repr(robotProperties.currentPosition)]
        else:
            print("Make node here" + repr(robotProperties.currentPosition))
            make_node(robotProperties.currentPosition, robotProperties.CurrentFacingDirection, robotProperties.CurrentNode, [robot.sense_steps(robot.SENSOR_FORWARD), robot.sense_steps(robot.SENSOR_RIGHT), robot.sense_steps(robot.SENSOR_LEFT)])
            robotProperties.CurrentNode = robotProperties.nodeDict[repr(robotProperties.currentPosition)]

        if robotProperties.CurrentNode.Paths[str(robotProperties.seekingdirection)] == "Available":
            print("My seeking direction is available" + str(robotProperties.seekingdirection))
            if robotProperties.seekingdirection == 1:
                step_north(1)
            elif robotProperties.seekingdirection == 3:
                step_south(1)
            elif robotProperties.seekingdirection == 4:
                step_west(1)
            elif robotProperties.seekingdirection == 2:
                step_east(1)
            robotProperties.CurrentNode.Paths[str(robotProperties.seekingdirection)] = "Choosen"
            robotProperties.CurrentNode.numdeadpaths = robotProperties.CurrentNode.numdeadpaths + 1
        else:
            if robotProperties.seekingdirection == 1:
                print("seek a different direction 1")
                robotProperties.seekingdirection = 2
            elif robotProperties.seekingdirection == 3:
                print("seek a different direction 3")
                robotProperties.seekingdirection = 4
            elif robotProperties.seekingdirection == 4:
                print("seek a different direction 4")
                robotProperties.seekingdirection = 1
            elif robotProperties.seekingdirection == 2:
                print("seek a different direction 2")
                robotProperties.seekingdirection = 3
            
            if robotProperties.CurrentNode.numdeadpaths >= 3:
                print("Dont do this")
                if robotProperties.CurrentNode.retreatDirection == "North":
                    step_north(1)
                elif robotProperties.CurrentNode.retreatDirection == "South":
                    step_south(1)
                elif robotProperties.CurrentNode.retreatDirection == "West":
                    step_west(1)
                elif robotProperties.CurrentNode.retreatDirection == "East":
                    step_east(1)
                #retreat

    ###########


#    while True:
#        randomDirection = random.randint(1, 4)
#        randomDistance = random.randint(1, 4)
#        if randomDirection == 1:
#            step_north(randomDistance)
#        elif randomDirection == 2:
#            step_east(randomDistance)
#        elif randomDirection == 3:
#            step_south(randomDistance)
#        elif randomDirection == 4:
#            step_west(randomDistance)
#        time.sleep(1)
#        print("Current Pos: " + str(robotProperties.currentPosition))
