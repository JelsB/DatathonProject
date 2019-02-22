import re
import nltk
from collections import Counter

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
        self.filtered_words = self.filter_on_stopwords()
        self.list_of_stems = self.get_stems()
        self.number_of_stems = self.get_total_stems()


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

    def filter_on_stopwords(self):
        stopwords = set(nltk.corpus.stopwords.words('english'))
        filtered_words = []
        for word in self.list_of_words:
            if word not in stopwords:
                filtered_words.append(word)
        return filtered_words

    def get_stems(self):
        words = self.filtered_words
        stemmed_words = []
        stemmer = nltk.stem.PorterStemmer()
        for w in words:
            stemmed_words.append(stemmer.stem(w))
        unique_stems = set(stemmed_words)
        return unique_stems

    def get_total_stems(self):
        return len(self.list_of_stems)

    # def get_breakdown(self):
    #     words = self.filtered_words
    #     positions = nltk.pos_tag(words)
    #     unique_positions = set(positions)
    #
    #
    #     return

    def replace_long_spaces(self, text):
        return re.sub(r'\s+', ' ', text)

    def remove_newline(self, text):
        return re.sub(r'\n+\s+', ' ', text)

    def remove_linenumber(self,text):
        return re.sub(r'[\n[0-9]+\.|^[0-9]+\.]','\n',text)

    def remove_trailing_and_leading_quote(self,text):
        return re.sub(r'[\'\n|\n\'|\' | \']','\n',text)

    def remove_parentheses(self,text):
        return re.sub(r'\n\(.\)','\n',text)

    def remove_common(self,text):
        return re.sub(r'[:|;|?|!|\.|,|\t]',' ',text)

    def clean_text_keep_punctuation(self):
        text = self.text
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




def make_speeches(pd_df):
    print('making objs')
    # print(pd_df.values)
    list_of_sp_obj = list((Speech(row) for idx, row in pd_df.iterrows()))
    list_of_sp_obj = sorted(list_of_sp_obj, key=lambda sp: sp.year)
    # print(len(list_of_sp_obj))
    print('done making objs')
    return list_of_sp_obj
