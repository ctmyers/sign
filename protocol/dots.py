from command import Command
import control


class Dots(object):
    def __init__(self, dots, label='A', locked=True):
        self.dots = dots
        self.label = label
        self.locked = locked
        self.height = len(dots)
        self.width = len(dots[0])

        data = []
        for row in dots:
            if len(row) != self.width:
                raise ValueError('malformed dot matrix')

            for dot in row:
                data.append(str(dot))

            data.append(control.NEW_LINE)
        data = ''.join(data)

        self.command = Command("%s%s%s%s%s" % (control.WRITE_SMALL_DOTS, label,
                                               "%02X" % self.height,
                                               "%02X" % self.width, data))

    @staticmethod
    def call(label):
        return control.CALL_SMALL_DOTS + label
