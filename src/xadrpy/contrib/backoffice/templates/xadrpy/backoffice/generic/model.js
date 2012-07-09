{% load xtemplates %}
Ext.define('{{ name }}', {
    extend: '{{ base }}',
    fields: {{ fields|JSON }},
{% if proxy == "rest" %}    
    proxy: {
        type: 'rest',
        url : '{{ url }}',
        reader: {
            type: 'json',
            root: 'response',
            successProperty: 'success'
        },
		writer: {
		    type: 'json',
		    allowSingle: false
		}
    }
{% elif proxy == "ajax" %}
    proxy: {
        type: 'ajax',
        api: {
            create  : '{{ create_url }}',
            read    : '{{ read_url }}',
            update  : '{{ update_url }}',
            destroy : '{{ delete_url }}'
        },
        appendId: true,
        reader: {
            type: 'json',
            root: 'response',
            successProperty: 'success'
        },
        writer: {
            type: 'json',
            allowSingle: false
        }
   }
{% endif %}
});