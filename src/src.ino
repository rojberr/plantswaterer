/*
  Plants waterer

  Turns on the water pump for a specified period of time when the measured soil humidity gets too low.

  This is an extremely popular DIY project that allows you to automatically water your plants according to the level of moisture in the soil.

  Most plants need less frequent watering, which can be provided with the use of this code.
  The measurement of soil moisture can be done with use of Capacitive Soil Moisture Sensor v1.2.
  (It is advised to use this model over non-protected resistance models. Check out this video:
  https://www.youtube.com/watch?v=udmJyncDvw0 )
  
  If you want to know what pin the on-board LED is connected to on your Arduino
  model, check the Technical Specs of your board at:
  https://www.arduino.cc/en/Main/Products

  modified 11 April 2022
  by @author rojberr
  @version 0.0.0

  This example code is shared on Github.

  https://github.com/rojberr/plants-waterer
*/

#include <Arduino.h>
#include <SoftwareSerial.h>

#define DEBUG true

int MOTOR_IN = 5;

int Pin1 = A0;

float sensor1Value = 0;


// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);

  Serial.begin(9600);

  pinMode(MOTOR_IN, OUTPUT);

  pinMode(Pin1, INPUT);

  delay(500);
}

// the loop function runs over and over again forever
void loop() {
  
  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);                       // wait for a second
  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  digitalWrite(MOTOR_IN, HIGH);
  delay(5000);                       // wait for a second

  digitalWrite(MOTOR_IN, HIGH);
  delay(5000); // 2 seconds
 
}
