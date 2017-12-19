import tqdm
import numpy as np
import pandas as pd

from process import load_data
from sklearn.preprocessing import normalize

from keras.models import Sequential, Model
from keras.layers import LSTM, Dropout, Dense, Input
from keras.layers import Conv1D, AveragePooling1D, Flatten, MaxPooling1D


def get_data():
    x_i = []
    for row in load_data():
        x_i.append(row)
        if len(x_i) > 400:
            yield np.array(x_i[:400]).reshape(-1, 400, 5), np.array(x_i[400]).reshape(-1, 5)
            x_i.pop(-1)


def toy_data():
    import random
    X = []
    y = []

    for i in tqdm.tqdm(xrange(4000)):
        nums = [random.randint(1, 10) for i in xrange(5)]
        x = [[random.randint(1, 10) for i in xrange(5)]]
        for j in xrange(400):
            x_i = []
            for k, num in enumerate(nums):
                x_i.append(x[0][k]*num*(j+1))
            x.append(x_i)
        x = np.array(x).reshape(-1, 1)
        x = list(normalize(x, axis=0).reshape(401, 5))

        y_i = x.pop()
        X.append(x)
        y.append(y_i)
    return np.array(X), np.array(y)


def lstm_model():
    '''
    acc: 0.9365
    [[ 0.05473945  0.01575779  0.01488676  0.00453565  0.06293829]]
    [0.05589061  0.01552517  0.01552517  0.00310503  0.06210067]
    '''
    model = Sequential()
    model.add(LSTM(100, input_shape=(400, 5)))
    # model.add(Dropout(0.5))
    model.add(Dense(1000, activation='relu'))
    model.add(Dense(500, activation='tanh'))
    model.add(Dense(200, activation='relu'))
    model.add(Dense(5, activation='linear'))
    model.compile(loss='mean_squared_error',
              optimizer='adam',
              metrics=['accuracy'])
    return model


def cnn_model():
    '''
    acc: 0.9620
    [[ 0.02803782  0.00446387  0.05051791  0.04457706  0.04525087]]
    [ 0.02566578  0.00380234  0.05133156  0.04562805  0.04562805]
    '''
    model = Sequential()
    model.add(Conv1D(32, 3, input_shape=(400, 5), activation='relu', padding='same'))
    model.add(MaxPooling1D())
    model.add(Flatten())
    model.add(Dense(1000, activation='relu'))
    model.add(Dense(500, activation='relu'))
    model.add(Dense(1000, activation='relu'))
    model.add(Dense(500, activation='relu'))
    model.add(Dense(200, activation='relu'))
    model.add(Dense(5, activation='linear'))
    model.compile(loss='mean_squared_error',
              optimizer='adam',
              metrics=['accuracy'])
    return model
    


if __name__ == '__main__':
    model = cnn_model()
    X, y = toy_data()
    model.fit(X, y, epochs=10)
    # print X.shape, y.shape
    # model.fit_generator(get_data(), steps_per_epoch=1000, epochs=30)
    # print X[0]
    # gen = get_data()
    # X, y = gen.next()
    # print model.predict(X)
    print y