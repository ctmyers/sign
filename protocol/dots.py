from command import Command
import control


class Dots(object):

    OFF = '0'
    RED = '1'
    GREEN = '2'
    AMBER = '3'

    colors = {' ': OFF, 'r': RED, 'g': GREEN, 'a': AMBER, 'o': AMBER}

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
            self.width = 0
            for row in dots:
                self.width = max(self.width, len(row))

        data = []
        for row in dots:
            for dot in row:
                if dot in Dots.colors:
                    dot = Dots.colors[dot]
                data.append(str(dot))
            
            while len(data) < self.width:
                data.append(Dots.OFF)

            data.append(control.NEW_LINE)
        data = ''.join(data)

        self.command = Command("%s%s%s%s%s" % (control.WRITE_SMALL_DOTS, label,
                                               "%02X" % self.height,
                                               "%02X" % self.width, data))

    @staticmethod
    def call(label):
        return control.CALL_SMALL_DOTS + label
