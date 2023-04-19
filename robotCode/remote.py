#-----------------------------------------#
# Name - IR-Finalized.py
# Description - The finalized code to read data from an IR sensor and then reference it with stored values
# Author - Lime Parallelogram
# License - Completely Free
# Date - 12/09/2019
#------------------------------------------------------------#
# Imports modules
import RPi.GPIO as GPIO
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
	
while True:
	inData = convertHex(getBinary()) #Runs subs to get incoming hex value
	for button in range(len(Buttons)):#Runs through every value in list
		if hex(Buttons[button]) == inData: #Checks this against incoming
			print(ButtonsNames[button]) #Prints corresponding english name for button
			
