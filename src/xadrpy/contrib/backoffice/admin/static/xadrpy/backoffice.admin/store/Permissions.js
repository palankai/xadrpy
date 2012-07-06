Ext.define('backoffice.admin.store.Permissions', {
    extend: 'Ext.data.Store',
    autoLoad: false,
    fields: ['name','description'],
    proxy: {
        type: 'ajax',
        url : CONFIG.api_path+'auth/get_permissions/',
        reader: {
            type: 'json',
            root: 'response',
            successProperty: 'success'
        }
    }
});