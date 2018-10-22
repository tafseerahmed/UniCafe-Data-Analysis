#!/usr/bin/env python
# coding: utf-8

# # Data Analysis - Area 3 (kumpula + vikki) - 12.09.2016 - 25.09.2018


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from weather import get_daily_weather_data_2016_to_2018
import seaborn as sns


weather =  get_daily_weather_data_2016_to_2018()
weather.drop(columns=["month"])

df = pd.read_csv('./data/customer_feedback.csv', sep=',')
df = df.drop(columns=["Area", "study", "Hour"])
df = df.rename(index=str, columns={"Date.1": "Day", "Date":"date"})
df['Date']=pd.to_datetime(df.Date)
df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
df['date']=pd.to_datetime(df.date)
data = pd.merge(df, weather, on="date", how="inner")

# These are the "Tableau 20" colors as RGB.    
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]    
  
# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
for i in range(len(tableau20)):    
    r, g, b = tableau20[i]    
    tableau20[i] = (r / 255., g / 255., b / 255.)   

plt.figure(figsize=(30, 15))   
ax = plt.subplot()
x=np.arange(len(data.date))
columns = ['Extremely Negative', 'Negative', 'Positive','Extremely Positive']
for i,y in enumerate(columns):
    plt.plot(x,data[y],color = tableau20[i])
plt.xticks(rotation='vertical',fontsize=40)
plt.yticks(fontsize=40)
start, end = ax.get_xlim()
plt.plot(x,4*data.air_temperature,color = 'black')
plt.plot(x,4*data.precipitation_intensity,color = 'purple')
plt.plot(x,4*data.cloud_amount,color = 'green')
plt.ylabel("No. of People", color='white', fontsize=30)
plt.xlabel("days", color='white', fontsize=30)
#ax.xaxis.set_ticks(np.arange(start, end, 50))
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
plt.grid(True)

ax.legend(loc='best',prop={'size':20})
plt.show()


# # Correlation Analysis with various parameters
# ## 1. Scatter Plots

x=['Extremely Negative', 'Negative',
       'Positive', 'Extremely Positive','Index', 'Net Promoter Score(tm)']

y=['precipitation_intensity', 'cloud_amount', 'air_temperature']
for i in y:
    for j in x:
        plt.figure(figsize=(30, 15))   
        ax = plt.subplot()
        plt.xticks(fontsize=40)
        plt.yticks(fontsize=40)
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')    
        plt.ylabel(i, color='white', fontsize=30)
        plt.xlabel(j, color='white', fontsize=30)
        plt.grid(True)
        sns.regplot(x=data[j], y=data[i], color=tableau20[0], scatter_kws={"alpha":0.5,'s':data['Total']}, line_kws={"color":"r","alpha":0.7,"lw":3},ax=ax)


# ## 2. Correlation Coefficients
# 

def plot_corr(df,size=10):
    '''Function plots a graphical correlation matrix for each pair of columns in the dataframe.

    Input:
        df: pandas DataFrame
        size: vertical and horizontal size of the plot'''

    corr = df.corr()
    fig, ax = plt.subplots(figsize=(size, size))
    f =ax.matshow(corr,cmap=plt.cm.GnBu)
    plt.xticks(range(len(corr.columns)), corr.columns,fontsize=30,color='white',rotation='vertical');
    plt.yticks(range(len(corr.columns)), corr.columns,fontsize=30,color='white');

df2=data[['Extremely Negative', 'Negative',
       'Positive', 'Extremely Positive','Total', 'Index', 'Net Promoter Score(tm)',
        'precipitation_intensity', 'cloud_amount', 'air_temperature']]
plot_corr (df2,20)


# ## 3. Time-Factor Analysis
# ### a. Weekly


TEMPLATE_DICT = {"Extremely Negative":0, "Negative":0, "Positive":0, "Extremely Positive":0}
monday,tuesday,wednesday,thursday,friday= {},{},{},{},{}
monday.update(TEMPLATE_DICT)
tuesday.update(TEMPLATE_DICT)
wednesday.update(TEMPLATE_DICT)
thursday.update(TEMPLATE_DICT)
friday.update(TEMPLATE_DICT)

for i in range (len(data["date"])):
    v = monday
    if data["Day of Week"][i] == "monday":
        v = monday
    elif data["Day of Week"][i] == "tuesday":
        v = tuesday
    elif data["Day of Week"][i] == "wednesday":
        v = wednesday
    elif data["Day of Week"][i] == "thursday":
        v = thursday
    elif data["Day of Week"][i] == "friday":
        v = friday
    v["Extremely Negative"]+=data["Extremely Negative"][i]
    v["Negative"]+=data["Negative"][i]
    v["Positive"]+=data["Positive"][i]
    v["Extremely Positive"]+=data["Extremely Positive"][i]
days=[monday,tuesday,wednesday,thursday,friday]  


counter = 0
names =["monday","tuesday","wednesday","thursday","friday"] 
fig, ax = plt.subplots(figsize=(15, 12))

plt.xlabel("Reactions",fontsize=14)
plt.ylabel("Number of people",fontsize=14)
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
for i in days:
    plt.bar(list(i.keys()), i.values(), color=tableau20[counter+2], label = names[counter],alpha=.7)
    counter +=1

ax.legend(loc=2, prop={'size':20})
plt.show()


mon,tue,wed,thu,fri= [],[],[],[],[]
for i in range (len(data["date"])):
    if data["Day of Week"][i] == "monday":
        mon.append(data["Total"][i])
    elif data["Day of Week"][i] == "tuesday":
        tue.append(data["Total"][i])
    elif data["Day of Week"][i] == "wednesday":
        wed.append(data["Total"][i])
    elif data["Day of Week"][i] == "thursday":
        thu.append(data["Total"][i])
    elif data["Day of Week"][i] == "friday":
        fri.append(data["Total"][i])
li = [mon,tue,wed,thu,fri]
fig, ax = plt.subplots(figsize=(20, 10))
plt.xlabel("days",fontsize=14)
plt.ylabel("Number of people",fontsize=14)
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)


for counter, i in enumerate(li):
    plt.plot(range(len(i)),i,color=tableau20[counter+4], label = names[counter])
plt.grid(True)
ax.legend(loc='best', prop={'size':20})
plt.show()


fig, ax = plt.subplots(figsize=(20, 10))
plt.xlabel("days",fontsize=14)
plt.ylabel("Number of people",fontsize=14)
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
for counter, i in enumerate(li):
    plt.scatter(range(len(i)),i,color=tableau20[counter+2], label = names[counter],s=i[counter]*.5, alpha=.8)
plt.grid(True)
ax.legend(loc=2, prop={'size':20})
plt.show()


# #### b. Monthly

# In[252]:


January.update(TEMPLATE_DICT)
February.update(TEMPLATE_DICT)
March.update(TEMPLATE_DICT)
April.update(TEMPLATE_DICT)
May.update(TEMPLATE_DICT)
June.update(TEMPLATE_DICT)
July.update(TEMPLATE_DICT)
August.update(TEMPLATE_DICT)
September.update(TEMPLATE_DICT)
October.update(TEMPLATE_DICT)
November.update(TEMPLATE_DICT)
December.update(TEMPLATE_DICT)

for i in range (len(data["date"])):
    v = monday
    if data["Month"][i] == "January":
        v = January
    elif data["Month"][i] == "February":
        v = February
    elif data["Month"][i] == "March":
        v = March
    elif data["Month"][i] == "April":
        v = April
    elif data["Month"][i] == "May":
        v = May
    elif data["Month"][i] == "June":
        v = June
    elif data["Month"][i] == "July":
        v = July
    elif data["Month"][i] == "August":
        v = August
    elif data["Month"][i] == "September":
        v = September
    elif data["Month"][i] == "October":
        v = October
    elif data["Month"][i] == "November":
        v = November
    elif data["Month"][i] == "December":
        v = December
    v["Extremely Negative"]+=data["Extremely Negative"][i]
    v["Negative"]+=data["Negative"][i]
    v["Positive"]+=data["Positive"][i]
    v["Extremely Positive"]+=data["Extremely Positive"][i]
m1=[January,February,March]
m2=[April,May,June]
m3=[July,August,September]
m4=[October,November,December]


counter = 0
names =['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
l = [m1,m2,m3,m4]
indx=-1
c=[5,10,15]
for k in l:
    fig, ax = plt.subplots(figsize=(15, 12))
    plt.xlabel("Reactions",fontsize=14)
    plt.ylabel("Number of people",fontsize=14)    
    for counter,i in enumerate(k):
        indx+=1
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        plt.ylim(0,15000)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=14)
        plt.bar(range(len(i)), list(i.values()), align='center',color=tableau20[(indx+2)%3],label = names[indx], alpha=.41,width=.99)
        plt.xticks(range(len(i)), list(i.keys()))
    ax.legend(prop={'size':20})


# ### c. Yearly

TEMPLATE_DICT = {"Extremely Negative":0, "Negative":0, "Positive":0, "Extremely Positive":0}
y_1617.update(TEMPLATE_DICT)
y_1718.update(TEMPLATE_DICT)

for i in range (len(data["date"])):
    if (data["Year"][i] == 2016 or data["Year"][i] == 2017):
        v = y_1617
    elif (data["Year"][i] == 2017 or data["Year"][i] == 2018):
        v = y_1718
    v["Extremely Negative"]+=data["Extremely Negative"][i]
    v["Negative"]+=data["Negative"][i]
    v["Positive"]+=data["Positive"][i]
    v["Extremely Positive"]+=data["Extremely Positive"][i]
years=[y_1617,y_1718]
names =["2016-17","2017-18"] 
fig, ax = plt.subplots(figsize=(15, 12))

plt.xlabel("Reactions",fontsize=14)
plt.ylabel("Number of people",fontsize=14)
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.bar(range(len(y_1617)), list(y_1617.values()),color='red',label = names[0], alpha=1,width=.99)
plt.bar(range(len(y_1718)), list(y_1718.values()) ,color=tableau20[0],label = names[1], alpha=1,width=.99)
plt.xticks(range(len(y_1617)), list(y_1617.keys()))

ax.legend(loc=2, prop={'size':20})
plt.show()




