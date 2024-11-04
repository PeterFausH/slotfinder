#!/bin/bash
#
# /home/pi/awattar/starte_Warmwasser_5kW_R8.sh
# ch sind die BCM Nummern der GPIOs 5,6,13,16,19,20,21,26
# Relais 8, Pin 26, einschalten ist 0, ausschalten ist 1
ch=26
state=0
gpio -g write $ch $state
echo "--->  $(date)  Start Relais 8 "
curl -s -XPOST http://localhost:8086/write?db=awattar --data-binary 'sensor,ort=R8 state=1'

