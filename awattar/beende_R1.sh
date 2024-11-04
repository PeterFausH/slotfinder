#!/bin/bash
#
# /home/pi/awattar/beende_Heizung_BAD_OG_R1.sh
# ch sind die BCM Nummern der GPIOs 5,6,13,16,19,20,21,26
# Relais 1, Pin 5, einschalten ist 0, ausschalten ist 1
ch=5
state=1
gpio -g write $ch $state
echo "<---  $(date)  Stopp Relais 1 BWWP"
curl -s -XPOST http://localhost:8086/write?db=awattar --data-binary 'sensor,ort=BWWP state=0'
