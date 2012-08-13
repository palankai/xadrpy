import logging
from hashlib import sha512
from uuid import uuid4
import time
import datetime
from django.utils.datastructures import SortedDict

logger = logging.getLogger("xadrpy.core.access.base")

class KeyGenerator(object):
    def __init__(self, length):
        self.length = length

    def __call__(self):
        return sha512(uuid4().hex).hexdigest()[0:self.length]

class TimestampGenerator(object):
    
    def __init__(self, seconds=0):
        self.seconds = seconds

    def __call__(self):
        return int(time.time()) + self.seconds

class ExpiredGenerator(object):
    
    def __init__(self, seconds=0):
        self.seconds = seconds

    def __call__(self):
        return datetime.datetime.now() + datetime.timedelta(seconds=self.seconds) 


class Right(object):
    def __init__(self, manager, key, title, description="", category=None, level=None):
        self.manager = manager
        self.key = key
        self.title = title
        self.description = description
        self.category = category
        self.level = level
    
    def get_category(self):
        return self.manager.get_category(self.category)
    
    def get_level(self):
        return self.manager.get_level(self.level)
    
    def to_dict(self):
        return {
            'key': self.key,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'category_title': self.get_category().title if self.category else None,
            'level': self.level,
            'level_title': self.get_level().title if self.level else None,
        }

class RightLevel(object):
    def __init__(self, manager, key, title, description=""):
        self.manager = manager
        self.key = key
        self.title = title
        self.description = description
        
    def to_dict(self):
        return {
            'key': self.key,
            'title': self.title,
            'description': self.description,
        }

class RightCategory(object):
    def __init__(self, manager, key, title, description=""):
        self.manager = manager
        self.key = key
        self.title = title
        self.description = description
        
    def to_dict(self):
        return {
            'key': self.key,
            'title': self.title,
            'description': self.description,
        }
        
        

class RightManager(object):
    
    def __init__(self):
        self.right_cls = Right
        self._levels = SortedDict()
        self._categories = SortedDict()
        self._rights = SortedDict()
    
    def register_level(self, key, title, description=""):
        self._levels[key] = RightLevel(self, key, title, description)

    def register_category(self, key, title, description=""):
        self._categories[key] = RightCategory(self, key, title, description)
    
    def register(self, key, title, description="", category="", level=""):
        self._rights[key]=Right(self, key, title, description=description, category=category, level=level)
        
    def get_category(self, category_key):
        return self._categories.get(category_key, None)

    def get_level(self, level_key):
        return self._levels.get(level_key, None)
    
    def get_right(self, key):
        return self._rights.get(key)
        
    def get_rights(self):
        return [self.get_right(key) for key in self._rights.keys()]

    def get_rights_dict(self):
        return [self.get_right(key).to_dict() for key in self._rights.keys()]

rights = RightManager()
