import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import datasets
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True)
print(X)
clf = LogisticRegression().fit(X,y)
pickle.dump(clf, open('model1.pkl','wb'))




