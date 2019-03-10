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

class node:

    def __init__(self, position, pathData):
        """ Create a new node at position """
        self.nodePosition = position # [x, y] will be a table

        self.Paths = {"North": False, "South": False, "West": False, "East": False}
        for i in range(0, len(pathData)):
            if pathData[i] > 0:
                pathData[i] = "Available"
            elif pathData[i] == 0:
                pathData[i] = "NoPath"
            else:
                pass # Keep pathdata as what it was when it was passed
        self.Paths["North"] = pathData[0]
        self.Paths["South"] = pathData[1]
        self.Paths["West"] = pathData[2]
        self.Paths["East"] = pathData[3]
        
        self.parentNode = None

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

    def make_node(position, facingDirection, distancefromWalls):
        if facingDirection == 1: # if the direction it is facing is North
            Northdistance = distancefromWalls[0]
            Southdistance = "ParentDirection"
            Westdistance = distancefromWalls[2]
            Eastdistance = distancefromWalls[1]
        elif facingDirection == 3: # if the direction it is facing is South
            pass
        elif facingDirection == 4: # if the direction it is facing is West
            pass
        elif facingDirection == 2: # if the direction it is facing is East
            pass
        robotNode = node(position, [Northdistance, Southdistance, Westdistance, Eastdistance])
        robotProperties.nodeDict[repr(position)] = robotNode





    # Getting basic information about the current maze and where everything that involves the actual robot goes ##############################################################################################

    packets = robot.sense_packets()
    print(packets)
    
    make_node(robotProperties.currentPosition, robotProperties.CurrentFacingDirection, [robot.sense_steps(robot.SENSOR_FORWARD), robot.sense_steps(robot.SENSOR_RIGHT), robot.sense_steps(robot.SENSOR_LEFT)])
    print( robotProperties.nodeDict[repr([0,0])].Paths["West"] )
    step_north(1)
    



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
