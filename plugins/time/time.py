from yapsy.IPlugin import IPlugin
from manager.message import Message

import protocol.control as control
import schedule


class Time(IPlugin, Message):
    def __init__(self):
        IPlugin.__init__(self)
        Message.__init__(self)

        self.text = control.SPEED_1 + '\x0B9 \x0B8' + control.NEW_LINE + control.CALL_TIME
        self.schedule = schedule.every(3).hours
