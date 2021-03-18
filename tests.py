import unittest
import main


class TestUnittestAssertions(unittest.TestCase):

    def test_LED_instance(self):
        self.test_LED = main.red_LED
        self.assertIsInstance(self.test_LED, main.Led)

# sprawdzamy czy włączy się gdy temperatura przekroczy 70 st.
    def test_temperature_check_led_on(self):
        # temperature 71 C
        self.test_LED = main.red_LED
        self.test_LED.led_off()
        led_value = main.check_sensor(alarm_threshold=70, test_temp_str="71C")
        self.assertEqual(led_value, 0)  # LED should be ON - 0





