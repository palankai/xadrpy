from django.utils.datastructures import SortedDict
from django.core.exceptions import FieldError

class BaseField(object):
    creation_counter = 0

    def set_name(self, name):
        self.name = name

    def set_source(self, source):
        self.source = source

class MetaclassFactory():
    def __init__(self, base_cls, options_cls, base_field_cls, field_mappings={}):
        self.base_cls = base_cls
        self.options_cls = options_cls
        self.base_field_cls = base_field_cls
        self.field_mappings = field_mappings

    def get_field_class(self, field):
        return self.field_mappings.get(field, self.base_field_cls)

    def fields_for_form(self, form, fields=None, exclude=None, field_callback=None):
        field_list = []
        ignored = []

        for name, f in form.base_fields.items():
            if fields is not None and not name in fields:
                continue
            if exclude and name in exclude:
                continue
    
            if field_callback is None:
                formfield = self.get_field_class(f)()
                formfield.set_name(name)
                formfield.set_source(f)
            elif not callable(field_callback):
                raise TypeError('formfield_callback must be a function or callable')
            else:
                formfield = field_callback(name, f)
    
            if formfield:
                field_list.append((name, formfield))
            else:
                ignored.append(name)
        field_dict = SortedDict(field_list)
        if fields:
            field_dict = SortedDict(
                [(f, field_dict.get(f)) for f in fields
                    if ((not exclude) or (exclude and f not in exclude)) and (f not in ignored)]
            )
        return field_dict
    
    def fields_for_model(self, model, fields=None, exclude=None, field_callback=None, need_readonly=True):
        field_list = []
        ignored = []
        opts = model._meta
        for f in opts.fields + opts.many_to_many:
            if not f.editable and not need_readonly:
                continue
            if fields is not None and not f.name in fields:
                continue
            if exclude and f.name in exclude:
                continue
    
            if field_callback is None:
                formfield = self.get_field_class(f)()
                formfield.set_name(f.name)
                formfield.set_source(f)

            elif not callable(field_callback):
                raise TypeError('formfield_callback must be a function or callable')
            else:
                formfield = field_callback(f.name, f)
    
            if formfield:
                field_list.append((f.name, formfield))
            else:
                ignored.append(f.name)
        field_dict = SortedDict(field_list)
        if fields:
            field_dict = SortedDict(
                [(f, field_dict.get(f)) for f in fields
                    if ((not exclude) or (exclude and f not in exclude)) and (f not in ignored)]
            )
        return field_dict
    
    
    def get_declared_fields(self, bases, attrs, with_base_fields=True):
        fields = [(field_name, attrs.pop(field_name)) for field_name, obj in attrs.items() if isinstance(obj, self.base_field_cls)]
        fields.sort(key=lambda x: x[1].creation_counter)
    
        if with_base_fields:
            for base in bases[::-1]:
                if hasattr(base, 'base_fields'):
                    fields = base.base_fields.items() + fields
        else:
            for base in bases[::-1]:
                if hasattr(base, 'declared_fields'):
                    fields = base.declared_fields.items() + fields
    
        return SortedDict(fields)

    def __call__(self, *args, **kwargs):
        cls = self.create()
        return cls(*args, **kwargs)

    def create(self):
        class Metaclass(type):
            def __new__(cls, name, bases, attrs):
                formfield_callback = attrs.pop('field_callback', None)
                try:
                    parents = [b for b in bases if issubclass(b, self.base_cls)]
                except NameError:
                    # We are defining ModelForm itself.
                    parents = None
                declared_fields = self.get_declared_fields(bases, attrs, False)
                new_class = super(Metaclass, cls).__new__(cls, name, bases,
                        attrs)
                if not parents:
                    return new_class
        
                opts = new_class._meta = self.options_cls(getattr(new_class, 'Meta', None))
                if getattr(opts, "form", None):
                    fields = self.fields_for_form(opts.form, opts.fields,
                                              opts.exclude, formfield_callback)
                    none_form_fields = [k for k, v in fields.iteritems() if not v]
                    missing_fields = set(none_form_fields) - \
                                     set(declared_fields.keys())
                    if missing_fields:
                        message = 'Unknown field(s) (%s) specified for %s'
                        message = message % (', '.join(missing_fields),
                                             opts.model.__name__)
                        raise FieldError(message)
                    # Override default model fields with any custom declared ones
                    # (plus, include all the other declared fields).
                    fields.update(declared_fields)
                elif opts.model:
                    # If a model is defined, extract form fields from it.
                    fields = self.fields_for_model(opts.model, opts.fields,
                                              opts.exclude, formfield_callback)
                    # make sure opts.fields doesn't specify an invalid field
                    none_model_fields = [k for k, v in fields.iteritems() if not v]
                    missing_fields = set(none_model_fields) - \
                                     set(declared_fields.keys())
                    if missing_fields:
                        message = 'Unknown field(s) (%s) specified for %s'
                        message = message % (', '.join(missing_fields),
                                             opts.model.__name__)
                        raise FieldError(message)
                    # Override default model fields with any custom declared ones
                    # (plus, include all the other declared fields).
                    fields.update(declared_fields)
                else:
                    fields = declared_fields
                for name, field in declared_fields.items():
                    field.set_name(name)
                new_class.declared_fields = declared_fields
                new_class.base_fields = fields
                return new_class
        return Metaclass 
