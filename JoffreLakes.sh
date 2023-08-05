#!/bin/bash

'''
Simple script to receive notification about available one-day-passes on Joffre Lake, BC, Canada

Helping to get them as soon as they will be available, because:
1) even website saying that "Passes can be booked starting at 7:00am, 
two days in advance of your planned visit." - this is not correct... 
passes appearing around 1:30 am and by 7:01am they are already gone

2) if somebody cancelled their passes - they are appearing online, 
but during the day they booked out in less then 20 seconds and at night
they can be available for more then 10 minutes - so, prepare autofill for 
information and keep webside https://reserve.bcparks.ca/dayuse/registration 
ready to be refreshed
'''

DATE="2023-08-05"
URL="https://jd7n1axqh0.execute-api.ca-central-1.amazonaws.com/api/reservation?facility=Joffre%20Lakes&park=0363"
LOG=log.txt

while true; do
	curl $URL 2>/dev/null | tee -a $LOG
	date | tee -a $LOG
	(tail -1 $LOG | grep "\"${DATE}\":{\"DAY\":{\"capacity\":\"Low\"") && beep 2>/dev/null
	sleep 5
done
