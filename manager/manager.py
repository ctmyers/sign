from yapsy.PluginManager import PluginManager
import schedule


class Manager(object):
    def __init__(self):
        self.al_text = [chr(x) for x in range(0x20, 0x7F) if x not in [0x30]]
        self.al_string = [chr(x) for x in range(0x20, 0x7F) if x not in [0x30, 0x3F]]
        self.al_dots = [chr(x) for x in range(0x20, 0x7F)]

        plugin_manager = PluginManager()
        plugin_manager.setPluginPlaces(['../plugins', './plugins'])
        plugin_manager.collectPlugins()

        plugins = plugin_manager.getAllPlugins()
        for p in plugins:
            plugin = p.plugin_object
            self.allocate(plugin)

            print plugin.string_count()
            print plugin.dots_count()

    def allocate(self, plugin):

        def get_labels(labels, count):
            if len(labels) < count:
                raise ValueError('could not allocate file label (too many messages)')
            return tuple(labels.pop(0) for _ in range(count))

        plugin.set_labels(get_labels(self.al_text, 1)[0],
                          get_labels(self.al_string, plugin.string_count()),
                          get_labels(self.al_dots, plugin.dots_count()))
