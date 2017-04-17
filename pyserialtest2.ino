#include <Servo.h>

Servo myservo;

int val;

void setup() {
  // initialize serial communication:
  myservo.attach(9);
  
  Serial.begin(9600);
  Serial.setTimeout(10);
 
  // initialize the LED pin as an output:
  //pinMode(ledPin, OUTPUT);
}

void loop() {
  // see if there's incoming serial data:
  if (Serial.available()) {
    // read the oldest byte in the serial buffer:
    val = Serial.parseInt();
    
    myservo.write(val);
  }
}
