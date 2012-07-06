{% load xtemplates %}
Ext.define('{{ name }}', {
    extend: 'Ext.data.Store',
    autoLoad: {{ autoload|JSON }},
    fields: {{ fields|JSON }},
    proxy: {
        type: 'ajax',
        url : CONFIG.api_path+'{{ url }}',
        reader: {
            type: 'json',
            root: 'response',
            successProperty: 'success'
        }
    }
});