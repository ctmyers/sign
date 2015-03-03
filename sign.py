#!/usr/bin/env python

from protocol.interface import NetworkInterface
from manager.manager import Manager
from protocol.special import Date, TimeOfDay, DayOfWeek

sign = NetworkInterface()

# set current time
sign.send(Date())
sign.send(TimeOfDay())
sign.send(DayOfWeek())

# run plugins
manager = Manager(sign)
manager.run()
