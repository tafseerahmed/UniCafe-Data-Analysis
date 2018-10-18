import numpy as np
import pandas as pd

#hours between 10-14 in utc time:
FILTER_WEATHER_HOURS = ['08:00', '09:00', '10:00', '11:00'] #TODO verify this is not different during daylight saving time

get_daily_mean = lambda df, column: df.groupby(['year', 'month', 'day'])[column].mean().values

def get_daily_weather_data_2016_to_2018():
    weather_data = pd.read_csv('./data/weather_by_hour_2016_to_2018.csv', sep=',')
    #remove times which are not around lunch time:
    weather_data = weather_data[weather_data.Time.isin(FILTER_WEATHER_HOURS)]
    #rename columns:
    weather_data = weather_data.rename(index=str, columns={"Year": "year", "m": "month", "d": "day"})
    #initialize empty data frame
    daily_data  = pd.DataFrame(columns = ['date', 'precipitation_intensity', 'cloud_amount', 'air_temperature', 'month'])
    #add date
    daily_data['date'] = pd.to_datetime(weather_data[['year', 'month', 'day']], utc=True).unique()
    #add some interesting weather data: 
    daily_data['precipitation_intensity'] = get_daily_mean(weather_data, 'Precipitation intensity (mm/h)') 
    daily_data['cloud_amount'] = get_daily_mean(weather_data, 'Cloud amount (1/8)')    
    daily_data['air_temperature'] = get_daily_mean(weather_data, 'Air temperature (degC)')    
    return daily_data
