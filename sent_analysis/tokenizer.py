'''
    Taken from keras API:
        https://github.com/fchollet/keras/blob/master/keras/preprocessing/text.py

'''

from __future__ import absolute_import
from __future__ import division

import string
import numpy as np

import re

import keras
from keras.datasets import imdb
from keras.preprocessing import text

class Tokenizer(object):
    def __init__(self, nb_words=None, filters=keras.preprocessing.text.base_filter(),
                 lower=True, split=' ', char_level=False):
        '''The class allows to vectorize a text corpus, by turning each
        text into either a sequence of integers (each integer being the index
        of a token in a dictionary) or into a vector where the coefficient
        for each token could be binary, based on word count, based on tf-idf...
        # Arguments
            nb_words: the maximum number of words to keep, based
                on word frequency. Only the most common `nb_words` words will
                be kept.
            filters: a string where each element is a character that will be
                filtered from the texts. The default is all punctuation, plus
                tabs and line breaks, minus the `'` character.
            lower: boolean. Whether to convert the texts to lowercase.
            split: character or string to use for token splitting.
            char_level: if True, every character will be treated as a word.
        By default, all punctuation is removed, turning the texts into
        space-separated sequences of words
        (words maybe include the `'` character). These sequences are then
        split into lists of tokens. They will then be indexed or vectorized.
        `0` is a reserved index that won't be assigned to any word.
        '''
        self.word_counts = {}
        self.word_docs = {}
        self.filters = filters
        self.split = split
        self.lower = lower
        self.nb_words = nb_words
        self.document_count = 0
        self.char_level = char_level

    def text_to_word_sequence(self, text):
        '''prune: sequence of characters to filter out
        '''
        if self.lower:
            text = text.lower()

        text = re.sub("[^0-9a-zA-Z _.,]", "", text)

        text = str(text).translate(string.maketrans(self.filters, self.split*len(self.filters)))

        seq = text.split(self.split)

        return [_f for _f in seq if _f]

    def apply_imdb(self):
        self.word_index = imdb.get_word_index()

    def texts_to_sequences(self, texts):
        '''Transforms each text in texts in a sequence of integers.
        Only top "nb_words" most frequent words will be taken into account.
        Only words known by the tokenizer will be taken into account.
        Returns a list of sequences.
        '''
        res = []
        for vect in self.texts_to_sequences_generator(texts):
            res.append(vect)
        return res

    def texts_to_sequences_generator(self, texts):
        '''Transforms each text in texts in a sequence of integers.
        Only top "nb_words" most frequent words will be taken into account.
        Only words known by the tokenizer will be taken into account.
        Yields individual sequences.
        # Arguments:
            texts: list of strings.
        '''
        nb_words = self.nb_words
        for text in texts:
            seq = text if self.char_level else self.text_to_word_sequence(text)
            vect = []
            for w in seq:
                i = self.word_index.get(w)
                if i is not None:
                    if nb_words and i >= nb_words:
                        continue
                    else:
                        vect.append(i)
            yield vect
