Ext.define('backoffice.admin.view.GroupList' ,{
    extend: 'Ext.grid.Panel',
    alias : 'widget.backoffice-grouplist',

    title : 'Csoportok',
    store: 'backoffice.admin.store.Groups',    

    initComponent: function() {
    	var groups_controller = BackOffice.getController('backoffice.admin.controller.GroupsController');
        this.columns = [
            { header: '#',  dataIndex: 'id', width: 50, align: "right"},
            { header: 'Csoport név',  dataIndex: 'name', flex: 1},
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
        			//users_controller.openUserEditDialog(model.get('id')); 
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
        			//users_controller.openUserDeleteDialog(model.get('id'), model.get("username")); 
        		}
            }
        ];

        this.tbar = {
        		xtype: 'toolbar',
        		items: [{
        			xtype: 'button',
        			text: 'Új csoport',
        			iconCls: 'icon-add',
        			action: 'openGroupAddDialog'
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
            store: 'backoffice.admin.store.Groups',   // same store GridPanel is using
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