import numpy as np
from numpy.polynomial.polynomial import polyfit
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from weather import get_daily_weather_data_2016_to_2018

## Initialization
chemicum_waste_data = pd.read_csv('data/chemicum_food_waste.csv')
exactum_waste_data = pd.read_csv('data/exactum_food_waste.csv')


columns = ['date', 'weekday', 'num_customers', 'cb', 'cbpc', 'twpc']
# cbpc: customer biowaste per customer (g), twpc: total waste per customer (g)
# twpc includes kitchen waste and other waste

waste_data = pd.DataFrame(columns=columns)

for index, c_row in chemicum_waste_data.iterrows():
    date, weekday = c_row['Date'], c_row['Weekday']
    e_row = exactum_waste_data.loc[exactum_waste_data['Date'] == date]
    if len(e_row) > 0:
        num_customers = int(c_row['Number of customers']) + int(e_row['Number of customers'])
        cb = 1000*(float(c_row['Customer biowaste (kg)']) + float(e_row['Customer biowaste (kg)']))
        cbpc = 1000*(float(c_row['Customer biowaste (kg)']) + float(e_row['Customer biowaste (kg)']))/num_customers
        twpc = 1000*(float(c_row['Total waste (kg)']) + float(e_row['Total waste (kg)']))/num_customers
        new_row = {'date': date, 'weekday': weekday, 'num_customers': num_customers, 'cb':cb, 'cbpc': cbpc, 'twpc': twpc}
        waste_data = waste_data.append(new_row, ignore_index=True)


## General metrics
mean_cbpc = waste_data.cbpc.mean()
mean_twpc = waste_data.twpc.mean()

## Weekday
mean_weekday_cbpc = waste_data.groupby(['weekday'])['cbpc'].mean()[['mon', 'tue', 'wed', 'thu', 'fri']]
mean_weekday_twpc = waste_data.groupby(['weekday'])['twpc'].mean()[['mon', 'tue', 'wed', 'thu', 'fri']]

# mean_weekday_cbpc.plot(x='weekday', y='cbpc', title='Customer biowaste per customer on weekdays (g)', grid=True) # shows much less waste on Monday
# plt.show()
# mean_weekday_twpc.plot(x='weekday', y='tbpc', title='Total waste per customer on weekdays (g)', grid=True) # shows much more waste on Friday
# plt.show()

## Customer waste proportion
waste_data['prop'] = waste_data.cbpc/waste_data.twpc
mean_weekday_prop = waste_data.groupby(['weekday'])['prop'].mean()[['mon', 'tue', 'wed', 'thu', 'fri']]
# mean_weekday_prop.plot(x='weekday', y='prop', title='Proportion of customer biowaste to total waste on weekdays', grid=True) # lowest on Monday, Friday and highest on Thursday
# plt.ylim(ymin=0.3)
# plt.show()

## Aggregate measurements
mean_weekday_num_customers = waste_data.groupby(['weekday'])['num_customers'].mean()[['mon', 'tue', 'wed', 'thu', 'fri']]
customers_per_day = mean_weekday_num_customers.mean()
customers_per_week = mean_weekday_num_customers.sum()
customers_per_year = customers_per_week*41  # got this number from counting weeks in the past year from dataset

print("Amount thrown out per person per day at Kumpula: %d g" % mean_cbpc)
print("Amount thrown out per day at Kumpula: %d kg" % (mean_cbpc*customers_per_day/1000))
print("Amount thrown out per week at Kumpula: %d kg" % (mean_cbpc*customers_per_week/1000))
print("Amount thrown out per year at Kumpula: %d kg" % (mean_cbpc*customers_per_year/1000))


## Food waste compared to weather
weather_data = get_daily_weather_data_2016_to_2018()
waste_data['date'] = pd.to_datetime(waste_data.date)

combined = pd.merge(waste_data, weather_data)

b, m = polyfit(combined['precipitation_intensity'], combined['cbpc'], 1)
# plt.plot(combined['precipitation_intensity'], combined['cbpc'], '.')
# plt.plot(combined['precipitation_intensity'], b + m * combined['precipitation_intensity'], '-')
# plt.show()

b, m = polyfit(combined['air_temperature'], combined['cbpc'], 1)
# plt.plot(combined['air_temperature'], combined['cbpc'], '.')
# plt.plot(combined['air_temperature'], b + m * combined['air_temperature'], '-')
# plt.show()
