from django.db import models
from xadrpy.core.models.fields.nullchar_field import NullCharField
from django.utils.translation import ugettext_lazy as _, get_language
from xadrpy.core.models.fields.nulltext_field import NullTextField
from xadrpy.core.models.fields.language_code_field import LanguageCodeField
import conf
import base
from django.contrib.contenttypes.models import ContentType
from xadrpy.utils.imports import get_class


class Unit(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))
    label = NullCharField(max_length=255, verbose_name=_("Label"))
    label_abbrev = NullCharField(max_length=255, verbose_name=_("Label abbrevation"))
    format = models.CharField(max_length=255, verbose_name=_("Format string"), help_text=_("eg. '%s km' or '$%s' -> 16 km, $16"))
    short_format = NullCharField(max_length=255, verbose_name=_("Format string (short)"), help_text=_("eg. '%s km' or '$%s' -> 16 km, $16"))
    is_callable = models.BooleanField(default=False, verbose_name=_("Is callable"), help_text=_("format string AND short format string are callable or not!"))
    
    class Meta:
        verbose_name = _("Measurement unit")
        verbose_name_plural = _("Measurement units")
        db_table = "xadrpy_dynamic_unit"
        ordering = ("label","name")

    def __unicode__(self):
        return self.label or self.name

class KeyTable(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))
    label = NullCharField(max_length=255, verbose_name=_("Label"))
    label_abbrev = NullCharField(max_length=255, verbose_name=_("Label abbrevation"))
    vtype = NullCharField(max_length=255, verbose_name=_("Value type"))

    class Meta:
        verbose_name = _("Key table")
        verbose_name_plural = _("Key table")
        db_table = "xadrpy_dynamic_key_table"
        ordering = ("label", "name")

    def __unicode__(self):
        return self.label or self.name


class KeyTableEntry(models.Model):
    key_table = models.ForeignKey(KeyTable, related_name="entries", verbose_name=_("Key table"))
    value = NullCharField(max_length=255, verbose_name=_("Value"))
    label = models.CharField(max_length=255, verbose_name=_("Label"))
    label_abbrev = NullCharField(max_length=255, verbose_name=_("Label abbrevation"))
    is_default = models.BooleanField(default=False, verbose_name=_("Is default"))
    position = models.IntegerField(default=1, verbose_name=_("Position index"))

    class Meta:
        verbose_name = _("Key table entry")
        verbose_name_plural = _("Key table entries")
        db_table = "xadrpy_dynamic_key_table_entry"
        ordering = ("position", "label")
        unique_together = ("key_table", "value",)
    
    def __unicode__(self):
        return self.label

class AttributeType(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))
    vtype = NullCharField(max_length=255, verbose_name=_("Value type"))
    unit = models.ForeignKey(Unit, blank=True, null=True, related_name="+", verbose_name=_("Measurement unit"))
    label = models.CharField(max_length=255, verbose_name=_("Label"))
    label_abbrev = NullCharField(max_length=255, verbose_name=_("Label abbrevation"))
    key_table = models.ForeignKey(KeyTable, blank=True, null=True, related_name="+", verbose_name=_("Key table"))  
    default_type = models.PositiveSmallIntegerField(default=0, choices=conf.DEFAULT_TYPES, verbose_name=_("Type of default"))
    default = models.TextField(blank=True, null=True, verbose_name=_("Default value"))
    content_types = models.ManyToManyField(ContentType, blank=True, null=True, db_table="xadrpy_dynamic_attribute_type_content_types", verbose_name=_("Related tables"), 
                                           help_text=_("leave blank if you need attach the attribute to any table"))

    class Meta:
        verbose_name = _("Attribute type")
        verbose_name_plural = _("Attribute types")
        db_table = "xadrpy_dynamic_attribute_type"
        ordering = ("name",)
    
    def __unicode__(self):
        return self.label

class AttributeCollection(models.Model):
    attribute_type = models.ForeignKey(AttributeType, verbose_name=_("Attribute type"))
    language_code = LanguageCodeField(blank=True, null=True, verbose_name=_("Language"))
    
    as_int = models.IntegerField(null=True, blank=True, verbose_name=_("as integer"))
    as_float = models.FloatField(null=True, blank=True, verbose_name=_("as float"))
    as_str = NullCharField(verbose_name=_("as string"))
    as_text = NullTextField(verbose_name=_("as text"))
    as_bool = models.NullBooleanField(verbose_name=_("as boolean"))
    as_date = models.DateTimeField(null=True, blank=True, verbose_name=_("as date"))
    as_datetime = models.DateTimeField(null=True, blank=True, verbose_name=_("as datetime"))

    def get_vtype_class(self):
        if hasattr(self, "_vtype_object"):
            return self._vtype_object
        self._vtype_object = get_class(self.attribute_type.vtype)(self) 
        return self._vtype_object
    
    def get_value(self):
        vtype = self.attribute_type.vtype
        if not vtype: return self.as_text
        if vtype in ['int','float','str','text','bool','date','datetime']:
            return getattr(self, "as_%s" % self.attribute_type.vtype)
        return self.get_vtype_class().get_value()
    
    def set_value(self, value):
        vtype = self.attribute_type.vtype
        if not vtype:
            self.as_text = value
        if vtype in ['int','float','str','text','bool','date','datetime']:
            setattr(self, "as_%s" % vtype, value)
        self.get_vtype_class().set_value(value)

    class Meta:
        abstract=True

    @classmethod
    def register(cls, origin_cls):
        field = origin_cls._attribute_foreign_key_field
        
        def get_attribute(self, name, language_code=None):
            if language_code==True:
                language_code = get_language()
            try:
                try:
                    kwargs = {field.name: self, "language_code":language_code, "attribute_type__name": name}
                    obj = cls.objects.get(**kwargs)
                except:
                    attribute_type = AttributeType.objects.get(name=name)
                    kwargs = {field.name: self, "language_code":language_code, "attribute_type": attribute_type}
                    obj = cls(**kwargs)
                    obj.set_defaults(getattr(obj, field.name))
                    obj.save()
                return obj 
            except cls.DoesNotExist:
                return self
            
        def get_attributes_object(self):
            return base.Attributes(self)
            
        setattr(origin_cls, "get_attribute", get_attribute)
        setattr(origin_cls, "get_attributes_object", get_attributes_object)
        setattr(origin_cls, "attributes", property(origin_cls.get_attributes_object))

    def set_defaults(self, origin, field_name, language_code):
        pass
