
import logging
import time

import spacy


class Operations:
    def __init__(self, tokenization=True, stemming=False, lemmatization=False):
        self.__tokenization = tokenization
        self.__stemming = stemming
        self.__lemmatization = lemmatization
        self.__nlp = spacy.load("en", disable=['ner','tagger'])



    def __apply_tokenization(self, data, column):
        tokens = []
        lemmas = []
        pos = []
        total_tokens = []

        for doc in self.__nlp.pipe(data[column].astype("unicode").values, batch_size=128, n_threads=-1):
            if doc.is_parsed:
                tokens.append([n.text for n in doc])
                lemmas.append([n.lemma_ for n in doc])
                pos.append([n.pos_ for n in doc])
                total_tokens.append(doc.__len__())
            else:
                tokens.append(None)
                lemmas.append(None)
                pos.append(None)
                total_tokens.append(None)


        data[str(column) + str('_tokens')] = tokens
        data[str(column) + str('_lemmas')] = lemmas
        data[str(column) + str('_pos')] = pos
        data[str(column) + str('_count')] = total_tokens

    def apply_operations(self, data, interim_filepath, filename):
        logger = logging.getLogger(__name__)
        print(self.__tokenization)
        if self.__tokenization is not None:
            if '_tok' in filename:
                logger.warn("This input file already had _tok in name, hence" + 
                            " tokenization will not be applied. However execution continues.")
            else:
                logger.info("Applying tokenization in text")

                total_time = 0
                for column in self.__tokenization:
                    start_time = time.time()
                    self.__apply_tokenization(data, column)
                    elapsed_time = time.time() - start_time
                    total_time += elapsed_time
                    logger.info("Column: {1} - Tokenization - Elapsed Time: {0}".format(elapsed_time,column))

                data.to_csv(interim_filepath +  str(filename[:-4]) + str('_') + str('tok') + str('.csv'))

