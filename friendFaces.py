import time
import configparser
from server import Server
from neopixel import *
from gpiozero import Button


class FriendFaces:
    def __init__(self):
        self.cfg = configparser.ConfigParser()
        self.load_config()

        self.default_color_r = self.cfg.get('GENERAL', 'COLOR_R')
        self.default_color_g = self.cfg.get('GENERAL', 'COLOR_G')
        self.default_color_b = self.cfg.get('GENERAL', 'COLOR_B')

        self.server = Server(
            self.cfg.get('PUSHER', 'APPID'),
            self.cfg.get('PUSHER', 'APPKEY'),
            self.cfg.get('PUSHER', 'APPSECRET'),
            self.cfg.get('PUSHER', 'CHANNELNAME'),
            self.cfg.get('PUSHER', 'CLUSTER')
        )

        self.initializes_gpios()

        self.strip = Adafruit_NeoPixel(
            self.cfg.getint('LED', 'COUNT'),
            self.cfg.getint('LED', 'PIN'),
            self.cfg.getint('LED', 'FREQ_HZ'),
            self.cfg.getint('LED', 'DMA'),
            self.cfg.getint('LED', 'INVERT'),
            self.cfg.getint('LED', 'BRIGHTNESS'),
            self.cfg.getint('LED', 'CHANNEL'),
            self.cfg.getint('LED', 'STRIP')
        )
        self.strip.begin()  # Initialize neopixel library
        self.rainbow(self.strip)

    def load_config(self):
        """Loads the configuration from the file"""
        self.cfg.read('config.ini')

    def save_config(self):
        """Saves the configuration to the file"""
        with open('config.ini', 'w') as configfile:
            self.cfg.write(configfile)

    def initializes_gpios(self):
        """Initializes each button to the configured pin and bind's the event to the button"""
        self.button = Button(self.cfg.getint('TOUCH', 'PIN'))
        self.button1 = Button(self.cfg.getint('TOUCH', 'PIN1'))
        self.button2 = Button(self.cfg.getint('TOUCH', 'PIN2'))
        self.button3 = Button(self.cfg.getint('TOUCH', 'PIN3'))
        self.button4 = Button(self.cfg.getint('TOUCH', 'PIN4'))

        # Say hello button
        self.button.when_pressed = self.say_hello_button

        # Changing color button
        self.button1.when_held = self.change_color_on_touch
        self.button1.when_released = self.save_color_in_memory

        # Manual ON
        self.button2.when_pressed = self.manual_turn_on

        # Manual OFF
        self.button3.when_pressed = self.manual_turn_off

    def say_hello_button(self):
        self.server.send_message(
            'Hello title',
            'Hello message'
        )

    def received_hello(self):
        """turn on the light for X seconds"""
        self.rainbow(self.strip)

    def change_color_on_touch(self):
        """Change the color incrementally while pressing the button and returns the value"""
        r = self.default_color_r
        g = self.default_color_g
        b = self.default_color_b

        if r > 0 & b == 0:
            r -= 1
            g += 1

        if g > 0 & r == 0:
            g -= 1
            b += 1

        if b > 0 & g == 0:
            r += 1
            b -= 1

        self.default_color_r = r
        self.default_color_g = g
        self.default_color_b = b

    def save_color_in_memory(self):
        """Saves the color into the SD card to reuse"""
        self.cfg['GENERAL']['COLOR_R'] = self.default_color_r
        self.cfg['GENERAL']['COLOR_G'] = self.default_color_g
        self.cfg['GENERAL']['COLOR_B'] = self.default_color_b
        self.save_config()

    def manual_turn_on(self):
        strip = self.strip
        """manually turns on the lamp"""
        for i in range(max(strip.numPixels(), strip.numPixels())):
            strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()

    def manual_turn_off(self):
        strip = self.strip
        """Manually turns off the lamp"""
        for i in range(max(strip.numPixels(), strip.numPixels())):
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

    def rainbow(self, wait_ms=20, iterations=1):
        strip = self.strip
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256 * iterations):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, self.wheel((i + j) & 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
        self.manual_turn_off()
