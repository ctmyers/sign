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
manager = Manager(sign)

# sign.send(MemoryConfig([dots]).command)
# time.sleep(6)

d = """
ooooo   oooo  oooooooooo  ooooooooo    ooooooooo    ooooo   oooo  g
goooo   goog  goooggggoo   ooogggooo    ooogggooo   gooog   goog  gg
 ooooo   oo    ooo    go   ooo    ooo   ooo    ooo   ooo     oo    gggg
 ooooo   oo    ooo     g   ooo    ooo   ooo    ooo   ooo     oo    ggggr
 oooooo  oo    ooo         ooo    ooo   ooo    ooo   ooo     oo    ggrrrrr
 oogooo  oo    ooo   o     ooo    ooo   ooo    ooo   ooo     oo    grrrrrrr
 oo oooo oo    ooooooo     ooo   ooog   ooo   ooog   ooo     oo    rrrrrrrrrr
 oo gooo oo    ooogggo     oooooooog    oooooooog    ooo     oo     rrrrrrrrrrr
 oo  ooo oo    ooo   g     oooggggg     oooggggg     ooo     oo      rrrrrrrrrrr
 oo  gooooo    ooo         ooo          ooo          ooo     oo      rrrrrrrrrrr
 oo   ooooo    ooo     o   ooo          ooo          ooo     oo       rrrrrrrrrr
 oo   goooo    ooo     o   ooo          ooo          ooo     oo        rrrrrrrrr
 oo    oooo    ooo    oo   ooo          ooo          gooo   oog         rrrrrrrr
oooo   gooo   oooooooooo  ooooo        ooooo          goooooog           rrrrrrr
gggg    ggg   gggggggggg  ggggg        ggggg           gggggg             rrrrrr"""

# sign.send(Dots(d).command)

# time.sleep(6)

# sign.send(Text([Message('ayy', positions.TOP, modes.HOLD),
#                 Message('rofl', positions.BOTTOM, modes.COMPRESSED_ROTATE),
#                 Message(Dots.call('A'))]).command)
