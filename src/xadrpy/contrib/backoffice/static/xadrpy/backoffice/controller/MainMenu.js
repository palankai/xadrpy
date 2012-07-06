Ext.define('backoffice.controller.MainMenu', {
    extend: 'Ext.app.Controller',
    
    views: [
        'MainMenu',
    ],
    
    onLaunch: function(application) {
    	var mainMenu = this.getView("backoffice.view.MainMenu");
    	var header = Ext.getCmp('header');
    	header.add(mainMenu);
    }
    
});
