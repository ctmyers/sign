# coding=utf-8

from yapsy.IPlugin import IPlugin
from manager.message import Message

from protocol.string import String
import protocol.control as control

import schedule
import forecastio


class Weather(IPlugin, Message):
    def __init__(self):
        IPlugin.__init__(self)
        Message.__init__(self)

        self.text = control.SPEED_1 + '%s' + control.NEW_LINE + '%s'
        self.schedule = schedule.every(1).hours
        self.lat = '38.9901'
        self.lon = '-76.9319'
        self.api_key = open('plugins/key.txt', 'r').read().rstrip()

    @staticmethod
    def _convert(value):
        if type(value) == str:
            return value.encode('ascii', 'ignore')
        else:
            return str(value)

    # translations for unicode strings
    _translations = {
        ord(u'–'): u'-'
    }

    def get_weather(self):
        forecast = forecastio.load_forecast(self.api_key, self.lat, self.lon)

        c = Weather._convert
        t = Weather._translations

        temp = c(int(forecast.hourly().data[0].temperature))
        feels = c(int(forecast.hourly().data[0].apparentTemperature))
        humidity = c(int(forecast.daily().data[0].humidity * 100))

        today = forecast.hourly().summary
        today = c(today.translate(t))

        return {'temp': temp, 'feels': feels, 'humidity': humidity, 'today': today}

    def get_commands(self):
        w = self.get_weather()
        return (String('%sF (%sF)%s%s%%' % (w['temp'],
                                            w['feels'],
                                            control.NEW_LINE,
                                            w['humidity']),
                       self.labels_string[0]),
                String(w['today'], self.labels_string[1]))
