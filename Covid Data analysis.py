#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
import os
import urllib
get_ipython().run_line_magic('matplotlib', 'inline')



#Downloading data from various sources.

# files = { "WHO-COVID-19-global-data.csv" : "https://covid19.who.int/WHO-COVID-19-global-data.csv",
#           "time_series_covid19_confirmed_global.csv": "https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
#           "time_series_covid19_deaths_global.csv": "https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",
#           "time_series_covid19_recovered_global.csv": "https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
#          }

# for file,url in files.items():
#     os.makedirs(file_path, exist_ok=True)
#     csv_path = os.path.join(file_path,file)
#     urllib.request.urlretrieve(url,csv_path)





#Using downloaded file
file_path = os.path.join("data","covid")
covid_df = pd.read_csv("D:\Mihir\Study\Projects\GitHub\Covid--19_Dashboard\data\India\covid_19_india.csv")
vaccine_df = pd.read_csv("D:\Mihir\Study\Projects\GitHub\Covid--19_Dashboard\data\India\covid_vaccine_statewise.csv")

#Dropping Time

covid_df.drop(["Sno", "Time", "ConfirmedIndianNational", "ConfirmedForeignNational"], inplace = True, axis = 1)


covid_df['Date'] = pd.to_datetime(covid_df['Date'],format = '%Y-%m-%d')
covid_df['year'] = covid_df['Date'].dt.year
covid_df['month'] = covid_df['Date'].dt.month


#Active cases = Total number of confirmed cases - the sum of cured cases + deaths reported


#Active cases

covid_df['Active_cases'] = covid_df['Confirmed'] - (covid_df['Cured'] + covid_df['Deaths'])

#Making a pivot table

statewise = pd.pivot_table(covid_df, values = ['Confirmed', 'Deaths', 'Cured'], index = 'State/UnionTerritory', aggfunc = max)

#Recovery Rate = (Total number of cured cases / Total number of confirmed cases) * 100

statewise['Recovery Rate'] = (statewise['Cured']/statewise['Confirmed']) * 100


#Mortality Rate = (Total number of Deaths / Total number of confirmed cases) * 100

statewise['Mortality Rate'] = (statewise['Deaths']/statewise['Confirmed']) * 100


statewise = statewise.sort_values(by = 'Confirmed', ascending = False)

#read documentation on cmaps in matplotlib.org website

statewise.style.background_gradient( cmap = 'cubehelix' )

#Top 10 active cases states

top_10_active_cases = covid_df.groupby(by = 'State/UnionTerritory').max()[['Active_cases', 'Date']].sort_values(by = ['Active_cases'], ascending = False).reset_index()


fig = plt.figure(figsize = (16,9))


plt.title('Top 10 States with most active cases in India', size = 25)

ax = sns.barplot(data = top_10_active_cases.iloc[:10], y = 'Active_cases', x = 'State/UnionTerritory', linewidth = 2, edgecolor = 'red')


#Top 10 active cases states

top_10_active_cases = covid_df.groupby(by = 'State/UnionTerritory').max()[['Active_cases', 'Date']].sort_values(by = ['Active_cases'], ascending = False).reset_index()
fig = plt.figure(figsize = (16,9))
plt.title('Top 10 States with most active cases in India', size = 25)
ax = sns.barplot(data = top_10_active_cases.iloc[:10], y = 'Active_cases', x = 'State/UnionTerritory', linewidth = 2, edgecolor = 'red')
plt.xlabel('States')
plt.ylabel('Total Active Cases')
plt.show()


#Top states with highest deaths

top_10_deaths = covid_df.groupby(by = 'State/UnionTerritory').max()[['Deaths', 'Date']].sort_values(by = ['Deaths'], ascending = False).reset_index()
fig = plt.figure(figsize = (18,5))
plt.title('Top 10 States with most Deaths in India', size = 25)
ax = sns.barplot(data = top_10_deaths.iloc[:12], y = 'Deaths', x = 'State/UnionTerritory', linewidth = 2, edgecolor = 'black')
plt.xlabel('States')
plt.ylabel('Total Deaths')
plt.show()

#To fix - duplication of states 

#Growth trend


#f_quarter = covid_df.groupby(by = 'month').max()
f_quarter = covid_df.groupby(by = 'month').sum()
fig = plt.figure(figsize = (12,6))
states_for_plot = ['Maharashtra', 'Karnataka','Kerala', 'Tamil Nadu', 'Uttar Pradesh']
#ax = sns.lineplot(data = covid_df[covid_df['State/UnionTerritory'].isin(['Maharashtra', 'Karnataka','Kerala', 'Tamil Nadu', 'Uttar Pradesh'])],x = 'Date', y = 'Active_cases', hue = 'State/UnionTerritory')
ax = sns.lineplot(data = covid_df[covid_df['State/UnionTerritory'].isin(states_for_plot)],x = 'Date', y = 'Active_cases', hue = 'State/UnionTerritory')
ax.set_title("Top 5 Affected States in India", size = 16)

#Question - Insights from the plot above
# - We observe a sudden increase in active cases after March 2021.

vaccine_df.rename(columns = {'Updated On' : 'Vaccine_Date'}, inplace = True)

vaccine_df.isnull().sum()

vaccination = vaccine_df.drop(columns = ['Sputnik V (Doses Administered)', 'AEFI', '18-44 Years (Doses Administered)','45-60 Years (Doses Administered)', '60+ Years (Doses Administered)'], axis = 1)


#Male vs Female vaccination

male  = vaccination['Male(Individuals Vaccinated)'].sum()
female = vaccination['Female(Individuals Vaccinated)'].sum()
px.pie(names = ['Male', 'Female'], values = [male,female], title = "Vacctination based on Genders")

#Remove rows where state = India

vaccine = vaccine_df[vaccine_df.State != 'India']

vaccine.rename(columns = { 'Total Individuals Vaccinated': 'Total'}, inplace = True)


#Most vaccinated States

max_vac = vaccine.groupby('State')['Total'].sum().to_frame('Total')
max_vac = max_vac.sort_values('Total', ascending= False) [:5]

fig = plt.figure(figsize = (10,5))
plt.title('Top 5 Vaccinated States in India', size = 20)
x = sns.barplot(data = max_vac.iloc[:10],y = max_vac.Total, x = max_vac.index, linewidth = 2, edgecolor = 'black' )
plt.xlabel('States')
plt.ylabel('Vaccination')
plt.show()

#least vaccinated States

least_vac = vaccine.groupby('State')['Total'].sum().to_frame('Total')
least_vac = least_vac.sort_values('Total', ascending= True) [:5]


fig = plt.figure(figsize = (10,5))
plt.title('Top 5 Least Vaccinated States in India', size = 20)
x = sns.barplot(data = max_vac.iloc[:10],y = least_vac.Total, x = least_vac.index, linewidth = 2, edgecolor = 'grey' )
plt.xlabel('States')
plt.ylabel('Vaccination')
plt.show()

