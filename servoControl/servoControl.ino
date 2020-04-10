#include <Servo.h>

Servo servo;
int angle = 180;
int incomingByte;      // a variable to read incoming serial data into

void setup() {
  servo.attach(8);
  servo.write(angle);
  Serial.begin(9600);

}

void loop() 
{
  if (Serial.available() > 0) {

    incomingByte = Serial.read();

    if (incomingByte == 'H') {
      for(angle = 180; angle > 120; angle--)    
      {                                
        servo.write(angle);           
        delay(3);       
      } 
      for(angle = 120; angle < 180; angle++)  
      {                                  
        servo.write(angle);               
        delay(3);                   
      } 
    }

  }
} 
