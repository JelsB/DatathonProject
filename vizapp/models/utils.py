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


unique_countries = ['MDV', 'FIN', 'NER', 'URY', 'ZWE', 'PHL', 'SDN', 'RUS', 'CHN', 'ESP', 'SUR', 'ARG', 'SLV', 'MYS', 'NPL', 'PRT', 'COL', 'BLR', 'MAR', 'LCA', 'EGY', 'MEX', 'BEL', 'BRN', 'RWA', 'CAN', 'ALB', 'GRC', 'KNA', 'GUY', 'LBR', 'ATG', 'MOZ', 'JPN', 'GAB', 'BGD', 'SWE', 'TUR', 'TCD', 'SYR', 'CMR', 'JAM', 'LUX', 'ITA', 'AGO', 'CRI', 'CSK', 'BFA', 'MNG', 'BHR', 'HTI', 'OMN', 'CIV', 'TGO', 'CYP', 'MUS', 'MMR', 'ARE', 'GTM', 'GRD', 'LBY', 'LKA', 'TZA', 'SGP', 'NOR', 'LAO', 'ISL', 'AFG', 'CHL', 'DMA', 'UKR', 'KEN', 'BLZ', 'FRA', 'MLI', 'VCT', 'VEN', 'MLT', 'GHA', 'GIN', 'GBR', 'ISR', 'YUG', 'BRB', 'IRQ', 'HUN', 'AUT', 'POL', 'GNB', 'BWA', 'MRT', 'SWZ', 'DNK', 'DOM', 'MDG', 'NIC', 'BDI', 'CUB', 'IRN', 'PAK', 'SEN', 'BGR', 'YEM', 'STP', 'NLD', 'VUT', 'BOL', 'PNG', 'SLB', 'DEU', 'ROU', 'KHM', 'TUN', 'BRA', 'IND', 'IDN', 'AUS', 'COD', 'HND', 'GNQ', 'FJI', 'IRL', 'DZA', 'USA', 'LSO', 'GMB', 'PER', 'DDR', 'THA', 'JOR', 'COG', 'NGA', 'ECU', 'SAU', 'QAT', 'SYC', 'ETH', 'TTO', 'PRY', 'VNM', 'NZL', 'PAN', 'MWI', 'DJI', 'BEN', 'SOM', 'ZMB', 'CPV', 'BHS', 'KWT', 'UGA', 'COM', 'ZAF', 'LBN', 'SLE', 'KOR', 'BIH', 'TON', 'EU', 'HRV', 'NRU', 'TUV', 'NAM', 'SMR', 'LIE', 'MKD', 'TLS', 'FSM', 'KIR', 'BTN', 'SVK', 'WSM', 'MNE', 'GEO', 'LTU', 'AND', 'TJK', 'MHL', 'EST', 'LVA', 'CAF', 'TKM', 'MDA', 'SSD', 'KGZ', 'AZE', 'PSE', 'PRK', 'CZE', 'ERI', 'ARM', 'UZB', 'PLW', 'VAT', 'MCO', 'CHE', 'KAZ', 'SVN']

unique_countries_dic = {key:val for key, val in country_dic.items() if key in unique_countries}
# with shapes_file.open() as f:
#     country_shapes = bkm.GeoJSONDataSource(geojson=f.read())
