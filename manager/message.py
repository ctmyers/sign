from Queue import Queue


class Message(object):

    def __init__(self):
        self.text = None
        self.schedule = None

        self.label = None
        self.labels_string = ()
        self.labels_dots = ()

        self.messages = Queue()

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
        return ((16, 16),) * self.dots_count()

    def update(self):
        pass
