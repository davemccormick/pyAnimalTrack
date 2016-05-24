from cx_Freeze import *
import os, pip

includefiles = ['pyAnimalTrack\\ui\\View']

setup(name=("PYANIMALTRACK"),
      version = "1",
      description = "pyAnimalTrack",
      options = {'build_exe': {'include_files':includefiles}}, 
      executables = [Executable("pyAnimalTrackRunner.py")],
      )