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

class Bus(IPlugin, Message):
    def __init__(self):
        IPlugin.__init__(self)
        Message.__init__(self)

        self.text = control.SPEED_1 + '%s' + control.NEW_LINE + '%s'
        self.schedule = schedule.every(1).hours

        lines = [line.strip() for line in open('plugins/bus/bus.config').readlines()]
        config = {}
        for line in lines:
            line = line.split("=")
            config[line[0].strip()] = line[1].strip()

        self.agency = config["agency"]
        self.stop_id = config["stop_id"]
        self.ignore_routes = config["ignore_routes"].strip().split(",")

    def get_schedule(self):
        r = requests.get('http://' + "webservices.nextbus.com/service/publicXMLFeed?command=predictions&a="+ self.agency +"&stopId=" + self.stop_id + "&useShortTitles=true")
        soup = BeautifulSoup(r.text)
        schedule = {}

        for message in soup.findAll('predictions'):
            msg_attrs = dict(message.attrs) # loads the message attributes
            schedule['stop_name'] = Bus._convert(msg_attrs['stoptitle'])
            if message.find('direction') != None and not Bus._convert(msg_attrs['routetag']) in self.ignore_routes:
                for predict in message.find('direction').findAll('prediction'):
                    predict_attrs = dict(predict.attrs) # loads each prediction
                    schedule[Bus._convert(predict["minutes"])] = Bus._convert(msg_attrs["routetitle"]).translate(None, string.digits).rstrip() # adds the route name to the schedule with the wait time as the key
        return schedule

    
    @staticmethod
    def _convert(value):
        if type(value) == str:
            return value.encode('ascii', 'ignore')
        else:
            return str(value)


    def get_commands(self):
        w = self.get_schedule()
        keys = sorted(w.keys())
        if keys != None and len(keys) >= 1:
            return String( "%s %s %s: %s %s %s: %s" % (w['stop_name'], 
                control.NEW_LINE, 
                keys[0], 
                w[keys[0]], 
                control.NEW_LINE, 
                keys[1], 
                w[keys[1]]))
        else:
            return 'No stop predictions'


if __name__ == "__main__":
    bus = Bus()
    print bus.get_commands().data()