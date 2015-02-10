from yapsy.IPlugin import IPlugin
from manager.message import Message

import schedule
import random


class Test(IPlugin, Message):
    def __init__(self):
        IPlugin.__init__(self)
        Message.__init__(self)
        self.text = '<red>|%s| <amber>|%s| <green>|%s|'
        self.schedule = schedule.every(10).seconds

    def update(self):
        pass