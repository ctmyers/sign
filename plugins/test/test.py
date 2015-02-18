from yapsy.IPlugin import IPlugin
from manager.message import Message

from protocol.dots import Dots

import protocol.positions as positions
import protocol.control as control

import schedule


class Test(IPlugin, Message):
    def __init__(self):
        IPlugin.__init__(self)
        Message.__init__(self)

        self.text = control.SPEED_1 + '%d'
        self.schedule = schedule.every(1).minutes

        self.position = positions.MIDDLE

    def get_commands(self):
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

        return (Dots(d, self.labels_dots[0]), )

