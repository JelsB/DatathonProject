import pickle
from pathlib import Path
# import bokeh.models as bkm


pick_file = Path.cwd().joinpath('data/members_dic.pkl')
# shapes_file = Path.cwd().joinpath('data/countries.geo.json')
shapes_file = Path.cwd().joinpath('data/country_geo.pkl')

with pick_file.open(mode='rb') as pkl_file:
    country_dic = pickle.load(pkl_file)

with shapes_file.open(mode='rb') as pkl_file:
    country_shapes = pickle.load(pkl_file)

# with shapes_file.open() as f:
#     country_shapes = bkm.GeoJSONDataSource(geojson=f.read())
