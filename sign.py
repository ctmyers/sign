#!/usr/bin/env python

from protocol.interface import NetworkInterface
from protocol.special import MemoryConfig
from protocol.text import Text, Message
from protocol.dots import Dots

import protocol.positions as positions
import protocol.modes as modes

from manager.manager import Manager

import time


sign = NetworkInterface()

manager = Manager()

# sign.send(MemoryConfig([dots]).command)
# time.sleep(6)

d = """ooooo   oooo  oooooooooo  ooooooooo
goooo   goog  goooggggoo   ooogggooo
 ooooo   oo    ooo    go   ooo    ooo
 ooooo   oo    ooo     g   ooo    ooo
 oooooo  oo    ooo         ooo    ooo
 oogooo  oo    ooo   o     ooo    ooo
 oo oooo oo    ooooooo     ooo   ooog
 oo gooo oo    ooogggo     oooooooog
 oo  ooo oo    ooo   g     oooggggg
 oo  gooooo    ooo         ooo
 oo   ooooo    ooo     o   ooo
 oo   goooo    ooo     o   ooo
 oo    oooo    ooo    oo   ooo
oooo   gooo   oooooooooo  ooooo
gggg    ggg   gggggggggg  ggggg"""

# sign.send(Dots(d).command)

# time.sleep(6)
# sign.send(Text([Message('ayy', positions.TOP, modes.HOLD),
#                 Message('rofl', positions.BOTTOM, modes.COMPRESSED_ROTATE),
#                 Message(Dots.call('A'))]).command)
