# Line Coordinated Delivery Robot

This project is an autonomously moving line-following delivery robot that can be controlled remotely using a webserver and a remote controller. It is built for Raspberry Pi OS using the Raspberry Pi 3B+, Python3 & Flask, and HTML/CSS for the webserver.

![picture of our robot](https://media.discordapp.net/attachments/1027203991064563754/1097950567113965578/20230418_110553.jpg?width=816&height=612)

# Features
* The robot is capable of autonomously moving along a black line using infrared sensors. Counts white squares on line to know what room it is in front of.
* It can carry up to 1kg of payload in it's container.
* It can be remotely controlled using a webserver
* It can be remotely controlled using a remote controller and reciever 
* The webserver is built using Python3 and Flask, and allows users to control the robot's movement and delivery actions through a web GUI interface.
* The robot's hardware is based on the Raspberry Pi 3B+ and its GPIO pins are used to control the motors and read sensor inputs.

# Requirements
* Raspberry Pi 3B+ running Raspberry Pi OS
* Bread Board
* 3 Infrared line sensors
* Motors and Motor driver module
* Robot chassis 
* Power source (such as a battery pack)
* Remote control and reciver 


# Installation and Usage

Clone the repository to your Raspberry Pi:

`git clone https://github.com/IndecisiveMagician/Line-Coordinated-Delivery-Robot.git`


Once in your Raspberry Pi OS enviroment, Install the required dependencies from the command line:

`sudo apt-get update`

`sudo apt install python3-flask`

Connect the infrared sensors and motor driver module to the Raspberry Pi's GPIO pins as per the wiring diagram provided in the credits of this repository. Now you can pick whether to control the robot using a webserver or controller. 

## Start Webserver
To start website first power on the pi and cd to the folder that contains the webserver python file 'https_webserver.py'. Change line 8 of http_webserver.py `host='youriphere` to your ip you are hosting on. The IP can be found with the following command:

`ip -4 address|grep inet`

Start the webserver: 

`python3 https_webserver.py`

You will see "Server Starts -" followed by the address to type in your browser. Put this in your browser search bar and now you can freely control the robot by picking the room number on the GUI buttons to send it to. You can also put the IP directly into the search bar and log in using the credentials saved in users.json.

## Control using Remote

Navigate to the folder that contains the remote movement python code in the terminal. 

Run the remote movement code:

`python3 movementWithRemote.py`

Now you can freely control the robot by pressing the remote buttons that corredespond to the room you want it to stop at. 

## Authors

- Nicole Pililyan [@NicoleP23](https://www.github.com/NicoleP23)
- Chico General [@cmgeneral0106](https://www.github.com/cmgeneral0106)
- Mad Perry [@IndecisiveMagician](https://www.github.com/IndecisiveMagician)
- Timothy Farr [@timtim20](https://www.github.com/timtim20)
- Jaci Taylor [@jt1938](https://www.github.com/jt1938)



## License

[GPL-2.0 license](https://github.com/IndecisiveMagician/Line-Coordinated-Delivery-Robot/blob/main/LICENSE.md)


## Credits
Special thanks to the following resources:

[Line following IR Sensor Tutorial](https://thepihut.com/blogs/raspberry-pi-tutorials/how-to-use-the-tcrt5000-ir-line-follower-sensor-with-the-raspberry-pi)

[IR remote reciever decoder](https://github.com/Lime-Parallelogram/pyIR)

[Motor Driver GPIO Pinout](https://learn.adafruit.com/adafruit-tb6612-h-bridge-dc-stepper-motor-driver-breakout)

[Motors GPIO Pinout](https://www.adafruit.com/product/3777)

[Webserver interface](https://www.aranacorp.com/en/create-a-web-interface-to-control-your-raspberry-pi/)

[Flask-SocketIO](https://pypi.org/project/Flask-SocketIO/)

[python3](https://www.python.org/downloads/)

