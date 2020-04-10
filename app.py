# How to add autostart:
# 1. nano /home/pi/.config/lxsession/LXDE-pi/autostart
# 2. @lxterminal -e python3 /home/pi/TortFeeder/app.py

# Import libraries
import RPi.GPIO as GPIO
import time
from flask import Flask,request,render_template,send_from_directory,jsonify
import json
import os



# Define variables
# startAngle = 180
# endAngle = 140

# Method to set the angle
# def setAngle(angle):
# 	servo1.ChangeDutyCycle(2+(angle/18))
# 	time.sleep(0.5)
# 	#servo1.ChangeDutyCycle(0)

# Feed method to quickly change angle and dispense food
def feedMotorTurn():
	# Set GPIO numbering mode
	GPIO.setmode(GPIO.BOARD)
	# Set pin 11 as an output, and define as servo1 as PWM pin
	GPIO.setup(11,GPIO.OUT)
	servo1 = GPIO.PWM(11,50) # pin 11 for servo1, pulse 50Hz
	# Start PWM running, with value of 0 (pulse off)
	servo1.start(0)
	time.sleep(1)

	# Servo movement to dispense food
	servo1.ChangeDutyCycle(7.5)  # turn towards 90 degree
	time.sleep(1) # sleep 1 second
	servo1.ChangeDutyCycle(12.5)  # turn towards 180 degree
	time.sleep(1) # sleep 1 second
	
	# Clean up ports
	servo1.stop()
	GPIO.cleanup()
	time.sleep(1)

app = Flask(__name__)

# Define default route for app
@app.route("/")
def root():
	return render_template("home.html")

# Feed request
@app.route("/feed", methods= ['POST'])
def feed():
	feedMotorTurn()
	return jsonify(status="success")

# Prevent caching
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

# Run the server
if __name__ == "__main__":
	useDebug = True
	app.run(host='0.0.0.0', port=5000, debug=useDebug)