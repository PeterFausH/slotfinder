#!/bin/bash
#
# /home/pi/awattar/starte_Heizung_SPIELZIMMER_R5.sh
# ch sind die BCM Nummern der GPIOs 5,6,13,16,19,20,21,26
# Relais 4, Pin 16, einschalten ist 0, ausschalten ist 1
ch=16
state=1
gpio -g write $ch $state
echo "<---  $(date)  Stopp Relais 4 "
curl -s -XPOST http://localhost:8086/write?db=awattar --data-binary 'sensor,ort=R4 state=0'
