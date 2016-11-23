# -*- coding: utf-8 -*-
## Train Dataset
##   enables to retrieve data in order to provide training

"""
    Implementation of database queries API

    BD description:
                    Input: String of 256 char;
                    Label: 0, 1, 2.

    OBS: Pode alterar as assinaturas ou os comentários, só manter as funções
         da API que tá tranquilo.

"""

from py2neo import *
import numpy as np

#   OBS: Permitir que seja instanciado um database para test e train set
#        http://stats.stackexchange.com/questions/19048/what-is-the-difference-between-test-set-and-validation-set
#        Basicamente, separar da DB 20% para test e 80% para train
class tr_dataset:
    ## Initialize class
    ##    batch size := instances from database returned at once
    def __init__(self, batch_size):
        self.batch_size = batch_size
        self.pointer = 0
        self.g = Graph(password = "123456")
        #self.g = Graph(bolt = False, password = "neo4j")

        query = "match (n) return n"
        self.data = self.g.run(query).data()

        self.max_len_phrase = max(len(x['n']['frase']) for x in self.data)

    ## Returns next (available) batch, i.e. (input, labels)
    ## 
    ##    OBS: retorna um novo batch de arquivos do banco de dados,
    ##         do formato (por exemplo):    
    ##         input  = np.chararray(shape=(len(batch)), itemsize=140)
    ##         labels = np.ndarray(shape=(len(batch), 2),
    ##                             dtype=np.uint8)
    ##
    ##    dicas: - verificar se o que está retornando existe (x is None)):
    ##           - escolher queries de maneira randômica (mas sem repetir)
    ##           - caso o banco de dados tenha finalizado os arquivos,
    ##             começar novamente o ciclo e continuar retornando os arquivos 
    ##             novamente
    def get_next_batch(self, restart = False):

        if restart == True:
            self.pointer = 0

        input = np.chararray(self.batch_size, self.max_len_phrase, unicode = True)
        labels = np.ndarray(shape = (self.batch_size), dtype = np.float64)

        i = self.pointer
        k = 0
        while k < self.batch_size:
            if i >= len(self.data):
                i = 0
            input[k] = self.data[i]['n']['frase']
            labels[k] = self.data[i]['n']['val']
            k += 1
            i += 1

        self.pointer = i

        return input, labels
