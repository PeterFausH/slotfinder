#!/bin/bash
#
# /home/pi/awattar/starte_Heizung_FAMILIENZIMMER_OG_R6.sh
# ch sind die BCM Nummern der GPIOs 5,6,13,16,19,20,21,26
# Relais 6, Pin 20, einschalten ist 0, ausschalten ist 1
ch=20
state=0
gpio -g write $ch $state
echo "--->  $(date)  Start Relais 6 "
curl -s -XPOST http://localhost:8086/write?db=awattar --data-binary 'sensor,ort=R6 state=1'
