Ext.define('backoffice.view.UserChangePasswordDialog', {
    extend: 'Ext.window.Window',

    title : 'Saját új jelszó beállítás',
    layout: 'fit',
    modal: true,
    iconCls: 'icon-edit',
    monitorValid:true,
    
    initComponent: function() {
    	this.store = Ext.data.StoreManager.lookup("backoffice.store.Users");
        this.items = [
            {
                xtype: 'form',
                bodyPadding: 5,
                url: CONFIG.api_path+'xadrpy.contrib.backoffice/change_password/',
                items: [
                    {
                        xtype: 'textfield',
                        name : 'original_password',
                        inputType: 'password',
                        fieldLabel: 'Eredeti jelszó',
                        width: 400,
                        allowBlank: false,
                    },
                    {
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
        		Ext.MessageBox.show({                                                                                                                                                                         
                    msg: 'Jelszavát megváltoztattuk!',
                    width:300,                                                                                                                                                                       
                    buttons : Ext.MessageBox.OK,
        		});                                                                                                                                                                                           
        		setTimeout(function(){                                                                                                                                                                        
                    Ext.MessageBox.hide();                                                                                                                                                               
        		}, 2000);
                this.close();
            },
        	failure: ResponseHandler.handleFormFailure
        });
        
    }

});