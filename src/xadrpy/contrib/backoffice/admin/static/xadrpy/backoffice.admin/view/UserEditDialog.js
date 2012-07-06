Ext.define('backoffice.admin.view.UserEditDialog', {
    extend: 'Ext.window.Window',
    alias : 'widget.backoffice-usereditdialog',

    title : 'Felhasználó módosítása',
    layout: 'fit',
    modal: true,
    iconCls: 'icon-edit',
    monitorValid:true,
    
    initComponent: function() {
    	this.store = Ext.data.StoreManager.lookup("backoffice.admin.store.Users");
        this.items = [
            {
                xtype: 'form',
                bodyPadding: 5,
                url: CONFIG.api_path+'xadrpy.contrib.backoffice.admin/edit_user/'+this.user_id+"/",
                items: [
                    {
                        xtype: 'textfield',
                        name : 'username',
                        fieldLabel: 'Felhasználó név',
                        width: 400,
                        allowBlank: false,
                        minLength: 3
                    },
                    {
                        xtype: 'textfield',
                        name : 'last_name',
                        fieldLabel: 'Vezeték név',
                        width: 400,
                    },
                    {
                        xtype: 'textfield',
                        name : 'first_name',
                        fieldLabel: 'Kereszt név',
                        width: 400,
                    }
                    ,{
                        xtype: 'textfield',
                        name : 'email',
                        vtype: 'email',
                        fieldLabel: 'E-mail cím',
                        width: 400
                    }
                    ,{
                        xtype: 'checkbox',
                        name : 'is_superuser',
                        fieldLabel: 'Rendszergazda',
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
    
    setParams: function(user_id) {
    	var user = this.store.getById(user_id);
       	var win    = this;
        var form   = win.down('form');
        var values = form.getValues();
        form.getForm().setValues({
        	username: user.get('username'),
        	is_superuser: user.get('is_superuser'),
        	email: user.get('email'),
        	first_name: user.get('first_name'),
        	last_name: user.get('last_name')
        });
    	
    }

});