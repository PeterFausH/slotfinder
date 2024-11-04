#!/bin/bash
#
# /home/pi/awattar/starte_Heizung_SPIELZIMMER_R5.sh
# ch sind die BCM Nummern der GPIOs 5,6,13,16,19,20,21,26
# Relais 5, Pin 19, einschalten ist 0, ausschalten ist 1
ch=19
state=0
gpio -g write $ch $state
echo "--->  $(date)  Start Relais 5 "
curl -s -XPOST http://localhost:8086/write?db=awattar --data-binary 'sensor,ort=R5 state=1'
