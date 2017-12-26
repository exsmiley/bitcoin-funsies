import tqdm
import time
import random
import numpy as np
import pandas as pd

from process import load_data, only_close, load_2017, load_daily
from sklearn.preprocessing import normalize
from keras.models import load_model
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


def get_2017():
    print 'loading only 2017...'
    data = load_2017()
    X = []
    y = []

    x_run = []
    for num in tqdm.tqdm(data):
        x_run.append(num)
        if len(x_run) > 400:
            X.append(x_run[:400])
            y.append(x_run[400])
            x_run.pop(0)

    X = np.array(X).reshape(-1, 400, 1)
    y = np.array(y).reshape(-1, 1)
    print 'loaded!'
    return X, y


def get_close():
    print 'loading close...'
    data = only_close()
    X = []
    y = []

    x_run = []
    for num in tqdm.tqdm(data):
        x_run.append(num)
        if len(x_run) > 400:
            X.append(x_run[:400])
            y.append(x_run[400])
            x_run.pop(0)

    X = np.array(X).reshape(-1, 400, 1)
    y = np.array(y).reshape(-1, 1)
    print 'loaded!'
    return X, y


def get_daily():
    print 'loading daily...'
    data = load_daily()
    X = []
    y = []

    x_run = []
    for num in tqdm.tqdm(data):
        x_run.append(num)
        if len(x_run) > 7:
            X.append(x_run[:7])
            y.append(x_run[7][0])
            x_run.pop(0)

    X = np.array(X).reshape(-1, 7, 4)
    y = np.array(y).reshape(-1, 1)
    print 'loaded!'
    return X, y


def toy_data():
    import random
    X = []
    y = []

    for i in tqdm.tqdm(xrange(4000)):
        num = random.randint(1, 10)
        x = [random.randint(1, 10)]
        exp = random.randint(1, 3)
        for j in xrange(400):
            x_i = x[0]*num*(j+1)**exp
            x.append(x_i)
        x = np.array(x).reshape(-1, 1)
        x = list(normalize(x, axis=0).reshape(401, 1))

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
    model.add(Dense(1, activation='linear'))
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
    model.add(Conv1D(16, 3, input_shape=(400, 1), padding='same'))
    model.add(AveragePooling1D())
    # model.add(Conv1D(32, 3, input_shape=(400, 1), activation='relu', padding='same'))
    # model.add(MaxPooling1D())
    model.add(Flatten())
    model.add(Dense(2000, activation='relu'))
    # model.add(Dense(1000, activation='relu'))
    # model.add(Dense(1000, activation='relu'))
    # model.add(Dense(500, activation='relu'))
    # model.add(Dense(100, activation='relu'))
    model.add(Dense(1, activation='linear'))
    # model.compile(loss='mean_absolute_percentage_error',
    #           optimizer='adam',
    #           metrics=['mae'])
    return model

def daily_cnn_model():
    '''
    acc: 0.9620
    [[ 0.02803782  0.00446387  0.05051791  0.04457706  0.04525087]]
    [ 0.02566578  0.00380234  0.05133156  0.04562805  0.04562805]
    '''
    model = Sequential()
    model.add(Conv1D(16, 3, input_shape=(7, 4), padding='same'))
    model.add(AveragePooling1D())
    # model.add(Conv1D(32, 3, input_shape=(400, 1), activation='relu', padding='same'))
    # model.add(MaxPooling1D())
    model.add(Flatten())
    model.add(Dense(300, activation='relu'))
    # model.add(Dense(1000, activation='relu'))
    # model.add(Dense(1000, activation='relu'))
    # model.add(Dense(500, activation='relu'))
    # model.add(Dense(100, activation='relu'))
    model.add(Dense(1, activation='linear'))
    # model.compile(loss='mean_absolute_percentage_error',
    #           optimizer='adam',
    #           metrics=['mae'])
    return model
    


if __name__ == '__main__':
    X, y = get_daily()
    model = daily_cnn_model()
    # model = load_model('try2.h5')
    model.compile(loss='mean_squared_error',
              optimizer='adam',
              metrics=['mae', 'mean_absolute_percentage_error'])
    num_epochs = 1
    for epoch in xrange(num_epochs):
    # # X, y = toy_data()
        model.fit(X, y, epochs=1, batch_size=10)
    #     model.save('cls{}_{}.h5'.format(epoch+1, time.time()))
    # error = 0
    # num_test = 1000
    # norm_num = 1
    # for i in tqdm.tqdm(xrange(num_test)):
    #     ind = int(random.random()*len(X))
    #     if ind+60 < len(X):
    #         # guess price an hour from now
    #         els = list((X[ind]+3000)*3000)
    #         for j in xrange(59):
    #             guess = model.predict(np.array(els).reshape(1, 400, 1))[0][0]
    #             els.append(guess)
    #             els.pop(0)
    #         guess = model.predict(np.array(els).reshape(1, 400, 1))[0][0]
    #         actual = (y[ind+60][0]+3000)*3000
    #         error += (guess-actual)
    # print 'Avg Error:', error/num_test*norm_num
    # # print X.shape, y.shape
    # # model.fit_generator(get_data(), steps_per_epoch=1000, epochs=30)
    # # print X[0]
    # # gen = get_data()
    # # X, y = gen.next()
    # # print model.predict(X), y
