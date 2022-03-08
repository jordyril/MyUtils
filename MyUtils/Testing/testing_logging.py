from MyUtils.logging import MyLogger
import logging
import os
import time

# TODO- create better structure  + use unittest

os.chdir(f"{os.getcwd()}\\MyUtils/Testing")

# =============================================================================
# LOGGING MODULE ADD ONS
# =============================================================================
# logger = MyLogger(
#     "test_MyLogger",
#     log_folder=True,
#     level=logging.INFO,
#     formatting="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
#     date_format="%d/%m/%Y %H:%M:%S",
#     mode="w",
# )
# logger.logger.inofo("test")

# =============================================================================
# SIMPLE TEXT LOGGING
# =============================================================================
logger = MyLogger("test", log_folder=True, mode="a")

logger.write("Test")

logger.check("INFO")

# logger.check("Test2")
