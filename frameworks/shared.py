import os
import shutil


def safe_remove(path):
    if os.path.exists(path):
        shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)


def safe_mkdir(path):
    safe_remove(path)
    os.makedirs(path)
