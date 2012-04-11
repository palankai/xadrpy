from django.db import models
import random
import conf 
from xadrpy.utils.randomlib import get_random
random.seed()

class UniqueIdManager(models.Manager):
    
    def get_unique_id(self, prefix=None, suffix=None, length=conf.UNIQUE_ID_DEFAULT_LENGTH, chars=conf.UNIQUE_ID_DEFAULT_CHARS):
        while True:
            try:
                unique_id = self.create(unique_id=get_random(length, chars), prefix=prefix, suffix=suffix)
                return unique_id
            except:
                pass

class UniqueId(models.Model):
    prefix = models.CharField(max_length=255, blank=True, null=True)
    suffix = models.CharField(max_length=255, blank=True, null=True)
    unique_id = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ("prefix","unique_id","suffix")
        db_table = "xadrpy_unique_id"
    
    def get_id(self):
        if not self.prefix and not self.suffix: 
            return self.unique_id
        if self.prefix and not self.suffix:
            return "%s-%s" % (self.prefix, self.unique_id) 
        if self.prefix and self.suffix:
            return "%s-%s-%s" % (self.prefix, self.unique_id, self.suffix) 
        if not self.prefix and self.suffix:
            return "%s-%s" % (self.unique_id, self.suffix) 
    
    objects = UniqueIdManager()

#class SerialIdManager(models.Manager):
#    
#    def get_unique_id(self, prefix=None, suffix=None):
#        serial_id = self.create(prefix=prefix, suffix=suffix)
#        return serial_id
#
#
#class SerialId(models.Model):
#    prefix = models.CharField(max_length=255, blank=True, null=True)
#    suffix = models.CharField(max_length=255, blank=True, null=True)
#    serial = models.BigIntegerField()
#    created = models.DateTimeField(auto_now_add=True)
#
#    class Meta:
#        unique_together = ("prefix","serial","suffix")
#        db_table = "xadrpy_serial_id"
#    
#    objects = UniqueIdManager()
