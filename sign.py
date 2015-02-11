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
manager.run()

d = """ooooo   oooo  oooooooooo  ooooooooo    ooooooooo    ooooo   oooo  o
goooo   goog  goooggggoo   ooogggooo    ooogggooo   gooog   goog  oo
 ooooo   oo    ooo    go   ooo    ooo   ooo    ooo   ooo     oo    oooo
 ooooo   oo    ooo     g   ooo    ooo   ooo    ooo   ooo     oo    oooog
 oooooo  oo    ooo         ooo    ooo   ooo    ooo   ooo     oo    ooggggg
 oogooo  oo    ooo   o     ooo    ooo   ooo    ooo   ooo     oo    oggggggg
 oo oooo oo    ooooooo     ooo   ooog   ooo   ooog   ooo     oo    gggggggggg
 oo gooo oo    ooogggo     oooooooog    oooooooog    ooo     oo     ggggggggggg
 oo  ooo oo    ooo   g     oooggggg     oooggggg     ooo     oo      ggggggggggg
 oo  gooooo    ooo         ooo          ooo          ooo     oo      ggggggggggg
 oo   ooooo    ooo     o   ooo          ooo          ooo     oo       gggggggggg
 oo   goooo    ooo     o   ooo          ooo          ooo     oo        ggggggggg
 oo    oooo    ooo    oo   ooo          ooo          gooo   oog         gggggggg
oooo   gooo   oooooooooo  ooooo        ooooo          goooooog           ggggggg
gggg    ggg   gggggggggg  ggggg        ggggg           gggggg             gggggg"""

"""
msgs = list()

msgs.append(Text([Message('heyy', positions.TOP, modes.HOLD),
                  Message('rofl', positions.BOTTOM, modes.COMPRESSED_ROTATE),
                  Message(Dots.call('D'))]))


msgs.append(Dots(d, label='D'))

sign.send(MemoryConfig(msgs))

for m in msgs:
    sign.send(m)
"""
