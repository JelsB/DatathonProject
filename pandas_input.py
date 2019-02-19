import pandas as pd
from pathlib import Path

filename = Path.cwd().joinpath('/data/UN/un-general-debates.csv')

data = pd.read_csv(filename)
# print(data.head())
print(data.columns)
