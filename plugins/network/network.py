# coding=utf-8

from yapsy.IPlugin import IPlugin
from manager.message import Message

from protocol.string import String
import protocol.control as control

import schedule
import requests
from bs4 import BeautifulSoup

class Network(IPlugin, Message):
    def __init__(self):
        IPlugin.__init__(self)
        Message.__init__(self)

        self.text = control.SPEED_1 + '%s' + control.NEW_LINE + '%s'
        self.schedule = schedule.every(1).hours

        lines = [line.strip() for line in open('filename')]
        config = {}
        for line in lines:
            line = line.rstrip.spilt("=")
            config[line[0]] = line[1]

        self.ip = config["ip"]
        self.user = config["user"]
        self.password = config["password"]

    def get_bandwidth(self):
        c = Network._convert
        _get_control()
        r = requests.get('http://' + self.ip + "/RST_stattbl.htm", auth=(self.user,self.password))
        soup = BeautifulSoup(r.text)
        data = []
        table = soup.find('table', border='1', cellpadding='0')
        data = _get_data_from_table(table)
        if len(data) is not 0:
            upstream = _bytes_to_mb(float(c(data[1][5])))
            downstream = _bytes_to_mb(float(float(c(data[1][6]))))
            print "upstream:   %s" % upstream
            print "downstream: %s" % downstream
            return {'up': upstream, 'down': downstream}
        return None

    def get_total(self):
        c = Network._convert
        _get_control()
        r = requests.get('http://' + '192.168.1.1' + "/traffic_meter.htm", auth=('admin','password'))
        soup = BeautifulSoup(r.text)
        table = soup.find('table', border='1', cellpadding='0')
        data = _get_data_from_table(table)
        if len(data) is not 0:
            total_uploaded_today = _mb_to_gb(float(c(data[2][2])))
            total_downloaded_today = _mb_to_gb(float(c(data[2][3])))
            total_uploaded_month = _mb_to_gb(float(c(data[5][2]).split("/")[0].strip()))
            total_downloaded_month = _mb_to_gb(float(c(data[5][3]).split("/")[0].strip()))
            print "total_uploaded_today:   %s" % total_downloaded_today
            print "total_downloaded_today: %s" % total_uploaded_today
            print "total_uploaded_month:   %s" % total_uploaded_month
            print "total_downloaded_month: %s" % total_downloaded_month
            return {'uptd': total_uploaded_today, 'dwtd': total_downloaded_today, 'upmnth': total_uploaded_month, 'dwmnth': total_downloaded_month}
        return None

    def _mb_to_gb(self,data):
        units = "MB"
        if data > 1024:
            units = "GB"
            data = data / 1024
        return "%s %s" % data, units

    def _bytes_to_mb(self, data):
        units = "KB/s"
        data = data / 1024
        if data > 1024:
            data = data / 1024
            units = "MB/s"
        return "%s %s" % data, units

    def _get_control(self):
        r= requests.get('http://' + '192.168.1.1' + '/start.htm', auth=('admin','password'))
        table = BeautifulSoup(r.text).find('table', cellpadding='0', cellspacing='0')
        if table is None:
            r= requests.get('http://' + '192.168.1.1' + '/multi_login.cgi?id=1766147816', auth=('admin','password'), params={'act':'yes'})

    def _get_data_from_table(self, table):
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

                if len(columns) is not 0:
                    data.append(columns) # Get rid of empty values
        return data

    @staticmethod
    def _convert(value):
        if type(value) == str:
            return value.encode('ascii', 'ignore')
        else:
            return str(value)


    def get_commands(self):
        w = self.get_total()
        if w != None:
            return (String('^ today:%s %s v today:%s %s ^ month:%s %s v month: %s' % (w['uptd'],
                                                control.NEW_LINE,
                                                w['dwtd'],
                                                control.NEW_LINE,
                                                w['upmnth']),
                                                control.NEW_LINE,
                                                w['dwmnth']))
        return None