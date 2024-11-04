#!/bin/bash
xms=$(date +"%y-%m-%d %H:%M")
cd /home/pi/awattar
# home/pi/awattar/alleRelais_aus.sh
gpio -g mode 5 out
gpio -g mode 6 out
gpio -g mode 13 out
gpio -g mode 16 out
gpio -g mode 19 out
gpio -g mode 20 out
gpio -g mode 21 out
gpio -g mode 26 out
echo $xms: alle Relais per Script ausgeschaltet!


