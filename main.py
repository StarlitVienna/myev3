#!/usr/bin/env python3

import math
import time
from pybricks.ev3devices import *
from pybricks.parameters import *
from pybricks.robotics import *
from pybricks.tools import wait
from pybricks.hubs import EV3Brick

ev3 = EV3Brick()
motorA = Motor(Port.A)
motorB = Motor(Port.B)
left_motor = motorA
right_motor = motorB
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=152)
robot.settings(straight_speed=200, straight_acceleration=100, turn_rate=100)

color_sensor_in1 = ColorSensor(Port.S1)
color_sensor_in2 = ColorSensor(Port.S2)
obstacle_sensor = UltrasonicSensor(Port.S3)
gyro_sensor= GyroSensor(Port.S4)

motorC = Motor(Port.C)

times_turned = None
white_color = None
normal_vel = None

def check_gl():
  global times_turned, white_color, normal_vel
  while color_sensor_in1.color() == Color.GREEN:
    robot.straight(25)

def check_gr():
  global times_turned, white_color, normal_vel
  while color_sensor_in2.color() == Color.GREEN:
    robot.straight(25)


print('Color 6 = white')
times_turned = 0
white_color = 6
normal_vel = 5
while True:
  if (obstacle_sensor.distance()) < 10:
    times_turned = 0
    while (obstacle_sensor.distance()) <= 10:
      robot.turn(45)
      times_turned = times_turned + 1
  else:
    if color_sensor_in1.color() == Color.BLACK and color_sensor_in2.color() == Color.BLACK:
      while color_sensor_in1.color() == Color.BLACK and color_sensor_in2.color() == Color.BLACK:
        motorA.dc(normal_vel)
        motorB.dc(normal_vel)
        print('BLACK both BOTH')
      robot.straight(369)
      if color_sensor_in1.color() == Color.GREEN or color_sensor_in2.color() == Color.GREEN:
        robot.straight(30)
    elif color_sensor_in1.color() == white_color and color_sensor_in2.color() == Color.BLACK:
      robot.drive(25, 15)
      print('WHITE left BLACK right')
    elif color_sensor_in1.color() == Color.BLACK and color_sensor_in2.color() == white_color:
      robot.drive(25, (-15))
      print('WHITE right BLACK left')
    elif color_sensor_in1.color() == Color.GREEN and color_sensor_in2.color() == white_color:
      check_gl()
      robot.turn((-90))
      robot.straight(35)
      print("It's green left!")
    elif color_sensor_in1.color() == white_color and color_sensor_in2.color() == Color.GREEN:
      check_gr()
      robot.turn(90)
      robot.straight(35)
      print("It's green right!")
    elif color_sensor_in1.color() == Color.GREEN and color_sensor_in2.color() == Color.GREEN:
      robot.straight(200)
      robot.turn(180)
      robot.straight(20)
    elif color_sensor_in1.color() == white_color and color_sensor_in2.color() == white_color:
      motorA.dc(normal_vel)
      motorB.dc(normal_vel)
      print('WHITE both')
    elif color_sensor_in1.color() == Color.RED or color_sensor_in2.color() == Color.RED:
      robot.stop()
      break
