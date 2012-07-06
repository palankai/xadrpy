Ext.define("backoffice.admin.Module", {
	extend: 'backoffice.Module',

	onLaunch: function() {
		var main_menu = Ext.getCmp("MainMenu");
		main_menu.add({ xtype: 'button', text: 'Adminisztráció', iconCls: 'icon-settings', menu: [
                              { text: 'Felhasználók', iconCls: 'icon-users', action: 'backoffice-userlist', handler: defaultAction },
                              { text: 'Csoportok', iconCls: 'icon-users', action: 'backoffice-grouplist', handler: defaultAction },
                              { text: 'Rendszer beállítások', iconCls: 'icon-clients' },
                      ]});
	}

});