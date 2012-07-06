from django import forms
from django.utils.translation import ugettext as _

class FormException(Exception):
    
    def __init__(self, *forms_or_formsets):
        super(FormException, self).__init__(_("Data fill error"))
        self.fields = {}
        self.field_errors = {}
        self.non_field_errors = []
        for form_or_formset in forms_or_formsets:
            if isinstance(form_or_formset, forms.Form) or isinstance(form_or_formset, forms.ModelForm):
                if form_or_formset.errors:
                    self.get_single_form_errors(form_or_formset)
            else:
                if form_or_formset.errors:
                    for form in form_or_formset.forms:
                        if form.errors:
                            self.get_single_form_errors(form)

    def get_single_form_errors(self, form):
        field_errors = {}
        non_field_errors = []
        fields = {}
        for field in form:
            fields[form.prefix+"-"+field.name if form.prefix else field.name] = unicode(field.label)
        for k,v in form.errors.items():
            if k=="__all__":
                non_field_errors=v
            else:
                if form.prefix:
                    field_errors[form.prefix+"-"+k]=v
                else:
                    field_errors[k]=v
        self.field_errors.update(field_errors)
        self.non_field_errors.extend(non_field_errors)
        self.fields.update(fields)
        return fields, non_field_errors, field_errors
