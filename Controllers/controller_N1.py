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

def control_robot(robot):

    robotProperties = robotInheritence

    # Setting up movement functions
    def step_north():
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
        robot.step_forward() # Step forward after now facing North
        robotProperties.currentPosition[1] = robotProperties.currentPosition[1] + 1 # Change the current Y position by 1

    def step_south():
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
        robot.step_forward() # Step forward after now facing South
        robotProperties.currentPosition[1] = robotProperties.currentPosition[1] - 1 # Change the current Y position by -1

    def step_west():
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
        robot.step_forward() # Step forward after now facing West
        robotProperties.currentPosition[0] = robotProperties.currentPosition[0] - 1 # Change the current X position by -1

    def step_east():
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
        robot.step_forward() # Step forward after now facing East
        robotProperties.currentPosition[0] = robotProperties.currentPosition[0] + 1 # Change the current X position by 1

    # Getting basic information about the current maze
    packets = robot.sense_packets()
    print(packets)
    while True:
        randomDirection = random.randint(1, 4)
        if randomDirection == 1:
            step_north()
        elif randomDirection == 2:
            step_east()
        elif randomDirection == 3:
            step_south()
        elif randomDirection == 4:
            step_west()
        time.sleep(1)
        print("Current Pos: " + str(robotProperties.currentPosition))