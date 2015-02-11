from yapsy.IPlugin import IPlugin
from manager.message import Message

from protocol.string import String

from collections import OrderedDict
import json
import time
import urllib
import schedule


class Weather(IPlugin, Message):
    def __init__(self):
        IPlugin.__init__(self)
        Message.__init__(self)

        self.text = '|%s| [%s] l%sl'
        self.schedule = schedule.every(1).minutes
        self.location = '20740'

        self.get_weather()
        self.get_precipitation()

    def get_weather(self):
        url = 'https://query.yahooapis.com/v1/public/yql?q=' \
              'select * from weather.forecast where woeid in ' \
              '(select woeid from geo.places(1) where text="%s")&format=json' % self.location

        data = json.loads(urllib.urlopen(url).read())
        data = data['query']['results']['channel']
        today, tomorrow = {}, {}

        temp_units = data['units']['temperature'].encode('ascii', 'ignore')
        print temp_units

        temp = data['item']['condition']['temp'].encode('ascii', 'ignore')
        humidity = data['atmosphere']['humidity'].encode('ascii', 'ignore')
        print temp, humidity

        today['high'] = data['item']['forecast'][0]['high'].encode('ascii', 'ignore')
        today['low'] = data['item']['forecast'][0]['low'].encode('ascii', 'ignore')
        today['condition'] = data['item']['forecast'][0]['text'].encode('ascii', 'ignore')
        print today

        tomorrow['high'] = data['item']['forecast'][1]['high'].encode('ascii', 'ignore')
        tomorrow['low'] = data['item']['forecast'][1]['low'].encode('ascii', 'ignore')
        tomorrow['condition'] = data['item']['forecast'][1]['text'].encode('ascii', 'ignore')
        print tomorrow

    def get_precipitation(self):
        lat = '39.003'
        lon = '-76.935'
        url = 'http://isitgoingtorain.com/data/nearest.php?' \
              'callback=iigtrData&latitude=%s&longitude=%s' % (lat, lon)

        data = json.loads(urllib.urlopen(url).read()[10:-1])

        days = {time.strptime(k[:-6], '%a, %d %b %Y %H:%M:%S'): data['Pp'][k] for k in data['Pp']}
        s = sorted(days)

        print 'evening precip: %s' % days[s[0]]
        print 'morning precip: %s' % days[s[1]]

    def get_commands(self):
        return [String('11', self.labels_string[0]),
                String('23', self.labels_string[1]),
                String('35', self.labels_string[2])]
