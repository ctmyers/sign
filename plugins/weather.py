from yapsy.IPlugin import IPlugin
from manager.message import Message

from protocol.string import String
import protocol.control as control

from collections import OrderedDict
import json
import time
import urllib
import schedule


class Weather(IPlugin, Message):
    def __init__(self):
        IPlugin.__init__(self)
        Message.__init__(self)

        self.text = control.SPEED_1 + '%s' + control.NEW_PAGE + '%s'
        self.schedule = schedule.every(1).minutes
        self.location = '20740'
        self.lat = '39.003'
        self.lon = '-76.935'

    def get_weather(self):
        url = 'https://query.yahooapis.com/v1/public/yql?q=' \
              'select * from weather.forecast where woeid in ' \
              '(select woeid from geo.places(1) where text="%s")&format=json' % self.location

        data = json.loads(urllib.urlopen(url).read())
        data = data['query']['results']['channel']
        today, tomorrow = {}, {}

        units = data['units']['temperature'].encode('ascii', 'ignore')

        temp = data['item']['condition']['temp'].encode('ascii', 'ignore')
        humidity = data['atmosphere']['humidity'].encode('ascii', 'ignore')

        today['high'] = data['item']['forecast'][0]['high'].encode('ascii', 'ignore')
        today['low'] = data['item']['forecast'][0]['low'].encode('ascii', 'ignore')
        today['condition'] = data['item']['forecast'][0]['text'].encode('ascii', 'ignore')

        tomorrow['high'] = data['item']['forecast'][1]['high'].encode('ascii', 'ignore')
        tomorrow['low'] = data['item']['forecast'][1]['low'].encode('ascii', 'ignore')
        tomorrow['condition'] = data['item']['forecast'][1]['text'].encode('ascii', 'ignore')

        return {'temp': temp, 'humidity': humidity, 'units': units,
                'today': today, 'tomorrow': tomorrow}

    def get_precipitation(self):
        url = 'http://isitgoingtorain.com/data/nearest.php?' \
              'callback=iigtrData&latitude=%s&longitude=%s' % (self.lat, self.lon)

        data = json.loads(urllib.urlopen(url).read()[10:-1])

        days = {time.strptime(k[:-6], '%a, %d %b %Y %H:%M:%S'): data['Pp'][k] for k in data['Pp']}
        s = sorted(days)

        return {'morning': days[s[0]], 'evening': days[s[1]]}

    def get_commands(self):
        weather = self.get_weather()
        precip = self.get_precipitation()

        return [String('%s' % weather['temp'], self.labels_string[0]),
                String('rain: %s' % precip['morning'], self.labels_string[1])]
