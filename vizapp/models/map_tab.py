import bokeh.plotting as bkp
import bokeh.models as bkm


def make_map():

    with open("./countries.geo.json", "r") as f:
        countries = bkm.GeoJSONDataSource(geojson=f.read())

    p = bkp.figure(width=1000, height=600, tools=tools, title='World Countries',
                   x_axis_label='Longitude', y_axis_label='Latitude')
    p.background_fill_color = "aqua"
    p.x_range = bkm.Range1d(start=-180, end=180)
    p.y_range = bkm.Range1d(start=-90, end=90)
    p.patches("xs", "ys", color="white", line_color="black", source=countries)

    layout = row(p)

    # Make a tab with the layout
    tab = Panel(child=layout, title='Word frequency')

    return tab
