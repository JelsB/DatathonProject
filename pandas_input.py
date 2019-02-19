import pandas as pd
from pathlib import Path
import json
##########################################################
# with json_file.open('r') as f:
#         data_dict = json.load(f)
#         print('Done reading in')
###########################################################
#work with only one year of data (for now)
year = 1989
#Path to the data
filename = Path('./data/UN/un-general-debates.csv')
#Load in the data and print the first 5 lines
data = pd.read_csv(filename)
# print(data.head())

#data['country']
#These two are equivalent. The first part also allows row slicing
# print(data.ix[:,'year'])
# print('###############')
# print(data['year'])

#Filter data from the year we want to work with:
year_indices = data['year']==year
#data['year_indices'] gives us the data frame with entries of the year we want.
#we can further obtain the countries that participated that year with
print(data[year_indices]['country'])
