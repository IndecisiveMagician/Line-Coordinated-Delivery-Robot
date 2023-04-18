#!/usr/bin/python

from RPi import GPIO
from time import sleep
import time

GPIO.setmode(GPIO.BOARD)

# set up GPIO pins
GPIO.setup(33, GPIO.IN) # Connected to Left IR Sensor
GPIO.setup(35, GPIO.IN) # Connected to Right IR Sensor
GPIO.setup(7, GPIO.OUT) # Connected to PWMA
GPIO.setup(29, GPIO.OUT) # Connected to AIN2
GPIO.setup(12, GPIO.OUT) # Connected to AIN1
GPIO.setup(13, GPIO.OUT) # Connected to STBY
GPIO.setup(15, GPIO.OUT) # Connected to BIN1
GPIO.setup(16, GPIO.OUT) # Connected to BIN2
GPIO.setup(37, GPIO.OUT) # Connected to PWMB

print("running!")
time.sleep(5)

i = 0

try:
      while (i < 45):
            if GPIO.input(33):
                  #turn left
                  print("Robot is straying off to the right, move left captain!")
                  # Motor A:
                  GPIO.output(12, GPIO.LOW) # Set AIN1
                  GPIO.output(29, GPIO.HIGH) # Set AIN2
                  # Motor B:
                  GPIO.output(15, GPIO.HIGH) # Set BIN1
                  GPIO.output(16, GPIO.LOW) # Set BIN2
                  # Set the motor speed
                  # Motor A:
                  GPIO.output(7, GPIO.HIGH) # Set PWMA
                  # Motor B:
                  GPIO.output(37, GPIO.HIGH) # Set PWMB
                  # Disable STBY (standby)
                  GPIO.output(13, GPIO.HIGH)
                  sleep(0.3)
            elif GPIO.input(35):
                  #turn right
                  print("Robot is straying off to the left, move right captain!")
                  # Motor A:
                  GPIO.output(12, GPIO.HIGH) # Set AIN1
                  GPIO.output(29, GPIO.LOW) # Set AIN2
                  # Motor B:
                  GPIO.output(15, GPIO.LOW) # Set BIN1
                  GPIO.output(16, GPIO.HIGH) # Set BIN2
                  # Set the motor speed
                  # Motor A:
                  GPIO.output(7, GPIO.HIGH) # Set PWMA
                  # Motor B:
                  GPIO.output(37, GPIO.HIGH) # Set PWMB
                  # Disable STBY (standby)
                  GPIO.output(13, GPIO.HIGH)
                  sleep(0.3)
            else:
                  # Drive the motor clockwise
                  print("Go straight")
                  # Motor A:
                  GPIO.output(12, GPIO.HIGH) # Set AIN1
                  GPIO.output(29, GPIO.LOW) # Set AIN2
                  # Motor B:
                  GPIO.output(15, GPIO.HIGH) # Set BIN1
                  GPIO.output(16, GPIO.LOW) # Set BIN2
                  # Set the motor speed
                  # Motor A:
                  GPIO.output(7, GPIO.HIGH) # Set PWMA
                  # Motor B:
                  GPIO.output(37, GPIO.HIGH) # Set PWMB
                  # Disable STBY (standby)
                  GPIO.output(13, GPIO.HIGH)
                  sleep(0.3)
            i += 1
            print(i)
      # Reset all the GPIO pins by setting them to LOW
      GPIO.output(12, GPIO.LOW) # Set AIN1
      GPIO.output(29, GPIO.LOW) # Set AIN2
      GPIO.output(7, GPIO.LOW) # Set PWMA
      GPIO.output(13, GPIO.LOW) # Set STBY
      GPIO.output(15, GPIO.LOW) # Set BIN1
      GPIO.output(16, GPIO.LOW) # Set BIN2
      GPIO.output(37, GPIO.LOW) # Set PWMB
      GPIO.cleanup()
except:
	GPIO.cleanup()
