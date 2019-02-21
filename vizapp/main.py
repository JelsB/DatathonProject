# Pandas for data management
import pandas as pd

# os methods for manipulating paths
from pathlib import Path

# Bokeh basics
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs


# Each tab is drawn by one script
from models.speech import speech_tab,create_dictionary_mentions


# Using included state data from Bokeh for map
from bokeh.sampledata.us_states import data as states

# Read data into dataframes
filename = Path('./data/UN/un-general-debates.csv')
#Load in the data and print the column names
dataset = pd.read_csv(filename)
raw_speeches = dataset.text
sample_raw_speeches = raw_speeches[:50]
sample_dataset = dataset[:50]
# print(raw_speeches)
# flights = pd.read_csv(join(dirname(__file__), 'data', 'flights.csv'),
# 	                                          index_col=0).dropna()

# Formatted Flight Delay Data for map
# map_data = pd.read_csv(join(dirname(__file__), 'data', 'flights_map.csv'),
#                             header=[0,1], index_col=0)

# Create each of the tabs
<<<<<<< HEAD
create_dictionary_mentions(dataset)
exit()
tab1 = speech_tab(sample_raw_speeches)
=======
tab1 = speech_tab(sample_dataset)
>>>>>>> 7c8380c39dba3e42500bffd1ecec0bb65e9c7256
# tab2 = density_tab(flights)
# tab3 = table_tab(flights)
# tab4 = map_tab(map_data, states)
# tab5 = route_tab(flights)

# Put all the tabs into one application
tabs = Tabs(tabs = [tab1])#, tab2, tab3, tab4, tab5])
