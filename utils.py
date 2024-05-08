import os
import sys


def setup_project_directories(dir_name):
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    src_dir = os.path.join(project_dir, dir_name)
    sys.path.append(project_dir)
    sys.path.insert(0, src_dir)
