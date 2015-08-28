# cx_Freeze setup file

import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": []}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Easyfig",
        version = "2.2.2",
        description = "Easy genome comparison figures.",
        options = {"build_exe": build_exe_options},
        executables = [Executable("Easyfig.py", base=base)])