#!/usr/bin/env python

from protocol.interface import NetworkInterface
from manager.manager import Manager

sign = NetworkInterface()
manager = Manager(sign)
manager.run()
