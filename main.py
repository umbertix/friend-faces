from friendFaces import FriendFaces
from neopixel import *

try:
    main = FriendFaces()
    while True:
        pass
except KeyboardInterrupt:
    main.colorWipe(main.offColor)
