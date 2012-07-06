Ext.define('backoffice.admin.view.UserList' ,{
    extend: 'Ext.grid.Panel',
    alias : 'widget.backoffice-userlist',

    title : 'Felhasználók',
    store: 'backoffice.admin.store.Users',    

    initComponent: function() {
    	var users_controller = BackOffice.getController('backoffice.admin.controller.UsersController');
        this.columns = [
            { header: '#',  dataIndex: 'id', width: 50, align: "right"},
            { header: 'Felhasználónév',  dataIndex: 'username', flex: 1},
            { header: 'Teljes név',  dataIndex: 'full_name', flex: 1},
            { header: 'E-mail cím',  dataIndex: 'email', flex: 1},
            { header: 'Rendszergazda',  dataIndex: 'is_superuser', flex: 1},
            { xtype: 'actioncolumn',
            	width: 32,
            	align: 'center',
            	sortable:false,
            	resizable: false,
            	hideable: false,
            	menuDisabled: true,
        		icon: CONFIG.icons+'edit.png',
        		tooltip: "Szerkesztés",
        		scope: this,
        		action: "edit",
        		handler: function(grid, rowIndex, colIndex, button, event, model) {
        			users_controller.openUserEditDialog(model.get('id')); 
        		}
            },
            { xtype: 'actioncolumn',
            	width: 32,
            	align: 'center',
            	sortable:false,
            	resizable: false,
            	hideable: false,
            	menuDisabled: true,
        		icon: CONFIG.icons+'lock-edit.png',
        		tooltip: "Jelszó változtatás",
        		scope: this,
        		action: "reset-password",
        		handler: function(grid, rowIndex, colIndex, button, event, model) {
        			users_controller.openUserResetPasswordDialog(model.get('id')); 
        		}
            },
            { xtype: 'actioncolumn',
            	width: 32,
            	align: 'center',
            	sortable:false,
            	resizable: false,
            	hideable: false,
            	menuDisabled: true,
            	icon: CONFIG.icons+'delete.png',
        		tooltip: "Törlés",
        		scope: this,
        		action: "delete",
        		handler: function(grid, rowIndex, colIndex, button, event, model) { 
        			users_controller.openUserDeleteDialog(model.get('id'), model.get("username")); 
        		}
            }
        ];

        this.tbar = {
        		xtype: 'toolbar',
        		items: [{
        			xtype: 'button',
        			text: 'Új felhasználó',
        			iconCls: 'icon-add',
        			action: 'openAddUserDialog'
        		},{
        			xtype: 'button',
        			text: 'Frissítés',
        			iconCls: 'icon-refresh',
        			scope: this,
        			handler: function() {
        				this.getStore().load();
        			}
        		}]
        }
        this.dockedItems=[{
            xtype: 'pagingtoolbar',
            store: 'backoffice.admin.store.Users',   // same store GridPanel is using
            dock: 'bottom',
            pageSize: 50,
            displayInfo: true,
            displayMsg: 'Sorok: {0} - {1}; Összesen: {2} sor',
            emptyMsg: "Nincs adat",
            firstText: "Első",
            prevText: "Előző",
            nextText: "Következő",
            lastText: "Utolsó",
            refreshText: "Frissít",
            afterPageText: " / {0}",
            beforePageText: "Oldal"
            
        }];
        
        this.selType = "checkboxmodel";
        this.selModel = {
        	allowDeselect: true,
        	injectCheckbox: "last",
        	mode: 'MULTI',
        }
        
        this.callParent(arguments);
        this.getStore().load();        

    }
});