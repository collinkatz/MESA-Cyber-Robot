import logging
import os
import datetime
import math

# Setup a timestamped logfile for this run in the logs directory
timestamp = datetime.datetime.now().strftime('%Y-%m-%d--%H-%M-%S')
#logfilename = 'D:\\Collin\\Documents\\Python\\MESA Cyber Robot\\Repository\\Logs\\robot_logfile_' + timestamp + '.txt'
#logging.basicConfig(filename=logfilename,level=logging.DEBUG)

# Seting up variables for absolute coordinate system || Robot will be keeping track of its own coordinates as well as coordinates of packets and viruses in relation to the starting point (origin)
currentXposition = 0
currentYposition = 0
CurrentFacingDirection = 1 # Direction is represented in a number from 1 to 4 || 1 is North, 2 is East, 3 is South, and 4 is West

# Setting up movement functions
def step_north(robot):
    global currentYposition
    if CurrentFacingDirection == 3: # if the direction it is facing is south
        robot.turn_left()
        robot.turn_left()
    elif CurrentFacingDirection == 4: # if the direction it is facing is West
        robot.turn_right()
    elif CurrentFacingDirection == 2:
        robot.turn_left()
    elif CurrentFacingDirection == 1: # if the direction it is facing is North
        # Do nothing
        pass

    robot.step_forward() # Step forward after now facing North
    currentYposition = currentYposition + 1 # Change the current Y position by 1

def control_robot(robot):
    # Getting basic information about the current maze
    packets = robot.sense_packets()
    logging.info(packets)

class Dog:

    def turn_left(self):
        print( "To Da Left" )    
    
    def turn_right(self):
        print( "To Da Right" )
    
    def step_forward(self):
        print( "Steppity Step")

if __name__ == "__main__":
    dog = Dog()
    otherDog = Dog()
    step_north(dog)

