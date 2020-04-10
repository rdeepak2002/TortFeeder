# How to add autostart:
# 1. nano /home/pi/.config/lxsession/LXDE-pi/autostart
# 2. @lxterminal -e python3 /home/pi/TortFeeder/app.py

# Import libraries
from flask import Flask,request,render_template,send_from_directory,jsonify,Response
from importlib import import_module
from camera_opencv import Camera
import time
import json
import os
import serial

# Create the flask server
app = Flask(__name__)

# Define default route for app
@app.route("/")
def root():
	return render_template("home.html")

# Feed method to call arduino with serial communication
def feedMotorTurn():
	ser = serial.Serial('/dev/ttyACM0', 9800,timeout=1)
	time.sleep(2)
	ser.write(b'H')
	ser.close()

# Feed request
@app.route("/feed", methods= ['POST'])
def feed():
	feedMotorTurn()
	time.sleep(1)
	return jsonify(status="success")

# Video streaming generator function
def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Video streaming route
@app.route('/video_feed')
def video_feed():
	return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

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