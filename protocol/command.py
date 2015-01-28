from config import config
import control


class Command(object):
    def __init__(self, data, typecode=config.typecode, address=config.address):
        self.data = "%s%s%s%s%s%s%s" % (control.NUL * 5, control.SOH,
                                        typecode, address, control.STX,
                                        data, control.EOT)
