"""
Created on Tue Jul 31 14:27:25 2018

@author: jordy
"""

# =============================================================================
# Packages
# =============================================================================
import pickle
import os

# =============================================================================
# PICKLE
# =============================================================================


def open_from_pickle(filename):
    """
    Opening pickle file
    """
    with open("Data/" + filename + ".pickle", "rb") as handle:
        b = pickle.load(handle)
    return b


def save_to_pickle(filename, dic):
    """
    Saving an object to a pickle file
    """
    # create Data folder
    if not os.path.exists("Data"):
        os.makedirs("Data")

    with open(filename + ".pickle", "wb") as handle:
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

    def save_to_pickle(self, filename, dic, destination=False):
        """
        Saving an object to a pickle file
        """
        if not destination:
            file = f"{self.folder_path}{filename}.pickle"
        else:
            file = f"{destination}/{filename}.pickle"

        with open(file, "wb") as handle:
            pickle.dump(dic, handle, protocol=pickle.HIGHEST_PROTOCOL)

        return None

    def open_from_pickle(self, filename, destination=False):
        """
        Opening pickle file
        """
        if not destination:
            file = f"{self.folder_path}{filename}.pickle"
        else:
            file = f"{destination}/{filename}.pickle"
        with open(file, "rb") as handle:
            data = pickle.load(handle)
        return data


class DataReader(DataProcessor):
    def __init__(self, subfolder="Data"):
        super().__init__(subfolder)


class DataOutputting(DataProcessor):
    def __init__(self, subfolder=".Output"):
        super().__init__(subfolder)
