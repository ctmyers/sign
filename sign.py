from protocol.interface import NetworkInterface
from protocol.text import Text, Message

import protocol.positions as positions
import protocol.modes as modes

sign = NetworkInterface()
sign.send(Text([Message('ayy', positions.TOP, modes.HOLD),
                Message('lmao', positions.BOTTOM, modes.FIREWORKS)]).command)