from config import config
import control


class Command(object):
    def __init__(self, typecode=config.typecode, address=config.address):
        self.typecode = typecode
        self.address = address
        self._command = ''
        self._data = None

    def data(self):
        if self._data is None:
            self._data = "%s%s%s%s%s%s%s" % (control.NUL * 5, control.SOH,
                                             self.typecode, self.address,
                                             control.STX, self._command, control.EOT)
        return self._data