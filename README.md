![Joffre Lakes Provincial Park](header.png)

# INTRO

British Colombia has day-use pass for some popular parks. Sometimes it's difficult to get them 
because of so many people are trying to get them.

So, this small "helper" is providing notification about availability of one-day-passes on Joffre Lake 
and helping to get them as soon as they will be available, because, as I found during analytics:

1) even website saying that "Passes can be booked starting at 7:00am, two days in advance of your 
planned visit." - this is not correct... Passes appearing around 1:30 am and by 7:01am they are 
already gone

2) if somebody cancelled their passes - they are appearing online, but during the day they booked out 
in less then 20 seconds and at night they can be available for more then 10 minutes

So, prepare autofill information in your browser, just need:
- first name, 
- last name 
- and email address (note that you can only get 1 reservation for single email) 

and keep website https://reserve.bcparks.ca/dayuse/registration ready to be refreshed as soon as 
computer will start beeping

## Collector

Main script `./JoffreLakes.sh` is helping to receive notification in bash (beep) that tickets for 
particular day become available.

Output is `log.txt` file which can be used for analyzing purposes, but main purpose is realtime notification

## Analyzer

`./plot.py` providing some plots based on log information from `./JoffreLakes.sh`, such as:

Date when information has been collected
How many tickets (up-to 4) was available at this moment for current and next 2 days
Gap if script was not running at some time and log is inconsistent

Output is 4 files:
- `log.df` - panda dataframe file which can be used for testing instead of re-processing log file each time
- `plot.png` - plot for full period and each available day available in `log.txt`
![plot.png](plot.png)
- `plot-2023-08-05.png` - plot for full period, but only for 2023-08-05 passes
![plot-2023-08-05.png](plot-2023-08-05.png)
- `plot-2023-08-05.png` - plot for limited period (`2023-08-04 00:00:00 - 2023-08-04 08:00:00`) 
and only for 2023-08-06 passes
![plot-2023-08-05.png](plot-2023-08-05.png)

