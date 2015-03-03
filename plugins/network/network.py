# coding=utf-8

from yapsy.IPlugin import IPlugin
from manager.message import Message

from protocol.string import String
import protocol.control as control

import schedule
import requests
import re
from bs4 import BeautifulSoup


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            if abs(num) < 100.0:
                if abs(num) < 10.0:
                    return "%1.2f%s%s" % (num, unit, suffix)
                return "%2.1f%s%s" % (num, unit, suffix)
            return "%3.0f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)


class Network(IPlugin, Message):
    def __init__(self):
        IPlugin.__init__(self)
        Message.__init__(self)

        self.text = control.SPEED_1 + '%s' + control.NEW_LINE + '%s'
        self.schedule = schedule.every(1).minutes

        c = {}
        with open('plugins/network/network.config', 'r') as conf:
            for line in conf.readlines():
                s = line.split('=')
                c[s[0].strip()] = s[1].strip()

        self.ip = c['ip']
        self.user = c['user']
        self.password = c['password']

    def get_bandwidth(self):
        c = Network._convert
        self.get_control()

        r = requests.get('http://' + self.ip + "/RST_stattbl.htm", auth=(self.user, self.password))
        soup = BeautifulSoup(r.text)
        table = soup.find('table', border='1', cellpadding='0')
        data = Network._get_data_from_table(table)

        if len(data) is not 0:
            upstream = sizeof_fmt(float(c(data[1][5])))
            downstream = sizeof_fmt(float(float(c(data[1][6]))))
            return {'up': upstream, 'down': downstream}

        return None

    def get_total(self):
        c = Network._convert
        self.get_control()

        r = requests.get('http://' + self.ip + "/traffic_meter.htm", auth=(self.user, self.password))
        soup = BeautifulSoup(r.text)
        table = soup.find('table', border='1', cellpadding='0')
        data = Network._get_data_from_table(table)

        if len(data) != 0:
            total_uploaded_today = sizeof_fmt(float(c(data[2][2])) * 1000000)
            total_downloaded_today = sizeof_fmt(float(c(data[2][3])) * 1000000)
            total_uploaded_month = sizeof_fmt(float(c(data[5][2]).split("/")[0].strip()) * 1000000)
            total_downloaded_month = sizeof_fmt(float(c(data[5][3]).split("/")[0].strip()) * 1000000)
            return {'up_today': total_uploaded_today, 'down_today': total_downloaded_today,
                    'up_month': total_uploaded_month, 'down_month': total_downloaded_month}

        return None

    def get_control(self):
        r = requests.get('http://' + self.ip + '/start.htm', auth=(self.user, self.password))
        table = BeautifulSoup(r.text).find('table', cellpadding='0', cellspacing='0')
        if table is None:
            r = requests.get('http://' + self.ip + '/multi_login.cgi?id=1766147816',
                             auth=(self.user, self.password), params={'act': 'yes'})

    @staticmethod
    def _get_data_from_table(table):
        pattern = re.compile('(\d\s\W)*')
        data = []
        if table is None:
            print "Could not access router due to someone using it"
        else:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                columns = []
                for ele in cols:
                    text = ' '.join(ele.text.split())
                    match = pattern.match(text)
                    if match is not None and text is not "":
                        columns.append(text)

                if len(columns) != 0:
                    data.append(columns)  # Get rid of empty values
        return data

    @staticmethod
    def _convert(value):
        if type(value) == str:
            return value.encode('ascii', 'ignore')
        else:
            return str(value)

    def get_commands(self):
        w = self.get_total()

        if w:
            return (String('Today %s/%s' %
                           (w['up_today'], w['down_today']), self.labels_string[0]),
                    String('This Month %s/%s' %
                           (w['up_month'], w['down_month']), self.labels_string[1]))

        return (String('network failed', self.labels_string[0]),
                String('', self.labels_string[1]))