from protocol.interface import NetworkInterface
from protocol.special import MemoryConfig
from protocol.text import Text, Message
from protocol.dots import Dots

import protocol.positions as positions
import protocol.modes as modes


import time


sign = NetworkInterface()

sign.send(MemoryConfig([dots]).command)

time.sleep(6)

sign.send(Dots(['00000111100000',
                '00011111111000',
                '00111111111100',
                '01111111111110',
                '11111111111110',
                '11111111111110',
                '11111111111111',
                '11111111111111',
                '10000111100010',
                '10000111000000',
                '00000011000010',
                '01000111000100',
                '00111111111100',
                '00011111111000',
                '00001111100000',
                '00000011000000']).command)
time.sleep(6)

sign.send(Text([Message('ayy', positions.TOP, modes.HOLD),
                Message('lmao', positions.BOTTOM, modes.COMPRESSED_ROTATE),
                Message(Dots.call('A'))]).command)
