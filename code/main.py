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

import time
from machine import Pin, ADC
from pimoroni import Button, RGBLED
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P4

## I/O setup & variables
DEBUG = True
MOTOR_OUT_PIN = 10
SENSOR_IN_PIN = 27
sensor_in = ADC(SENSOR_IN_PIN)
motor_out = Pin(MOTOR_OUT_PIN, Pin.OUT)
led_pin = Pin("LED", Pin.OUT)

## Display setup & variables
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P4, rotate=0)
display.set_backlight(0.5)
display.set_font("bitmap8")
WIDTH, HEIGHT = display.get_bounds()

led = RGBLED(6, 7, 8)
button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
CYAN = display.create_pen(0, 255, 255)
MAGENTA = display.create_pen(255, 0, 255)
YELLOW = display.create_pen(255, 255, 0)
GREEN = display.create_pen(0, 255, 0)


def clear():  # func we call to clear the screen
    led.set_rgb(0, 0, 0)  # turn the LED off
    display.set_pen(BLACK)  # black background
    display.clear()  # clears the screen setting to black
    display.update()  # performs the actual screen update


def setup():
    motor_out.high()  # turn the motor off
    blink_welcome()
    clear()


def blink_welcome():
    led_pin.on()
    time.sleep(.5)
    led_pin.off()
    time.sleep(.5)
    led.set_rgb(255, 0, 0)  # turn the LED off
    time.sleep(.1)
    led.set_rgb(0, 255, 0)  # turn the LED off
    time.sleep(.1)
    led.set_rgb(0, 0, 255)  # turn the LED off
    time.sleep(.1)


def loop():
    boundary_humidity = 50000
    while True:
        time.sleep(0.2)  # wait for 0.5 seconds
        print("Plant - Moisture Level:")
        sensor_value = sensor_in.read_u16()
        print(sensor_value)
        if sensor_value > boundary_humidity:
            motor_out.high()  # turn the motor on
        else:
            motor_out.high()  # turn the motor off

        if button_a.read():  # if a button press is detected then...
            clear()  # clear to black
            display.set_pen(WHITE)  # change the pen colour
            if boundary_humidity < 90000:
                boundary_humidity += 1000
                display.text("Boundary humidity increased", 10, 10, 240, 4)  # display some text on the screen
            else:
                display.text("Boundary humidity already max", 10, 10, 240, 4)
            display.update()  # update the display
            time.sleep(0.5)  # pause for a sec
            clear()  # clear to black again
        elif button_b.read():
            clear()
            display.set_pen(CYAN)
            if boundary_humidity > 0:
                boundary_humidity -= 1000
                display.text("Boundary humidity decreased", 10, 10, 240, 4)  # display some text on the screen
            else:
                display.text("Boundary humidity already min", 10, 10, 240, 4)
            display.update()
            time.sleep(.5)
            clear()
        elif button_x.read():
            clear()
            display.set_pen(MAGENTA)
            display.text("Button X pressed", 10, 10, 240, 4)
            display.update()
            time.sleep(1)
            clear()
        elif button_y.read():
            clear()
            display.set_pen(YELLOW)
            display.text("Button Y pressed", 10, 10, 240, 4)
            display.update()
            time.sleep(1)
            clear()
        else:
            display.set_pen(GREEN)
            display.text(f"Boundary humidity = {boundary_humidity}\n"
                         "+ Press A to increase\n"
                         "- Press B to decrease", 7, 7, 240, 2)
            display.update()
        time.sleep(0.1)  # this number is how frequently the Pico checks for button presses


if __name__ == '__main__':
    setup()
    loop()
