# How to add autostart:
# 1. nano /home/pi/.config/lxsession/LXDE-pi/autostart
# 2. @lxterminal -e python3 /home/pi/TortFeeder/app.py

# Import libraries
import RPi.GPIO as GPIO
import time
from flask import Flask,request,render_template,send_from_directory,jsonify
import json
import os
import serial

app = Flask(__name__)

# Define default route for app
@app.route("/")
def root():
	return render_template("home.html")

# Feed method to call arduino with serial communication
def feedMotorTurn():
	ser = serial.Serial('/dev/ttyACM0', 9800,timeout=1)
	time.sleep(1)
	ser.write(b'H')
	ser.close()

# Feed request
@app.route("/feed", methods= ['POST'])
def feed():
	feedMotorTurn()
	time.sleep(2)
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