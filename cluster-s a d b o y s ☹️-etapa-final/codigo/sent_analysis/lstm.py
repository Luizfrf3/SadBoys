'''
    Project: Sentiment Analysis Classifier
        Rate a given text as a sentiment, ranging from 0 to 1.

    Authors: Isadora Sophia
             Matheus Diamantino

'''

import numpy as np

from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Embedding
from keras.layers import LSTM, SimpleRNN, GRU, Flatten, Convolution1D, MaxPooling1D 
from keras.datasets import imdb

def main():
    ## set things up
    model_name = "SA_2.h5"
    SEED = 1337  # for reproducibility
    np.random.seed(SEED)

    max_features = 7000
    maxlen = 70  # cut texts after this number of words (among top max_features most common words)
    batch_size = 128
    dim = 32

    drop_rate = .2
    max_epochs = 2

    ## prepare data
    print('Loading data...')
    (X_train, y_train), (X_test, y_test) = imdb.load_data(nb_words=max_features)
    print(len(X_train), 'train sequences')
    print(len(X_test), 'test sequences')

    ## pad sequences
    print('Pad sequences (samples x time)')
    X_train = sequence.pad_sequences(X_train, maxlen=maxlen)
    X_test = sequence.pad_sequences(X_test, maxlen=maxlen)
    print('X_train shape:', X_train.shape)
    print('X_test shape:', X_test.shape)

    ## build sentiment analysis model
    print('Build model...')
    model = Sequential()
    model.add(Embedding(max_features, dim, input_length=maxlen, dropout=drop_rate))

    ## deep cnn approach
    model.add(Convolution1D(nb_filter=dim, filter_length=3, border_mode='same', activation='relu'))
    model.add(MaxPooling1D(pool_length=2))
    model.add(Flatten())
    model.add(Dense(250, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    ## LSTM approach
    # model.add(LSTM(output_dim=dim, dropout_W=drop_rate, dropout_U=drop_rate))
    # model.add(Dense(1))
    # model.add(Activation('sigmoid'))

    ## get ready!
    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    ## train it
    print('Train...')
    model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=max_epochs,
              validation_data=(X_test, y_test))

    ## validate
    score, acc = model.evaluate(X_test, y_test,
                                batch_size=batch_size)
    print('Test score:', score)
    print('Test accuracy:', acc)

    ## save it
    model.save(model_name) 

if __name__ == "__main__":
    main()