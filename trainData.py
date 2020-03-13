import pandas as pd
import numpy as np
import os
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from sklearn.model_selection import train_test_split

trainX = []
trainY = []
np.set_printoptions(suppress=True)

for file in os.listdir('trainData'):
    data = pd.read_csv('trainData/'+file)
    label = data['성공'].iloc[0]
    del data['Unnamed: 0'], data['날짜'], data['8일선'], data['10일선'], data['30일선'], data['45일선'], data['60일선'], data['120일선'], data['성공']
    trainX.append(data.values)
    trainY.append(label)
trainX = np.asarray(trainX, dtype=np.float32)
trainY = np.asarray(trainY, dtype=np.float32)

X_train, X_test, Y_train, Y_test = train_test_split(trainX, trainY, test_size=0.2)

regressor = Sequential()

regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], 7)))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50))
regressor.add(Dropout(0.2))

regressor.add(Dense(units = 1))

regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

regressor.fit(X_train, Y_train, epochs = 100, batch_size = 32)

regressor.save_weights('model.h5')

scores = regressor.evaluate(X_test, Y_test, batch_size=16)
print(scores)
# print("%s: %.2f%%" % (regressor.metrics_names[1], scores[1]*100))