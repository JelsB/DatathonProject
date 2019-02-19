import pandas as pd
from pathlib import Path
import json

with json_file.open('r') as f:
        data_dict = json.load(f)
    print('Done reading in')

filename = Path('./data/UN/un-general-debates.csv')

data = pd.read_csv(filename)
# print(data.head())

#data['country']
#These two are equivalent. The first part also allows row slicing
print(data.ix[:,'year'])
print('###############')
print(data['year'])
