from protocol.text import Text
from protocol.string import String
from protocol.dots import Dots
import protocol.control as control


class Message(object):

    def __init__(self):
        self.text = None
        self.schedule = None

        self.label = None
        self.labels_string = ()
        self.labels_dots = ()

    def text_command(self):
        cmd = self.text
        for s in self.labels_string:
            cmd = cmd.replace('%s', String.call(s), 1)
        for d in self.labels_dots:
            cmd = cmd.replace('%d', Dots.call(d), 1)
        return Text(cmd, self.label)

    def get_commands(self):
        """ Returns a list of string and dots commands that will be sent """
        return []

    def set_labels(self, text, strings, dots):
        self.label = text
        self.labels_string = strings
        self.labels_dots = dots

    def string_count(self):
        return self.text.count("%s")

    def string_lengths(self):
        return (100,) * self.string_count()

    def dots_count(self):
        return self.text.count("%d")

    def dots_sizes(self):
        return ({'width': 80, 'height': 16},) * self.dots_count()

    def to_config(self):
        t = [Text(messages=self.text, label=self.label)]

        s = [String('', self.labels_string[i],
                    self.string_lengths()[i])
             for i in range(self.string_count())]

        d = [Dots('', label=self.labels_dots[i],
                  width=self.dots_sizes()[i]['width'],
                  height=self.dots_sizes()[i]['height'])
             for i in range(self.dots_count())]

        return t + s + d
