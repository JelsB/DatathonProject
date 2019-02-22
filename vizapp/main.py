# Pandas for data management
import pandas as pd

# os methods for manipulating paths
from pathlib import Path

#pickle for the dictionary
import pickle

# Bokeh basics
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs


# Each tab is drawn by one script
from models.speech import speech_tab
from models.country import create_dict


# Using included state data from Bokeh for map
from bokeh.sampledata.us_states import data as states

# Read data into dataframes
filename = Path('./data/UN/un-general-debates.csv')
#Load in the data and print the column names
dataset = pd.read_csv(filename)
raw_speeches = dataset.text
sample_raw_speeches = raw_speeches[:]
sample_dataset = dataset[:]
# print(raw_speeches)
# flights = pd.read_csv(join(dirname(__file__), 'data', 'flights.csv'),
# 	                                          index_col=0).dropna()

# load in country code dictionary:
with open('./data/members_dic.pkl', 'rb') as pkl_file:
    country_dic = pickle.load(pkl_file)

# Formatted Flight Delay Data for map
# map_data = pd.read_csv(join(dirname(__file__), 'data', 'flights_map.csv'),
#                             header=[0,1], index_col=0)

# Create each of the tabs
# tab1 = speech_tab(sample_dataset)

# tab2 = density_tab(flights)
# tab3 = table_tab(flights)
# tab4 = map_tab(map_data, states)
# tab5 = route_tab(flights)

create_dict(dataset)
# Put all the tabs into one application
tabs = Tabs(tabs = [tab1])#, tab2, tab3, tab4, tab5])

# Put the tabs in the current document for display
curdoc().add_root(tabs)
