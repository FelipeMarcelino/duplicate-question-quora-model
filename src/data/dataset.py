import pandas  as pd
import sys
import os

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), ""))

from features.build_features import Operations

class Data:
    def __init__(self, tokenization,input_filepath,interim_filepath, output_filepath ):
        self.__input_filepath = input_filepath
        self.__interim_filepath = interim_filepath
        self.__output_filepath = output_filepath

        # Get name of file without filepath and .csv extension
        self.__filename = str(input_filepath).split('/')[-1].replace(".csv","")
        self.__data = None
        self.__operations = Operations(tokenization=tokenization)

        # Open file
        self.__open_file()

    def __open_file(self):
        self.__data = pd.read_csv(self.__input_filepath)

    def apply_operations(self):
        self.__operations.apply_operations(self.__data, self.__interim_filepath, self.__filename)

    def get_input_filepath(self):
        return self.__input_filepath

    def get_output_filepath(self):
        return self.__output_filepath

    def get_operations(self):
        return self.__operations


