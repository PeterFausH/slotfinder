#!/bin/bash
#
# /home/pi/awattar/beende_Heizung_KUECHE_EG_R2.sh
# ch sind die BCM Nummern der GPIOs 5,6,13,16,19,20,21,26
# Relais 2, Pin 6, einschalten ist 0, ausschalten ist 1
ch=6
state=1
gpio -g write $ch $state
echo "<---  $(date)  Stopp Relais 2 WärmePumpe"
curl -s -XPOST http://localhost:8086/write?db=awattar --data-binary 'sensor,ort=WP state=0'
