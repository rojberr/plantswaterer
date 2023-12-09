import time
from machine import Pin, ADC
from pimoroni import Button, RGBLED
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P4

# SQLite
conn = sqlite3.connect('watering.db')
cursor = conn.cursor()

# create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS watering_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        watering_date TEXT,
        watering_time TEXT
    )
''')
conn.commit()

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
X_max = 134
Y_max = 239
X_Bar_Width = 40     #set a width for the bars
X_Bar_Start = round(((X_max / 2) - (X_Bar_Width / 2))) #Find start point so bar is centered


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

#define bar graph segment colors:
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

def show_moisture_level(sensor_value):
    B_height = 20                         #Bar height setting for each segment
    Y_POS = Y_max -B_height                 #Start at bottom, move upwards
    for index, value in enumerate(range(50000, 150000, 10000)):                  #Step through all 10 segments
        if (value <= sensor_value):                    #If this segment 'b' is within level range
            display.set_pen(b_color[index])     #Set it's color for this position
        else:                               #
            display.set_pen(BLACK)          #Set color to erase a previous color
                                            #Draw the rectangle to create the bar
        display.rectangle(X_Bar_Start,Y_POS,X_Bar_Width,B_height)  
        display.update()                    #Update display to reflect new data
        Y_POS -= B_height                   #Decrement position for next bar

def log_watering():
    watering_time = time.localtime()
    date_value = f"{watering_time.tm_year}-{watering_time.tm_mon:02d}-{watering_time.tm_mday:02d}"
    time_value = f"{watering_time.tm_hour:02d}:{watering_time.tm_min:02d}:{watering_time.tm_sec:02d}"
    cursor.execute('INSERT INTO watering_log (watering_date, watering_time) VALUES (?, ?)', (date_value, time_value))
    conn.commit()

def display_last_watering():
    cursor.execute('SELECT * FROM watering_log ORDER BY watering_date, watering_time DESC LIMIT 1')
    last_watering = cursor.fetchone()
    if last_watering:
        last_watering_str = f"{last_watering[1]} - {last_watering[2]}"
    else:
        last_watering_str = "No records"
    picodisplay.set_pen(255, 255, 255)
    picodisplay.clear()
    picodisplay.text("Last watering:", 10, 10, 200, 3)
    picodisplay.text(last_watering_str, 10, 40, 200, 3)
    picodisplay.update()
    time.sleep(1)
    picodisplay.clear()

def display_current_moisture(sensor_value):
    picodisplay.set_pen(255, 255, 255)
    picodisplay.clear()
    picodisplay.text("Current Moisture:", 10, 10, 200, 3)
    picodisplay.text(f"{sensor_value}%", 10, 40, 200, 3)
    picodisplay.update()
    time.sleep(1)
    picodisplay.clear()

def loop():
    boundary_humidity = 50000
    while True:
        time.sleep(0.2)  # wait for 0.5 seconds
        print("Plant - Moisture Level:")
        sensor_value = sensor_in.read_u16()
        print(sensor_value)
        show_moisture_level(sensor_value) 
        log_watering()
        if sensor_value > boundary_humidity:
            motor_out.high()  # turn the motor on
        else:
            motor_out.high()  # turn the motor off

        if button_a.read():  # if a button press is detected then...
            display_last_watering()     #show when was last watering
        elif button_b.read():
            display_current_moisture(sensor_value)  #show current moisture
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
