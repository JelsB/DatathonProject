import pandas as pd
from pathlib import Path
import matplotlib
#This is only when using python3 with Mac
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import json
##########################################################
#snipped to open a .json file (country abbreviations)
# with json_file.open('r') as f:
#         data_dict = json.load(f)
#         print('Done reading in')
###########################################################


#Path to the data
filename = Path('./data/UN/un-general-debates.csv')
#Load in the data and print the column names
data = pd.read_csv(filename)
print(data.columns)

#work with only one year of data (for now) or country (for example India)
year_of_interest = 1989
country_of_interest = 'IND'

#The sessions go from 25 to 70, each corresponding to a year from 1970 to 2015
print(f'Sessions from {data.session.min()} to {data.session.max()}')
print(f'during the years {data.year.min()} to {data.year.max()}')

#Two ways to slice by column name:
#The first one also allows row slicing
# print(data.ix[:,'year'])
#The second is easier to read and gives us the same result
# print(data['year'])

#Filter data from the year we want to work with:
year_indices = data.year==year_of_interest
country_indices = data.country==country_of_interest

#data['year_indices'] gives us the data frame with entries of the year we want.
#we can further obtain the countries that participated that year with
# countries = data.country[year_indices].values
#if we do not use the '.values', then we get a recarray which has a dtype='object'
# print(len(countries))
years_array = data.year[country_indices]
print(years_array.values)
data['country'].value_counts().plot(kind='bar')
# plt.show()
# data.plot(y=countries,kind='bar')

#get a unique list of countries and get yearly data country by country
# unique_countries = data.country.unique()
# for c in unique_countries:
