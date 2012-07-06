Ext.define('backoffice.admin.view.UserAddDialog', {
    extend: 'Ext.window.Window',
    alias : 'widget.backoffice-useradddialog',

    title : 'Új felhasználó hozzáadása',
    layout: 'fit',
    modal: true,
    iconCls: 'icon-add',
    monitorValid:true,
    
    initComponent: function() {
        this.items = [
            {
                xtype: 'form',
                bodyPadding: 5,
                url: CONFIG.api_path+'xadrpy.contrib.backoffice.admin/add_user/', 
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
                        xtype: 'textfield',
                        name : 'password',
                        inputType: 'password',
                        fieldLabel: 'Jelszó',
                        width: 400,
                        allowBlank: false,
                        minLength: 3
                    },
                    {
                        xtype: 'textfield',
                        name : 'password2',
                        inputType: 'password',
                        fieldLabel: 'Jelszó (ismét)',
                        width: 400,
                        allowBlank: false,
                        minLength: 3
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
        
    }

});