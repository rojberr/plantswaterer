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

b_color = []                                       #List to hold the colors
b_color.append(display.create_pen(255, 255, 255))  #White
b_color.append(display.create_pen(210, 210, 210))  #Gray
b_color.append(display.create_pen(000, 255, 255))  #Cyan
b_color.append(display.create_pen(000, 200, 200))  #Cyan
b_color.append(display.create_pen(100, 100, 255))  #Blue
b_color.append(display.create_pen(000, 000, 255))  #Blue
b_color.append(display.create_pen(155, 155, 000))  #Yellow
b_color.append(display.create_pen(255, 255, 000))  #Yellow
b_color.append(display.create_pen(255, 125, 000))  #Orange
b_color.append(display.create_pen(255, 000, 000))  #Red



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
    last_watering = ''
    while True:
        time.sleep(0.2)  # wait for 0.5 seconds
        print("Plant - Moisture Level:")
        sensor_value = sensor_in.read_u16()
        print(sensor_value)
        if sensor_value > boundary_humidity:
            motor_out.high() # turn the motor on
            last_watering = time.localtime()
        else:
            motor_out.high()  # turn the motor off

        if button_a.read():  # if a button press is detected then...
            clear()  # clear to black
            display.set_pen(WHITE)  # change the pen colour
            if boundary_humidity < 90000:
                boundary_humidity += 1000
                display.text("Boundary humidity increased to", 10, 10, 240, 3)
                display.set_pen(MAGENTA)
                display.text(f"{boundary_humidity}", 10, 100, 240, 3)# display some text on the screen
            else:
                display.text("Boundary humidity already max", 10, 10, 240, 3)
            display.update()  # update the display
            time.sleep(2)  # pause for a sec
            clear()  # clear to black again
        elif button_b.read():
            clear()
            display.set_pen(WHITE)
            if boundary_humidity > 0:
                boundary_humidity -= 1000
                display.text(f"Boundary humidity decreased to", 10, 10, 240, 3)  # display some text on the screen
                display.set_pen(MAGENTA)
                display.text(f"{boundary_humidity}", 10, 100, 240, 3)
            else:
                display.text("Boundary humidity already min", 10, 10, 240, 3)
            display.update()
            time.sleep(2)
            clear()
        elif button_x.read():
            X_Bar_Start = 0
            Y_POS = HEIGHT - 30  # Adjust the starting Y position as needed
            X_Bar_Width = WIDTH // 10  # Assuming 10 segments
            B_height = 30  # Adjust the height of the rectangles as needed
            clear()
            sensor_value2 = 90000
            for index, value in enumerate(range(boundary_humidity-1000, 140000, 10000)):
                
                if value <= sensor_value2:
                    display.set_pen(b_color[index])
                    # Calculate the coordinates and dimensions for the rectangle
                    x = X_Bar_Start + index * X_Bar_Width
                    y = Y_POS
                    width = X_Bar_Width
                    height = B_height

                    display.rectangle(x, y, width, height)
                    display.update()
            percentage_text = f"{int((sensor_value2 - 40000) / 1000)}%"
            # Calculate the coordinates for centering the text
            text_width = len(percentage_text) * 8  # Assuming bitmap8 font width
            text_height = 8  # Assuming bitmap8 font height

            text_x = (WIDTH - text_width) // 2 - 20
            text_y = (HEIGHT - text_height) // 2 - 30
            display.text(percentage_text, text_x, text_y, 240, 6)
            display.update()
            time.sleep(1)
            clear()
        elif button_y.read():
            clear()
            display.set_pen(WHITE)
            if last_watering == '' :
                last_watering = time.localtime()
            date_value = f"{last_watering[0]}-{last_watering[1]:02d}-{last_watering[2]:02d}"
            time_value = f"{last_watering[3]:02d} : {last_watering[4]:02d} : {last_watering[5]:02d}"
            #print(f"Last watering: \n {date_value} \n {time_value}")
            display.text(f"Last watering: \n {date_value} \n {time_value}",8,9,240,3)
              # Adjust the vertical position as needed
            display.update()
            time.sleep(3)
            clear()
        else:
            display.set_pen(WHITE)
            display.text(f"Boundary humidity={boundary_humidity}\n"
                         "A - increase boundary humidity\n"
                         "B - decrease boundary humidity\n"
                         "X - humidity level\n"
                         "Y - last watering", 7, 7, 240, 2)
            display.update()
        time.sleep(0.1)  # this number is how frequently the Pico checks for button presses
            

if __name__ == '__main__':
    setup()
    loop()

