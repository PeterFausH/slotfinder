ergBWWP=$(gpio -g read 5 2>&1)
ergWP=$(gpio -g read 6 2>&1)
ergGS=$(gpio -g read 13 2>&1)
erg4=$(gpio -g read 16 2>&1)
erg5=$(gpio -g read 19 2>&1)
erg6=$(gpio -g read 20 2>&1)
erg7=$(gpio -g read 21 2>&1)
erg8=$(gpio -g read 26 2>&1)

if [ $ergBWWP -eq "1" ] 
 then
	echo Brauchwasser-Wärmepumpe ist aus
else
	echo an: Brauchwasser-Wärmepumpe
fi 
if [ $ergWP -eq "1" ] 
 then
	echo Wärmepumpe Heizung ist aus
else
	echo an: Wärmepumpe Heizung
fi 
if [ $ergGS -eq "1" ] 
 then
	echo Geschirrspüler ist aus
else
	echo an: Geschirrspüler
fi 
if [ $erg4 -eq "1" ] 
 then
	echo R4 BCM 16 ist aus
else
	echo an: R4 BCM 16
fi 
if [ $erg5 -eq "1" ] 
 then
	echo R5 BCM 19 ist aus
else
	echo an: R5 BCM 19
fi 
if [ $erg6 -eq "1" ] 
 then
	echo R6 BCM 20 ist aus
else
	echo an: R6 BCM20
fi 
if [ $erg7 -eq "1" ] 
 then
	echo R7 BCM 21 ist aus
else
	echo an: R7 BCM 21
fi 
if [ $erg8 -eq "1" ] 
 then
	echo R8 BCM 26 ist aus
else
	echo an: R8 BCM 26
fi 

echo       $ergBWWP      $ergWP      $ergGS      $erg4      $erg5      $erg6     $erg7     $erg8


