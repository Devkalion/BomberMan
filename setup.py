# command: python setup.py build

from cx_Freeze import setup, Executable
from os import environ
environ['TCL_LIBRARY'] = "C:\\Users\\Rustan\\AppData\\Local\\Programs\\Python\\Python35-32\\tcl\\tcl8.6"
environ['TK_LIBRARY'] = "C:\\Users\\Rustan\\AppData\\Local\\Programs\\Python\\Python35-32\\tcl\\tk8.6"

setup(name="Bomberman",
      version='1.2.4',
      options={"build_exe": {"packages": ["pygame", "random", "sys"],
                             "include_files": ["Resources/"]}},
      executables=[Executable(script="start.py",
                              icon='Resources/images/Bomberman-icon.ico',
                              base='Win32GUI',
                              targetName='Bomberman.exe')])
