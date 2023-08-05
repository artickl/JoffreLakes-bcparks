#!/usr/bin/env python

'''
Main script is $ ./JoffreLakes.sh
which is checking when passes are show up for Joffre Lakes: 
https://reserve.bcparks.ca/dayuse/registration

This script is just analytics for results, which helped to find:
1) even website saying that "Passes can be booked starting at 7:00am, 
two days in advance of your planned visit." - this is not correct... 
passes appearing around 1:30 am and by 7:01am they are already gone

2) if somebody cancelled their passes - they are appearing online, 
but during the day they booked out in less then 20 seconds and at night
they can be available for more then 10 minutes
'''

import datetime

import json

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import mplcyberpunk
import seaborn as sns

#log from bash script
file_in="log.txt"

#df file, so, analytics can be taken from it after first run
df_file="log.df"

#lazy to use args
#load=True #to load existing set
load=False #to generate new set from log file

file = open(file_in, 'r')
lines = file.readlines()

if load:
    df = pd.read_pickle(df_file)
else:
    df = pd.DataFrame()

    #didn't thing about log formatting originally and it was too 
    # late to change it later when it was already running for couple days
    
    #Lines in log looks like this:
    # {"2023-08-04":{"DAY":{"capacity":"Full","max":0}},"2023-08-05":{"DAY":{"capacity":"Full","max":0}},"2023-08-06":{"DAY":{"capacity":"Full","max":0}}}Fri 04 Aug 2023 08:48:48 AM PDT
    
    #this process for 2 days of logs taking around couple minutes
    for line in lines:
        info_json_str, info_date_str, _ = line.partition(line[-32:])
        
        info_line = {}
        #info_date - drop new line, convert to time
        #Fri 04 Aug 2023 08:48:48 AM PDT
        info_date_str = info_date_str.rstrip(info_date_str[-1])
        info_line['date'] = datetime.datetime.strptime(info_date_str,"%a %d %b %Y %H:%M:%S %p %Z")

        #info_json - convert to proper items
        try:
            info_json = json.loads(info_json_str)

            for info_json_date in info_json:
                info_line[info_json_date]=info_json[info_json_date]['DAY']['max']
                #print(info_json_date)
        except ValueError as e:
            print(f"Line: {line}")
            print(f"Date: {info_date_str}")
            print(f"JSON: {info_json}")
            print(f"Error: {e}")
            pass

        df = df._append(info_line, ignore_index=True)
    
    df.to_pickle(df_file)

# sometimes computer was falling asleep unfortunately 
df['gap'] = df['date'].sort_values().diff().dt.total_seconds() 

print(df)
print(df.info())
print(df.describe())

#general plot for all available days
plt.style.use("cyberpunk")
df.plot.area(x='date', y=['2023-08-03','2023-08-04','2023-08-05','2023-08-06','gap'], figsize=(50,10), subplots=True)
mplcyberpunk.add_glow_effects()
plt.savefig(f'plot.png')
plt.close()

#plot only for interesting for me day - which I missed to book, but with notification was able to still get them
plt.style.use("cyberpunk")
df.plot.area(x='date', y=['2023-08-05'], figsize=(50,10), subplots=True)
mplcyberpunk.add_glow_effects()
plt.savefig(f'plot-2023-08-05.png')
plt.close()

#plot for new tickets on next day
plt.style.use("cyberpunk")
str_06_d=datetime.datetime.strptime("2023-08-04 00:00:00","%Y-%m-%d %H:%M:%S")
str_06_u=datetime.datetime.strptime("2023-08-04 08:00:00","%Y-%m-%d %H:%M:%S")
df5 = df[~(df['date'] < str_06_d)]
df5 = df5[~(df5['date'] > str_06_u)]
print(df5.head())
df5.plot.area(x='date', y=['2023-08-06'], figsize=(50,10), subplots=True)
mplcyberpunk.add_glow_effects()
plt.savefig(f'plot-2023-08-06.png')
plt.close()