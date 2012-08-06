from django.db import models


class ClassField(object):

    def __init__(self, class_name=None, members_field=None):
        self.class_name = class_name
        self.members_field = members_field
