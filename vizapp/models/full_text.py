from collections import Counter
from bokeh.layouts import widgetbox, row
from bokeh.models.widgets import TextInput, Select, Paragraph
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Panel
from bokeh.palettes import Category20c, Category20_16

from .utils import country_dic


def text_tab(list_of_sp_obj):


    def make_text_data(list_of_sp_obj, country, year):
        year = int(year)
        print(year, country)
        for sp in list_of_sp_obj:
            if (sp.year==year and sp.country in country):
                print('YES')
                data={'text':[sp.cleaned_sentences]}
                return ColumnDataSource(data)

    def make_text_plot(src):
        print(src)
        p = Paragraph(text=src.data['text'][0], width=1000)
        return p

    def update(attr, old, new):
        c_name = country_select.value
        country_combos = [str(sp.year) for sp in list_of_sp_obj if sp.country==c_name ]
        years = sorted(country_combos)
        print(years, type(years))
        select_speech.options = years

    def update_speech(attr, old, new):
        print('change speech!!!')
        print(select_speech.value, country_select.value)
        new_text_src = make_text_data(list_of_sp_obj, country_select.value,
                                      select_speech.value)
        print(new_text_src)
        # print(text_input.value, word_frequency_to_plot)
        src.data.update(new_text_src.data)
        print(src)




    country_select = Select(title="Option:", value="FRA",
                            options=list(country_dic.keys()))
    country_select.on_change('value', update)

    select_speech = Select(title="Speech:", value="1970",)
    select_speech.on_change('value', update_speech)

    src = make_text_data(list_of_sp_obj, country_select.value, select_speech.value)
    p = make_text_plot(src)
    # Put controls in a single element
    controls = widgetbox(country_select, select_speech)

    # Create a row layout
    layout = row(controls, p)

    # Make a tab with the layout
    tab = Panel(child=layout, title='Speech')

    return tab
