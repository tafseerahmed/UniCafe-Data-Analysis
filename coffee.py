import numpy as np
import pandas as pd
from dateutil.parser import parse as parse_datetime
from datetime import datetime
import matplotlib.pyplot as plt
import calendar
from weather import get_daily_weather_data_2016_to_2018 

DATE_NAMES = list(calendar.day_name)
DATE_FORMAT = '%d.%m.%Y' # e.g 13.1.2016
parse_date = lambda date_str: np.datetime64(datetime.strptime(date_str, DATE_FORMAT))

#initialize data
sales_data = pd.read_csv('./data/kumpula_coffees.csv', sep=';').rename(index=str, columns={"date": "date_str"})
weather_data = get_daily_weather_data_2016_to_2018()

#general metrics
mean_sold = sales_data.number_sold.mean()
std_sold = sales_data.number_sold.std()

#weekday metrics
sales_data['date'] = sales_data.date_str.apply(parse_date)
sales_data['weekday'] = sales_data.date.apply(lambda dt: DATE_NAMES[dt.weekday()])
weekday_means = sales_data.groupby(['weekday'])['number_sold'].mean()

#joining datasets
combined = pd.merge(sales_data, weather_data)

#drawing charts
plt.scatter(combined['precipitation_intensity'], combined['number_sold'])      
plt.show()

print(f'Number of observations is {sales_data.shape[0]}.')
print(f'Mean number of coffees sold is {round(mean_sold)}.')
print(f'The standard deviation is {round(std_sold)}.')
for i, v in weekday_means.items():
    print(f'Mean for {i} {round(v)}')
