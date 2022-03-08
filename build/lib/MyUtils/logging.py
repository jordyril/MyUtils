# =============================================================================
# Packages
# =============================================================================
import logging
from .general import create_subfolder
import os
from datetime import datetime


# =============================================================================
# CREATE BASECLASS +FUNCTIONS
# =============================================================================
class LogReader(object):
    def __init__(self):
        pass

    @property
    def logs(self):
        try:
            with open(self.logfile) as f:
                _logs = f.read()
        except FileNotFoundError:
            return ""
        return _logs

    def check(self, text):
        return False if text not in self.logs else True


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
        date_format="%d/%m/%Y %H:%M:%S",
        mode="a",
    ):
        self.logger = self._create_logger(
            filename, log_folder, level, formatting, date_format, mode
        )

    def _create_logger(
        self, name, log_folder, level, formatting, date_format, mode,
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
        formatter = logging.Formatter(formatting, datefmt=date_format)  # logging format

        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        return logger

    def __repr__(self):
        return self.logger.__repr__()


# def create_logging(
#     name,
#     log_folder=False,
#     level=logging.INFO,
#     formatting="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
#     date_format="%d/%m/%Y %H:%M:%S",
#     mode="a",
# ):
#     # logging
#     log_file = f"{name}.log"  # file name

#     if log_folder:
#         create_logfolder()
#         log_file = "Logs/" + log_file

#     logger = logging.getLogger(log_file)  # create logger
#     logger.setLevel(level)

#     file_handler = logging.FileHandler(log_file, mode=mode)
#     formatter = logging.Formatter(formatting, datefmt=date_format)  # logging format

#     file_handler.setFormatter(formatter)

#     logger.addHandler(file_handler)

#     return logger


# =============================================================================
# SIMPLE TEXT LOGGING
# =============================================================================
class MyLogger(LogReader):
    def __init__(
        self,
        filename,
        log_folder=False,
        date_format="%d/%m/%Y %H:%M:%S",
        clean_file=False,
        extension="log",
        duplicates=False,
    ):
        self._check_logfile(filename, log_folder, extension, clean_file)
        self._date_format = date_format
        self._duplicate = duplicates
        self._prefix = "INFO"

    def write(self, text, mode="a"):
        with open(self.logfile, mode) as f:
            f.write(f"{self._now()}:{self._prefix}:{text}\n")

    def _check_logfile(self, filename, log_folder, extension, clean_file):
        file = f"{filename}.{extension}"
        if log_folder:
            create_logfolder()
            file = "Logs/" + file
        self.logfile = file
        if (not os.path.exists(self.logfile)) | (clean_file):
            file = open(self.logfile, "w+")
            file.close()

    def _now(self):
        return datetime.now().strftime(self._date_format)

    def __name__(self):
        return f"{self.logfile}"

    def __repr__(self):
        return self.logs
