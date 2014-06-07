#!/usr/bin/python3.2
# -*- coding: utf-8 -*-

# Die Sensoren mÃÂ¼ssen mit "modprobe w1-gpio" und "modprobe w1-therm" aktiviert 

# Import der Module
import sys
import os
from time import *

# Zeitvariable definieren
lt = localtime()


# 1-Wire Slave-Liste oeffnen
file = open('/sys/devices/w1_bus_master1/w1_master_slaves') #Verzeichniss evtl. anpassen

# 1-Wire Slaves auslesen
w1_slaves = file.readlines()

# 1-Wire Slave-Liste schliessen
file.close()

# Header fuer Bildschirmausgabe
print('Sensor ID       | Temperatur')
print('----------------------------')

# Fuer jeden 1-Wire Slave eine Ausgabe
for line in w1_slaves:

 # 1-wire Slave extrahieren
 w1_slave = line.split("\n")[0]



 crc = 'NO'
 stringvalue = ' ' 
 while crc != "YES":

 # 1-wire Slave Datei oeffnen
   file = open('/sys/bus/w1/devices/' + str(w1_slave) + '/w1_slave')




 # Inhalt des 1-wire Slave File auslesen
   filecontent = file.read()

 # 1-wire Slave File schliessen
   file.close()

 # Temperatur Daten auslesen

   crc         = filecontent.split("\n")[0].split(" ")[11] 
   stringvalue = filecontent.split("\n")[1].split(" ")[9]

 temperature = float(stringvalue[2:]) / 1000
 temperature = round(temperature,1)
 # Temperatur konvertieren

 # Temperatur ausgeben
 print(str(w1_slave) + ' |  %5.3f °C' % temperature)

 # Werte in Datei schreiben
 # Zeit und Datum erfassen
 Datum = strftime("%d.%m.%Y")
 Uhrzeit = strftime("%H:%M:%S")
 
 # Textdatei oeffnen
 fobj_out = open("/home/karl/temp-daten.txt","a")
 # Daten in Textdatei schreiben
 fobj_out.write(Datum + ", " + Uhrzeit +", " + '%4.1f' % temperature + '   ' + crc + "\n")
 # Textdatei schliessen
 fobj_out.close()
