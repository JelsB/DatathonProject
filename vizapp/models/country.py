import re
from collections import Counter
from bokeh.layouts import widgetbox
from bokeh.models.widgets import TextInput
import pickle
from models.speech import Speech

# load in country code dictionary:
with open('../data/members_dic.pkl', 'rb') as pkl_file:
    country_dic = pickle.load(pkl_file)

dict_mentions = dict()
dict_is_mentioned_by = dict()

class Country(object):
    "the country related dictionary creation"

    def __init__(self, df_row):
        super(Country, self).__init__()
        self.year = df_row.year
        self.country = df_row.country
        self.mentions = self


    def find_country_in_text(self,row):
        sp = Speech(row)
        for country_abbr,country_name in country_dic.itmes():
            if country_name in sp.word_frequency.keys():
                dict_mentions[self.country][self.year][country_name]=sp.word_frequency[country_name]
                dict_is_mentioned_by[country_name][self.year][self.country]=sp.word_frequency[country_name]

    def create_dictionary_mentions(pd_df):


def create_dict(pd_df):
    find_country_in_text(row for idx,row in pd_df.iterrows())


    list_of_sp_obj = list((Speech(row) for idx, row in pd_df.iterrows()))
