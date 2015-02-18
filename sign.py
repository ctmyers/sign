#!/usr/bin/env python

from protocol.interface import NetworkInterface
from manager.manager import Manager
from protocol.special import TimeOfDay, DayOfWeek

sign = NetworkInterface()

# set current time
sign.send(TimeOfDay())
sign.send(DayOfWeek())

# run plugins
manager = Manager(sign)
manager.run()
