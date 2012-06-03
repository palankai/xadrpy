import os
import codecs

ROOT = os.path.realpath(os.path.dirname(__file__))
VERSION = codecs.open(os.path.join(ROOT, 'VERSION')).read()
CURRENT_PATH = os.getcwd()  

SKELETONS_PATH = os.path.join(ROOT,"skeletons")
