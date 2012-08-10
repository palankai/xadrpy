from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.comments.models import Comment
import mptt.models
import mptt.managers
import mptt.fields

class Feedback(mptt.models.MPTTModel, Comment):
    parent = mptt.fields.TreeForeignKey('self', null=True, blank=True, related_name='answers')
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Title"))
    site_name = models.CharField(max_length=255, blank=True, null=True)
    language_code = models.CharField(max_length=5, blank=True, null=True, verbose_name=_("Language code"))
    is_remote = models.BooleanField(default=False, verbose_name=_("Is remote"))

    tree = mptt.managers.TreeManager()

    class Meta:
        verbose_name = _("Feedback")
        verbose_name_plural = _("Feedback")
        db_table = "xadrpy_feedback_feedback"
        ordering = ('tree_id', 'lft')

