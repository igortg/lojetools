from cx_Freeze import setup, Executable
import os
import shutil
import sys

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "compressed": True,
    "append_script_to_exe": True,
    "build_exe": "theves_etiquetas",
    "silent": True,
#     "include_files": [("../src/lps.ini", "lps.ini")] 
}

executable = Executable(
    "../src/product_data_generator/main.py",
    base="Win32GUI",
    targetName="theves_etiquetas.exe"
    )

setup(
    name = "theves_etiquetas",
    version = "13.05",
    description = "Theves Etiquetas",
    options = {"build_exe": build_exe_options},
    executables = [executable]
    )


shutil.make_archive("theves_etiquetas", "zip", root_dir=".", base_dir="theves_etiquetas")
