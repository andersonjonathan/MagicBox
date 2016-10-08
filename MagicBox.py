from time import sleep

import serial
from threading import Thread

from utils.volume import set_volume


class MagicBox:
    _raw_pins = {'A0': 0,
                 'A1': 0,
                 'D0': 0,
                 'D1': 0,
                 'D2': 0,
                 'D11': 0,
                 'D12': 0,
                 'B0': 0,
                 'B1': 0,
                 'B2': 0}

    LEFT_BUTTON = 0
    CENTER_BUTTON = 1
    RIGHT_BUTTON = 2

    UP = 0
    CENTER = 1
    DOWN = 2

    LEFT_SWITCH = 3
    RIGHT_SWITCH = 4

    CENTER_WHEEL_INNER = 5
    CENTER_WHEEL_OUTER = 6

    def __init__(self, serial_port='/dev/ttyACM0'):
        self.serial_port = serial_port
        self.thread = Thread(target=self.read_serial)  # thread used to update the data from the serial interface.
        self.thread.start()

    def read_serial(self):
        ser = serial.Serial(self.serial_port)
        while True:
            res = ser.readline().decode("utf-8")
            res = res.rstrip()
            key, val = res.split(':')
            val = int(val)
            # if val < 2 or not self._raw_pins[key] in [val-1, val, val+1]:  # Only update if the change is significant
            self._raw_pins[key] = val

    def is_pressed(self, button):
        if button == MagicBox.LEFT_BUTTON:
            return self._raw_pins['B2'] == 1
        elif button == MagicBox.CENTER_BUTTON:
            return self._raw_pins['B1'] == 1
        elif button == MagicBox.RIGHT_BUTTON:
            return self._raw_pins['B0'] == 1

    def get_switch_state(self, switch):
        if switch == MagicBox.LEFT_SWITCH:
            if self._raw_pins['D11'] == 1:
                return MagicBox.CENTER
            elif self._raw_pins['D12'] == 1:
                return MagicBox.DOWN
        elif switch == MagicBox.RIGHT_SWITCH:
            if self._raw_pins['D0'] == 1:
                return MagicBox.UP
            elif self._raw_pins['D1'] == 1:
                return MagicBox.CENTER
            elif self._raw_pins['D2'] == 1:
                return MagicBox.DOWN

    @staticmethod
    def _calc_center_wheel_percentage(value):
        return max(min(int(abs(value * value - 448900) / 4489), 100), 0)

    def wheel_in_percentage(self, wheel):
        if wheel == MagicBox.CENTER_WHEEL_INNER:
            return self._calc_center_wheel_percentage(self._raw_pins['A0'])
        elif wheel == MagicBox.CENTER_WHEEL_OUTER:
            return self._calc_center_wheel_percentage(self._raw_pins['A1'])


def main():
    box = MagicBox()
    while True:
        left = box.wheel_in_percentage(MagicBox.CENTER_WHEEL_INNER)
        right = box.wheel_in_percentage(MagicBox.CENTER_WHEEL_OUTER)
        set_volume(left, right)
        sleep(0.5)


if __name__ == '__main__':
    main()
