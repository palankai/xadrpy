from django.db import models

class ConsumerManager(models.Manager):
    
    def create_static(self, static_key, name, site=None, description=None, redirect_uri=None, consumer_type=None, scope=[], data=None):
        consumer, unused = self.get_or_create(static_key=static_key, site=site)
        consumer.name = name
        consumer.site = site
        consumer.description = description
        consumer.redirect_uri = redirect_uri
        consumer.consumer_type = consumer_type
        consumer.scope = scope
        consumer.save()
        if data:
            consumer.set_initial_data(data)
        return consumer
    
    def get_static(self, static_key, site=None):
        return self.get(static_key=static_key, site=site)
