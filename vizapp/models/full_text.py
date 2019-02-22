
def text_tab(list_of_sp_obj):

    def make_text_plot(list_of_sp_obj, src):
        pass

    def update(attr, old, new):
        new_text_src = make_data_set(list_of_sp_obj,
                                      select.value,
                                      multi_select.value,
                                      total_box.active)
        # print(text_input.value, word_frequency_to_plot)
        src.data.update(new_text_src.data)
        pie_src.data.update(pie_src_new.data)


    country_combos =

    country_select = Select(title="Option:", value="foo",
                            options=list(country_dic.items())
    select = Select(title="Speech:", value="USA 1970", options=country_combos)
