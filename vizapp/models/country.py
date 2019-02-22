import re
from collections import Counter
from bokeh.layouts import widgetbox, row
from bokeh.models.widgets import TextInput
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Panel
from bokeh.palettes import Category20c
from bokeh.transform import cumsum
import pickle
from .speech import Speech

# load in country code dictionary:
with open('data/members_dic.pkl', 'rb') as pkl_file:
    country_dic = pickle.load(pkl_file)
#hello
dict_mentions = dict()
dict_is_mentioned_by = dict()

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


    list_of_sp_objects = list((Speech(row) for idx, row in pd_df.iterrows()))
    for sp in list_of_sp_objects:
        find_country_in_text(sp)
    with open('mentions.pickle', 'wb') as handle:
        print('Saving "Mentions" dictionary')
        pickle.dump(dict_mentions, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('is_mentioned_by.pickle','wb') as handles:
        print('Saving "Is Mentioned By" dictionary')
        pickle.dump(dict_is_mentioned_by, handles, protocol=pickle.HIGHEST_PROTOCOL)


def country_tab(pd_df):

    def update(attr, old, new):
        print('updating', multi_select.value)
        (word_frequency_to_plot,
        pie_src_new) = make_data_set(list_of_sp_obj,
                                    text_input.value,
                                     multi_select.value)
        # print(text_input.value, word_frequency_to_plot)
        src.data.update(word_frequency_to_plot.data)
        pie_src.data.update(pie_src_new.data)

    def search_mentions(input_countries,output_countries):
        '''Input countries: ['USA','CHN']
           Output countries: ['IND','PAK','COL']
           number of times input countries mention output countries
           returns a dict of dicts.
           ex: {'USA':{'IND':[[1989,1990,1995],[2,3,4],
                    'PAK':[[1975,1988,1999,2012],[1,2,3,1]],
                    'COL':[[2000,2001],[1,4]]},
                'CHN':{'IND':[[1979,1996,2010],[1,2,4]],
                         'PAK':[[1975,1988,1999,2012],[1,2,3,1]],
                         'COL':[[2000,2001],[1,4]]}}
          '''
        specific_mentions_dict=dict()
        for i in input_countries:
            try:
                dict_of_int = mentions_dict[i]
            except KeyError:
                #Do something, this is temporary
                print("Invalid country, next one...")
                continue
            specific_mentions_dict[i]=dict()
            for o in output_countries:
                years,mentions = yearwise_data(i,o,'mentions')
                specific_mentions_dict[i][o]=[years,mentions]
        return specific_mentions_dict

    def search_is_mentioned_by(input_countries,output_countries):
        '''Input countries: ['USA','CHN']
           Output countries: ['IND','PAK','COL']
           number of times input countries are mentioned by output countries
           returns a dict of dicts.
           ex: {'USA':{'IND':[[1989,1990,1995],[2,3,4],
                    'PAK':[[1975,1988,1999,2012],[1,2,3,1]],
                    'COL':[[2000,2001],[1,4]]},
                'CHN':{'IND':[[1979,1996,2010],[1,2,4]],
                         'PAK':[[1975,1988,1999,2012],[1,2,3,1]],
                         'COL':[[2000,2001],[1,4]]}}
          '''
        specific_mentioned_by_dict=dict()
        for i in input_countries:
            try:
                dict_of_int = mentions_dict[i]
            except KeyError:
                #Do something, this is temporary
                print("Invalid country, next one...")
                continue
            specific_mentioned_by_dict[i]=dict()
            for o in output_countries:
                years,mentions = yearwise_data(i,o,'is_mentioned_by')
                specific_mentioned_by_dict[i][o]=[years,mentions]
        return specific_mentioned_by_dict


    def yearwise_data(inp_country, out_country,m):
        '''Function to get yearly data on either mentions or is mentioned by
        data for a specific country.
        @param inp_country: country input.
        @param out_country: country of interest
        @param m: 'mentions' or 'is_mentioned_by'
        Example: After receiving an input country 'IND', to find the number of
        mentions of 'USA' in speeches by 'IND'.
        -Here, dict_of_interest is the mentions dict of IND
        >>>yearwise_data('IND','USA','mentions')
        <returns two arrays: years and mentions
        >>>[1971,1975,1995,2000],[1,2,2,1]

        The same thing can be applied to an is_mentioned_by dict
        '''
        # [x for x in dict_searched_country[1989] if x[0]=='COL']
        with open(Path(f'{m}.pickle'), 'rb') as pkl_file:
            dict = pickle.load(pkl_file)
            try:
                dict_of_int = dict[inp_country]
            except KeyError:
                print("Check the country again!")
                return None,None
        years = list(dict_of_int.keys()).sort()
        number_of_mentions=[]
        for y in years:
            mentions = [x for x in dict_searched_country[y] if x[0]==out_country]
            if len(mentions):
                number_of_mentions.append(mentions[0])
            else:
                number_of_mentions.append(0)
        return years,number_of_mentions

    def basic_country_stats(pd_df_country,years_array):
        '''@param pd_df_country: the dataset filtered by the country input
        @param years_array: depends on input from slider
        '''

        list_of_sp_objs=list(Speech(row) for idx,row in pd_df_country.iterrows())

    def make_data_set(speeches, word, selected_countries):
        counter = Counter()
        country_counter = Counter()
        dict_of_selected_counters = dict()

        for c in selected_countries:
            dict_of_selected_counters[c] = Counter()

        if ' ' in word:
            for sp in speeches:
                count = sp.text.count(word)
                if count > 0:
                    sp.word_frequency[word] = count

        # counts = defaultdict(int)
        for sp in speeches:
            counter[sp.year] += sp.word_frequency[word]
            country_counter[sp.country] += sp.word_frequency[word]

            if sp.country in selected_countries:
                if sp.word_frequency[word]:
                    add = sp.word_frequency[word]
                else:
                    add = 0
                dict_of_selected_counters[sp.country][sp.year] += add
        # sort by years
        years = []
        counts = []


        for yr, cnt in sorted(counter.items()):
            years.append(yr)
            counts.append(cnt)

        selected_data = dict()
        for country_name, cnter in dict_of_selected_counters.items():
            selected_data[country_name] = []
            for yr in years:
                if yr in cnter:
                    count = cnter[yr]
                else:
                    count = float('nan')
                selected_data[country_name].append(count)
        print(selected_data)
            #
            # for yr, cnt in sorted(val.items()):
            #     if not yr in years:
            #         selected_data[key].append(0)
            #     else:
            #         selected_data[key].append(cnt)

            # selected_data[key] = list(sorted(val.values()))
            # selected_data[f'years_{key}'] = list(val.keys())
        multi_counts = [counts] + [val for val in selected_data.values()]
        multi_years = [years]*len(multi_counts)
        data = {'counts':multi_counts, 'years': multi_years}


        country_data = make_pie_data(country_counter)

        return ColumnDataSource(data), ColumnDataSource(country_data)



    text_input = TextInput(value="war", title="Label:")
    text_input.on_change('value', update)

    # multi country select
    multi_select = MultiSelect(title="Countries:", value=['CHN'],
                                options=list(country_dic.items()))
    multi_select.on_change('value', update)
    #

    src, pie_src = make_data_set(list_of_sp_obj, text_input.value, multi_select.value)

    p = make_plot(src, multi_select.value)
    pie = make_pie_plot(pie_src)
    # Put controls in a single element
    controls = widgetbox(text_input, multi_select)


    # Create a row layout
    layout = row(controls, p, pie)

    # Make a tab with the layout
    tab = Panel(child=layout, title = 'Word frequency')

    return tab
