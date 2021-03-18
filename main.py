# led_timer.deinit()

"""
The irq() method accepts the following arguments:

trigger: this defines the trigger mode. There are 3 different conditions:

Pin.IRQ_FALLING: to trigger the interrupt whenever the pin goes from HIGH to LOW;

Pin.IRQ_RISING: to trigger the interrupt whenever the pin goes from LOW to HIGH.

3: to trigger the interrupt in both edges (this means, when any change is detected)

handler: this is a function that will be called when an interrupt is detected, in this case the handle_interrupt() function.

https://randomnerdtutorials.com/micropython-interrupts-esp32-esp8266/

# https://bulldogjob.pl/news/1342-pisanie-testow-jednostkowych-w-pythonie-dobre-praktyki

"""

from machine import Pin, Timer, I2C
from BME280 import BME280

from led import Led

scl = 5
sda = 4

i2c = I2C(scl=Pin(scl), sda=Pin(sda))
try:
    sensor = BME280(address=0x77, i2c=i2c)
except OSError as error:
    print("Sensor error: ", error)

red_LED = Led(0)
blue_LED = Led(2)
button = Pin(13, Pin.IN, Pin.PULL_UP)

led_timer = Timer(0)
debounce_timer = Timer(1)


def led_timer_callback(timer):
    blue_LED.led_toggle()
    print("LED changed!") # nie zalecane!!!


def read_button():
    button_value = button.value()

    if not button_value:
        print("button pressed!")

    return button_value


def red_led_on_button():
    button_value = button.value()

    if not button_value:
        print("button pressed!")
        red_LED.led_on()
    else:
        print("button depressed!")
        red_LED.led_off()


# Na początek zmieniamy wartość progu temperatury na 70 st:

def button_interrupt_callback(timer):
    red_led_on_button()
    check_sensor(70)
    return timer


# zastanówmy się jak sprawdzić czy dioda się zapaliła? Całe szczęście pisząc naszą klasę dla diody pamiętaliśmy o umieszczeniu returna zwaracającego wartość diody - to nam znacznie ułatwi testowanie.
# wprowdzimy też zmniany w funkcji sprawdzania temperatury, wykorzystując zwracaną wartość diody:

def check_sensor(alarm_threshold, test_temp_str: str = False):
    try:
        if not test_temp_str:
            temp_str = sensor.temperature
        else:
            temp_str = test_temp_str

    except (OSError, NameError) as err:
        print("Sensor error: ", err)
        return False
    else:
        print(temp_str)
        temp = round(float(temp_str[:-1]))
        if temp >= alarm_threshold:
            led_value = red_LED.led_on()
            print("LED VALUE: ", led_value)
        else:
            led_value = red_LED.led_off()
            print("LED VALUE: ", led_value)

        return led_value


def debounce(pin):
    # Start or replace a timer for 200ms, and trigger on_pressed.
    debounce_timer.init(mode=Timer.ONE_SHOT, period=200, callback=button_interrupt_callback)
    return pin


# led_timer.init(mode=Timer.PERIODIC, period=3000, callback=led_timer_callback)
button.irq(trigger=Pin.IRQ_FALLING, handler=debounce)

