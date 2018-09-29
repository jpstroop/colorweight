from sys import path
from os.path import abspath
from os.path import dirname
from os.path import realpath

# This is necessary so that we can use this as a CLI and a module (unlikely but
# importing relative to this directory as opposed to ../../cw feels wrong)
path.append(abspath(dirname(dirname(realpath(__file__)))))
from cw.utils.color_analysis import ImageAnalyzer
