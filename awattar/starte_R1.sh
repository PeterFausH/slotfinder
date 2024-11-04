#!/bin/bash
#
# /home/pi/awattar/starte_Heizung_BAD_OG_R1.sh
# ch sind die BCM Nummern der GPIOs 5,6,13,16,19,20,21,26
# Relais 1, Pin 5, einschalten ist 0, ausschalten ist 1
#uuid=eb4bfba0-96ba-11eb-8b57-bdfda9c5a7bd
ch=5
state=0
gpio -g write $ch $state
echo "--->  $(date)  Start Relais 1 BWWP"
curl -s -XPOST http://localhost:8086/write?db=awattar --data-binary 'sensor,ort=BWWP state=1'
