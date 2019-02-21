import re
from collections import Counter

class Speech(object):
    """docstring for Speech."""
    def __init__(self, text):
        super(Speech, self).__init__()
        self.text = text
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




def speech_tab(pd_series):

    def do_stuff(list_of_sp_obj):
        for sp in list_of_sp_obj:
            print(f'Number of words: {sp.number_of_words}')
            print(f'Average word length: {sp.average_word_length}')
            print(f"Times \"war\" mentioned: {sp.word_frequency['war']}")

    def make_plot(src):
        pass


    print('making objs')
    # print(pd_series.values)
    list_of_sp_obj = list((Speech(text) for text in pd_series.values))
    print('done making objs')
    do_stuff(list_of_sp_obj)

def create_dictionary_mentions(pd_df):
    dict_is_mentioned_by = {}
    dict_mentions = {}
    
