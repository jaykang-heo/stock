import pandas as pd
from keras import models, layers

data = pd.read_csv('trainData/0.csv')
del data['Unnamed: 0'], data['8일선'], data['10일선'], data['30일선'], data['45일선'], data['60일선'], data['120일선']


print(data)