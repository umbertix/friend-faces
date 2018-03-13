# Friend faces

Interconnected touch activated lamps

### Aim of the project
The aim of this project is to create a pair of "lamps" that are interconnected through internet over wifi and that respond to the event of each other.
The "lamp" will hold up to 5 capacitive sensors (touch/proximity) and will run different actions on the lamp.

- Manually activate the LED ring
- Manually deactivate the LED ring
- Change the color of the LED ring gradually, and save the resultant color.
- Send greetings. Send a "ping" message to the other lamp <- This was my main goal

### Requirements
The links to the components are just a suggestion on where to get them. Internet is full of shops selling the very same components.
- [Raspberry Pi Zero Wireless](https://www.adafruit.com/product/3400) (Raspberry Pi Z W)
- MicroSD card for the Pi
- [NeoPixel LED ring](https://www.adafruit.com/product/1643) (default 12 leds)
- A free account in [Pusher](www.pusher.com)
- [Capacitive sensor]((https://www.adafruit.com/product/1362)) (5-pad)
- You will also need some electric cables to connect everything together. 

### Installation

- Install Raspbian into the Raspberry
- Set up the wifi. (I recommend using a headless installation)
- SSH into the raspberry
- [Install the rpi_ws281x Library](https://learn.adafruit.com/neopixels-on-raspberry-pi/software)
    - sudo apt-get update
    - sudo apt-get install build-essential python-dev git scons swig
    - git clone https://github.com/jgarff/rpi_ws281x.git
    - cd rpi_ws281x
    - scons
    - cd python
    - sudo python setup.py install
- Install the project
    - git clone https://github.com/umbertix/friend-faces.git
    - cd friend-faces
    - sudo python setup.py install
-Config your lamp
    - Within the project there is file named `config.ini` and hold your credentials for the pusher service.
    You will need to update those in order to communicate, also if you decide to use any other pin setup or ring size.
