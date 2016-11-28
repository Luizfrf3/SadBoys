'''
    Project: Sentiment Analysis Classifier
        Rate a tweets as a sentiment, ranging from 0 to 1.
        Based on a string input

    Authors: Isadora Sophia
             Matheus Diamantino

'''

import numpy as np

import keras
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from keras.utils import np_utils
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Activation, Embedding
from keras.layers import LSTM, SimpleRNN, GRU
import sys

import tokenizer

sys.path.insert(0, '../')
from BD.tw_dataset import tw_dataset

def main():
    ## recover model
    model_name = "data/SA.h5"
    model = load_model(model_name)

    ## parameters 
    max_features = 7000
    maxlen = 70   # cut texts after this number of words (among top max_features most common words)
    batch_size = 32

    c = 0

    
    X = [raw_input()]

    ## preprocess text
    tk = tokenizer.Tokenizer(nb_words=max_features)
    tk.apply_imdb()

    X = tk.texts_to_sequences(X)
    print(X)

    ## pad sequence
    X = sequence.pad_sequences(X, maxlen=maxlen)

    ## get output
    Y = model.predict(X, batch_size=batch_size, verbose=0)

    ## change to correct format
    for x in Y:
        for w in x:
            return w

    

if __name__ == "__main__":
    main()
