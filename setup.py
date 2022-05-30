"""
Created on Tue Jul 31 12:29:16 2018

@author: jordy
"""

"""MyUtils package setup script

   To create a source distribution of the MyUtils
   package run

   python MyUtils.py sdist

   which will create an archive file in the 'dist' subdirectory.
   The archive file will be  called 'MyUtils-X.X.zip' and will
   unpack into a directory 'MyUtils-X.X'.

   An end-user wishing to install the MyUtils package can simply
   unpack 'MyUtils-X.X.zip' and from the 'MyUtils-X.X' directory and
   run

   python setup.py install

   which will ultimately copy the MyUtils package to the appropriate
   directory for 3rd party modules in their Python installation
   (somewhere like 'c:\python27\libs\site-packages').

   To create an executable installer use the bdist_wininst command

   python setup.py bdist_wininst

   which will create an executable installer, 'MyUtils-X.X.win32.exe',
   in the current directory.

"""

import setuptools


# package naming
DISTNAME = "MyUtils"

# descriptions
DESCRIPTION = "'MyUtils'"
with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

# developer(s)
AUTHOR = "Jordy Rillaerts"
EMAIL = "jordy_rillaerts13@hotmail.com"

URL = "https://github.com/jordyril/MyUtils"

# versioning
MAJOR = 1
MINOR = 0
MICRO = 3
ISRELEASED = False
VERSION = "%d.%d.%d" % (MAJOR, MINOR, MICRO)
QUALIFIER = ""

FULLVERSION = VERSION
write_version = True

# if not ISRELEASED:
# FULLVERSION += '.dev'

# DEPENDENCIES = ["pandas", "numpy", "roman", "linearmodels", "arch"]

DEPENDENCIES = []
with open("requirements.txt", "r", encoding="utf-8") as requirements:
    for line in requirements:
        DEPENDENCIES.append(line.strip())

setuptools.setup(
    name=DISTNAME,
    version=FULLVERSION,
    author=AUTHOR,
    author_email=EMAIL,
    maintainer=AUTHOR,
    maintainer_email=EMAIL,
    install_requires=DEPENDENCIES,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,
    long_description_content_type="test/markdown",
    packages=["MyUtils", "MyUtils.estimation", "MyUtils.simulation"],
)
