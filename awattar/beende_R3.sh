#!/bin/bash
#
# /home/pi/awattar/beende_Heizung_WOHNZIMMER_R3.sh
# ch sind die BCM Nummern der GPIOs 5,6,13,16,19,20,21,26
# Relais 3, Pin 13, einschalten ist 0, ausschalten ist 1
ch=13
state=1
gpio -g write $ch $state
echo "<---  $(date)  Stopp Relais 3 Geschirr"
curl -s -XPOST http://localhost:8086/write?db=awattar --data-binary 'sensor,ort=Geschirr state=0'
