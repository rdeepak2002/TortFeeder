# Import libraries
#import RPi.GPIO as GPIO
import time
from flask import Flask

# Set GPIO numbering mode
# GPIO.setmode(GPIO.BOARD)

# # Set pin 11 as an output, and define as servo1 as PWM pin
# GPIO.setup(11,GPIO.OUT)
# servo1 = GPIO.PWM(11,50) # pin 11 for servo1, pulse 50Hz

# # Start PWM running, with value of 0 (pulse off)
# servo1.start(0)

# # Define variables
# startAngle = 180
# endAngle = 140

# # Method to set the angle
# def setAngle(angle):
# 	servo1.ChangeDutyCycle(2+(angle/18))
# 	time.sleep(0.2)
# 	servo1.ChangeDutyCycle(0)

# # Feed method to quickly change angle and dispense food
# def feed():
# 	setAngle(startAngle)
# 	setAngle(endAngle)
# 	setAngle(startAngle)

# # Start the motor at the necessary start angle
# setAngle(startAngle)

# # Call feed to dispense food
# feed()

app = Flask(__name__)

# Define default route for app
@app.route("/")
def hello():
	return "Hello, World!"

# Run the server
if __name__ == "__main__":
	app.run(debug=True)