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
year = 1989
country = 'IND'

#Two ways to slice by column name:
#The first one also allows row slicing
# print(data.ix[:,'year'])
#The second is easier to read and gives us the same result
# print(data['year'])

#Filter data from the year we want to work with:
year_indices = data.year==year
country_indices = data.country==country
#data['year_indices'] gives us the data frame with entries of the year we want.
#we can further obtain the countries that participated that year with
# countries = data[year_indices].country.values
# print(len(countries))
years_array = data.year[country_indices]
print(years_array.values)
data['country'].value_counts().plot(kind='bar')
plt.show()
# data.plot(y=countries,kind='bar')
