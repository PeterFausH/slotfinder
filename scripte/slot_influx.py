#!/usr/bin/python3
# -*- coding: utf-8 -*-

# in crontab einbinden und um 18:00 Uhr laufen lassen
# skript trägt die Stundenpreise in die Influxdb ein.
# PFu: 15.12.20 aufgeräumt, Kommentare verbessert
# config.read('/home/pi/slot/influx.conf')
# Umsatzsteuer mit berücksichtigt.
        
import requests
import json
import sys
import datetime
import dateutil
import configparser
from datetime import timezone
from dateutil import tz
from datetime import timedelta
from influxdb import InfluxDBClient

data = None
config = None
client = None


def getDataFromServer():
        global config

        try:
                #set start timestamp
                starttime = datetime.datetime.now(tz=timezone.utc)+datetime.timedelta(hours=2)
                print('check am: ',starttime)
                starttime = starttime.replace(hour=0, minute=0, second=0)
                # hier sind andere Tage möglich
                #aktueller Tag:
                #starttime = starttime+datetime.timedelta(days=0)
                #der morgige Tag:
                starttime = starttime+datetime.timedelta(days=0)
                starttime = starttime+datetime.timedelta(hours=-2)
                #der gestrige Tag:
                #starttime = starttime-datetime.timedelta(days=1)

                print('Start-time:',starttime)
                print('')
                starttimestamp = str(int(starttime.timestamp()))

                #set end timestamp
                endtime = starttime + datetime.timedelta(days=2)
                endtimestamp = str(int(endtime.timestamp()))
                print('End-time:  ',endtime)
                print('')
                req = requests.get('https://api.awattar.de/v1/marketdata?start=' + starttimestamp + '000&end=' + endtimestamp + '000')
                #req = requests.get('https://api.awattar.de/v1/marketdata')

                if req.status_code != requests.codes.ok: return 0

                return req.json()

        except Exception as e:
                print(str(e))
                return 0



def writeDataToInfluxDB():
        global data
        global config

        #[InfluxDB]
        #enable = true
        #server = 192.168.200.223
        #port = 8086
        #database = home
        #username = home
        #password = siemens

        client = InfluxDBClient(
                config['InfluxDB']['Server'],
                config['InfluxDB']['Port'],
                config['InfluxDB']['Username'],
                config['InfluxDB']['Password'],
                config['InfluxDB']['Database'])

        #get each json item
        for item in data:
                valuestarttime = item['start_timestamp']
                valueprice = item['marketprice']
                valuestarttime = valuestarttime / 1000 #remove milliseconds
                # habe utc weg vo fromtimestamp(valuestarttime)
                json_body = [{
                                "measurement": "Energymarketprice",
                                #"time": datetime.datetime.fromtimestamp(valuestarttime).isoformat() + 'Z',
                                "time": datetime.datetime.utcfromtimestamp(valuestarttime).isoformat(),
                                "fields": {
                                        "value": float((valueprice/10)*1.19)
                                }
                        }]
                print(datetime.datetime.fromtimestamp(valuestarttime).isoformat(),valueprice,valueprice/10*1.19)
                result = client.write_points(json_body,protocol=u'json',time_precision='s')

def main(argv):
        global config
        global data
        config = configparser.ConfigParser()
        #/home/peterf/python-scripte/awattar/scripte
        config.read('/home/pi/slot/influx.conf')
        out = getDataFromServer()
        data = out['data']
        #write data to InfluxDB
        if config['InfluxDB']['enable']:
               writeDataToInfluxDB()



if __name__ == "__main__":
        main(sys.argv[1:])
