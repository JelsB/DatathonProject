from math import pi
from collections import Counter
from bokeh.layouts import widgetbox, row, column
from bokeh.models.widgets import TextInput, MultiSelect, Toggle, CheckboxGroup
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Panel, Range1d
from bokeh.palettes import Category20c, Category20_16
from bokeh.transform import cumsum
from bokeh.models import LogColorMapper, LinearColorMapper
from bokeh.palettes import Viridis256 as palette

# from .utils import country_dic
from .utils import country_dic
from .utils import country_shapes
from .utils import unique_countries_dic


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
        prepared_map_data = make_map_data(country_counter)

        return (ColumnDataSource(data), ColumnDataSource(country_data),
                ColumnDataSource(prepared_map_data))

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

    def make_map_data(country_counter):
        most_common = country_counter.most_common(500)
        unzipped = list(zip(*most_common))
        countries = list(unzipped[0])
        country_counts = list(unzipped[1])

        data = dict()
        data['country'] = countries
        data['counts'] = country_counts

        k = list(country_shapes.keys())
        country_xs = [country_shapes[i]['lats'] for i in k]
        country_ys = [country_shapes[i]['lons'] for i in k]
        country_names = [country_shapes[i]['name'] for i in k]
        # country_rates = list(range(len(country_names)))

        country_rates = [float('NaN')]*len(country_names)
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

    def make_plot(src, selected_countries):
        p = figure(plot_width=400, plot_height=400)
        # print('SRC', src['years'], src['counts'])
        # print(src.daa['labels'])
        p.multi_line('years', 'counts', color='colors', legend='labels',
                     source=src)
        p.xaxis.axis_label = 'Year'
        p.yaxis.axis_label = 'Counts'
        #
        # print(selected_countries)
        # for country in selected_countries:
        #     p.line('years', country, source=src)

        return p

    def make_pie_plot(src):

        p = figure(plot_width=400, plot_height=400, title="Pie Chart",
                   toolbar_location=None, tools="hover",
                   tooltips="@country: @counts", x_range=(-0.5, 1.0))

        p.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True),
                end_angle=cumsum('angle'),
                line_color="white", fill_color='color',
                legend='country', source=src)

        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color = None

        return p

    def make_map(src_map):
        color_mapper = LinearColorMapper(palette=palette)
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

    def make_flamingo(url):
        p = figure(x_range=(0, 100), y_range=(0, 100), plot_width=80,
                   plot_height=300,
                   toolbar_location=None, title=None)

        p.image_url(url=[url], x=0, y=30,
                    w=120, h=20)
        p.axis.visible = False
        p.grid.visible = False
        p.outline_line_color = None
        return(p)

    def update(attr, old, new):
        print('updating', multi_select.value)
        (word_frequency_to_plot,
         pie_src_new, map_src_new) = make_data_set(list_of_sp_obj,
                                                   text_input.value,
                                                   multi_select.value,
                                                   total_box.active)
        # print(text_input.value, word_frequency_to_plot)
        src.data.update(word_frequency_to_plot.data)
        pie_src.data.update(pie_src_new.data)
        map_src.data.update(map_src_new.data)

    word_colors = Category20_16
    word_colors.sort()

    text_input = TextInput(value="war", title="Label:")
    text_input.on_change('value', update)

    # multi country select
    multi_select = MultiSelect(title="Countries:", size=20, value=['CHN'],
                               options=list(unique_countries_dic.items()))
    multi_select.on_change('value', update)

    total_box = CheckboxGroup(labels=['Show Total'], active=[0, 1])
    total_box.on_change('active', update)

    src, pie_src, map_src = make_data_set(list_of_sp_obj, text_input.value,
                                          multi_select.value, total_box.active)

    p = make_plot(src, multi_select.value)
    pie = make_pie_plot(pie_src)
    map = make_map(map_src)

    url = ('https://cdn5.vectorstock.com/i/thumb-large/12/79/cartoon-flamingo-vector-5151279.jpg')
    flamingo = make_flamingo(url)

    # Put controls in a single element
    controls = widgetbox(text_input, total_box, multi_select)

    # Create a row layout
    layout = row(column(controls, flamingo), column(p, pie), map)

    # Make a tab with the layout
    tab = Panel(child=layout, title='Word frequency')

    return tab
