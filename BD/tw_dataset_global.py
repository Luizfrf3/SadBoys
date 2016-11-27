# -*- coding: utf-8 -*-
## Tweet Dataset
##   enables to modify dataset by classifying a tweet as a sentiment,
##   represented by a float ranging from 0 (bad) to 1 (good)

"""
    Implementacao de uma API que retorna os textos dos tweets
    e atualiza o sentimento (label) apos passar pela rede
    neural imlementada com machine learning

    Autores: Lucas Alves Racoci - RA 156331
             Luiz Fernando Rodrigues da Fonseca - RA 156475

"""

from py2neo import *
import numpy as np
from py2neo.packages.httpstream import http

class tw_dataset:
    ## Initialize class
    ##    batch size := quantidade de textos retornados de uma vez
    def __init__(self, batch_size):

        # Inicializa ponteiros e tempo do socket do neo4j
        http.socket_timeout = 9999

        self.batch_size = batch_size
        self.pointer = 1
        self.return_size = 0

        # Inicializa variaveis que serao utilizadas no processo
        #self.g = Graph(password = "123456")
        self.g = Graph(bolt = False, password = "neo4j")

        query = "match (tg:tweetglobal) return max(length(tg.text)) as max_len"

        self.max_len_text = int(self.g.run(query).data()[0]['max_len'])

        query = "match (tg:tweetglobal) return count(tg) as size"

        self.size = int(self.g.run(query).data()[0]['size'])

        query = "match (tg:tweetglobal) return tg.text as text, id(tg) as id"

        self.cursor = self.g.run(query)

        self.ids = []

        ## Retorna proximo batch disponivel, i.e. (input)
    ## 
    ##    OBS: retorna um novo batch de arquivos do banco de dados,
    ##         do formato:    
    ##         tweets = np.chararray(shape=(len(batch)), itemsize=140)
    def get_next_batch(self, restart = False):

        if restart == True:
            self.pointer = 1

        if self.batch_size + self.pointer - 1 <= self.size:
            self.return_size = self.batch_size
        else:
            self.return_size = self.size - self.pointer + 1
            
        tweets = np.chararray(self.return_size, self.max_len_text, unicode = True)
        self.ids = np.chararray(self.return_size, self.max_len_text, unicode = True)

        k = 0
        while k < self.return_size:
            t = self.cursor.next()
            tweets[k] = t['text']
            self.ids[k] = t['id']
            k += 1

        self.pointer += k

        return tweets

    ## Recebe informacao de sentimento do ultimo batch e atualiza os tweets
    ##
    ##    Seria um formato estilo:
    ##         labels = np.ndarray(shape=(len(batch), 2),
    ##                             dtype=np.uint8)
    def update(self, labels):

        if self.return_size <= 0:
            return False

        k = 0
        while k < self.return_size:
            query = "match (tg:tweetglobal) where id(tg) = %s set tg.label = %f" % (self.ids[k], labels[k])
            self.g.run(query)
            k += 1

        return True

    ## Checa se ja acabou os tweets
    def finished(self):
        return self.pointer > self.size
