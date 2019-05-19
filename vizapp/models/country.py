import re
from collections import Counter
from bokeh.layouts import widgetbox, row, column
from bokeh.models.widgets import TextInput, MultiSelect, Toggle, CheckboxGroup, Dropdown
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Panel, Range1d
from bokeh.palettes import Category20c, Category20_16
from bokeh.io import output_file, show
from bokeh.transform import cumsum
from .make_speeches import Speech
from pathlib import Path
import pickle
from bokeh.models import LogColorMapper
from bokeh.palettes import Viridis6 as palette


from .utils import country_shapes
from .utils import country_dic

list_country_codes = list(country_dic.keys())
dict_mentions = dict()
dict_is_mentioned_by = dict()


def create_dict(list_of_sp_obj):

    def find_country_in_text(sp_obj):
        for country_abbr, country_name in country_dic.items():
            if country_name in sp_obj.word_frequency.keys():
                try:
                    x = dict_mentions[sp_obj.country]
                except KeyError:
                    dict_mentions[sp_obj.country] = dict()
                print(f'Sp obj country name {sp_obj.country}')
                if sp_obj.year in dict_mentions[sp_obj.country]:
                    dict_mentions[sp_obj.country][sp_obj.year].append(
                        [country_abbr, sp_obj.word_frequency[country_name]])
                else:
                    dict_mentions[sp_obj.country][sp_obj.year] = [
                        [country_abbr, sp_obj.word_frequency[country_name]]]

                try:
                    x = dict_is_mentioned_by[country_abbr]
                except KeyError:
                    dict_is_mentioned_by[country_abbr] = dict()
                print(f'Country name: {country_name} and abbr {country_abbr}')
                print(f'Sp obj country name {sp_obj.country}')
                if sp_obj.year in dict_is_mentioned_by[country_abbr]:
                    dict_is_mentioned_by[country_abbr][sp_obj.year].append(
                        [sp_obj.country, sp_obj.word_frequency[country_name]])
                else:
                    dict_is_mentioned_by[country_abbr][sp_obj.year] = [
                        [sp_obj.country, sp_obj.word_frequency[country_name]]]

    for sp in list_of_sp_obj:
        find_country_in_text(sp)
    with open('mentions.pickle', 'wb') as handle:
        print('Saving "Mentions" dictionary')
        pickle.dump(dict_mentions, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('is_mentioned_by.pickle', 'wb') as handles:
        print('Saving "Is Mentioned By" dictionary')
        pickle.dump(dict_is_mentioned_by, handles, protocol=pickle.HIGHEST_PROTOCOL)


def country_tab(list_sp_objs):

    def make_data_set(speeches, country, type_display):
        counter = Counter()
        overall_counter = Counter()
        word_counter = dict()

        dict_of_selected_counters_inp = search_mentions(country)
        dict_of_selected_counters_out = search_is_mentioned_by(country)
        tot_mentions = Counter()
        tot_mentioned_by = Counter()

        for k, val in dict_of_selected_counters_inp.items():
            tot_mentions += Counter(dict(dict_of_selected_counters_inp[k]))

        for k, val in dict_of_selected_counters_inp.items():
            tot_mentioned_by += Counter(dict(dict_of_selected_counters_out[k]))

        sp_country = []
        for s in speeches:
            if s.country == country:
                sp_country.append(s)

        # sp_country = speeches[idx]
        # counts = defaultdict(int)
        for sp in list(sp_country):
            overall_counter += sp.word_frequency

        most_common_words = list(dict(overall_counter.most_common(10)).keys())
        most_common_counter = Counter()
        for mcw in most_common_words:
            most_common_counter[mcw] = overall_counter[mcw]
        word = list(dict(most_common_counter).keys())
        counts = list(dict(most_common_counter).values())
        # for sp in sp_country:
        #     counter[sp.year] += sp.word_frequency[word]

        for w in most_common_words:
            word_counter[w] = Counter()
            for sp in sp_country:
                if sp.word_frequency[w]:
                    add = sp.word_frequency[w]
                else:
                    add = 0
                word_counter[w][sp.year] += add

        years = range(1970, 2016, 1)
        selected_data = dict()
        for w, cnter in word_counter.items():
            selected_data[w] = []
            for yr in years:
                if yr in cnter:
                    count = cnter[yr]
                else:
                    count = float('nan')
                selected_data[w].append(count)
        # print(selected_data)

        multi_counts = [val for val in selected_data.values()]
        multi_years = [years] * len(multi_counts)
        colors = word_colors[:len(multi_counts)]
        labels = most_common_words
        data = {'counts': multi_counts, 'years': multi_years, 'colors': colors,
                'labels': labels}
        if type_display == 'mentions':
            prepared_map_data = make_map_data(tot_mentions)
        else:
            prepared_map_data = make_map_data(tot_mentioned_by)
        print(data)
        return ColumnDataSource(data), ColumnDataSource(prepared_map_data)

    def update(attr, old, new):
        country_code = list(country_dic.keys())[list(
            country_dic.values()).index(country_input.value)]
        print('updating ', country_input.value, country_code, dropdown.value)
        (word_frequency_to_plot,
         map_data) = make_data_set(list_sp_objs,
                                   country_code, dropdown.value)
        # print(country_input.value, word_frequency_to_plot)
        src.data.update(word_frequency_to_plot.data)
        map_src.data.update(map_data.data)

    def search_mentions(input_country, output_countries=list_country_codes):
        specific_mentions_dict = yearwise_data(input_country, 'mentions')
        return specific_mentions_dict

    def search_is_mentioned_by(input_country, output_countries=list_country_codes):

        specific_mentioned_by_dict = yearwise_data(input_country, 'is_mentioned_by')
        return specific_mentioned_by_dict

    def yearwise_data(inp_country, m):
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
        # print(inp_country,out_country,m)
        input_file = Path.cwd().joinpath(f'data/{m}.pickle')
        # Path.cwd().joinpath('data/members_dic.pkl')

        with input_file.open('rb') as pkl_file:
            dict = pickle.load(pkl_file)
            try:
                dict_of_int = dict[inp_country]
            except KeyError:
                print("Check the country again!")
                return None, None
        years = sorted(list(dict_of_int.keys()))
        return dict_of_int

    def make_plot(src):
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

    def make_map_data(country_counter1):
        # 1 A mentions B , 2 A is mentioned by B
        unzipped = list(zip(*country_counter1))
        countries = list(dict(country_counter1).keys())
        country_counts = list(dict(country_counter1).values())

        data = dict()
        data['country'] = countries
        data['counts'] = country_counts

        k = list(country_shapes.keys())
        country_xs = [country_shapes[i]['lats'] for i in k]
        country_ys = [country_shapes[i]['lons'] for i in k]
        country_names = [country_shapes[i]['name'] for i in k]
        # country_rates = list(range(len(country_names)))

        country_rates = [float('NaN')] * len(country_names)
        country_inds = {country_shapes[j]['ID']: i for i, j in enumerate(k)}

        for i in range(len(data['country'])):
            try:
                country_rates[country_inds[data['country'][i]]] = data['counts'][i]
            except:
                pass

        src_map = dict(
            x=country_xs,
            y=country_ys,
            name=country_names,
            rate=country_rates,
        )

        return src_map

    def make_map(src_map, country, type_display):
        color_mapper = LogColorMapper(palette=palette)
        TOOLS = "pan,wheel_zoom,reset,hover,save"

        p = figure(plot_width=1150, plot_height=800,
                   title='World Map', tools=TOOLS,
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

    country_input = TextInput(value="India", title="Label:")
    country_code = list(country_dic.keys())[list(country_dic.values()).index(country_input.value)]
    country_input.on_change('value', update)

    # For the dropdown
    menu = [("Mentions", "mentions"), ("Is mentioned by", "is_mentioned_by")]
    dropdown = Dropdown(label="Type of display", button_type="primary", value='mentions', menu=menu)
    dropdown.on_change('value', update)

    word_colors = Category20_16
    word_colors.sort()

    src, map_src = make_data_set(list_sp_objs, country_code, dropdown.value)

    p = make_plot(src)
    map = make_map(map_src, country_input, dropdown.value)
    # Put controls in a single element
    controls = widgetbox(country_input)

    # Create a row layout
    layout = row(column(controls, dropdown), map)

    # Make a tab with the layout
    tab = Panel(child=layout, title='Country referencing')

    return tab
