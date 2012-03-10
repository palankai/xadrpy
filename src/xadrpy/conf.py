import os
import codecs

ROOT = os.path.realpath(os.path.dirname(__file__))
VERSION = codecs.open(os.path.join(ROOT, 'VERSION')).read()
