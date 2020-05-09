#!/usr/bin/env python
import rospy
from std_msgs.msg import UInt16
from geometry_msgs.msg import Twist
import time
import sys
import os

rospy.init_node('zumo_object_avoid', anonymous=True) #creating a new node 
pub = rospy.Publisher('/zumo/3/cmd_vel', Twist, queue_size=10) # publishing to zumo/3/cmd_vel

current_topic = 0 #defining variables
new_topic = 1

def right(): #turn right function
 vel_msg = Twist()
 vel_msg.linear.x = 0
 vel_msg.linear.y = -1
 vel_msg.linear.z = 0
 vel_msg.angular.x = 0
 vel_msg.angular.y = 0
 vel_msg.angular.z = 0
 vel_msg.linear.x = 0
 pub.publish(vel_msg)

def left(): #turn left function
 vel_msg = Twist()
 vel_msg.linear.x = 0
 vel_msg.linear.y = 1
 vel_msg.linear.z = 0
 vel_msg.angular.x = 0
 vel_msg.angular.y = 0
 vel_msg.angular.z = 0
 vel_msg.linear.x = 0
 pub.publish(vel_msg)


def handle_zumo_sensor(wall_msg):
 global current_topic
 if(wall_msg.data < 20):
     new_topic = 2 #changing the variables when sensor data is less than 20
     right() #actually publish a new message..
 else:
     new_topic = 1

def handle_zumo_leftsensor(wall_msg):
 global current_topic
 if(wall_msg.data < 20):
     new_topic = 2
     right() #actually publish a new message..
 else:
     new_topic = 1

def handle_zumo_rightsensor(wall_msg):
 global current_topic
 if(wall_msg.data < 20):
     new_topic = 2
     left() #actually publish a new message..
 else:
     new_topic = 1



 #only change topics if we need to.
 if(current_topic ==1 and new_topic == 2):
  os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/3/cmd_vel") #switiching between nodes

  current_topic = 2
 if(current_topic ==2 and new_topic == 1):
  os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/1/cmd_vel")
  current_topic = 1

rospy.Subscriber('/zumo/front', UInt16, handle_zumo_sensor) # getting sensor data from sensors by subscribing to data being published
rospy.Subscriber('/zumo/left', UInt16, handle_zumo_leftsensor)
rospy.Subscriber('/zumo/right', UInt16, handle_zumo_rightsensor)
#take over
os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/1/cmd_vel") # turning to the forward node when there is no condition being satisfied
current_topic = 1
rospy.spin()
