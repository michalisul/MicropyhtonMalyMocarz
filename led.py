from machine import Pin


class Led:

    def __init__(self, pin: int):
        self.led = Pin(pin, Pin.OUT)

    # określamy co nasze funkcja ma robić:

    def led_on(self):
        self.led.off()
        return self.led.value()

    def led_off(self):
        self.led.on()
        return self.led.value()

    def led_toggle(self):
        led_value = self.led.value()

        if led_value:
            self.led_on()
        else:
            self.led_off()