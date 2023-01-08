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

int MOTOR_OUT = 5;
int SENSOR_IN = 0;

float sensorValue = 0;


// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);

  Serial.begin(9600);
  pinMode(MOTOR_OUT, OUTPUT);
  pinMode(SENSOR_IN, INPUT);
  delay(500);
}

// the loop function runs over and over again forever
void loop() {
  
//  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED and PUMP on (HIGH is the voltage level)
//  digitalWrite(MOTOR_OUT, HIGH);
//  
//  delay(2000);                       // wait for 5 seconds
//
//  digitalWrite(LED_BUILTIN, LOW);    // turn the LED and PUMP off by making the voltage LOW
//  digitalWrite(MOTOR_OUT, HIGH);
  delay(500);                      // wait for 5 seconds

  Serial.println("Plant - Moisture Level:");
  sensorValue = analogRead(SENSOR_IN);
  Serial.println(sensorValue);
    if (sensorValue > 425) {
    digitalWrite(MOTOR_OUT, LOW);
  } else {
    digitalWrite(MOTOR_OUT, HIGH);
  }
}
