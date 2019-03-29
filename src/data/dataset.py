import pandas  as pd

from operations import Operations

class Data:
    def __init__(self, input_filepath, output_filepath, operations):
        self.__input_filepath = input_filepath
        self.__output_filepath = output_filepath
        self.__data = None
        self.__operations = Operations(tokenization=operations['tokenization'],stemming=operations['stemming'],lemmatization=operations['lemmatization'])

        # Open file and apply operations into data
        self.__open_file()
        self.__operations.apply_operations(self.__data)



    def __open_file(self):
        self.__data = pd.read_csv(self.__input_filepath)

    def get_input_filepath(self):
        return self.__input_filepath

    def get_output_filepath(self):
        return self.__output_filepath

    def get_operations(self):
        return self.__operations


