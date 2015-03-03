__author__ = 'Carson'

# coding=utf-8

from yapsy.IPlugin import IPlugin
from manager.message import Message

from protocol.string import String
import protocol.control as control

import schedule
import requests
from bs4 import BeautifulSoup
import string
from string import digits

class NextBus(IPlugin, Message):
    def __init__(self):
        IPlugin.__init__(self)
        Message.__init__(self)

        self.text = control.SPEED_1 + '%s'
        self.schedule = schedule.every(1).minutes

        lines = [line.strip() for line in open('plugins/nextbus/nextbus.config').readlines()]
        config = {}
        for line in lines:
            line = line.split("=")
            config[line[0].strip()] = line[1].strip()

        self.agency = config["agency"]
        self.stop_id = config["stop_id"]
        self.ignore_routes = config["ignore_routes"].strip().split(",")

    def get_schedule(self):
        r = requests.get('http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=' + self.agency +
                         '&stopId=' + self.stop_id + '&useShortTitles=true')
        soup = BeautifulSoup(r.text)
        sched = {}

        for message in soup.findAll('predictions'):
            msg_attrs = dict(message.attrs) # loads the message attributes
            sched['stop_name'] = NextBus._convert(msg_attrs['stoptitle'])
            if message.find('direction') is not None and \
                    not NextBus._convert(msg_attrs['routetag']) in self.ignore_routes:
                for predict in message.find('direction').findAll('prediction'):
                    predict_attrs = dict(predict.attrs) # loads each prediction
                    # adds the route name to the schedule with the wait time as the key
                    sched[NextBus._convert(predict["minutes"])] = \
                        NextBus._convert(msg_attrs["routetitle"]).translate(None, string.digits).rstrip()
        return sched

    @staticmethod
    def _convert(value):
        if type(value) == str:
            return value.encode('ascii', 'ignore')
        else:
            return str(value)

    def get_commands(self):
        w = self.get_schedule()
        stop_name = w['stop_name']
        w.pop('stop_name', None)
        keys = [int(k) for k in w.keys()]
        keys.sort()

        if keys is not None and len(keys) >= 1:
            return (String("%s %s %d min: %s %s %d min: %s" %
                           (stop_name, control.NEW_LINE,
                            keys[0], w[str(keys[0])], control.NEW_LINE,
                            keys[1], w[str(keys[1])]), self.labels_string[0]), )

        return (String('No stop predictions', self.labels_string[0]), )
