import tensorflow as tf
import numpy as np
import random


# try to learn a cos function

def input_evaluation_set():
    features = np.array([random.random()*2-1 for i in xrange(1000)]).reshape(-1, 1)
    labels = np.array([np.cos(val) for val in features]).reshape(-1, 1)
    return features, labels

class CosModel(object):

    def __init__(self):
        self.create_graph()

    def create_graph(self):
        self.session = tf.Session()

        self.input_layer = tf.placeholder(tf.float32, [None, 1])
        self.labels = tf.placeholder(tf.float32, [None, 1])

        fc1 = tf.layers.dense(self.input_layer, 100, activation=tf.nn.relu)
        fc2 = tf.layers.dense(fc1, 100, activation=tf.nn.relu)

        self.out_layer = tf.layers.dense(fc2, 1)

        self.loss = tf.reduce_mean(tf.squared_difference(self.labels, self.out_layer))
        
        self.optimizer = tf.train.AdamOptimizer(1e-3)
        self.train = self.optimizer.minimize(self.loss)

        initializer = tf.global_variables_initializer()
        self.session.run(initializer)

        self.saver = tf.train.Saver()

    def learn(self, x, y):
        x = np.array(x).reshape(-1,1)
        y = np.array(y).reshape(-1,1)
        loss, train = self.session.run([self.loss, self.train], feed_dict={
            self.input_layer: x,
            self.labels: y
        })
        print loss

    def predict(self, x):
        x = np.array(x).reshape(-1,1)
        return self.session.run([self.out_layer], feed_dict={
            self.input_layer: x,
        })[0][0]



if __name__ == '__main__':
    model = CosModel()

    num_epochs = 1000

    for _ in xrange(num_epochs):
        train_x, train_y = input_evaluation_set()
        model.learn(train_x, train_y)

    test_x, test_y = input_evaluation_set()


    print model.predict(test_x[0]), test_y[0]



