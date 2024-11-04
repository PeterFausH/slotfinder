#!/usr/bin/python3
# -*- coding: utf-8 -*-

# origin comes from:
#__author__ = "Peter Gransdorfer"
#__copyright__ = "Copyright 2019"
#__license__ = "GPL"
#__maintainer__ = "Peter Gransdorfer"
#__email__ = "peter.gransdorfer[AT]cattronix[com]"
#
# modified by "Peter F"
# email "pf@nc-lux.com"


import requests
import http.client
import urllib.parse
import json
import os
import re
import sys
import getopt
import datetime
import dateutil
import configparser
import math
from string import Template
from datetime import timezone
from dateutil import tz
from datetime import timedelta
from crontab import CronTab
from influxdb import InfluxDBClient

data = None
config = None

# Instanz für user Crontab erstellen
cron = CronTab(user='pi')
# alle Cronjobs von gestern entfernen
starttime=datetime.datetime.now(tz=timezone.utc)-datetime.timedelta(days=1)
print('automatic Relais aWATTar Tag:'+str(starttime.day))
cron.remove_all(comment='automatic Relais aWATTar Tag:'+str(starttime.day))
cron.write()

def getDataFromServer():
        """
    Get the market data from API of the next day
    Returns
    -------
    int
        Returns the response from the API
    """
        global config

        try:
                #set start timestamp
                starttime = datetime.datetime.now(tz=timezone.utc)+datetime.timedelta(hours=2)
                #fake um andere Tage abzurufen
                #starttime = datetime.datetime.now(tz=timezone.utc)-datetime.timedelta(days=178)
                print('check am: ',starttime)
                #print(starttime.hour)
                #slots ab jetzt suchen, da noch vor 14 Uhr und morgen unbekannt ist.
                if starttime.hour < 14:
                        print('noch zu früh, suche Slot für den Rest des aktuellen Tages')
                        starttime = starttime+datetime.timedelta(days=0)
                #slots für den morgigen ganzen Tag suchen (Normalfall)
                else:
                        starttime = starttime.replace(hour=0, minute=0, second=0)
                        starttime = starttime+datetime.timedelta(days=1)
                        
                print(starttime)
                starttimestamp = str(int(starttime.timestamp()))
                
                #set end timestamp
                endtime = starttime + datetime.timedelta(days=2)
                endtimestamp = str(int(endtime.timestamp()))
                
                req = requests.get('https://api.awattar.de/v1/marketdata?start=' + starttimestamp + '000&end=' + endtimestamp + '000')
                #req = requests.get('https://api.awattar.de/v1/marketdata')
                
                if req.status_code != requests.codes.ok: return 0
                
                return req.json()
        
        except Exception as e:
                print(str(e))
                return 0

                
def searchBestStartingPoint(starttime, periode, duration):
        """
    Search the best starting point.
    Parameters
    ----------
    starttime : int
        Start time [hour]
    periode : int
        Time range [hour]
    duration : int
        Duration of usage[hour]
    Returns
    -------
    int
        Returns the best starting point
    """

        lowestprice = 99999.0
        lowestpricetime = None
        startatindex = None
        durationround = math.ceil(duration)
        datalenght = len(data) - (durationround - 1)

        #get each json item
        for i in range(0,datalenght):
        
                item = data[i]          
                #get values from response
                valuestarttime = item['start_timestamp']
                valueprice = item['marketprice']
                
                valuestarttime = datetime.datetime.utcfromtimestamp(valuestarttime / 1000).replace(tzinfo=timezone.utc)
                valuestarttime = valuestarttime.astimezone(tz.tzlocal())

                if valuestarttime.hour >= starttime:
                        
                        if startatindex == None:
                                startatindex = i
                                
                        rangesum = 0
                        
                        for x in range(0, durationround):
                                xtime = datetime.datetime.utcfromtimestamp(data[i+x]['start_timestamp'] / 1000)
                                rangesum += data[i+x]['marketprice']
                        
                        averageprice = rangesum / durationround
                        
                        if averageprice < lowestprice:
                                lowestprice = averageprice
                                lowestpricetime = valuestarttime
                
                #Loop finished
                if startatindex != None:
                        if i >= (startatindex + (periode-1)):
                                break

        print('{:20s}: Start {:%d.%m.%Y %H:%M} für {:2.1f} Stunden  ({:3.1f} ct/kWh) {:2.1f} T:{:2.1f}ct/kWh '.format(section,lowestpricetime, duration, lowestprice/10, lowestprice/10-price_average, 18.9+lowestprice/10))
        return lowestpricetime


def parseConfig():
        """
    Read config file and parse all Task sections
    """ 
        global config
        global data
        global section

        for section in config.sections():

                #process only section which contains 'Task'
                if 'Task' in section:
                        if config.getboolean(section, 'enable'):

                                #get best start time 
                                starttime = searchBestStartingPoint(config.getint(section, 'Starttime'),config.getint(section, 'Periode'),config.getfloat(section, 'Duration'))
                                endtime = starttime + timedelta(minutes=60*config.getfloat(section, 'Duration'))

                                #hier den user:pi crontab schreiben lassen Start
                                #
                                job = cron.new(command=config.get(section, 'commando_start'))
                                job.minute.on(starttime.strftime("%M"))
                                job.hour.on(starttime.strftime("%H"))
                                starttime = datetime.datetime.now(tz=timezone.utc)
                                job.set_comment("automatic Relais aWATTar Tag:"+str(starttime.day))
                                cron.write()
                                # Ende
                                job = cron.new(command=config.get(section, 'commando_stop'))
                                job.minute.on(endtime.strftime("%M"))
                                job.hour.on(endtime.strftime("%H"))
                                job.set_comment("automatic Relais aWATTar Tag:"+str(starttime.day))
                                cron.write()



def ermittlePreise(typ):
        # parameter ist 2.Teil nach price_
        # nutze dazu die Loxone-Schnittstelle
        price = ['price_low','price_high','price_median','price_average']
        req = requests.get('https://api.awattar.de/v1/marketdata/current.yaml')
        lines = (req.text).split('\n')
        for line in lines:
            res = line.split(':')
            if res[0] in price:
                if typ in res[0]:
                    price = res[1]
        return(price)

                
def main(argv):
        """
    Main routine
    """ 
        global config
        global data
        # Average Preis weitergeben für Auswertung der Differenz 
        global price_average

        #Preisinfo holen über loxone-Schnittstelle
        print('günstigster Preis ist: {:2.1f} ct/kWh'.format(float((ermittlePreise('low')))))
        print('höchster Preis ist: {:2.1f} ct/kWh'.format(float((ermittlePreise('high')))))
        print('average Preis ist: {:2.1f} ct/kWh'.format(float((ermittlePreise('average')))))
        price_average = float((ermittlePreise('average')))
        print('median Preis ist: {:2.1f} ct/kWh'.format(float((ermittlePreise('median')))))

        config = configparser.ConfigParser()
        config.read('/home/pi/scripte/awattar_scheduler.conf')
        out = getDataFromServer()
        #print(out)

        #return if response is empty
        if out == 0:
                print('Can''t download data from server') 
                return
        
        data = out['data']
        parseConfig()


if __name__ == "__main__":
        main(sys.argv[1:])
