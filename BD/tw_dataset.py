# -*- coding: utf-8 -*-
## Tweet Dataset
##   enables to modify dataset by classifying a tweet as a sentiment,
##   represented by a float ranging from 0 (bad) to 1 (good)

"""
    Implementation of database queries API

    BD description:
                    Input: String of 256 char;

    OBS: Pode alterar as assinaturas ou os comentários, só manter as funções
         da API que tá tranquilo.

"""

from py2neo import *
import numpy as np

class tw_dataset:
    ## Initialize class
    ##    batch size := instances from database returned at once
    def __init__(self, batch_size):

        self.batch_size = batch_size
        self.pointer = 1
        self.return_size = 0

        #self.g = Graph(password = "123456")
        self.g = Graph(bolt = False, password = "neo4j")

        query = "match (t:tweet) return max(length(t.text)) as max_len"

        self.max_len_text = int(self.g.run(query).data()[0]['max_len'])

        query = "match (t:tweet) return count(t) as size"

        self.size = int(self.g.run(query).data()[0]['size'])

        query = "match (t:tweet) return t, ID(t) as id"

        self.cursor = self.g.run(query)

        self.ids = []

    ## Returns next (available) batch, i.e. (input)
    ## 
    ##    OBS: retorna um novo batch de arquivos do banco de dados,
    ##         do formato (por exemplo):    
    ##         tweets = np.chararray(shape=(len(batch)), itemsize=140)
    ##
    ##    dicas: - verificar se o que está retornando existe (x is None)):
    ##           - escolher queries de maneira randômica (mas sem repetir)
    ##           - caso o banco de dados tenha finalizado os arquivos,
    ##             começar novamente o ciclo e continuar retornando os arquivos 
    ##             novamente
    def get_next_batch(self, restart = False):

        if restart == True:
            self.pointer = 1

        if self.batch_size + self.pointer - 1 <= 5:
            self.return_size = self.batch_size
        else:
            self.return_size = self.size - self.pointer + 1
            
        tweets = np.chararray(self.return_size, self.max_len_text, unicode = True)
        self.ids = np.chararray(self.return_size, self.max_len_text, unicode = True)

        k = 0
        while k < self.return_size:
            t = self.cursor.next()['t']
            tweets[k] = t['text']
            self.ids[k] = t['id']
            k += 1

        self.pointer += k

        return tweets

    ## Receive information related to batch of last batch of tweets and
    ## update database
    ##
    ##    Seria um formato estilo:
    ##         labels = np.ndarray(shape=(len(batch), 2),
    ##                             dtype=np.uint8)
    ##    Ver qual a melhor forma de identificar os tweets a serem utilizados!
    ##    Seja com um índice interno na classe registrando os tweets ou um
    ##    parâmetro que a função recebe com os índices de cada tweet, por ex.
    def update(self, labels):
        return
