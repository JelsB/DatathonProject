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
                # data={'text':[sp.cleaned_sentences]}
                data={'text':sp.list_of_words}
                return ColumnDataSource(data)

    def get_source_text(src):
        text = ' '.join(['{}'.format(t) for t in src.data['text']])
        return ColumnDataSource({'text':[text]})

    def make_text_plot(src):
        txt = get_source_text(src)
        p = Paragraph(text=txt.data['text'][0],width=800,height=400)
        return p

    def update(attr, old, new):
        c_name = country_select.value
        country_combos = [str(sp.year) for sp in list_of_sp_obj if sp.country==c_name ]
        years = sorted(country_combos)
        print(years, type(years))
        select_speech.options = years

    def update_speech(attr, old, new):
        new_text_src = make_text_data(list_of_sp_obj, country_select.value,
                                      select_speech.value)
        src.data.update(new_text_src.data)
        par.text = ' '.join(['{}'.format(t) for t in src.data['text']])




    country_select = Select(title="Option:", value="FRA",
                            options=list(country_dic.keys()))
    country_select.on_change('value', update)

    select_speech = Select(title="Speech:", value="1970",options=None)
    # select_speech = Select(title="Speech:")
    select_speech.on_change('value', update_speech)

    src = make_text_data(list_of_sp_obj, country_select.value, select_speech.value)
    # par = Paragraph()
    par = make_text_plot(src)

    # Put controls in a single element
    controls = widgetbox(country_select, select_speech)

    # Create a row layout
    layout = row(controls, par)

    # Make a tab with the layout
    tab = Panel(child=layout, title='Speech')

    return tab
