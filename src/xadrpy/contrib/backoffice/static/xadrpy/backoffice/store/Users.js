Ext.define('backoffice.store.Users', {
    extend: 'Ext.data.Store',
    autoLoad: false,
    fields: ['id','username','display','full_name'],
    proxy: {
        type: 'ajax',
        url : CONFIG.api_path+'xadrpy.contrib.backoffice/user_list/',
        reader: {
            type: 'json',
            root: 'response',
            successProperty: 'success'
        }
    }
});