import math

import tflearn
import tensorflow as tf
from loadDataset import load_dataset

# Get data
print("Loading Dataset")
X, Y, testX, testY = load_dataset()
print("Dataset Loaded")
print("Building Neural Network structure")

# Building deep neural network
input_layer = tflearn.input_data(shape=[None, len(X[0])])
dense1 = tflearn.fully_connected(input_layer, 1000, activation='tanh',
                                 regularizer='L2', weight_decay=0.001)

dropout1 = tflearn.dropout(dense1, 0.8)
dense2 = tflearn.fully_connected(dropout1, 200, activation='tanh',
                                 regularizer='L2', weight_decay=0.001)

dropout2 = tflearn.dropout(dense2, 0.8)
dense3 = tflearn.fully_connected(dropout2, 100, activation='tanh',
                                 regularizer='L2', weight_decay=0.001)

dropout3 = tflearn.dropout(dense3, 0.8)
linear = tflearn.fully_connected(dropout3, 1, activation='linear')

# Regression using SGD with learning rate decay and Top-3 accuracy
sgd = tflearn.SGD(learning_rate=0.1, lr_decay=0.8, decay_step=1000)
top_k = tflearn.metrics.Top_k(3)
net = tflearn.regression(linear, optimizer=sgd, metric=top_k,
                         loss=tf.keras.losses.MeanSquaredError())

print("Training")
# Training
model = tflearn.DNN(net, tensorboard_verbose=0)
model.fit(X, Y, n_epoch=100, validation_set=.33,
          show_metric=True, run_id="dense_model")

model.save("models/model1.tf")