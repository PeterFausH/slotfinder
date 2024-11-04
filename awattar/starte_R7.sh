#!/bin/bash
#
# /home/pi/awattar/starte_Warmwasser_3kW_R7.sh
# ch sind die BCM Nummern der GPIOs 5,6,13,16,19,20,21,26
# Relais 7, Pin 21, einschalten ist 0, ausschalten ist 1
ch=21
state=0
gpio -g write $ch $state
echo "--->  $(date)  Start Relais 7 "
curl -s -XPOST http://localhost:8086/write?db=awattar --data-binary 'sensor,ort=R7 state=1'


