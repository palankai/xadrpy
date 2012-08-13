from xadrpy.utils.jsonlib import JSONEncoder
from xadrpy.contrib.backoffice.ext.base import JSFunction
from django.utils.safestring import mark_safe
from xadrpy.utils.declarative import BaseField, MetaclassFactory
from xadrpy.core.api.decorators import APIObject
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.template.context import RequestContext
from xadrpy.core.models.libs import model_to_dict
from django import forms
from xadrpy.core.forms.exceptions import FormException
encoder = JSONEncoder()

class Field(BaseField):
    
    def __init__(self, dataType=None, dateFormat=None, defaultValue=None, mapping=None, persist=None, sortDir=None, useNull=None, calc=None):
        self.easy = dataType==None and dateFormat==None and defaultValue==None and mapping==None and persist==None and sortDir==None and useNull==None
        self.name = None
        self.source = None
        self.dataType = dataType or "auto"
        self.dateFormat = dateFormat
        self.defaultValue = defaultValue or ""
        self.mapping = mapping or True
        self.persist = persist or True
        self.sortDir = sortDir or "ASC"
        self.useNull = useNull or False
        self.calc = calc
    
    
    def to_data(self):
        if self.easy:
            return self.name
        return {
            'name': self.name,
            'type': self.dataType,
            'dateFormat': self.dateFormat,
            'defaultValue': self.defaultValue,
            'mapping': self.mapping,
            'persist': self.persist,
            'sortDir': self.sortDir,
            'useNull': self.useNull,
        }
    
    def get_value(self, record):
        if callable(self.calc):
            return self.calc(record)
        return getattr(record, self.name, self.defaultValue)

class ModelBased(APIObject):
    
    @APIObject.response(pattern=r"(?P<pk>[0-9]+)?$")
    def main(self, request, pk=None):
        if request.method == "GET":
            return self.read(request, pk)

        if request.method == "POST":
            return self.create(request)

        if request.method == "PUT":
            return self.update(request, pk)

        if request.method == "DELETE":
            return self.delete(request, pk)

    @APIObject.response(pattern=r"read/(?P<pk>[0-9]+)?$")
    def read(self, request, pk=None):
        pk = request.GET.get('id', pk)
        if pk:
            obj = self._meta.model.objects.get(pk=pk)
            return self.record_to_dict(obj)
        qs, total = self._get_queryset(request, True)
        result = []
        for row in qs:
            record = model_to_dict(row, self._meta.fields, self._meta.exclude)
            for field_name in self.base_fields:
                if self._meta.fields and field_name not in self._meta.fields:
                    continue
                if self._meta.exclude and field_name in self._meta.exclude:
                    continue
                record[field_name] = self.base_fields[field_name].get_value(row)
            result.append(record)
        return result, total
    

    @APIObject.response(pattern=r"create/$")
    def create(self, request, pk=None):
        form_cls = self.get_form_cls()
        
        if request.DATA == False and request.method in ["POST"] and request.POST:
            form = form_cls(request.POST)
            if not form.is_valid():
                raise FormException(form)
            instance = form.save()
            return self.record_to_dict(instance)
        
        results = []
        for POST in request.POSTS:
            form = form_cls(POST)
            if not form.is_valid():
                raise FormException(form)
            instance = form.save()
            results.append(self.record_to_dict(instance))
        return results
    
    @APIObject.response(pattern=r"update/(?P<pk>[0-9]+)?$")
    def update(self, request, pk=None):
        form_cls = self.get_form_cls()

        if request.DATA == False and request.method in ["POST","PUT"] and request.POST:
            obj = self._meta.model.objects.get(pk=request.POST.get('id'))
            form = form_cls(request.POST, instance=obj)
            if not form.is_valid():
                raise FormException(form)
            instance = form.save()
            return self.record_to_dict(instance)
        
        results = []
        for POST in request.POSTS:
            obj = self._meta.model.objects.get(pk=POST.get('id'))
            form = form_cls(POST, instance=obj)
            if not form.is_valid():
                raise FormException(form)
            instance = form.save()
            results.append(self.record_to_dict(instance))
        return results
    
    @APIObject.response(pattern=r"delete/(?P<pk>[0-9]+)?$")
    def delete(self, request, pk=None):
        pk = pk or request.GET.get('id') 
        if pk:
            obj = self._meta.model.objects.get(pk=pk)
            obj.delete()
            return True
        
        for POST in request.POSTS:
            obj = self._meta.model.objects.get(pk=POST.get('id'))
            obj.delete()
        return True

    def get_form_cls(self):
        if self._meta.form:
            return self._meta.form
        class Form(forms.ModelForm):
            class Meta:
                model = self._meta.model
        return Form

    def _get_queryset(self, request, need_total=False):
        query_set = self._meta.model.objects.get_query_set()
        
        if request.PARAMS.orders:
            query_set = query_set.order_by(*request.PARAMS.orders)
        if request.PARAMS.filters:
            query_set = query_set.filter(**request.PARAMS.filters)
        
        if need_total:
            total = query_set.count()
            
        if request.PARAMS.start:
            query_set = query_set[request.PARAMS.start:]
        if request.PARAMS.limit:
            query_set = query_set[:request.PARAMS.limit]
        if need_total:
            return query_set, total
        return query_set        

    def record_to_dict(self, obj):
        record = model_to_dict(obj, self._meta.fields, self._meta.exclude)
        for field_name in self.base_fields:
            if self._meta.fields and field_name not in self._meta.fields:
                continue
            if self._meta.exclude and field_name in self._meta.exclude:
                continue
            record[field_name] = self.base_fields[field_name].get_value(obj)
        return record

class ModelOptions(object):
    def __init__(self, options=None):
        self.name = getattr(options, 'name', None)
        self.base = getattr(options, 'base', "Ext.data.Model")
        self.template = getattr(options, 'template', "xadrpy/backoffice/generic/model.js")
        self.proxy = getattr(options, "proxy", "rest")
        self.form = getattr(options, 'form', None)
        self.model = getattr(options, 'model', None)
        self.fields = getattr(options, 'fields', None)
        self.exclude = getattr(options, 'exclude', None)

class BaseModel(ModelBased):

    def render(self, request):
        print dir(self.base_fields)
        ctx = {
            'name': self._meta.name,
            'base': self._meta.base,
            'url': reverse(self.main),
            'create_url': reverse(self.create),
            'update_url': reverse(self.update),
            'read_url': reverse(self.read),
            'delete_url': reverse(self.delete),
            'proxy': self._meta.proxy,
            'fields': [field.to_data() for field in self.base_fields.values()], 
        }
        return render_to_string(self._meta.template, ctx, RequestContext(request))

    def register_in_api(self, interface, prefix):
        if not self._meta.name:
            self._meta.name = interface.namespace+".model."+self.__class__.__name__
        super(BaseModel, self).register_in_api(interface, prefix)

class StoreOptions(object):
    def __init__(self, options=None):
        self.name = getattr(options, 'name', None)
        self.base = getattr(options, 'base', "Ext.data.Store")
        self.template = getattr(options, 'template', "xadrpy/backoffice/generic/store.js")
        self.autoload = getattr(options, 'autoload', False)
        self.proxy = getattr(options, "proxy", "rest")
        self.form = getattr(options, 'form', None)
        self.model = getattr(options, 'model', None)
        self.model_obj = getattr(options, 'model_obj', None)
        self.fields = getattr(options, 'fields', None)
        self.exclude = getattr(options, 'exclude', None)

class BaseStore(ModelBased):

    def render(self, request):
        ctx = {
            'name': self._meta.name,
            'base': self._meta.base,
            'autoload': self._meta.autoload,
            'model_name': self._meta.model_obj._meta.name if self._meta.model_obj else None,
            'url': reverse(self.main),
            'create_url': reverse(self.create),
            'update_url': reverse(self.update),
            'read_url': reverse(self.read),
            'delete_url': reverse(self.delete),
            'proxy': self._meta.proxy,
            'fields': [field.to_data() for field in self.base_fields.values()], 
        }
        return render_to_string(self._meta.template, ctx, RequestContext(request))

    def register_in_api(self, interface, prefix):
        if not self._meta.name:
            self._meta.name = interface.namespace+".store."+self.__class__.__name__
        super(BaseStore, self).register_in_api(interface, prefix)

class Model(BaseModel):
    __metaclass__ = MetaclassFactory(BaseModel, ModelOptions, Field)
      
class Store(BaseStore):
    __metaclass__ = MetaclassFactory(BaseStore, StoreOptions, Field)
