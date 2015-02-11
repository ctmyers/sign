from yapsy.IPlugin import IPlugin
from manager.message import Message

from protocol.string import String
from protocol.dots import Dots

import schedule
import random


class Test(IPlugin, Message):
    def __init__(self):
        IPlugin.__init__(self)
        Message.__init__(self)
        self.text = '<red>|%s| <amber>[%s] <green>|%s| %d'
        self.schedule = schedule.every(5).seconds

    def get_commands(self):
        return [String('1', self.labels_string[0]).command,
                String('2', self.labels_string[1]).command,
                String('3', self.labels_string[2]).command,
                Dots('111\n222\n333', self.labels_dots[0]).command]

