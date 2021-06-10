#!/usr/bin/python3

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import os
import urllib
import csv
from bs4 import BeautifulSoup
from datetime import date
from datetime import timedelta

#%% Set working directory and define constants
current_dir = os.getcwd()
index = 'rainwatch.html'

#%% Set dates
day = timedelta(days=1)
week4 = timedelta(days=7)
week3 = timedelta(days=14)
week2 = timedelta(days=21)
week1 = timedelta(days=28)
today = date.today()
yester = date.today() - day


#%% Import csv from NOAA LCD for Pease Airforce Base
prcp_df = pd.read_csv(
    'https://www.ncei.noaa.gov/data/local' \
    + '-climatological-data/access/2021/72605504743.csv',
    sep=',',
    usecols = [1,5,11],
    dtype = str,
    parse_dates = ['DATE'],
    na_values = 'T'
)

#%% Time periods (four weeks)
end_week4 = prcp_df.loc[len(prcp_df)-1,'DATE']
start_week4 = pd.to_datetime(end_week4-week4)
end_week3 = pd.to_datetime(end_week4-week4-day)
start_week3 = pd.to_datetime(end_week4-week3)
end_week2 = pd.to_datetime(end_week4-week3-day)
start_week2 = pd.to_datetime(end_week4-week2)
end_week1 = pd.to_datetime(end_week4-week2-day)
start_week1 = pd.to_datetime(end_week4-week1)

#%% Format dataframe and divide into last four weeks
prcp_df['DATE'] = prcp_df['DATE'].replace('T', ' ')
prcp_df.fillna(0, inplace=True)
prcp_df = prcp_df.set_index(['DATE'])
week1_df = prcp_df[start_week1:end_week1].copy()
week2_df = prcp_df[start_week2:end_week2].copy()
week3_df = prcp_df[start_week3:end_week3].copy()
week4_df = prcp_df[start_week4:end_week4].copy()
ttlweek1 = week1_df['HourlyPrecipitation'].astype(float).sum().round(2)
ttlweek2 = week2_df['HourlyPrecipitation'].astype(float).sum().round(2)
ttlweek3 = week3_df['HourlyPrecipitation'].astype(float).sum().round(2)
ttlweek4 = week4_df['HourlyPrecipitation'].astype(float).sum().round(2)

#%% Plot last four weeks of precipitation
fig, axs = plt.subplots(4,1)
print(week4_df)
axs[0].bar(
    week4_df.index.values,
    week4_df['HourlyPrecipitation'].astype(float).round(2),
    width=0.01
)
axs[1].bar(
    week3_df.index.values,
    week3_df['HourlyPrecipitation'].astype(float).round(2),
    width=0.01
)
axs[2].bar(
    week2_df.index.values,
    week2_df['HourlyPrecipitation'].astype(float).round(2),
    width=0.01
)
axs[3].bar(
    week1_df.index.values,
    week1_df['HourlyPrecipitation'].astype(float).round(2),
    width=0.01
)
plt.xlabel('Date (Day of Month and Time of Day)')
axs[0].set_ylabel('Precipitation (in/hr)')
axs[1].set_ylabel('Precipitation (in/hr)')
axs[2].set_ylabel('Precipitation (in/hr)')
axs[3].set_ylabel('Precipitation (in/hr)')
axs[0].set_ylim(ymin=0)
axs[1].set_ylim(ymin=0)
axs[2].set_ylim(ymin=0)
axs[3].set_ylim(ymin=0)
axs[0].legend(['Total: ' + str(ttlweek4) + ' in'])
axs[1].legend(['Total: ' + str(ttlweek3) + ' in'])
axs[2].legend(['Total: ' + str(ttlweek2) + ' in'])
axs[3].legend(['Total: ' + str(ttlweek1) + ' in'])
fig.set_size_inches(8,8)
plt.tight_layout()
plt.savefig(
    current_dir + '/weeklyrain.png',
    dpi=600
)
plt.close()

#%% Import data from weather.gov for Pease Airforce Base (more updated)
# Fetch the html file
url = 'https://w1.weather.gov/data/obhistory/KPSM.html'
html = urllib.request.urlopen(url).read()

# Parse the html file
soup = BeautifulSoup(html, 'html.parser')

# Format the parsed html file
strhtm = soup.prettify()
xlist = []
for x in soup.find_all('td'):
    xlist += [x]
xlist = xlist[8:len(xlist)-4]
i = 1
spacer = 0
wthr_prcp_list = []
# Compile precipitation values
for rain in xlist:
    if i % (16 + spacer) == 0:
        wthr_prcp_list += [rain.string]
        spacer += 18
    else:
        pass
    i += 1
# Compile dates
i = 1
spacer = 0
wthr_date_list = []
for d in xlist:
    if i % (1 + spacer) == 0:
        wthr_date_list += [d.string]
        spacer += 18
    else:
        pass
    i += 1
# Compile times
i = 1
spacer = 0
wthr_time_list = []
for t in xlist:
    if i % (2 + spacer) == 0:
        wthr_time_list += [t.string]
        spacer += 18
    else:
        pass
    i += 1
# Create dataframe
wthrgov_dict = {
    'Date':wthr_date_list,
    'Time':wthr_time_list,
    'HourlyPrecipitation':wthr_prcp_list
}
wthrgov_df = pd.DataFrame(wthrgov_dict)
wthrgov_df.replace(to_replace=['None'], value=np.nan, inplace=True)
wthrgov_df.fillna('0.00',inplace=True)
wthrgov_df['Datetime'] = wthrgov_df['Date'] + ' ' + wthrgov_df['Time']
current_prcp = wthrgov_df.loc[0, 'HourlyPrecipitation']
sixhr_prcp=wthrgov_df.loc[0:5,'HourlyPrecipitation'].astype(float).sum().round(2)
today_date = wthrgov_df.loc[0,'Date']
wthrgov_today_df = wthrgov_df[wthrgov_df['Date'] == today_date]
today_prcp=wthrgov_today_df['HourlyPrecipitation'].astype(float).sum().round(2)
threeday_prcp = wthrgov_df['HourlyPrecipitation'].astype(float).sum().round(2)
print('Last hour\'s precipitation is: ' + current_prcp + ' in')
print('Six hour precipitation is: ' + str(sixhr_prcp) + ' in')
print('The total precipitation today is: ' + str(today_prcp) + ' in')

#%% Plot precipitation from weather.gov
fig, ax = plt.subplots()

# Reverse wthrgov_df
wthrgov_df_rev = wthrgov_df.iloc[::-1].copy()
ax.bar(
    wthrgov_df_rev['Datetime'],
    wthrgov_df_rev['HourlyPrecipitation'].astype(float),
    width=0.5
)
plt.xlabel('Date')
ax.set_ylabel('Precipitation (in/hr)')
ax.set_ylim(ymin=0)
fig.set_size_inches(8,8)
date_xt = wthrgov_df.loc[:, 'Datetime'].to_numpy()[::3]
plt.xticks(date_xt, rotation=45)
ax.legend(['Total: ' + str(threeday_prcp) + ' in'])
plt.tight_layout()
plt.savefig(
    current_dir + '/weathergovrain.png',
    dpi=600
)
plt.close()

#%% Update dashboard
curr_prcp_out = open('current.txt','w')
curr_prcp_out.write(current_prcp)
curr_prcp_out.close()
sixhr_prcp_out = open('sixhour.txt','w')
sixhr_prcp_out.write(str(sixhr_prcp))
sixhr_prcp_out.close()
today_prcp_out = open('today.txt','w')
today_prcp_out.write(str(today_prcp))
today_prcp_out.close()
# Last update
lastupdate = wthrgov_df['Time'].iloc[0]
time_out = open('time.txt','w')
time_out.write(lastupdate)
time_out.close()
