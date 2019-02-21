import re
from math import pi
from collections import Counter, defaultdict
from bokeh.layouts import widgetbox, row
from bokeh.models.widgets import TextInput
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Panel
from bokeh.palettes import Category20c
from bokeh.transform import cumsum


class Speech(object):
    """docstring for Speech."""
    def __init__(self, df_row):
        super(Speech, self).__init__()
        self.year = df_row.year
        self.country = df_row.country
        self.session = df_row.session
        self.text = df_row.text
        self.cleaned_text = self.remove_punctuations()
        self.list_of_words = self.split_text()
        self.number_of_words = self.count_total_words()
        self.average_word_length = self.get_average_word_length()
        self.number_of_sentences = self.count_sentences()
        self.word_frequency = self.count_unique_words()


    def count_total_words(self):
        return len(self.list_of_words)

    def get_average_word_length(self):
        return sum([len(word) for word in self.list_of_words])/self.number_of_words

    def count_sentences(self):
        """Count punctuations"""
        return len(re.findall('[.?!]', self.text))

    def count_unique_words(self):
        """
        Return Counter object.

        Looks like a dict.
        Example:
        >>> words = ['a', 'b', 'c', 'a', 'rr', 'rr']

        >>> Counter(words)
        Counter({'a': 2, 'rr': 2, 'b': 1, 'c': 1})

        """
        return Counter(self.list_of_words)

    def most_used_words(self, show=10):
        """Return sorted list of tuples with word and frequency

        [('a', 2), ('rr', 2), ('b', 1)]

        """
        # Counter obj
        return self.word_frequency.most_common(show)

    def replace_long_spaces(self, text):
        return re.sub(r'\s+', ' ', text)

    def remove_newline(self, text):
        return re.sub(r'\n+\s+', '', text)

    def remove_comma(self, text):
        return re.sub(r',', ' ', text)

    def remove_dot(self, text):
        return re.sub('\.', ' ', text)

    def remove_punctuations(self):

        text = self.remove_comma(self.text)
        text = self.remove_dot(text)
        text = self.remove_newline(text)
        text = self.replace_long_spaces(text)

        return text

    def split_text(self):
        list_of_words = self.cleaned_text.split(" ")
        # remove leftover empty elements
        list_of_words = list(filter(None, list_of_words))

        return list_of_words




def speech_tab(pd_df):

    def do_stuff(list_of_sp_obj):
        for sp in list_of_sp_obj:
            print(f'Number of words: {sp.number_of_words}')
            print(f'Average word length: {sp.average_word_length}')
            print(f"Times \"war\" mentioned: {sp.word_frequency['war']}")


    def make_data_set(speeches, word):
        counter = Counter()
        country_counter = Counter()

        # counts = defaultdict(int)
        for sp in speeches:
            counter[sp.year] += sp.word_frequency[word]
            country_counter[sp.country] += sp.word_frequency[word]

        # sort by years
        years = []
        counts = []

        for yr, cnt in sorted(counter.items()):
            years.append(yr)
            counts.append(cnt)

        data = {'counts':counts, 'years': years}


        country_data = make_pie_data(country_counter)

        return ColumnDataSource(data), ColumnDataSource(country_data)

    def make_pie_data(country_counter, max_countries=10):
        if max_countries>20:
            print('CAN\'T')

        most_common = country_counter.most_common(max_countries)
        unzipped = list(zip(*most_common))
        countries = unzipped[0]
        country_counts = unzipped[1]
        data = dict()
        data['country'] = countries
        data['counts'] = country_counts
        # NOTE: this is wrt the most common ones. TDOD change!
        total_counts = sum(data['counts'])
        data['angle'] = [i/total_counts*2*pi for i in data['counts']]
        data['color'] = Category20c[len(data['country'])]

        return data


    def make_plot(src):
        p = figure(plot_width=400, plot_height=400)
        # print('SRC', src['years'], src['counts'])
        p.line('years', 'counts', source=src)

        return p

    def make_pie_plot(src):

        p = figure(plot_height=350, title="Pie Chart", toolbar_location=None,
               tools="hover", tooltips="@country: @counts", x_range=(-0.5, 1.0))

        p.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True),
        end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend='country', source=src)

        p.axis.axis_label=None
        p.axis.visible=False
        p.grid.grid_line_color = None

        return p



    def update(attr, old, new):
        word_frequency_to_plot, pie_src_new = make_data_set(list_of_sp_obj, text_input.value)
        # print(text_input.value, word_frequency_to_plot)
        src.data.update(word_frequency_to_plot.data)
        pie_src.data.update(pie_src_new.data)



    print('making objs')
    # print(pd_df.values)
    list_of_sp_obj = list((Speech(row) for idx, row in pd_df.iterrows()))
    list_of_sp_obj = sorted(list_of_sp_obj, key=lambda sp: sp.year)
    print(len(list_of_sp_obj))
    print('done making objs')
    do_stuff(list_of_sp_obj)



    text_input = TextInput(value="war", title="Label:")

    text_input.on_change('value', update)

    src, pie_src = make_data_set(list_of_sp_obj, text_input.value)

    p = make_plot(src)
    pie = make_pie_plot(pie_src)
    # Put controls in a single element
    controls = widgetbox(text_input)
    # controls = WidgetBox(carrier_selection, binwidth_select, range_select)


    # Create a row layout
    layout = row(controls, p, pie)

    # Make a tab with the layout
    tab = Panel(child=layout, title = 'Word frequency')

    return tab
