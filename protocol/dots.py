from command import Command
import control


class Dots(object):

    OFF = '0'
    RED = '1'
    GREEN = '2'
    ORANGE = '3'
    colors = {' ': OFF, 'r': RED, 'g': GREEN, 'o': ORANGE}

    def __init__(self, dots, label='A', locked=True, width=None, height=None):
        self.dots = dots
        self.label = label
        self.locked = locked

        if type(dots) == str:
            dots = dots.split('\n')

        self.height = height if height else len(dots)
        if width:
            self.width = width
        else:
            m = 0
            for row in dots:
                m = max(0, len(row))
            self.width = m

        data = []
        for row in dots:
            if len(row) != self.width:
                raise ValueError('malformed dot matrix')

            for dot in row:
                if dot in Dots.colors:
                    dot = Dots.colors[dot]
                data.append(str(dot))

            data.append(control.NEW_LINE)
        data = ''.join(data)

        self.command = Command("%s%s%s%s%s" % (control.WRITE_SMALL_DOTS, label,
                                               "%02X" % self.height,
                                               "%02X" % self.width, data))

    @staticmethod
    def call(label):
        return control.CALL_SMALL_DOTS + label
