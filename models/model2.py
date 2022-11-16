import pandas as pd
import numpy as np
import pickle

data = pd.read_csv("https://raw.githubusercontent.com/jbrownlee/Datasets/master/daily-total-female-births.csv",parse_dates=True,infer_datetime_format=True,index_col=0)
rolling_mean_7 = data.Births.rolling(7).mean().shift(1)
rolling_mean_7.to_pickle("model2.pkl")
