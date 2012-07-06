Ext.define('backoffice.admin.controller.UsersController', {
    extend: 'Ext.app.Controller',
    
    views: [
        'backoffice.admin.view.UserList',
        'backoffice.admin.view.UserAddDialog',
        'backoffice.admin.view.UserEditDialog',
    ],
    
    stores:[
       'backoffice.admin.store.Users',
    ],
    
    onLaunch: function(application) {
    },

	init: function(application) {
		this.application = application;
        this.control({
	        '[action=openAddUserDialog]': {
	            click: this.openUserAddDialog
	        }
        });
	},

    openUserAddDialog: function() {
    	var view = Ext.widget('backoffice-useradddialog', {});
    	view.on("saved", function() {
    		this.getStore('backoffice.admin.store.Users').load();
    	}, this);
    	view.show();
    },
    openUserEditDialog: function(user_id) {
    	var view = Ext.widget('backoffice-usereditdialog', {user_id: user_id});
    	view.setParams(user_id);
    	view.on("saved", function() {
    		this.getStore('backoffice.admin.store.Users').load();
    	}, this);
    	view.show();
    },

    openUserResetPasswordDialog: function(user_id) {
    	var view = Ext.create("backoffice.admin.view.UserResetPasswordDialog", {user_id: user_id});
    	view.show();
    },
    
    openUserDeleteDialog: function(user_id, username) {
    	Ext.Msg.show({
    	     title:'Felhasználó törlése',
    	     msg: 'Valóban törölni szeretné a "'+username+'" nevű felhasználót?',
    	     buttons: Ext.Msg.YESNO,
    	     icon: Ext.Msg.QUESTION,
    	     fn: function(answer) {
    	    	 if(answer == "yes") {
    	    		 Ext.Ajax.request({
    	    			scope: this,
    	    			url: CONFIG.api_path+"xadrpy.contrib.backoffice.admin/del_user/"+user_id+"/",
    	    			success: function(response) {
    	    				this.getStore('backoffice.admin.store.Users').load();
    	    			}
    	    		 });
    	    	 }
    	     },
    	     scope: this
    	});
    },
    
    deleteUser: function() {
    	console.log("delete...")
    }
    
});
