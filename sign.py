from protocol.interface import NetworkInterface
from protocol.special import MemoryConfig
from protocol.text import Text, Message
from protocol.dots import Dots

import protocol.positions as positions
import protocol.modes as modes

import time


sign = NetworkInterface()

#sign.send(MemoryConfig([dots]).command)
#time.sleep(6)


d = ['     rrrr     ',
     '   rrrrrrrr   ',
     '  rrrrrrrrrr  ',
     ' rrrrrrrrrrrr ',
     'rrrrrrrrrrrrr ',
     'rrrrrrrrrrrrr ',
     'rrrrrrrrrrrrrr',
     'rrrrrrrrrrrrrr',
     'r    rrrr   r ',
     'r    rrr      ',
     '  g   rr g  r ',
     ' r   rrr   r  ',
     '  rrrrrrrrrr  ',
     '   rrrrrrrr   ',
     '    rrrrr     ',
     '      rr      ']

sign.send(Dots(d).command)
time.sleep(6)

sign.send(Text([Message('ayy', positions.TOP, modes.HOLD),
                Message('lmao', positions.BOTTOM, modes.COMPRESSED_ROTATE),
                Message(Dots.call('A'))]).command)
