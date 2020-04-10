# How to add autostart:
# 1. nano /home/pi/.config/lxsession/LXDE-pi/autostart
# 2. @lxterminal -e python3 /home/pi/TortFeeder/app.py

# Import libraries
import RPi.GPIO as GPIO
import time
from flask import Flask,request,render_template,send_from_directory,jsonify
import json
import os

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# Set pin 11 as an output, and define as servo1 as PWM pin
GPIO.setup(11,GPIO.OUT)
servo1 = GPIO.PWM(11,50) # pin 11 for servo1, pulse 50Hz

# Start PWM running, with value of 0 (pulse off)
servo1.start(0)

# Define variables
startAngle = 180
endAngle = 140

# Prevent motor malfunction
motorBusy = False

# Method to set the angle
def setAngle(angle):
	servo1.ChangeDutyCycle(2+(angle/18))
	time.sleep(0.3)
	servo1.ChangeDutyCycle(0)

# Feed method to quickly change angle and dispense food
def feedMotorTurn():
	motorBusy = True
	setAngle(startAngle)
	setAngle(endAngle)
	setAngle(startAngle)

app = Flask(__name__)

# Define default route for app
@app.route("/")
def root():
	return render_template("home.html")

# Feed request
@app.route("/feed", methods= ['POST'])
def feed():
	if(motorBusy == False):
		feedMotorTurn()
		time.sleep(0.8)
		motorBusy = False
		return jsonify(status="success")
	else:
		return jsonify(status="busy")

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