###############################################################################
# Team Name:      Viking 1 Veterans                                           #
#                                                                             #
# Contributors:   Collin Katz, Ayana Monroe, Abhinav Modugula, and David Huh  #
#                                                                             #
# Email:          collin.katz@gmail.com, ayana.r.monroe@gmail.com,            #
#                 abhimodugula@gmail.com, davidjo.huh@gmail.com               #
# School:         Long Reach High School                                      #
# Date Created:   Wednesday February 16, 2019, 10:18 AM                       #
###############################################################################

import math
import time

class robotInheritence:
    """ Class:          robotInheritence
        Description:    an object that contains information about the current
                        state of the robot.
        Attributes:     currentPacketNumber -   the index in the list of packets which contains the packet position
                                                that the robot is currently trying to reach.
                        currentFacingDirection - the direction that the robot is currently facing represented as a
                                                number from 1 to 4. 1 = North, 2 = East, 3 = South, and 4 = West
                        currentPosition     -   the position on a grid of the robot relative to the starting point
                                                represented as an array in the form [X, Y].
                        currentNode         -   the node instance that the robot currently shares the same position
                                                as.
                        nodeDict            -   a dictionary that contains every node that has been initialized.
                                                Each node is indexed in nodeDict at its position as an array
                                                represented as a string in the form "[X, Y]".
    """
    currentPacketNumber = 0
    currentFacingDirection = 1
    currentPosition = [0, 0]
    currentNode = None
    nodeDict = {}

class node:
    """ Class:          node
        Description:    an object that represents the position on the grid as a node in a graph
                        that has information about the current position and its surroundings, as
                        well as information about the parent
        
        Attributes:     nodePosition    -   current node position relative to a grid that has the
                                            origin set to the starting position of the robot.  It
                                            is an array of the form [x,y]
                        retreatDirection -  a string representing the direction the robot will step
                                            in when retreating out of a dead end. Either "North",
                                            "South", "East", or "West"
                        numDeadpaths    -   the number of directions from a node that are blocked by
                                            an adjacent wall.
                        numLivepaths    -   the number of directions from a node that are not blocked
                                            by an adjacent wall.
                        numberOfAdjacentExistingNodes - the number of nodes that exist in positions
                                            adjacent to the position of the current node and also have
                                            an unblocked path from this node to them.
                        paths           -   a dictionary containing the current status of all paths in
                                            each direction away from this node indexed at the direction
                                            of the path. Each index will have a value of "Available" if
                                            there is no wall in that direction, "NoPath" if there is a
                                            wall in that direction, or "ParentDirection" if the path in
                                            that direction leads to the node the robot was previously on
                                            when this node was initialized.
                        adjacentNodes   -   Positions of possible nodes in every direction from this
                                            node indexed at the direction they may exist in from this
                                            node.
                        inCurrentPath   -   a value of True indicates that this node is currently part
                                            of the path to the packet that the robot is currently
                                            seeking.
                        ParentNode      -   node object that the robot was previously on when this node
                                            was initialized.
    """

    def __init__(self, position, retreatNode, pathData): 
        """ Function:       __init__
            Description:    initializes a node object based on information on the current position
                            and the parent node's information
            
            Parameters:     self        -   object reference
                            position    -   position passed from control_robot, it's an array of x and y
                                            position values relative to a grid whose origin is the start
                                            position of the robot
                            retreatNode -   node object that the robot was previously on
                            pathData    -   array of distances to the closest wall in every cardinal direction 
                                            except for the direction the robot came from, which has the value
                                            of "parent direction"
            Returns:        An initialized node object
        """
        self.nodePosition = position
        self.retreatDirection = ""
        self.numDeadpaths = 0
        self.numLivepaths = 0
        self.numberOfAdjacentExistingNodes = 0
        self.paths = {"North": False, "South": False, "West": False, "East": False}
        self.adjacentNodes = {"North": [self.nodePosition[0], self.nodePosition[1] + 1], "South": [self.nodePosition[0], self.nodePosition[1] - 1], "West": [self.nodePosition[0] - 1, self.nodePosition[1]], "East": [self.nodePosition[0] + 1, self.nodePosition[1]]}
        self.inCurrentPath = True

        #--This sets up all values in self.paths based on pathData--#
        for i in range(0, len(pathData)):
            if isinstance(pathData[i], str):
                print "The passed value is a string"
                self.numLivepaths += 1
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
                    print str(i) + "\t" + str(pathData[i])
                    pathData[i] = "Available"
                    self.numLivepaths += 1
                elif pathData[i] == 0:
                    print str(i) + "\t" + str(pathData[i])
                    pathData[i] = "NoPath"
                    self.numDeadpaths += 1
                else:
                    print "node: why so negative?"
            else:
                print "Look man, I don't know who you are or how you got here, but you need to leave"
        ###########

        self.paths["North"] = pathData[0]
        self.paths["South"] = pathData[1]
        self.paths["West"] = pathData[2]
        self.paths["East"] = pathData[3]
        self.parentNode = retreatNode

def control_robot(robot):

    robotProperties = robotInheritence

    #--Setting up movement functions--# A movement function will turn the robot towards the cardinal direction and make it step a specified distance in that direction
    def step_north(distance):
        """ Function:       step_north
            Description:    Moves the robot a specified distance North, changes the robots
                            current position to its new position relative to the origin after
                            stepping North, and changes currentFacingDirection to 1.
            
            Parameters:     distance    -   the distance to move the robot
            Returns:        A robot moved a specified distance North
        """
        #--Rotates the robot to face North based on currentFacingDirection--#
        if robotProperties.currentFacingDirection == 3: # if South
            robot.turn_left()
            robot.turn_left()
        elif robotProperties.currentFacingDirection == 4: # if West
            robot.turn_right()
        elif robotProperties.currentFacingDirection == 2: # if East
            robot.turn_left()
        elif robotProperties.currentFacingDirection == 1: # if North
            pass
        ###########
        robot.step_forward(distance)
        robotProperties.currentPosition[1] += distance
        robotProperties.currentFacingDirection = 1

    def step_south(distance):
        """ Function:       step_south
            Description:    Moves the robot a specified distance South, changes the robots
                            current position to its new position relative to the origin after
                            stepping South, and changes currentFacingDirection to 3.
            
            Parameters:     distance    -   the distance to move the robot
            Returns:        A robot moved a specified distance South
        """
        #--Rotates the robot to face South based on currentFacingDirection--#
        if robotProperties.currentFacingDirection == 1: # if North
            robot.turn_left()
            robot.turn_left()
        elif robotProperties.currentFacingDirection == 4: # if West
            robot.turn_left()
        elif robotProperties.currentFacingDirection == 2: # if East
            robot.turn_right()
        elif robotProperties.currentFacingDirection == 3: # if South
            pass
        ###########
        robot.step_forward(distance)
        robotProperties.currentPosition[1] -= distance
        robotProperties.currentFacingDirection = 3

    def step_west(distance):
        """ Function:       step_west
            Description:    Moves the robot a specified distance West, changes the robots
                            current position to its new position relative to the origin after
                            stepping West, and changes currentFacingDirection to 4.
            
            Parameters:     distance    -   the distance to move the robot
            Returns:        A robot moved a specified distance West
        """
        #--Rotates the robot to face West based on currentFacingDirection--#
        if robotProperties.currentFacingDirection == 1: # if North
            robot.turn_left()
        elif robotProperties.currentFacingDirection == 3: # if South
            robot.turn_right()
        elif robotProperties.currentFacingDirection == 2: # if East
            robot.turn_left()
            robot.turn_left()
        elif robotProperties.currentFacingDirection == 4: # if West
            pass
        ###########
        robot.step_forward(distance)
        robotProperties.currentPosition[0] -= distance
        robotProperties.currentFacingDirection = 4

    def step_east(distance):
        """ Function:       step_east
            Description:    Moves the robot a specified distance East, changes the robots
                            current position to its new position relative to the origin after
                            stepping East, and changes currentFacingDirection to 2.
            
            Parameters:     distance    -   the distance to move the robot
            Returns:        A robot moved a specified distance East
        """
        #--Rotates the robot to face East based on currentFacingDirection--#
        if robotProperties.currentFacingDirection == 1: # if North
            robot.turn_right()
        elif robotProperties.currentFacingDirection == 3: # if South
            robot.turn_left()
        elif robotProperties.currentFacingDirection == 4: # if West
            robot.turn_left()
            robot.turn_left()
        elif robotProperties.currentFacingDirection == 2: # if East
            pass
        ###########
        robot.step_forward(distance)
        robotProperties.currentPosition[0] += distance
        robotProperties.currentFacingDirection = 2
    ###########

    def make_node(position, facingDirection, retreatNode, distancefromWalls): # Function that decides how to create a node based on info it is given
        """ Function:       make_node
            Description:    Creates a node instance and passes values to __init__ function
                            of node classabout the nodes surroundings and its positions so 
                            the node can be initialized.
            
            Parameters:     position            -   the position to be passed to the node to initialize the node
                                                    in.
                            facingDirection     -   the direction the robot is currently facing to be used to
                                                    decide which direction will be passed as parent direction
                                                    and which values in distancefromWalls correspond to which
                                                    direction.
                            retreatNode         -   the node that the robot was previously on.
                            distancefromWalls   -   an array that contains the distances from the walls on the left,
                                                    right, and front of the robot. This is used to decide which
                                                    distances correspond to which cardinal directions so they can
                                                    be passed to the __init__ function of the node class
            Returns:        An instance of a node indexed at its position in robotProperties.nodeDict
        """
        if facingDirection == 1: # if North
            Northdistance = distancefromWalls[0]
            Southdistance = "ParentDirection"
            Westdistance = distancefromWalls[2]
            Eastdistance = distancefromWalls[1]
        elif facingDirection == 3: # if South
            Northdistance = "ParentDirection"
            Southdistance = distancefromWalls[0]
            Westdistance = distancefromWalls[1]
            Eastdistance = distancefromWalls[2]
        elif facingDirection == 4: # if West
            Northdistance = distancefromWalls[1]
            Southdistance = distancefromWalls[2]
            Westdistance = distancefromWalls[0]
            Eastdistance = "ParentDirection"
        elif facingDirection == 2: # if East
            Northdistance = distancefromWalls[2]
            Southdistance = distancefromWalls[1]
            Westdistance = "ParentDirection"
            Eastdistance = distancefromWalls[0]
        robotNode = node(position, retreatNode, [Northdistance, Southdistance, Westdistance, Eastdistance]) # Creating a node using the filtered information
        robotProperties.nodeDict[repr(position)] = robotNode # Adding the new node to the robots node dictionary
    
    def update_node(position, facingDirection):
        """ Function:       update_node
            Description:    changes the parentDirection property of nodes that
                            have been used in a previous path in order to create
                            a new path with its own chain of parent nodes.
            
            Parameters:     position            -   the position of the node to be updated.
                            facingDirection     -   the direction the robot is currently facing to be used to
                                                    decide which direction will be updated as the new parent direction
                                                    for the node and which old parent direction to set as "Available".
            Returns:        An instance of a node indexed at its position in robotProperties.nodeDict
        """
        if facingDirection == 1: # if North
            robotProperties.currentNode.paths["South"] = "ParentDirection"
            robotProperties.currentNode.retreatDirection = "South"
        elif facingDirection == 3: # if South
            robotProperties.currentNode.paths["North"] = "ParentDirection"
            robotProperties.currentNode.retreatDirection = "North"
        elif facingDirection == 4: # if West
            robotProperties.currentNode.paths["East"] = "ParentDirection"
            robotProperties.currentNode.retreatDirection = "East"
        elif facingDirection == 2: # if East
            robotProperties.currentNode.paths["West"] = "ParentDirection"
            robotProperties.currentNode.retreatDirection = "West"
        robotProperties.currentNode.paths[robotProperties.currentNode.retreatDirection] = "Available"


    def Retreat(): # Moves robot back to the previous node
        """ Function:       Retreat
            Description:    Makes the robot step in the retreat direction
                            of a node in order to get out of a dead end or already
                            explored area.
            
            Parameters:     None
            Returns:        A robot moved in the retreat direction of the node it was previously
                            on.
        """
        if robotProperties.currentNode.retreatDirection == "North":
            print "Retreating North"
            step_north(1)
        elif robotProperties.currentNode.retreatDirection == "South":
            print "Retreating South"
            step_south(1)
        elif robotProperties.currentNode.retreatDirection == "West":
            print "Retreating West"
            step_west(1)
        elif robotProperties.currentNode.retreatDirection == "East":
            print "Retreating East"
            step_east(1)
    
    def ComputeCost(NodePosition, PacketPosition):
        """ Function:       ComputeCost
            Description:    Finds the linear distance between the position of
                            the packet the robot is currently seeking and the
                            position of the node which the robot is currently on.
                            The cost is used to prioritize stepping towards the packet.
            
            Parameters:     NodePosition    -   the position of the node the robot is on
                            PacketPosition  -   the position of the packet the robot is seeking
            Returns:        the distance between
        """
        d = math.sqrt( ( math.pow(PacketPosition[0]-NodePosition[0], 2) )+( math.pow(PacketPosition[1]-NodePosition[1], 2) ) ) # Linear distance equation
        return d

    # Getting basic information about the current maze and where everything that involves the actual robot goes ############################################################################################## This is where the fun begins
    packets = robot.sense_packets()
    robotProperties.currentPacketNumber = 1
    print packets

    #--Initilization of robot node system--# Makes first node and sets up origin point
    make_node(robotProperties.currentPosition, robotProperties.currentFacingDirection, robotProperties.currentNode, [robot.sense_steps(robot.SENSOR_FORWARD), robot.sense_steps(robot.SENSOR_RIGHT), robot.sense_steps(robot.SENSOR_LEFT)])
    robotProperties.currentNode = robotProperties.nodeDict[repr(robotProperties.currentPosition)]
    robot.turn_right()
    SouthWall = robot.sense_steps(robot.SENSOR_RIGHT)
    robot.turn_left()
    if SouthWall == 0:
        robotProperties.currentNode.paths["South"] = "NoPath"
    elif SouthWall > 0:
        robotProperties.currentNode.paths["South"] = "Available"
    ###########

    #--A* search--#

    while True: # Makes one cycle for every time the robot moves to a different position
        print "#--New Move--####################"
        print "Current packet number: " + str(robotProperties.currentPacketNumber)
        if robotProperties.currentPosition == packets[robotProperties.currentPacketNumber]:
            robot.jump()
            print "I Jumped"
            for i in robotProperties.nodeDict:
                robotProperties.nodeDict[i].inCurrentPath = False
            robotProperties.currentPacketNumber += 1

        #--Decides whether or not to make a node in the current location and update the robots current node if it was not in its current path--#
        if robotProperties.nodeDict.get(repr(robotProperties.currentPosition)) != None:
            print "Already a node here: " + repr(robotProperties.currentPosition)
            robotProperties.currentNode = robotProperties.nodeDict[repr(robotProperties.currentPosition)]
            if robotProperties.currentNode.inCurrentPath == False:
                update_node(robotProperties.currentPosition, robotProperties.currentFacingDirection)
                robotProperties.currentNode.inCurrentPath = True
        else:
            print "Make node here: " + repr(robotProperties.currentPosition)
            make_node(robotProperties.currentPosition, robotProperties.currentFacingDirection, robotProperties.currentNode, [robot.sense_steps(robot.SENSOR_FORWARD), robot.sense_steps(robot.SENSOR_RIGHT), robot.sense_steps(robot.SENSOR_LEFT)])
            robotProperties.currentNode = robotProperties.nodeDict[repr(robotProperties.currentPosition)]
        ###########

        robotProperties.currentNode.numberOfAdjacentExistingNodes = 0 # Changes the number of adjacent nodes the current node has each time the robot enters a node

        #--Uses ComputeCost() to decide which adjacent node has the lowest cost--#
        LowestCostDirection = ["Direction", 999] # Using 999 as a very large integer to find values that are lower than the previous value in a loop

        for i in robotProperties.currentNode.adjacentNodes:
            NodeToPacketDistance = ComputeCost(robotProperties.currentNode.adjacentNodes[i], packets[robotProperties.currentPacketNumber])
            if NodeToPacketDistance <= LowestCostDirection[1] and robotProperties.currentNode.paths[i] != "NoPath":
                if robotProperties.nodeDict.get(repr(robotProperties.currentNode.adjacentNodes[i])) != None:
                    if robotProperties.nodeDict[repr(robotProperties.currentNode.adjacentNodes[i])].inCurrentPath == False:
                        LowestCostDirection = [i, NodeToPacketDistance]
                else:
                    LowestCostDirection = [i, NodeToPacketDistance]

        print "Lowest Costs [Direction], [Distance]: " + str(LowestCostDirection[0]) + ", " + str(LowestCostDirection[1])
        ###########
        
        #--This decides what direction the robot will step in to explore a position without a node or with a node if the node is not part of the current path--#
        for i in robotProperties.currentNode.adjacentNodes:
            print "i = " + str(i)

            IfNodeExistsShouldIConsider = False

            if robotProperties.nodeDict.get(repr(robotProperties.currentNode.adjacentNodes[i])) != None:
                if robotProperties.nodeDict[repr(robotProperties.currentNode.adjacentNodes[i])].inCurrentPath == False:
                    print "Node Exists and I should consider stepping on it"
                    IfNodeExistsShouldIConsider = True

            if robotProperties.nodeDict.get(repr(robotProperties.currentNode.adjacentNodes[i])) == None or IfNodeExistsShouldIConsider == True: # If the robot does not find a node at an adjacent position
                if i == "North" and LowestCostDirection[0] == "North":
                    if robotProperties.currentNode.paths[i] != "NoPath" or IfNodeExistsShouldIConsider == True:
                        step_north(1)
                        print "Step North"
                        break
                    else:
                        pass
                elif i == "South" and LowestCostDirection[0] == "South":
                    if robotProperties.currentNode.paths[i] != "NoPath" or IfNodeExistsShouldIConsider == True:
                        step_south(1)
                        print "Step South"
                        break
                    else:
                        pass
                elif i == "West" and LowestCostDirection[0] == "West":
                    if robotProperties.currentNode.paths[i] != "NoPath" or IfNodeExistsShouldIConsider == True:
                        step_west(1)
                        print "Step West"
                        break
                    else:
                        pass
                elif i == "East" and LowestCostDirection[0] == "East":
                    if robotProperties.currentNode.paths[i] != "NoPath" or IfNodeExistsShouldIConsider == True:
                        step_east(1)
                        print "Step East"
                        break
                    else:
                        pass
            elif robotProperties.nodeDict.get(repr(robotProperties.currentNode.adjacentNodes[i])) != None and robotProperties.currentNode.paths[i] != "NoPath":
                robotProperties.currentNode.numberOfAdjacentExistingNodes += 1
        ###########

        print "Adjacent nodes to live paths: " + str(robotProperties.currentNode.numberOfAdjacentExistingNodes) + "\t" + str(robotProperties.currentNode.numLivepaths)
        
        if robotProperties.currentNode.numberOfAdjacentExistingNodes == robotProperties.currentNode.numLivepaths: # Conditions for retreating
            print "Trying retreat: " + robotProperties.currentNode.retreatDirection
            Retreat()
        
    ###########
