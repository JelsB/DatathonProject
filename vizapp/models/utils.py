import pickle
from pathlib import Path

pick_file = Path.cwd().joinpath('data/members_dic.pkl')


with pick_file.open(mode='rb') as pkl_file:
    country_dic = pickle.load(pkl_file)
