from django.contrib.admin import site, ModelAdmin, StackedInline
import models
from django.utils.translation import ugettext_lazy as _

class KeyTableEntryAdmin(StackedInline):
    model = models.KeyTableEntry
    extra = 1

class KeyTableAdmin(ModelAdmin):
    inlines = [KeyTableEntryAdmin]
    
class UnitAdmin(ModelAdmin):
    pass

class AttributeTypeAdmin(ModelAdmin):
    filter_horizontal = ['content_types']
    fieldsets = (
        (None, {
            'fields': ('name', 'label', 'label_abbrev')
        }),
        (None, {
            'fields': ('vtype','unit','key_table','default_type','default')
        }),
        (_("Attach"), {
            'fields': ('content_types',)
        }),
    )
    
site.register(models.KeyTable, KeyTableAdmin)
site.register(models.Unit, UnitAdmin)
site.register(models.AttributeType, AttributeTypeAdmin)



