from math import pi
from collections import Counter
from bokeh.layouts import widgetbox, row
from bokeh.models.widgets import TextInput, MultiSelect, Toggle, CheckboxGroup
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Panel, Range1d
from bokeh.palettes import Category20c, Category20_16
from bokeh.transform import cumsum
from bokeh.events import ButtonClick

# from .utils import country_dic
from .utils import country_dic
from .utils import country_shapes


def speech_tab(list_of_sp_obj):

    def make_data_set(speeches, word, selected_countries, show_total):
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

        multi_counts = [val for val in selected_data.values()]
        labels = selected_countries
        if show_total:
            multi_counts = [counts] + multi_counts
            labels = ['Total'] + labels

        colors = word_colors[:len(multi_counts)]
        multi_years = [years]*len(multi_counts)

        data = {'counts': multi_counts, 'years': multi_years, 'colors': colors,
                'labels': labels}

        country_data = make_pie_data(country_counter)

        return ColumnDataSource(data), ColumnDataSource(country_data)

    def make_pie_data(country_counter, max_countries=15):
        if max_countries > 19:
            print('CAN\'T')

        most_common = country_counter.most_common(max_countries)
        unzipped = list(zip(*most_common))
        countries = list(unzipped[0])
        country_counts = list(unzipped[1])
        data = dict()
        data['country'] = countries
        data['counts'] = country_counts
        all_counts = sum(country_counter.values())
        top_counts = len(country_counts)
        data['country'].append('other')
        data['counts'].append(all_counts-top_counts)

        # NOTE: this is wrt the most common ones. TDOD change!
        total_counts = sum(data['counts'])
        data['angle'] = [i/total_counts*2*pi for i in data['counts']]
        data['color'] = Category20c[len(data['country'])]

        return data

    def make_plot(src, selected_countries):
        p = figure(plot_width=400, plot_height=400)
        # print('SRC', src['years'], src['counts'])
        # print(src.daa['labels'])
        p.multi_line('years', 'counts', color='colors', legend='labels', source=src)
        #
        # print(selected_countries)
        # for country in selected_countries:
        #     p.line('years', country, source=src)

        return p

    def make_pie_plot(src):

        p = figure(plot_width=400, plot_height=400, title="Pie Chart", toolbar_location=None,
                   tools="hover", tooltips="@country: @counts", x_range=(-0.5, 1.0))

        p.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True),
                end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend='country', source=src)

        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color = None

        return p

    def make_map():
        tools = "pan,wheel_zoom,box_zoom,reset, hover"

        p = figure(width=1000, height=600, tools=tools,
                   title='World Countries', x_axis_label='Longitude',
                   y_axis_label='Latitude')
        p.background_fill_color = "midnightblue"
        p.x_range = Range1d(start=-180, end=180)
        p.y_range = Range1d(start=-90, end=90)
        p.patches("xs", "ys", color="white", line_color="black",
                  source=country_shapes)
        return p

    def update(attr, old, new):
        print('updating', multi_select.value)
        (word_frequency_to_plot,
         pie_src_new) = make_data_set(list_of_sp_obj,
                                      text_input.value,
                                      multi_select.value,
                                      total_box.active)
        # print(text_input.value, word_frequency_to_plot)
        src.data.update(word_frequency_to_plot.data)
        pie_src.data.update(pie_src_new.data)

    word_colors = Category20_16
    word_colors.sort()

    text_input = TextInput(value="war", title="Label:")
    text_input.on_change('value', update)

    # multi country select
    multi_select = MultiSelect(title="Countries:", value=['CHN'],
                               options=list(country_dic.items()))
    multi_select.on_change('value', update)

    total_box = CheckboxGroup(labels=['Show Total'], active=[0, 1])
    total_box.on_change('active', update)

    src, pie_src = make_data_set(list_of_sp_obj, text_input.value,
                                 multi_select.value, total_box.active)

    p = make_plot(src, multi_select.value)
    pie = make_pie_plot(pie_src)
    map = make_map()

    # Put controls in a single element
    controls = widgetbox(text_input, total_box, multi_select)

    # Create a row layout
    layout = row(controls, p, pie, map)

    # Make a tab with the layout
    tab = Panel(child=layout, title='Word frequency')

    return tab
