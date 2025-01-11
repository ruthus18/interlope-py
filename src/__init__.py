import os
import pathlib
import platform

VENDOR_PATH = pathlib.Path(__file__).parent.parent / 'vendor'


if platform.system() == 'Windows':
    os.add_dll_directory(VENDOR_PATH)
