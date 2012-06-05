from django.db import models
from xadrpy.contrib.unique_id.fields import UniqueIdField
try:
    import json
except:
    import simplejson as json

# Create your models here.
class Task(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)
    queue = models.CharField(max_length=255) #Queue
    message = models.TextField(blank=True, null=True) #JSONField
    response = models.TextField(blank=True, null=True) #JSONField
    
    def get_uid(self):
        return self.id
    
    def get_queue(self):
        return self.command
    
    def get_message(self):
        return json.loads(self.request)
    
    def set_message(self, message):
        self.message = json.dumps(message)
    
    def get_response(self):
        return json.loads(self.response)
    
    def set_response(self, response):
        self.response = json.dumps(response)
    