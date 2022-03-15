from MyUtils.logging import MyLogger
import logging
import numpy as np
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
logger = MyLogger("test/test2", log_folder=True, clean_file=True)

for i in range(6):
    logger.write(f"TEST{i}")

logger.check("TEST1999")
logger.check2("TEST2000")
# logger.check2("TEST2000")

import timeit

# timeit.timeit(lambda: logger.check2("Test2"), number=100000)
a = timeit.repeat(lambda: logger.check("Test2"), number=10000, repeat=10)
b = timeit.repeat(lambda: logger.check2("Test2"), number=10000, repeat=10)
c = timeit.repeat(lambda: logger.check3("Test2"), number=10000, repeat=10)

a = np.array(a)
b = np.array(b)
c = np.array(c)


((b - a) / a).mean()
((c - a) / a).mean()
((c - b) / b).mean()


c.std()
b.std()
a.std()
