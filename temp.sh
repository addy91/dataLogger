#!/bin/bash
# a script to read and save temperature readings from all the group 28 1-wire temperature sensors
#
# get all devices in the '28' family
FILES=`ls /sys/devices/w1_bus_master1/ | grep '^10-'`
# iterate through all the devices
for file in $FILES
    do
      # get the 2 lines of the response from the device
      GETDATA=`cat /sys/bus/w1/devices/w1_bus_master1/$file/w1_slave`
      GETDATA1=`echo "$GETDATA" | grep crc`
      GETDATA2=`echo "$GETDATA" | grep t=`
      # get temperature
      TEMP=`echo $GETDATA2 | sed -n 's/.*t=//;p'`
      #
        # test if crc is 'YES' and temperature is not -62 or +85
        if [ `echo $GETDATA1 | sed 's/^.*\(...\)$/\1/'` == "YES" -a $TEMP != "-62" -a $TEMP != "85000"  ]
           then
               # crc is 'YES' and temperature is not -62 or +85 - so save result
               echo `date +"%d-%m-%Y %H:%M:%S "; echo $GETDATA2 | sed -n 's/.*t=//;p'` >> /var/1w_files/$file
           else
               # there was an error (crc not 'yes' or invalid temperature)
               # try again after waiting 1 second
               sleep 1
               # get the 2 lines of the response from the device again
               GETDATA=`cat /sys/bus/w1/devices/w1_bus_master1/$file/w1_slave`
               GETDATA1=`echo "$GETDATA" | grep crc`
               GETDATA2=`echo "$GETDATA" | grep t=`
               # get the temperature from the new response
               TEMP=`echo $GETDATA2 | sed -n 's/.*t=//;p'`
                  if [ `echo $GETDATA1 | sed 's/^.*\(...\)$/\1/'` == "YES" -a $TEMP != "-62" -a $TEMP != "85000" ]
                      then
                      # save result if crc is 'YES' and temperature is not -62 or +85 - if not, just miss it and move on
                      echo `date +"%d-%m-%Y %H:%M:%S "; echo $GETDATA2 | sed -n 's/.*t=//;p'` >> /var/1w_files/$file
                  fi
               # this is a retry so log the failure - record date/time & device ID
               echo `date +"%d-%m-%Y %H:%M:%S"`" - ""$file" >> /var/1w_files/err.log
           fi
    done
exit 0
