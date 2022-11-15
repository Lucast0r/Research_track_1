from __future__ import print_function

import time
import numpy
from sr.robot import *


a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""

silver = True
""" boolean: variable for letting the robot know if it has to look for a silver or for a golden marker"""

R = Robot()
""" instance of the class Robot"""

N = 12 # Number of tokens to process
T = 2 # Number of types of tokens, in this case Silver and Gold

database = numpy.zeros((N/2,T),dtype=int) 

ltm = 0 # Line tracking matrix : tells us at what line we are and where we should write the next token number 
"""
Initialise the database as a matrix full of 0 :
Each line will have the number of the silver token in the first column 
and the number of the golden one in the second column.
This will allow us in the end to print which token is close to which token. 
"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_silver_token():
    """
    Function to find the closest silver token

    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:
            dist=token.dist
            rot_y=token.rot_y
            number =token.info[0]
            print (token.info)
    if dist==100:
        return -1, -1, -1
    else:
   	    return dist, rot_y, number

def find_golden_token():
    """
    Function to find the closest golden token

    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
            dist = token.dist
            rot_y = token.rot_y
            number = token.info[0]
            print(token.info)
    if dist==100:
        return -1, -1, -1
    else:
        return dist, rot_y, number

def goto_silver_token (dist, rot):

    """
    This function drives to the desired token and grabs it 
    It exits only once the object is grabed 
    """
    while 1:
        dist, rot_y,number = find_silver_token()
        if dist <d_th: # if we are close to the token, we try grab it.
            print("Found it!")
            return 
        elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
            print("Ah, that'll do.")
            drive(80, 0.5)
        elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
            print("Left a bit...")
            turn(-2, 0.5)
        elif rot_y > a_th:
            print("Right a bit...")
            turn(+2, 0.5)   


def gonear_golden_token (dist, rot):

    """
    This function drives to the desired token and grabs it 
    It exits only once the object is grabed 
    """
    while 1:
        dist, rot_y,number = find_golden_token()
        if dist <0.5: # if we are close to the token, we try grab it.
            print("Found it!")
            return 
        elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
            print("Ah, that'll do.")
            drive(60, 0.5)
        elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
            print("Left a bit...")
            turn(-2, 0.5)
            print (rot_y)
        elif rot_y > a_th:
            print("Right a bit...")
            turn(+2, 0.5)   
        
while 1:
    
    dist, rot_y, number_token = find_silver_token()
    while dist ==-1 or number_token in database:
        if database[(N/2-1),(T-1)]!=0:
            print ("Here is the database :",database)
            exit()
        dist, rot_y, number_token = find_silver_token()
        turn(2,0.5)
        
    if dist != -1 and number_token not in database: # Check if the token number is in the database
        database [ltm,0] = number_token # Store the number of the token in the database
        print (database)
        goto_silver_token(dist,rot_y) 
        if R.grab(): # if we grab the token, we move the robot forward and on the right, we release the token, and we go back to the initial position
            print("Gotcha!")
        dist, rot_y, number_token = find_golden_token()
        while dist == -1 or number_token in database:
            dist, rot_y, number_token = find_golden_token()
            turn(2,0.5)
        if dist !=-1 and number_token not in database: # Check if the token number is in the database 
            database [ltm,1] = number_token # Store the number of the token in the database
            print (database)
            ltm += 1 # We go to the next line 
            print ("gold")
            gonear_golden_token(dist,rot_y) 
            R.release() # Drop the silver token 
            drive(-60, 1)
    


