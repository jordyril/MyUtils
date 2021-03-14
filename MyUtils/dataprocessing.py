"""
Created on Tue Jul 31 14:27:25 2018

@author: jordy
"""

# =============================================================================
# Packages
# =============================================================================
import pickle
import os
import pandas as pd

from MyUtils._utils import extensions_dic

# =============================================================================
# PICKLE
# =============================================================================


def open_from_pickle(filename, folder="Data"):
    """
    Opening pickle file
    """
    with open(f"{folder}/{filename}.pickle", "rb") as handle:
        b = pickle.load(handle)
    return b


def save_to_pickle(filename, dic, folder="Data"):
    """
    Saving an object to a pickle file
    """
    # create Data folder
    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(f"{folder}/{filename}.pickle", "wb") as handle:
        pickle.dump(dic, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return None


# =============================================================================
# OTHER
# =============================================================================
def save_text_to_file(text, path_filename_extension):
    """
    Saves text into a file with the extension of your choice

    :param text: The string you want to write into a file
    :param path_file: the relative path you want the file to be written, including filename and extension

    Returns
    ----
    return : None

    """
    f = open(path_filename_extension, "w+")
    f.write(text)
    f.close()

    return None


# =============================================================================
# CLASSES
# =============================================================================
class DataProcessor(object):
    def __init__(self, subfolder="Data"):
        self.folder = subfolder

        if subfolder is None:
            self.folder_path = ""

        else:
            self.folder_path = f"{subfolder}/"
            # create subfolder
            if not os.path.exists(subfolder):
                os.makedirs(subfolder)

        self._to = ""
        self._read = ""
        self._ext = ""

    def _file_path(self, filename, extension, destination=False):
        if not destination:
            return f"{self.folder_path}{filename}.{extension}"
        else:
            return f"{destination}{filename}.{extension}"

    def _extension(self, ext):
        return extensions_dic[ext][0]

    def __getattr__(self, attr: str):
        if len(attr) > 3 and attr.startswith("to_"):
            self._to = attr
            try:
                self._ext = extensions_dic[attr[3:]][0]
            except KeyError:
                self._ext = attr[3:]
            return self.to

        elif len(attr) > 5 and attr.startswith("read_"):
            self._read = attr
            try:
                self._ext = extensions_dic[attr[5:]][0]
            except KeyError:
                self._ext = attr[5:]
            return self.read

        raise AttributeError(f"'{self.__class__}' object has no attribute '{attr}'")

    def to(self, df, filename, extension=None, *args, **kwargs):
        if extension:
            ext = extension
        else:
            ext = self._ext
        attr = self._to
        getattr(df, attr)(self._file_path(filename, ext), *args, **kwargs)

    def read(self, filename, *args, **kwargs):
        attr = self._read
        return getattr(pd, attr)(self._file_path(filename, self._ext), *args, **kwargs)

    def save_to_pickle(self, filename, dic, destination=False):
        """
        Saving an object to a pickle file
        """
        file = self._file_path(filename, "pickle", destination)

        with open(file, "wb") as handle:
            pickle.dump(dic, handle, protocol=pickle.HIGHEST_PROTOCOL)

        return None

    def open_from_pickle(self, filename, destination=False):
        """
        Opening pickle file
        """
        file = self._file_path(filename, "pickle", destination)
        with open(file, "rb") as handle:
            data = pickle.load(handle)
        return data


class DataReader(DataProcessor):
    def __init__(self, subfolder="Data"):
        super().__init__(subfolder)


class DataInputting(DataProcessor):
    def __init__(self, subfolder="Input"):
        super().__init__(subfolder)


class DataOutputting(DataProcessor):
    def __init__(self, subfolder=".Output"):
        super().__init__(subfolder)


# =============================================================================
# FUNCTIONS
# =============================================================================


def input_inter_output():
    return DataInputting(), DataProcessor("Intermediate"), DataOutputting()


def input_output():
    return DataInputting(), DataOutputting()


def inter_output():
    return DataProcessor("Intermediate"), DataOutputting()
