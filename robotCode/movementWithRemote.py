#-----------------------------------------#
# Name - IR-Finalized.py
# Description - The finalized code to read data from an IR sensor and then reference it with stored values
# Author - Lime Parallelogram
# License - Completely Free
# Date - 12/09/2019
#------------------------------------------------------------#
# Imports modules
from RPi import GPIO
from datetime import datetime
import time

# Static program vars
pin = 40  # Input pin of sensor (GPIO.BOARD)
Buttons = [0x300fd08f7, 0x300fd8877, 0x300fd48b7, 0x300fd28d7, 0x300fda857, 0x300fd6897, 0x300fd18e7, 0x300fd9867, 0x300fd58a7, 0x28807e619]  # HEX code list
ButtonsNames = ["ONE",   "TWO",      "THREE",       "FOUR",      "FIVE", "SIX",
    "SEVEN",  "EIGHT", "NINE", "ZERO"]  # String list in same order as HEX list

# Sets up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN)
GPIO.setup(33, GPIO.IN) # Connected to Left IR Sensor
GPIO.setup(35, GPIO.IN) # Connected to Right IR Sensor
GPIO.setup(31, GPIO.IN) # Connected to Middle IR Sensor
GPIO.setup(7, GPIO.OUT) # Connected to PWMA
GPIO.setup(29, GPIO.OUT) # Connected to AIN2
GPIO.setup(12, GPIO.OUT) # Connected to AIN1
GPIO.setup(13, GPIO.OUT) # Connected to STBY
GPIO.setup(15, GPIO.OUT) # Connected to BIN1
GPIO.setup(16, GPIO.OUT) # Connected to BIN2
GPIO.setup(37, GPIO.OUT) # Connected to PWMB

print("running!")
roomCounter = 0
roomNumber = 0
        

# Gets binary value


def getBinary():
	# Internal vars
	num1s = 0  # Number of consecutive 1s read
	binary = 1  # The binary value
	command = []  # The list to store pulse times in
	previousValue = 0  # The last value
	value = GPIO.input(pin)  # The current value

	# Waits for the sensor to pull pin low
	while value:
		time.sleep(0.0001) # This sleep decreases CPU utilization immensely
		value = GPIO.input(pin)
		
	# Records start time
	startTime = datetime.now()
	
	while True:
		# If change detected in value
		if previousValue != value:
			now = datetime.now()
			pulseTime = now - startTime #Calculate the time of pulse
			startTime = now #Reset start time
			command.append((previousValue, pulseTime.microseconds)) #Store recorded data
			
		# Updates consecutive 1s variable
		if value:
			num1s += 1
		else:
			num1s = 0
		
		# Breaks program when the amount of 1s surpasses 10000
		if num1s > 10000:
			break
			
		# Re-reads pin
		previousValue = value
		value = GPIO.input(pin)
		
	# Converts times to binary
	for (typ, tme) in command:
		if typ == 1: #If looking at rest period
			if tme > 1000: #If pulse greater than 1000us
				binary = binary *10 +1 #Must be 1
			else:
				binary *= 10 #Must be 0
			
	if len(str(binary)) > 34: #Sometimes, there is some stray characters
		binary = int(str(binary)[:34])
		
	return binary
	
# Convert value to hex
def convertHex(binaryValue):
	tmpB2 = int(str(binaryValue),2) #Temporarely propper base 2
	return hex(tmpB2)
	
def robot_move(roomNumber):
	global roomCounter
	global doBreak
	i = 0
	roomWait = 0
	while (i < 600):
		if GPIO.input(31):
			roomWait = 0
		if (not GPIO.input(33)) and (not GPIO.input(35)) and (not GPIO.input(31) and roomWait == 0):
			# Reset all the GPIO pins by setting them to LOW
			GPIO.output(12, GPIO.LOW) # Set AIN1
			GPIO.output(29, GPIO.LOW) # Set AIN2
			GPIO.output(7, GPIO.LOW) # Set PWMA
			GPIO.output(13, GPIO.LOW) # Set STBY
			GPIO.output(15, GPIO.LOW) # Set BIN1
			GPIO.output(16, GPIO.LOW) # Set BIN2
			GPIO.output(37, GPIO.LOW) # Set PWMB
			roomCounter = roomCounter + 1
			roomWait = 1
			if roomNumber == roomCounter:
				doBreak = 1
				print("found the room!")
				break
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
			  time.sleep(0.1)
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
			  time.sleep(0.1)
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
			  time.sleep(0.2)
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
	

try:	
	doBreak = 0
	while True:
		inData = convertHex(getBinary()) # Runs subs to get incoming hex value
		for button in range(len(Buttons)):# Runs through every value in list
			if hex(Buttons[button]) == inData: # Checks this against incoming
				print(ButtonsNames[button]) # Prints corresponding english name for button
				if (ButtonsNames[button] == "ONE"):
					print("button found")
					roomNumber = 1
					robot_move(roomNumber)
					if (doBreak == 1):
						break
				if (ButtonsNames[button] == "TWO"):
					print("button found")
					roomNumber = 2
					robot_move(roomNumber)
					if (doBreak == 1):
						break
				if (ButtonsNames[button] == "EIGHT"): # Button eight to stop
					doBreak = 1
					# Reset all the GPIO pins by setting them to LOW
					GPIO.output(12, GPIO.LOW) # Set AIN1
					GPIO.output(29, GPIO.LOW) # Set AIN2
					GPIO.output(7, GPIO.LOW) # Set PWMA
					GPIO.output(13, GPIO.LOW) # Set STBY
					GPIO.output(15, GPIO.LOW) # Set BIN1
					GPIO.output(16, GPIO.LOW) # Set BIN2
					GPIO.output(37, GPIO.LOW) # Set PWMB
					break
		if (doBreak == 1):
			break
	GPIO.cleanup()
except:
	print("ERROR")
	GPIO.cleanup()
