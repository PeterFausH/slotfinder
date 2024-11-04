#!/bin/bash
# array mit allen Relais-Nummern im BCM System
array=( 5 6 13 16 19 20 21 26 )
for i in "${array[@]}"
do
        gpio -g mode $i out
done
echo alle Relais auf Output gestellt
bash checkrelais.sh

