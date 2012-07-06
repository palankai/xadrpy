Ext.define('backoffice.admin.controller.GroupsController', {
    extend: 'Ext.app.Controller',
    
    views: [
        'backoffice.admin.view.GroupList',
        'backoffice.admin.view.GroupEditDialog',
    ],
    
    stores:[
       'backoffice.admin.store.Groups',
       'backoffice.admin.store.Permissions',
    ],

	init: function(application) {
		this.application = application;
        this.control({
	        '[action=openGroupAddDialog]': {
	            click: this.openGroupAddDialog
	        }
        });
	},

    openGroupAddDialog: function() {
    	var view = Ext.create('backoffice.admin.view.GroupEditDialog', {});
    	view.on("saved", function() {
    		this.getStore('backoffice.admin.store.Groups').load();
    	}, this);
    	view.show();
    },


    
});
