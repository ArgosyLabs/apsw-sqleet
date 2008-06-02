import os
import sys

from distutils.core import setup, Extension

define_macros=[]

# We always want threadsafe
define_macros.append( ('SQLITE_THREADSAFE', '1') )

# We don't want assertions
define_macros.append( ('NDEBUG', '1') )

# This includes the functionality marked as experimental in SQLite 3.
# Comment out the line to exclude them
define_macros.append( ('EXPERIMENTAL', '1') )

# If you compiled SQLite omitting functionality then specify the same
# defines here.  For example this exlcudes loadable extensions.
#
# define_macros.append( ('SQLITE_OMIT_LOAD_EXTENSION', '1') )

include_dirs=[]
library_dirs=[]

# Look for amalgamation in our directory or in sqlite3 subdirectory
amalgamation=(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "sqlite3.c"),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "sqlite3", "sqlite3.c")
    )

usingamalgamation=False
for path in amalgamation:
    if os.path.exists(path):
        if sys.platform=="win32":
            # double quotes get consumed by windows arg processing
            define_macros.append( ('APSW_USE_SQLITE_AMALGAMATION', '\\"'+path+'\\"') )
        else:
            define_macros.append( ('APSW_USE_SQLITE_AMALGAMATION', '"'+path+'"') )
        libraries=[]
        usingamalgamation=True
        break
    
if not usingamalgamation:
    # if there is a sqlite3 subdirectory then use that, otherwise
    # the system sqlite will be used
    if os.path.exists("sqlite3"):
        include_dirs=["sqlite3"]
        library_dirs=["sqlite3"]

    libraries=['sqlite3']

# setuptools likes to define NDEBUG even when we want debug stuff
if "--debug" in sys.argv:
    define_macros.append( ('APSW_NO_NDEBUG', 1) ) # double negatives are bad


# work out version number
version=open("apswversion.h", "rtU").read().split()[2].strip('"')

setup(name="apsw",
      version=version,
      description="Another Python SQLite Wrapper",
      long_description=\
"""A Python wrapper for the SQLite embedded relational database engine.
In contrast to other wrappers such as pysqlite it focuses on being
a minimal layer over SQLite attempting just to translate the
complete SQLite API into Python.""",
      author="Roger Binns",
      author_email="rogerb@rogerbinns.com",
      url="http://code.google.com/p/apsw/",
      download_url="http://code.google.com/p/apsw/downloads/list",
      classifiers=[
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: zlib/libpng License",
    "Operating System :: OS Independent",
    "Programming Language :: C",
    "Topic :: Database :: Front-Ends",
    ],
      keywords=["database", "sqlite"],
      platform="Any supported by both SQLite and Python",
      license="OSI Approved :: zlib/libpng License",

      ext_modules=[Extension("apsw",
                             ["apsw.c"],
                             include_dirs=include_dirs,
                             library_dirs=library_dirs,
                             libraries=libraries,
                             define_macros=define_macros)])

