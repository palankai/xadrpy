from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
import datetime

class Linkback(models.Model):
    content_type = models.ForeignKey(ContentType, verbose_name=_("Content type"), related_name="+")
    content_id = models.PositiveIntegerField(verbose_name=_("Content id"))
    content = generic.GenericForeignKey('content_type', 'content_id')
    
    url = models.URLField(verbose_name=_("URL"))
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Title"))
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Name"))
    excerpt = models.TextField(blank=True, null=True, verbose_name=_("Excerpt"))
    
    remote_ip = models.IPAddressField(verbose_name=_("Remote IP"))
    site = models.ForeignKey(Site, verbose_name=_("Site"))
    is_public = models.BooleanField(default=False, verbose_name=_("Is public"))
    submit_date = models.DateTimeField(default=None, verbose_name=_("Submit date"))
    
    class Meta:
        unique_together = ('content_type','content_id','url')
        verbose_name = _("Linkback")
        verbose_name_plural = _("Linkbacks")
        db_table = "xadrpy_linkback_linkback"
    
    def __unicode__(self):
        return u"Linkback from %s" % self.url

    def save(self, *args, **kwargs):
        if self.submit_date is None:
            self.submit_date = datetime.datetime.now()
        super(Linkback, self).save(*args, **kwargs)