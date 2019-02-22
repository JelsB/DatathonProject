import re
from collections import Counter
from bokeh.layouts import widgetbox
from bokeh.models.widgets import TextInput
import pickle
from models.speech import Speech

# load in country code dictionary:
with open('data/members_dic.pkl', 'rb') as pkl_file:
    country_dic = pickle.load(pkl_file)

dict_mentions = dict()
dict_is_mentioned_by = dict()

class Country(object):
    "the country related dictionary creation"

    def __init__(self, df_row):
        super(Country, self).__init__()
        self.year = df_row.year
        self.country = df_row.country



def create_dict(pd_df):

    def find_country_in_text(sp_obj):
        for country_abbr,country_name in country_dic.items():
            if country_name in sp_obj.word_frequency.keys():
                try:
                    x= dict_mentions[sp_obj.country]
                except KeyError:
                    dict_mentions[sp_obj.country] = dict()
                print(f'Sp obj country name {sp_obj.country}')
                if sp_obj.year in dict_mentions[sp_obj.country]:
                    dict_mentions[sp_obj.country][sp_obj.year].append([country_abbr,sp_obj.word_frequency[country_name]])
                else:
                    dict_mentions[sp_obj.country][sp_obj.year] = [[country_abbr,sp_obj.word_frequency[country_name]]]

                try:
                    x= dict_is_mentioned_by[country_abbr]
                except KeyError:
                    dict_is_mentioned_by[country_abbr] = dict()
                print(f'Country name: {country_name} and abbr {country_abbr}')
                print(f'Sp obj country name {sp_obj.country}')
                if sp_obj.year in dict_is_mentioned_by[country_abbr]:
                    dict_is_mentioned_by[country_abbr][sp_obj.year].append([sp_obj.country,sp_obj.word_frequency[country_name]])
                else:
                    dict_is_mentioned_by[country_abbr][sp_obj.year] = [[sp_obj.country,sp_obj.word_frequency[country_name]]]

                #
                # dict_mentions[sp_obj.country][sp_obj.year]=[country_abbr,sp_obj.word_frequency[country_name]]
                # print("didn't break one")
                # dict_is_mentioned_by[country_abbr][sp_obj.year][sp_obj.country]=sp_obj.word_frequency[country_name]
                # print("didn't break two")


    list_of_sp_obj = list((Speech(row) for idx, row in pd_df.iterrows()))
    for sp in list_of_sp_obj:
        find_country_in_text(sp)
    with open('mentions.pickle', 'wb') as handle:
        print('Saving "Mentions" dictionary')
        pickle.dump(dict_mentions, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('is_mentioned_by.pickle','wb') as handles:
        print('Saving "Is Mentioned By" dictionary')
        pickle.dump(dict_is_mentioned_by, handles, protocol=pickle.HIGHEST_PROTOCOL)
    # find_country_in_text(row for row in list_of_rows)
    # print(list_of_rows)
