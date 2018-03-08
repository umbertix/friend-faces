import time
from server import Server
from neopixel import *

import signal
import sys

HELLO_TIME = 1.5
COLOR = Color(255, 0, 0)  # Red

PUSHER_CHANNELNAME = 'friend-faces-channel'
PUSHER_APPKEY = 'b13d772cddbd6c3212fe'
PUSHER_APPSECRET = '97f73f04e6d8fb7a5811'
PUSHER_APPID = '485602'
PUSHER_CLUSTER = 'eu'

# LED strip configuration:
LED_COUNT = 12  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP = ws.WS2811_STRIP_GRB  # Strip type and colour ordering

# Touch sensor configuration
TOUCH_PIN = 1  # GPIO pin connected to the sensor.


class Main():
    def __init__(self):
        self.server = Server(PUSHER_APPID, PUSHER_APPKEY, PUSHER_APPSECRET, PUSHER_CHANNELNAME, PUSHER_CLUSTER)
        self.assignGPIOs()
        self.bindGPIOs()
        self.strip = Adafruit_NeoPixel(
            LED_COUNT,
            LED_PIN,
            LED_FREQ_HZ,
            LED_DMA,
            LED_INVERT,
            LED_BRIGHTNESS,
            LED_CHANNEL,
            LED_STRIP)
        self.strip.begin()  # Initialize neopixel library
        self.rainbow(self.strip)

    def assign_gpios(self):
        """Assigns and initializes all gpios inputs and outputs"""
        self.leds = new
        Gpio(17, 'out')
        self.button1 = new
        Gpio(4, 'in')
        self.button2 = new
        Gpio(5, 'in')
        self.button3 = new
        Gpio(6, 'in')
        self.button4 = new
        Gpio(7, 'in')
        self.button5 = new
        Gpio(8, 'in')

    def bind_gpios(self):
        """Bind all the GPIOS to their own events"""

    def say_hello_button(self):
        self.server.broadcastHello(channelName, 'Hello title', 'Hello message')

    def received_hello(self):
        """turn on the light for X seconds"""
        self.rainbow(self.strip)

    def changeColorOnTouch(self):
        """Change the color incrementally while pressing the button"""

    def saveColorInMemory(self, color):
        """Saves the color into the SD card to reuse"""

    @staticmethod
    def loadColorFromMemory():
        """Retrieves the color from the SD card"""
        # TODO: Implement, returning blue atm.
        return Color(0, 255, 0)

    @staticmethod
    def manualTurnOn(strip):
        """manually turns on the lamp"""
        for i in range(max(strip1.numPixels(), strip1.numPixels())):
            strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()

    @staticmethod
    def manualTurnOff(strip):
        """Manually turns off the lamp"""
        for i in range(max(strip1.numPixels(), strip1.numPixels())):
            strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()

    @staticmethod
    def wheel(pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170

        return Color(0, pos * 3, 255 - pos * 3)

    def rainbow(self, strip, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256 * iterations):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, wheel((i + j) & 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
        self.manualTurnOff()
