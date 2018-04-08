import time
import datetime
import configparser
import json
import logging
from sender import Sender
from receiver import Receiver
from neopixel import *
from gpiozero import Button
from logging.handlers import RotatingFileHandler

class FriendFaces:
    def __init__(self):
        self.init_logger()
        self.logger.debug('Initializing.....')
        self.cfg = configparser.ConfigParser()
        self.load_config()
        self.set_colors()
        self.logger.debug('Initializing sender....')
        self.lamp_status = 'off'

        # Sender will be used to send messages to the channel
        self.sender = Sender(
            self.cfg.get('PUSHER', 'APP_ID'),
            self.cfg.get('PUSHER', 'APP_KEY'),
            self.cfg.get('PUSHER', 'APP_SECRET'),
            self.cfg.get('PUSHER', 'CHANNEL_NAME'),
            self.cfg.get('PUSHER', 'CLUSTER'),
            encrypted=False
        )
        self.logger.debug('Initializing receiver....')
        self.receiver = Receiver(
            self.cfg.get('PUSHER', 'APP_KEY'),
            self.cfg.get('PUSHER', 'APP_SECRET'),
            self.cfg.get('PUSHER', 'CHANNEL_NAME'),
            self.cfg.get('PUSHER', 'EVENT_NAME'),
            self.received_hello
        )
        self.initializes_gpios()
        self.strip = Adafruit_NeoPixel(
            self.cfg.getint('LED', 'COUNT'),
            self.cfg.getint('LED', 'PIN'),
        )

        self.strip.begin()  # Initialize neopixel library
        self.set_brightness()
        self.logger.debug('!! READY !!')
        self.visual_feedback()

    def load_config(self):
        """Loads the configuration from the file"""
        self.logger.debug('Loading config')
        self.cfg.read('config.ini')

    def save_config(self):
        """Saves the configuration to the file"""
        self.logger.debug('Saving config')
        with open('config.ini', 'w') as configfile:
            self.cfg.write(configfile)

    def initializes_gpios(self):
        """Initializes each button to the configured pin and bind's the event to the button"""
        self.logger.debug('Initializing gpios....')
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
        self.logger.debug('Say Hello button')
        data = '{"sender": "' + self.cfg.get('PUSHER', 'SENDER_NAME') + '", "effect": "' + self.cfg.get('PUSHER', 'SENDER_EFFECT') + '"}'
        self.sender.send_message(
            self.cfg.get('PUSHER', 'EVENT_NAME'),
            data
        )

    def received_hello(self, *args, **kwargs):
        """turn on the light for X seconds"""
        self.logger.debug('Received !!!!!!!!!!')
        message_received = json.loads(args[0])
        self.logger.debug(message_received['sender'])
        self.logger.debug(message_received['effect'])
        if message_received['sender'] != self.cfg.get('PUSHER', 'SENDER_NAME'):
            self.visual_feedback(message_received['effect'])

    def change_color_on_touch(self):
        """Change the color incrementally while pressing the button and returns the value"""
        self.logger.debug('Changing color')
        r = self.default_color_r
        g = self.default_color_g
        b = self.default_color_b
        i = 0
        while self.button1.is_held or self.button1.is_pressed:
            i += 1
            if r > 0 and b == 0:
                r -= 1
                g += 1

            if g > 0 and r == 0:
                g -= 1
                b += 1

            if b > 0 and g == 0:
                r += 1
                b -= 1

            if i % 50 == 0:
                self.color_wipe(Color(r, g, b))
                time.sleep((self.strip.numPixels() * 10) / 1000.0)

        self.default_color_r = r
        self.default_color_g = g
        self.default_color_b = b

    def save_color_in_memory(self):
        """Saves the color into the SD card to reuse"""
        self.logger.debug('Saving color settings in permanent memory')
        self.cfg['GENERAL']['COLOR_R'] = str(self.default_color_r)
        self.cfg['GENERAL']['COLOR_G'] = str(self.default_color_g)
        self.cfg['GENERAL']['COLOR_B'] = str(self.default_color_b)
        self.set_colors()
        self.save_config()

    def manual_turn_on(self):
        """manually turns on the lamp"""
        self.logger.debug('ON')
        self.color_wipe(self.onColor)
        self.lamp_status = 'on'

    def manual_turn_off(self):
        """Manually turns off the lamp"""
        self.logger.debug('OFF')
        self.color_wipe(self.offColor)
        self.lamp_status = 'off'

    def color_wipe(self, color, wait_ms=60):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

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
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256 * iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((i + j) & 255))
            self.strip.show()
            time.sleep(wait_ms / 1000.0)
        self.manual_turn_off()

    def rainbow_cycle(self, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256*iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((int(i * 256 / self.strip.numPixels()) + j) & 255))
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def theater_chase_rainbow(self, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, self.wheel((i+j) % 255))
                self.strip.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, 0)

    def theater_chase(self, color, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, color)
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)

    def flash_effect(self):
        for q in range(20):
            self.color_wipe(self.flashColor, 1)
            self.color_wipe(self.offColor, 1)

    def visual_feedback(self, effect='wipe'):
        """Flash a color for Time and goes back to black"""
        self.logger.debug('Flashing')
        if effect == 'rainbow':
            self.rainbow()
        elif effect == 'chase':
            self.theater_chase(self.flashColor)
        elif effect == 'flash':
            self.flash_effect()
        else:
            self.color_wipe(self.flashColor)

        time.sleep(500 / 1000.0)
        self.set_lamp_to_status()

    def set_brightness(self):
        """Sets a lower brightness when at night"""
        self.logger.debug('Setting brightness')
        now = datetime.datetime.now()

        # Low light during 19-8 o'clock
        if 8 < now.hour < 19:
            self.strip.setBrightness(200)
        else:
            self.strip.setBrightness(15)

    def set_colors(self):
        """Sets the colors with the desired values"""
        self.logger.debug('Setting flash color')
        self.default_color_r = self.cfg.getint('GENERAL', 'COLOR_R')
        self.default_color_g = self.cfg.getint('GENERAL', 'COLOR_G')
        self.default_color_b = self.cfg.getint('GENERAL', 'COLOR_B')
        self.onColor = Color(self.default_color_r, self.default_color_g, self.default_color_b)
        self.flashColor = Color(48, 24, 201)
        self.offColor = Color(0, 0, 0, 1)

    def init_logger(self):
        """Initializes the logging with the rotating config"""
        self.logger = logging.getLogger('my_logger')
        self.logger.setLevel(logging.DEBUG)
        handler = RotatingFileHandler('my_log.log', maxBytes=2000, backupCount=3)
        self.logger.addHandler(handler)

    def set_lamp_to_status(self):
        if self.lamp_status == 'off':
            self.manual_turn_off()
        else:
            self.manual_turn_on()
