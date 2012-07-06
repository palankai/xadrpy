Ext.Loader.setConfig({
    enabled : true,
    disableCaching : true,
    paths : {'backoffice': STATIC_URL+"xadrpy/backoffice"}
});
Ext.Loader.setPath("Ext.ux", STATIC_URL+"xadrpy/vendor/extjs/ux");

Ext.onReady(function(){
    Ext.QuickTips.init();
 
    Ext.Ajax.extraParams = {
    		'access_token': "1231213"
    	};
	// Create a variable to hold our EXT Form Panel. 
	// Assign various config options as seen.	 
    var login = new Ext.FormPanel({ 
        labelWidth:80,
        url: CONFIG.api_path+'xadrpy.contrib.backoffice/login/', 
        frame:true, 
        defaultType:'textfield',
        monitorValid:true,
        defaults:{
        	  enableKeyEvents:true,
        	  listeners:{
        	    specialKey: function(field, el)
        	    {
        	      if(el.getKey() == Ext.EventObject.ENTER)
        	      {
        	    	  var buttons = field.up("form").down("button[isDefault]");
        	          if(buttons){
        	                  Ext.each(buttons,function(element){
    	                          element.fireEvent("click");
        	                  });
        	          }          	    	//var btn = field.up('form').down("button");
        	        //btn.handler.call(btn.scope);
        	      }
        	    }
        	  }
        	},        
        items:[{ 
                fieldLabel:'Username', 
                name:'username', 
                allowBlank:false,
                id: "username"
            },{ 
                fieldLabel:'Password', 
                name:'password', 
                inputType:'password', 
                allowBlank:false 
            }],
 
	// All the magic happens after the user clicks the button     
        buttons:[{ 
        		id: 'login-button',
                text:'Login',
                formBind: true,
                isDefault: true,
                // Function that fires when user clicks the button
                handler:function(){
                    login.getForm().submit({ 
                        method:'POST', 
                        waitTitle:'Connecting', 
                        waitMsg:'Sending data...',
                        success:function(){ 
	                        window.location = CONFIG.redirect_uri;
                        },
                        failure:function(form, action){
                            if(action.failureType == 'server'){
                                Ext.Msg.alert('Login Failed!', action.response.error.text); 
                            }else{ 
                                Ext.Msg.alert('Warning!', 'Authentication server is unreachable : ' + action.response.responseText); 
                            } 
                            login.getForm().reset();
                        }
                        
                    }); 
                } 
            }] 
    });
 
 
	// This just creates a window to wrap the login form. 
	// The login object is passed to the items collection.       
    var win = new Ext.Window({
    	title: CONFIG.title+" Login",
        layout:'fit',
        width:280,
        height:120,
        closable: false,
        resizable: false,
        plain: true,
        border: false,
        iconCls: 'icon-settings',
        items: [login]
	});
	win.show();
});