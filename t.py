#!/usr/bin/python
# -*- coding: iso8859-1 -*- 

# Import der Module
import os
import MySQLdb
from time import *

#-------------------------------------------------------------------------------
# Tabelle Zuordnung Ort und ID des Sensors
sensorTabelle = {"10-000802c27568" : "W1",
                 "10-000802c278e7" : "W2"
                }
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Einlesen der Sensoren
def readSensor(Sensor):
    crc = 'NO'
    stringvalue = ' '
    errorCounter = -1

    while (crc != "YES"):
        errorCounter = errorCounter + 1
        file = open('/sys/bus/w1/devices/' + str(Sensor) + '/w1_slave')
        filecontent = file.read()                       # Sensorwert auslesen
        file.close()
        crc = filecontent.split("\n")[0].split(" ")[11] # CRC auslesen
        stringvalue = filecontent.split("\n")[1].split(" ")[9]  # Temperatur auslesen

        # Wert konvertieren in Fliesskommazahl mit einer Stelle nach Komma
        temperature = round((float(stringvalue[2:]) / 1000), 1)
        e85 = round(temperature, 0)
        if (e85 == 85):                                 # 85 Grad-Fehler
            crc = 'NO'                                  # denn von vorne
            print (' %5.0f °C' % e85)
    return temperature, errorCounter                    # exit temperature + errorCounter
#-------------------------------------------------------------------------------

lt = localtime()                                        # aktuelle Zeit
file = open('/sys/devices/w1_bus_master1/w1_master_slaves')
w1_slaves = file.readlines()                            # Slaves auslesen
file.close()                                            # File wieder schliessen

tabellenname = "temp";
mysql_opts = {
    'host' : "localhost",
    'user' : "karl",
    'pass' : "2fast4y",
    'db'   : "dataLogger"
    }

db = MySQLdb.connect(mysql_opts['host'], mysql_opts['user'], mysql_opts['pass'], mysql_opts['db'])
cursor = db.cursor()
# Header fuer Bildschirmausgabe
print('Ort   | Temperatur |  FC ')
print('------+------------+-----')

# Fuer jeden 1-Wire Slave eine Ausgabe
for line in w1_slaves:
    w1_slave = line.split("\n")[0]     # 1-wire Slave extrahieren
    temp, errorCounter  = readSensor(w1_slave)
    pos  = str(sensorTabelle.get(str(w1_slave)))        # Ort aus Tabelle holen
    print ('  ' + pos + '  |  %5.1f °C' % temp + '  |   ' +  str(errorCounter))

    date = strftime("%Y.%m.%d")
    time = strftime("%H:%M:%S")
    fobj_out = open("/home/karl/temp.txt","a")          # Textdatei oeffnen
    # Daten in Textdatei schreiben
    fobj_out.write(date + ", " + time +", " + '%4.1f' % temp + ", " + pos + ", " + str(errorCounter) + "\n")
    fobj_out.close()    # Textdatei schliessen

    daten = (date, time, pos, temp, errorCounter)
    cursor.execute("""INSERT INTO temp (date, time, pos, temp, rem)
                      VALUES(%s, %s, %s, %s, %s)""", daten)

#cursor.execute("SELECT * FROM temp")
#for row in cursor:
#    print "d: %s, t: %s, o: %s, t: %s, o: %s" % row

db.commit()
cursor.close()
db.close()

