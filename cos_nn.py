import tensorflow as tf
import numpy as np
import random


# try to learn a cos function

def input_evaluation_set():
    features = [[random.random()*2-1, random.random()*2-1] for i in xrange(1000)]
    labels = [[np.cos(val2), np.sin(val1)] for (val1, val2) in features]
    return np.array(features).reshape(-1, 2), np.array(labels).reshape(-1, 2)

class CosModel(object):

    def __init__(self):
        self.create_graph()

    def create_graph(self):
        self.session = tf.Session()

        self.input_layer = tf.placeholder(tf.float32, [None, 2])
        self.labels = tf.placeholder(tf.float32, [None, 2])

        fc1 = tf.layers.dense(self.input_layer, 100, activation=tf.nn.relu)
        fc2 = tf.layers.dense(fc1, 100, activation=tf.nn.relu)

        self.out_layer = tf.layers.dense(fc2, 2)

        self.loss = tf.reduce_mean(tf.squared_difference(self.labels, self.out_layer))
        
        self.optimizer = tf.train.AdamOptimizer(1e-3)
        self.train = self.optimizer.minimize(self.loss)

        initializer = tf.global_variables_initializer()
        self.session.run(initializer)

        self.saver = tf.train.Saver()

    def learn(self, x, y, batch_size=10):
        x = np.array(x).reshape(batch_size, -1, 2)
        y = np.array(y).reshape(batch_size, -1, 2)
        losses = []
        for i in xrange(batch_size):
            loss, train = self.session.run([self.loss, self.train], feed_dict={
                self.input_layer: x[i],
                self.labels: y[i]
            })
            losses.append(loss)
        print 'loss:', np.mean(loss)

    def predict(self, x):
        x = np.array(x).reshape(-1, 2)
        return self.session.run([self.out_layer], feed_dict={
            self.input_layer: x,
        })



if __name__ == '__main__':
    model = CosModel()

    num_epochs = 100

    for _ in xrange(num_epochs):
        train_x, train_y = input_evaluation_set()
        model.learn(train_x, train_y)
        print 'example:', model.predict(train_x[0]), train_y[0]

    test_x, test_y = input_evaluation_set()

    print model.predict(test_x[0]), test_y[0]



