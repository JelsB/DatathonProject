import re
from collections import Counter
from bokeh.layouts import widgetbox, row
from bokeh.models.widgets import TextInput, MultiSelect, Toggle, CheckboxGroup
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Panel
from bokeh.palettes import Category20c
from bokeh.transform import cumsum
from .make_speeches import Speech
from pathlib import Path
import pickle

from .utils import country_dic

dict_mentions = dict()
dict_is_mentioned_by = dict()

def create_dict(list_of_sp_obj):

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

    for sp in list_of_sp_obj:
        find_country_in_text(sp)
    with open('mentions.pickle', 'wb') as handle:
        print('Saving "Mentions" dictionary')
        pickle.dump(dict_mentions, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('is_mentioned_by.pickle','wb') as handles:
        print('Saving "Is Mentioned By" dictionary')
        pickle.dump(dict_is_mentioned_by, handles, protocol=pickle.HIGHEST_PROTOCOL)


def country_tab(list_sp_objs):

    def make_data_set(speeches, country, selected_countries_inp, selected_countries_out):
        counter = Counter()
        overall_counter = Counter()
        word_counter = dict()

        dict_of_selected_counters_inp = search_mentions(selected_countries_inp,selected_countries_out)
        dict_of_selected_counters_out = search_is_mentioned_by(selected_countries_inp,selected_countries_out)
        tot_mentions = dict()
        tot_mentioned_by = dict()

        for i in selected_countries_inp:
            tot_mentions[i]=dict()
            # for k,val in dict_of_selected_counters_inp[i].items():
                # print(val[1])
                # tot_mentions[i][k] = sum(val[1])

        for o in selected_countries_out:
            tot_mentioned_by[o]=dict()
            # for k,val in dict_of_selected_counters_out[i].items():
                # tot_mentioned_by[i][k] = sum(val[1])

        sp_country=[]
        for s in speeches:
            if s.country==country:
                sp_country.append(s)

        # sp_country = speeches[idx]
        # counts = defaultdict(int)
        for sp in list(sp_country):
            overall_counter += sp.word_frequency

        most_common_words = list(dict(overall_counter.most_common(10)).keys())
        print(most_common_words)
        # for sp in sp_country:
        #     counter[sp.year] += sp.word_frequency[word]

        for w in most_common_words:
            word_counter[w]=Counter()
            for sp in sp_country:
                if sp.word_frequency[w]:
                    add=sp.word_frequency[w]
                else:
                    add = 0
                word_counter[w][sp.year] += add

        #sort by years
        years = []
        counts = []

        for yr, cnt in sorted(dict(overall_counter.most_common(10)).items()):
            years.append(yr)
            counts.append(cnt)

        selected_data = dict()
        for word, cnter in word_counter.items():
            selected_data[word] = []
            for yr in years:
                if yr in cnter:
                    count = cnter[yr]
                else:
                    count = float('nan')
                selected_data[word].append(count)
        print(selected_data)

        multi_counts = [counts] + [val for val in selected_data.values()]
        multi_years = [years]*len(multi_counts)
        data = {'counts':multi_counts, 'years': multi_years}

        return ColumnDataSource(data),most_common_words#, ColumnDataSource(country_data)

    def update(attr, old, new):
        print('updating',multi_select_inp.value)
        (word_frequency_to_plot,
        most_com_words) = make_data_set(list_sp_objs,
                                    country_code,multi_select_inp.value,multi_select_out.value)
        # print(country_input.value, word_frequency_to_plot)
        src.data.update(word_frequency_to_plot.data)

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
        years = sorted(list(dict_of_int.keys()))
        number_of_mentions=[]
        for y in years:
            mentions = [x for x in dict_of_int[y] if x[0]==out_country]
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

    def make_plot(src, selected_countries):
        p = figure(plot_width=400, plot_height=400)
        # print('SRC', src['years'], src['counts'])
        # print(src.daa['labels'])
        p.multi_line('years', 'counts', color='colors', legend='labels',
                     source=src)
        #
        # print(selected_countries)
        # for country in selected_countries:
        #     p.line('years', country, source=src)

        return p

    def make_map(src_map):
        color_mapper = LogColorMapper(palette=palette)
        TOOLS = "pan,wheel_zoom,reset,hover,save"

        p = figure(plot_width=1150, plot_height=800,
                   title="World map", tools=TOOLS,
                   x_axis_location=None, y_axis_location=None,
                   tooltips=[
                       ("Name", "@name"), ("Mentions", "@rate")  # ,
                       # ("(Long, Lat)", "($x, $y)")
                   ])
        p.grid.grid_line_color = None
        p.hover.point_policy = "follow_mouse"
        p.x_range = Range1d(start=-180, end=180)
        p.y_range = Range1d(start=-90, end=90)

        p.grid.grid_line_color = None

        p.patches('x', 'y', source=src_map,
                  fill_color={'field': 'rate', 'transform': color_mapper},
                  fill_alpha=0.7, line_color="white", line_width=0.5)

        return(p)

    country_input = TextInput(value="China", title="Label:")
    country_input.on_change('value', update)


    # multi country select
    multi_select_inp = MultiSelect(title="Countries of interest:", value=['CHN'],
                                options=list(country_dic.items()))
    multi_select_inp.on_change('value', update)
    #
    # multi country select
    multi_select_out = MultiSelect(title="Countries they mention:", value=['IND'],
                                options=list(country_dic.items()))
    multi_select_out.on_change('value', update)
    #
    country_code = list(country_dic.keys())[list(country_dic.values()).index(country_input.value)]
    src,mcw = make_data_set(list_sp_objs, country_code,multi_select_inp.value,multi_select_out.value)

    p = make_plot(src,mcw)
    # Put controls in a single element
    controls = widgetbox(country_input)
    controls2 = widgetbox(multi_select_inp,multi_select_out)

    # Create a row layout
    layout = row(controls, p, controls2)

    # Make a tab with the layout
    tab = Panel(child=layout, title = 'Most Common words')

    return tab
