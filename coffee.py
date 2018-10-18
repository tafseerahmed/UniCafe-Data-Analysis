import numpy as np
import pandas as pd
from dateutil.parser import parse as parse_datetime
from datetime import datetime
import matplotlib.pyplot as plt
import calendar
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
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

def draw_scatter(x_col_name, data=combined):
    plt.scatter(data[x_col_name], data['number_sold'], s=6)
    plt.title(" %s vs. coffee sales" % (x_col_name))   
    plt.xlabel(x_col_name)
    plt.ylabel("Sold units")
    plt.show()

combined.month = combined.date.apply(lambda date: date.month)
during_term = combined[combined.month.isin([1, 2, 3, 4, 9, 10, 11, 12])].dropna()

#regression and plots

#draw_scatter('precipitation_intensity')
#draw_scatter('cloud_amount')
#draw_scatter('air_temperature', during_term)

X = during_term[['air_temperature', 'precipitation_intensity', 'cloud_amount']]
Y =  during_term['number_sold']
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)
model = LinearRegression()
model.fit(X, Y)
y_pred = model.predict(X_test)

print('Coefficients: \n', model.coef_)
print("Mean squared error: %.2f"% mean_squared_error(y_test, y_pred))
print('Variance score: %.2f' % r2_score(y_test, y_pred))
print(f'Number of observations is {sales_data.shape[0]}.')
print(f'Mean number of coffees sold is {round(mean_sold)}.')
print(f'The standard deviation is {round(std_sold)}.')
for i, v in weekday_means.items():
    print(f'Mean for {i} {round(v)}')
