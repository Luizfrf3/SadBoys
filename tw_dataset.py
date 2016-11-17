# -*- coding: utf-8 -*-
## Tweet Dataset
##   enables to modify dataset by classifying a tweet as a sentiment,
##   represented by a float ranging from 0 (bad) to 1 (good)

"""
    Implementation of database queries API

    BD description:
                    Input: String of 256 char;
                    Label: 0, 1, 2.

    OBS: Pode alterar as assinaturas ou os comentários, só manter as funções
         da API que tá tranquilo.

"""

class tw_dataset:
    ## Initialize class
    ##    batch size := instances from database returned at once
    def __init__(self, batch_size):
        continue

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
