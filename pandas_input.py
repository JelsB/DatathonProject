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
#define a function to search for a keyword and return the year and country-wise
#counts
def search_keyword(data,keyword):
    indices = data.text.str.contains(keyword)
    print(f'{indices.values.sum()} out of {len(indices.values)} speeches have the word {keyword} in them')
    data_of_interest = data[indices]
    # data_of_interest.country.value_counts().plot(kind='bar')
    # data_of_interest.plot(x='year',y='country',kind='bar',subplots=True,sharex=True)
    data_of_interest.year.value_counts(ascending=True).plot(kind='bar')
    plt.show()
    return None

#Path to the data
filename = Path('./data/UN/un-general-debates.csv')
#Load in the data and print the column names
dataset = pd.read_csv(filename)
print(dataset.columns)

#work with only one year of data (for now) or country (for example India)
year_of_interest = 1989
country_of_interest = 'IND'

#The sessions go from 25 to 70, each corresponding to a year from 1970 to 2015
print(f'Sessions from {dataset.session.min()} to {dataset.session.max()}')
print(f'during the years {dataset.year.min()} to {dataset.year.max()}')

#Two ways to slice by column name:
#The first one also allows row slicing
# print(data.ix[:,'year'])
#The second is easier to read and gives us the same result
# print(data['year'])

#Filter data from the year we want to work with:
year_indices = dataset.year==year_of_interest
country_indices = dataset.country==country_of_interest

#data['year_indices'] gives us the data frame with entries of the year we want.
#we can further obtain the countries that participated that year with
# countries = data.country[year_indices].values
#if we do not use the '.values', then we get a recarray which has a dtype='object'
# print(len(countries))
years_array = dataset.year[country_indices]
print(f'List of years when {country_of_interest} has spoken')
print(years_array.values)
# dataset['country'].value_counts().plot(kind='bar')
#To find the indices where IND occurs in the country list (just as an example,
#this is meant to be used in the text column). Returns -1 where not found.
#Follows default indexing, but can be changed by giving a 'start' value.
#Verdict: str.find() does something weird, use str.contains()
# indices_country_find = data.country.str.find('IN')
# print(data.country.values[indices_country_find])
print('Using the search function "contains"')
indices_country_contains = dataset.country.str.contains('IND')
# print(dataset.country.values[indices_country_contains])

#now to try and apply this to the text column
text_contents = dataset.text[year_indices]
# plt.show()
# data.plot(y=countries,kind='bar')
search_keyword(dataset,"war")
#get a unique list of countries and get yearly data country by country
# unique_countries = data.country.unique()
# for c in unique_countries:
