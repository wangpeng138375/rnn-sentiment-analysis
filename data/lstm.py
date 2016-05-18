# -*- coding: utf-8 -*-
"""
Simple example using LSTM recurrent neural network to classify IMDB
sentiment dataset.

References:
    - Long Short Term Memory, Sepp Hochreiter & Jurgen Schmidhuber, Neural
    Computation 9(8): 1735-1780, 1997.
    - Andrew L. Maas, Raymond E. Daly, Peter T. Pham, Dan Huang, Andrew Y. Ng,
    and Christopher Potts. (2011). Learning Word Vectors for Sentiment
    Analysis. The 49th Annual Meeting of the Association for Computational
    Linguistics (ACL 2011).

Links:
    - http://deeplearning.cs.cmu.edu/pdfs/Hochreiter97_lstm.pdf
    - http://ai.stanford.edu/~amaas/data/sentiment/

"""
from __future__ import division, print_function, absolute_import

import pickle as pkl
import tflearn
from tflearn.data_utils import to_categorical, pad_sequences
from tflearn.datasets import imdb

import utils

# IMDB Dataset loading
print("Loading Data...")
data = pkl.load(open("sst_data.pkl", "rb"))
train = data['train']
test = data['test']
val = data['dev']
# train, val, test = imdb.load_data(path='imdb.pkl', maxlen=200,
#                                   n_words=20000)

trainX, trainY = utils.format_data(train[1:])
valX, valY = utils.format_data(val[1:])
testX, testY = utils.format_data(test[1:])

# Data preprocessing
# Sequence padding
print("Padding Sequences...")
trainX = pad_sequences(trainX, maxlen=200, value=0.)
testX = pad_sequences(testX, maxlen=200, value=0.)

# Converting labels to binary vectors
print("Converting labels to binary vectors.")
trainY = to_categorical(trainY, nb_classes=2)
valY = to_categorical(valY, nb_classes=2)
testY = to_categorical(testY, nb_classes=2)

# Network building
print("Building Network...")
net = tflearn.input_data([None, 200])
net = tflearn.embedding(net, input_dim=300000, output_dim=128)
net = tflearn.lstm(net, 128)
net = tflearn.dropout(net, 0.5)
net = tflearn.fully_connected(net, 2, activation='softmax')
net = tflearn.regression(net, optimizer='adam',
                         loss='categorical_crossentropy')

# Training
print("Training DNN...")
model = tflearn.DNN(net, clip_gradients=0., tensorboard_verbose=0)
model.fit(trainX, trainY, validation_set=(testX, testY), show_metric=True,
          batch_size=128)

print("Saving Model...")
model.save('lstm.tflearn')
