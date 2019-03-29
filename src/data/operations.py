import logging
import time

import spacy

logger = logging.getLogger(__file__)


class Operations:
    def __init__(self, tokenization=True, stemming=False, lemmatization=False):
        self.__tokenization = tokenization
        self.__stemming = stemming
        self.__lemmatization = lemmatization
        self.__nlp = spacy.load("en", disable=['parser','tagger','ner'])

    def apply_operations(self, data):
        if self.__tokenization is not None:
            logger.info("Applying tokenization in text")

            total_time = 0
            for column in self.__tokenization:
                start_time = time.time()
                self.__apply_tokenization(data, column)
                elapsed_time = time.time() - start_time
                total_time += elapsed_time
                logger.info("Column:{1} - Tokenization - Elapsed Time: {0}".format(elapsed_time,column))

    def __apply_tokenization(self, data, column):
        tokens = []
        lemmas = []
        pos = []
        for doc in self.__nlp.pipe(data[column].astype("unicode").values, batch_size=1000, n_threads=-1):
            if doc.is_parsed:
                tokens.append([n.text for n in doc])
                lemmas.append([n.lemma_ for n in doc])
                pos.append([n.pos_ for n in doc])
            else:
                tokens.append(None)
                lemmas.append(None)
                pos.append(None)

        data[str(column) + str('_tokens')] = tokens
        data[str(column) + str('_lemmas')] = lemmas
        data[str(column) + str('_pos')] = pos

    def __apply_stemming(self):
        pass

    def __aplly_lemmatization(self):
        pass
