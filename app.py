# How to add autostart:
# 1. nano /home/pi/.config/lxsession/LXDE-pi/autostart
# 2. @lxterminal -e sh /home/pi/TortFeeder/launch.sh

# Import libraries
from flask import Flask,send_file,request,render_template,send_from_directory,jsonify,Response
from importlib import import_module
from camera_opencv import Camera
import time
import json
import os
import serial

# Create the flask server
app = Flask(__name__)

# Define default route for app
@app.route('/')
def root():
	return render_template('home.html')

# Password request
@app.route('/checkPassword', methods= ['POST'])
def checkPassword():
	passIn = request.form['data']
	password = '095ce0e2e8896b400d5ca27ff55931ba87000ff8749977c8b003cf52f207ad02'
	if(passIn == password):
		return jsonify(status='correct')
	else:
		return jsonify(status='incorrect')

# Feed request to turn motor
@app.route('/feed', methods= ['POST'])
def feed():
	usbPort = '/dev/ttyACM0'
	try:
		ser = serial.Serial(usbPort, 9800,timeout=1)
		time.sleep(2)
		ser.write(b'H')
		ser.close()
		time.sleep(1)
		return jsonify(status='success')
	except:
		return jsonify(status='failure')

# Video streaming generator function
def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Video streaming route
@app.route('/video_feed')
def video_feed():
	return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

# For SSL Verification
@app.route('/.well-known/acme-challenge/<challenge>')
def letsencrypt_check(challenge):
	filename = app.root_path + '/.well-known/' + challenge
	return send_file(filename)

# Prevent caching
@app.after_request
def add_header(r):
	r.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
	r.headers['Pragma'] = 'no-cache'
	r.headers['Expires'] = '0'
	r.headers['Cache-Control'] = 'public, max-age=0'
	return r

# Run the server
if __name__ == '__main__':
	useDebug = True
	# app.run(host='0.0.0.0', port=5000, debug=useDebug)
	app.run(host='0.0.0.0', port=443, debug=useDebug, ssl_context=('certificate.crt', 'private.key'))
