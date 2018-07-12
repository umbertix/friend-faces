import pytest
from friendFaces import FriendFaces

main = FriendFaces()


def test_set_lamp_status():
    main.set_lamp_to_status()
    assert main.lamp_status == 'off'

    main.lamp_status = 'on'
    assert main.lamp_status == 'on'


def test_lamp_on():
    main.manual_turn_on()
    assert main.lamp_status == 'on'


def test_lamp_off():
    main.manual_turn_off()
    assert main.lamp_status == 'off'
