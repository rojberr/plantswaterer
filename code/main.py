# Plants Waterer

# Turns on the water pump for a specified period of time when the measured soil humidity gets too low.

# This is an extremely popular DIY project that allows you to automatically water your plants according to the level of moisture in the soil.

# Most plants need less frequent watering, which can be provided with the use of this code.
# The measurement of soil moisture can be done with use of Capacitive Soil Moisture Sensor v1.2.
# (It is advised to use this model over non-protected resistance models. Check out this video:
# https://www.youtube.com/watch?v=udmJyncDvw0 )

# If you want to know what pin the on-board LED is connected to on your Arduino
# model, check the Technical Specs of your board at:
# https://www.arduino.cc/en/Main/Products

# modified 11 April 2022
# by @author rojberr
# @version 0.0.0

# This example code is shared on Github.
# https://github.com/rojberr/plants-waterer

from machine import Pin, ADC
import time

DEBUG = True

MOTOR_OUT_PIN = 15
SENSOR_IN_PIN = 26
led_pin = Pin("LED", Pin.OUT)

motor_out = Pin(MOTOR_OUT_PIN, Pin.OUT)
sensor_in = ADC(SENSOR_IN_PIN)


def setup():
    led_pin.value(1)
    time.sleep(2)
    led_pin.value(0)
    # initialize digital pin LED_BUILTIN as an output.
    # motor_out.value(0)  # set motor output to LOW


def loop():
    time.sleep(0.2)  # wait for 0.5 seconds
    print("Plant - Moisture Level:")
    sensor_value = sensor_in.read_u16()
    print(sensor_value)
    if sensor_value > 50000:
        motor_out.value(1)  # turn the motor on
    else:
        motor_out.value(0)  # turn the motor off


while True:
    setup()
    loop()

