Ext.define('backoffice.admin.store.Groups', {
    extend: 'Ext.data.Store',
    autoLoad: false,
    fields: ['id','name'],
    proxy: {
        type: 'ajax',
        url : CONFIG.api_path+'xadrpy.contrib.backoffice.admin/get_groups/',
        reader: {
            type: 'json',
            root: 'response',
            successProperty: 'success'
        }
    }
});