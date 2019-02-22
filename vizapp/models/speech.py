import re
import nltk
from math import pi
from collections import Counter, defaultdict
from bokeh.layouts import widgetbox, row
from bokeh.models.widgets import TextInput, MultiSelect
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Panel
from bokeh.palettes import Category20c, Category20_16
from bokeh.transform import cumsum

# from .utils import country_dic
from .utils import country_dic



class Speech(object):
    """docstring for Speech."""
    def __init__(self, df_row):
        super(Speech, self).__init__()
        self.year = df_row.year
        self.country = df_row.country
        self.session = df_row.session
        self.text = df_row.text
        self.cleaned_sentences = self.clean_text_keep_punctuation()
        self.cleaned_text = self.clean_text_remove_punctuation()
        self.list_of_words = self.get_words()
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
        return len(nltk.tokenize.sent_tokenize(self.cleaned_sentences))

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

    # def remove_stopwords(self)


    def get_breakdown(self):
        stopwords = set(ntlk.corpus.stopwords.words('english'))
        filtered_words = []
        for word in self.list_of_words:
            if word not in stopwords:
                filtered_words.append(word)


        return

    def replace_long_spaces(self, text):
        return re.sub(r'\s+', ' ', text)

    def remove_newline(self, text):
        return re.sub(r'\n+\s+', '', text)

    def remove_tab(self,text):
        return re.sub(r'\t',' ',text)

    def remove_linenumber(self,text):
        return re.sub(r'\n[0-9]+.','\n',text)

    def remove_trailing_and_leading_quote(self,text):
        return re.sub(r'[\'\n,\n\',\' , \']','\n',text)

    def remove_parentheses(self,text):
        return re.sub(r'\n\(.\)','\n',text)

    def remove_common(self,text):
        return re.sub(r'[:,;,?,!,\.,\,,\t]',' ',text)

    def clean_text_keep_punctuation(self):
        text = self.text
        text = self.remove_tab(text)
        text = self.remove_linenumber(text)
        text = self.remove_trailing_and_leading_quote(text)
        text = self.remove_parentheses(text)
        text = self.remove_newline(text)
        text = self.replace_long_spaces(text)
        return text

    def clean_text_remove_punctuation(self):
        text = self.cleaned_sentences
        text = self.remove_common(text)
        text = self.replace_long_spaces(text)
        return text


    def get_words(self):
        list_of_words = nltk.tokenize.word_tokenize(self.cleaned_text)

        # remove leftover empty elements
        list_of_words = list(filter(None, list_of_words))
        return list_of_words




def speech_tab(pd_df):

    def do_stuff(list_of_sp_obj):
        for sp in list_of_sp_obj:
            print(f'Number of words: {sp.number_of_words}')
            print(f'Average word length: {sp.average_word_length}')
            print(f"Times \"war\" mentioned: {sp.word_frequency['war']}")


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

        multi_counts = [counts] + [val for val in selected_data.values()]
        multi_years = [years]*len(multi_counts)
        colors = word_colors[:len(multi_counts)]
        labels = ['Total'] + selected_countries
        print(labels)
        data = {'counts':multi_counts, 'years': multi_years, 'colors': colors,
                'labels': labels}


        country_data = make_pie_data(country_counter)

        return ColumnDataSource(data), ColumnDataSource(country_data)

    def make_pie_data(country_counter, max_countries=15):
        if max_countries>19:
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

        p.axis.axis_label=None
        p.axis.visible=False
        p.grid.grid_line_color = None

        return p



    def update(attr, old, new):
        print('updating', multi_select.value)
        (word_frequency_to_plot,
        pie_src_new) = make_data_set(list_of_sp_obj,
                                    text_input.value,
                                     multi_select.value)
        # print(text_input.value, word_frequency_to_plot)
        src.data.update(word_frequency_to_plot.data)
        pie_src.data.update(pie_src_new.data)



    print('making objs')
    # print(pd_df.values)
    list_of_sp_obj = list((Speech(row) for idx, row in pd_df.iterrows()))
    list_of_sp_obj = sorted(list_of_sp_obj, key=lambda sp: sp.year)
    # print(len(list_of_sp_obj))
    print('done making objs')
    # do_stuff(list_of_sp_obj)

    word_colors = Category20_16
    word_colors.sort()

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
