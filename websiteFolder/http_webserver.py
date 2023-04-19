#!/usr/bin/env python3

import RPi.GPIO as GPIO
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

host_name = '10.16.60.44'  # IP Address of Raspberry Pi
host_port = 8000


def setupGPIO():
	# Sets up GPIO
	GPIO.setmode(GPIO.BOARD)
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


def getTemperature():
	temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
	return temp


class MyServer(BaseHTTPRequestHandler):

	def do_HEAD(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def _redirect(self, path):
		self.send_response(303)
		self.send_header('Content-type', 'text/html')
		self.send_header('Location', path)
		self.end_headers()

	def do_GET(self):
		html = '''
<html>
<head>

</head>
<body style="background-color:#d3d3d3">
<h2 style="background: linear-gradient(to right, #80bdff 50%, #d3d3d3 100%);box-shadow: 0 4px 2px -2px gray;">
__Line Following Robot
         <div class="top-btn-group" style="text-align:right; margin: 5px 5px 5px 1px;">
            <button type="button" style="background-color: #80bdff; border: 1px solid blue; cursor: pointer;">Contact Us</button>
            <button class="circlebtn" type="button" style="border-radius: 50%; background-color: #80bdff; border: 1px solid blue; cursor: pointer;">?
            </button>
            <button onclick="location.href='10.16.60.44'" style="background-color: #80bdff; border: 1px solid blue; cursor: pointer;">Logout</button>
         </div>
      </h2>
<div style="width:300px;height:200px;overflow-y:scroll;padding:20px;background-color:#c1c1c1">
  <form action="/" method="POST">
    Pick a room :
    <input type="submit" name="submit" value="1"  style="height:35px; width:100%; margin-bottom: 5px; font-size:25px; cursor:pointer; border:1px solid blue; background-color:#80bdff;">
    <input type="submit" name="submit" value="2" style="height:35px; width:100%; margin-bottom: 5px; font-size:25px; cursor:pointer; border:1px solid blue; background-color:#80bdff;">
    <input type="submit" name="submit" value="3" style="height:35px; width:100%; margin-bottom: 5px; font-size:25px; cursor:pointer; border:1px solid blue; background-color:#80bdff;">
    <input type="submit" name="submit" value="4" style="height:35px; width:100%; margin-bottom: 5px; font-size:25px; cursor:pointer; border:1px solid blue; background-color:#80bdff;">
    <input type="submit" name="submit" value="5" style="height:35px; width:100%; margin-bottom: 5px; font-size:25px; cursor:pointer; border:1px solid blue; background-color:#80bdff;">
    <input type="submit" name="submit" value="6" style="height:35px; width:100%; margin-bottom: 5px; font-size:25px; cursor:pointer; border:1px solid blue; background-color:#80bdff;">
    <input type="submit" name="submit" value="7" style="height:35px; width:100%; margin-bottom: 5px; font-size:25px; cursor:pointer; border:1px solid blue; background-color:#80bdff;">
  </form>
</div>
    <div class="bottom-btn-group" style="padding:20px;margin-right:20px; ">
          <input class="bottom-btn" type="submit" name="submit" value="Stop Run" style=" cursor: pointer; background-color: #80bdff; width:170px;height:50px; font-size: 20px; border: 1px solid blue;">
         <button class="bottom-btn"style=" cursor: pointer; width:170px;height:50px;font-size: 20px; background-color: #80bdff; border: 1px solid blue;">Home</button>
    </div>
  </body>
  </html>
		'''
		temp = getTemperature()
		self.do_HEAD()
		self.wfile.write(html.format(temp[5:]).encode("utf-8"))

	def do_POST(self):

		content_length = int(self.headers['Content-Length'])
		post_data = self.rfile.read(content_length).decode("utf-8")
		post_data = post_data.split("=")[1]

		setupGPIO()

		if post_data == '1':
			i = 0
			roomWait = 0
			roomNumber = 1
			roomCounter = 0
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

			# Reset all the GPIO pins by setting them to LOW
			GPIO.output(12, GPIO.LOW) # Set AIN1
			GPIO.output(29, GPIO.LOW) # Set AIN2
			GPIO.output(7, GPIO.LOW) # Set PWMA
			GPIO.output(13, GPIO.LOW) # Set STBY
			GPIO.output(15, GPIO.LOW) # Set BIN1
			GPIO.output(16, GPIO.LOW) # Set BIN2
			GPIO.output(37, GPIO.LOW) # Set PWMB
		elif post_data == '2':
			i = 0
			roomWait = 0
			roomNumber = 2
			roomCounter = 0
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

			# Reset all the GPIO pins by setting them to LOW
			GPIO.output(12, GPIO.LOW) # Set AIN1
			GPIO.output(29, GPIO.LOW) # Set AIN2
			GPIO.output(7, GPIO.LOW) # Set PWMA
			GPIO.output(13, GPIO.LOW) # Set STBY
			GPIO.output(15, GPIO.LOW) # Set BIN1
			GPIO.output(16, GPIO.LOW) # Set BIN2
			GPIO.output(37, GPIO.LOW) # Set PWMB
		else:
			GPIO.cleanup()

		print("Room is {}".format(post_data))
		self._redirect('/')  # Redirect back to the root url


# # # # # Main # # # # #

if __name__ == '__main__':
	http_server = HTTPServer((host_name, host_port), MyServer)
	print("Server Starts - %s:%s" % (host_name, host_port))

	try:
		http_server.serve_forever()
	except KeyboardInterrupt:
		http_server.server_close()
