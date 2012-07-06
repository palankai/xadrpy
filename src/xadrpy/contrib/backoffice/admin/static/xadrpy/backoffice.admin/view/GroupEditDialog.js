Ext.define('backoffice.admin.view.GroupEditDialog', {
    extend: 'Ext.window.Window',

    title : 'Új csoport hozzáadása',
    layout: 'fit',
    modal: true,
    iconCls: 'icon-add',
    monitorValid:true,
    
    initComponent: function() {
    	var states = Ext.create('Ext.data.Store', {
    	    fields: ['abbr', 'name'],
    	    data : [
    	        {"abbr":"AL", "name":"Alabama"},
    	        {"abbr":"AK", "name":"Alaska"},
    	        {"abbr":"AZ", "name":"Arizona"}
    	    ]
    	});    	
    	
        this.items = [
            {
                xtype: 'form',
                bodyPadding: 5,
                url: CONFIG.api_path+'xadrpy.contrib.backoffice.admin/add_group/', 
                items: [
                    {
                        xtype: 'textfield',
                        name : 'name',
                        fieldLabel: 'Csoport név',
                        width: 400,
                        allowBlank: false,
                        minLength: 3,
                        maxLength: 80
                    },
                    {
                    	xtype: 'combobox',
                    	name: 'permissions',
                    	fieldLabel: 'Engedélyek',
                    	width: 400,
                    	multiSelect: true,
                    	queryMode: 'remote',
                    	store: 'backoffice.admin.store.Permissions',
                    	displayField: 'description',
                        valueField: 'name',
                        editable: false
                    },{
                    	xtype: 'datetimefield',
                    	name: 'dt',
                    	fieldLabel: 'Dátum',
                    	width: 400
                    	
                    }
                ],
                buttons : [
                           {
                               formBind: true,
                               text: 'Mentés',
                               action: 'save',
                               iconCls: 'icon-save',
                               scope: this,
                               handler: this.saveUser
                           },
                           {
                               text: 'Mégse',
                               iconCls: 'icon-cancel',
                               scope: this,
                               handler: this.close
                           }
                ]
            }
        ];

        this.callParent(arguments);
    },
    
    saveUser: function(button) {
       	var win    = button.up('window');
        var form   = win.down('form');
        var values = form.getValues();
    	if( !form.getForm().isValid() ) {
    		Ext.MessageBox.show({                                                                                                                                                                         
                msg: 'Kérem ellenőrizze az adatokat!',                                                                                                                           
                width:300,                                                                                                                                                                       
                buttons : Ext.MessageBox.OK,
                icon: Ext.MessageBox.WARNING,
    		});                                                                                                                                                                                           
    		setTimeout(function(){                                                                                                                                                                        
                 Ext.MessageBox.hide();                                                                                                                                                               
    		}, 2000);
    		return;
    	}
    		
        form.getForm().submit({ 
            method:'POST', 
            scope: this,
            success:function(){ 
                this.fireEvent("saved");
                this.close();
            },
            failure: ResponseHandler.handleFormFailure
        });
        
    },

    setParams: function(group_id) {
    	var user = this.store.getById(group_id);
       	var win    = this;
        var form   = win.down('form');
        var values = form.getValues();
        form.getForm().setValues({
        	name: user.get('name'),
        });
        this.title = "Csoport módosítása"
    	
    }
    

});