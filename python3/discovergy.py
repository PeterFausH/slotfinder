#!/usr/bin/python3
#https://github.com/jpbede/pydiscovergy/blob/master/pydiscovergy/pydiscovergy.py

from pydiscovergy import PyDiscovergy
#import datetime
import time
import json
#import schedule
#import requests
from influxdb import InfluxDBClient

# Configure InfluxDB connection variables
host = "127.0.0.1" 
port = 8086 
user = "grafana"
password = "herbi"
dbname = "awattar" 

# Influx Datenbank verbinden
#client = InfluxDBClient(host, port, user, password, dbname)

# Discovergy API abfragen
email = 'user@email.com'
password = '1234567'
clientname = 'HERBIE'
discovergy = PyDiscovergy(clientname)
discovergy.login(email, password)
# Get all meters for account
meters = discovergy.get_meters()
print(meters)

# json zusammenbauen für Influx-Datenbank
def add(name,wert):
    info=[{"measurement": "strombezug",
           "fields": {name : wert}}]
    #print(info)
    client.write_points(info)
    return

# Get all meters for account
meters = discovergy.get_meters()
#print(meters)
last = discovergy.get_last_reading("your_meter_number")
ph1=int(last['values']['power1']/1000)
ph2=int(last['values']['power2']/1000)
ph3=int(last['values']['power3']/1000)
total=int(last['values']['power']/1000)
add("phase1",ph1)
add("phase2",ph2)
add("phase3",ph3)
add("bezug",total)
print('Phasenwerte in Influx-DB abgelegt:',ph1,ph2,ph3,total)


