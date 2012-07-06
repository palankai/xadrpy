Ext.define('backoffice.view.MainMenu' ,{
	extend: "Ext.toolbar.Toolbar",
	alias: 'widget.MainMenu',
	id: 'MainMenu',
	items: [{ xtype: 'button', text: CONFIG.user_display, iconCls: 'icon-user', menu: [
                { text: 'Nyelv váltás', iconCls: 'icon-language-chooser', menu: [
              	    { text: 'Angol', iconCls: 'icon-gb' },
            	    { text: 'Magyar', iconCls: 'icon-hu' }
                ]},
    	        { text: 'Jelszó változtatás', iconCls: 'icon-change-password', handler: function() {
    	        	var dialog = Ext.create("backoffice.view.UserChangePasswordDialog");
    	        	dialog.show();
    	        }},
    	        { text: 'Beállítások', iconCls: 'icon-settings'},
    	        '-',
    	        { text: 'Kijelentkezés', iconCls: 'icon-logout', handler: function() { window.location = CONFIG.logout_url; } }
    	    ]}    	    
    ]
});