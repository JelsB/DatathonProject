import pickle
import pandas as pd
from pathlib import Path

# Bokeh basics
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs
from bokeh.themes import built_in_themes

# Each tab is drawn by one script
from models.speech import speech_tab
from models.full_text import text_tab
from models.country import country_tab
from models.make_speeches import (make_speeches, pickle_list_of_speeches,
                                  unpickle_list_of_speeches)

# Read data for first time
# Read data into dataframes
# filename = Path('./data/UN/un-general-debates.csv')
# dataset = pd.read_csv(filename)
# speech_objects = make_speeches(dataset)
# pickle_list_of_speeches(speech_objects, './data/')

# Read data from pickled file
speech_objects = unpickle_list_of_speeches(Path('./data/all_speeches.pickle'))

# Create each of the tabs
tab1 = speech_tab(speech_objects)
tab2 = country_tab(speech_objects)
tab3 = text_tab(speech_objects)

# Put all the tabs into one application
tabs = Tabs(tabs=[tab1, tab2, tab3])

# Put the tabs in the current document for display
curdoc().theme = 'light_minimal'
curdoc().add_root(tabs)
