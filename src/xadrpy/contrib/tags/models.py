from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from xadrpy.core.models.fields.nullchar_field import NullCharField
from django.utils.translation import ugettext_lazy as _

class Tag(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Title"), unique=True)
    slug = models.SlugField(max_length=255, verbose_name=_("Slug"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        db_table = "xadrpy_tags_tag"

class TaggedItem(models.Model):
    namespace = NullCharField(max_length=64, verbose_name=_("Namespace"))
    tag = models.ForeignKey(Tag, verbose_name=_('Tag'), related_name='items')
    content_type = models.ForeignKey(ContentType, verbose_name=_('Content type'))
    content_id = models.PositiveIntegerField(_('content id'), db_index=True)
    content = generic.GenericForeignKey('content_type', 'content_id')

    class Meta:
        unique_together = (('namespace', 'tag', 'content_type', 'content_id'),)
        verbose_name = _('Tagged item')
        verbose_name_plural = _('Tagged items')

    def __unicode__(self):
        if self.namespace:
            return u'%s-%s [%s]' % (self.content, self.namespace, self.tag)
        else:
            return u'%s [%s]' % (self.content, self.tag)
