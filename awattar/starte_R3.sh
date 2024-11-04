#!/bin/bash
#
# /home/pi/awattar/starte_Heizung_WOHNZIMMER_R3.sh
# ch sind die BCM Nummern der GPIOs 5,6,13,16,19,20,21,26
# Relais 3, Pin 13, einschalten ist 0, ausschalten ist 1
ch=13
erg=0
gpio -g write $ch $erg
curl -s -XPOST http://localhost:8086/write?db=awattar --data-binary "sensor,ort=Geschirr state=1"
echo "--->  $(date)  Start Relais 3 Geschirr"
