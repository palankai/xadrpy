Ext.define('backoffice.admin.store.Users', {
    extend: 'Ext.data.Store',
    autoLoad: false,
    fields: ['id','username','email','full_name','last_name','first_name','display','is_superuser'],
    proxy: {
        type: 'ajax',
        url : CONFIG.api_path+'xadrpy.contrib.backoffice.admin/get_users/',
        reader: {
            type: 'json',
            root: 'response',
            successProperty: 'success'
        }
    }
});