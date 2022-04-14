# =============================================================================
# Packages
# =============================================================================
import logging
from .general import create_subfolder
import os
from datetime import datetime
import mmap

# =============================================================================
# CREATE BASECLASS +FUNCTIONS
# =============================================================================


class LogReader(object):
    def __init__(self):
        pass

    @property
    def logs(self):
        with open(self.logfile, "r") as f:
            _logs = f.read()
        return _logs

    @property
    def lines(self):
        with open(self.logfile, "r") as f:
            _lines = f.readlines()
        return _lines

    def check(self, text):
        with open(self.logfile, "rb", 0) as file, mmap.mmap(
            file.fileno(), 0, access=mmap.ACCESS_READ
        ) as s:
            if s.find(text.encode()) != -1:
                return True
            return False

    # def check2(self, text):
    #     return False if text not in self.logs else True

    # def check3(self, text):
    #     with open(self.logfile) as f:
    #         return text in f.read()


def create_logfolder():
    create_subfolder("Logs")


# =============================================================================
# LOGGING MODULE ADD ONS
# =============================================================================


class LoggingExtended(LogReader):
    def __init__(
        self,
        filename,
        log_folder=False,
        level=logging.INFO,
        formatting="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
        datetime_format="%d/%m/%Y %H:%M:%S",
        mode="a",
    ):
        self.logger = self._create_logger(
            filename, log_folder, level, formatting, datetime_format, mode
        )

    def _create_logger(
        self, name, log_folder, level, formatting, datetime_format, mode,
    ):
        logging.shutdown()
        # logging
        self.logfile = f"{name}.log"  # file name

        if log_folder:
            create_logfolder()
            self.logfile = "Logs/" + self.logfile

        logger = logging.getLogger(self.logfile)  # create logger
        logger.setLevel(level)

        file_handler = logging.FileHandler(self.logfile, mode=mode)
        formatter = logging.Formatter(
            formatting, datefmt=datetime_format
        )  # logging format

        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        return logger

    def __repr__(self):
        return self.logger.__repr__()


# =============================================================================
# SIMPLE TEXT LOGGING
# =============================================================================
class MyLogger(LogReader):
    def __init__(
        self,
        filename,
        log_folder=False,
        datetime_format=None,
        datetime_freq="s",
        clean_file=False,
        extension="log",
        duplicates=False,
    ):
        self._check_logfile(filename, log_folder, extension, clean_file)
        self._datetime_freq_formatting(datetime_freq, datetime_format)
        self._duplicate = duplicates
        self._prefix = "INFO"

    def delete(self, text):
        lines = self.lines
        with open(self.logfile, "w+") as file:
            for line in lines:
                if text in line:
                    continue
                file.write(line)

    def replace(self, to_drop, replacement):
        lines = self.lines
        with open(self.logfile, "w+") as file:
            for line in lines:
                if to_drop in line:
                    line.replace(to_drop, replacement)
                file.write(line)

    def write(self, text, mode="a"):
        with open(self.logfile, mode) as f:
            f.write(f"{self._now()}:{self._prefix}:{text}\n")

    def _check_logfile(self, filename, log_folder, extension, clean_file):
        file = f"{filename}.{extension}"

        if log_folder:
            create_logfolder()
            file = "Logs/" + file

        self.logfile = file

        if (self.__exists) & (clean_file):
            os.remove(self.logfile)

        if (not self.__exists) | (clean_file):
            # os.makedirs(self.logfile)
            file = open(self.logfile, "w+")
            title = f"INITIALIZATION:{self.logfile}"
            file.write(f"{len(title) * '#'}\n{title}\n{len(title) * '#'}\n")
            file.close()

    def _datetime_freq_formatting(self, datetime_freq, datetime_format):
        if (datetime_format is not None) & (datetime_freq is not None):
            raise ValueError("Either specify date frequency or date format, not both")

        if datetime_freq.lower() == "s":
            self._datetime_format = "%d/%m/%Y %H:%M:%S"
        elif datetime_freq.lower() == "d":
            self._datetime_format = "%d/%m/%Y"
        else:
            if datetime_format is None:
                raise NotImplementedError(
                    "This date frequency is not implemented yet, specify the datetime_format parameter instead"
                )
            self._datetime_format = datetime_format

    def _now(self):
        return datetime.now().strftime(self._datetime_format)

    def __name__(self):
        return f"{self.logfile}"

    def __repr__(self):
        return self.logs

    @property
    def __exists(self):
        return os.path.exists(self.logfile)
