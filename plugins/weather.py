from yapsy.IPlugin import IPlugin
from manager.message import Message

from protocol.string import String
import protocol.control as control

from collections import OrderedDict
import json
import time
import urllib
import schedule
import forecastio

class Weather(IPlugin, Message):
    def __init__(self):
        IPlugin.__init__(self)
        Message.__init__(self)

        self.text = control.SPEED_1 + '%s' + control.NEW_PAGE + '%s'
        self.schedule = schedule.every(1).hours
        self.lat = '38.9901'
        self.lon = '-76.9319'
        self.API_KEY = open('plugins/key.txt','r').read()

    def get_weather(self):
        forecast = forecastio.load_forecast(self.API_KEY, self.lat, self.lon)

        temp = forecast.hourly().data[0].temperature
        humidity = forecast.daily().data[0].humidity
        today = forecast.hourly().summary
        tomorrow = forecast.daily().data[1].summary
        tomorrow_rain = forecast.daily().data[1].precipProbability
        tomorrow_temp_max = forecast.daily().data[1].temperatureMax
        tomorrow_temp_min = forecast.daily().data[1].temperatureMin
        alert_message = "None"
        if forecast.alerts() is not None:
            alerts = forecast.alerts()
            for alert in alerts:
                alert_message += " " + alert.title

        return {'temp': temp, 'humidity': humidity,
                'today': today, 'tomorrow': tomorrow, 'alerts': alert_message}

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

def main():
    weather = Weather()
    weather.get_weather()

if __name__ == "__main__":
    main()