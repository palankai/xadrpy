var BackOffice;

Ext.application({
    name: 'backoffice',
    appFolder: STATIC_URL+'xadrpy/backoffice',
    
    launch: function() {
    	BackOffice = this;

    	Ext.QuickTips.init();    	
    	

    	var viewport = Ext.create('Ext.container.Viewport', {
            layout: 'border',
            id: 'viewport',
    		style: {
    			backgroundColor: "white",
    		},
    		shadow: "sides",
    		shodowOffset: 3,
            padding: '10 10 10 10',
            border: '3 3 3 3',
            items: [{
            	region: 'north',
            	xtype: 'panel',
            	title: CONFIG.title,
            	id: 'header',
            }, 
            {
            	xtype: 'tabpanel',
                region: 'center',
                id: 'content',
                activeTab: 0,      // First tab active by default
                items: [{
                    title: 'Asztal',
                    xtype: 'panel',
                }]    		
            } 
            ]
        });
    },
    controllers: CONFIG.controllers,
});


function defaultAction(menu_item) {
	if(menu_item.action) {
		addViewTab(menu_item.text, menu_item.action);
	}
}

function addViewTab(title, xtype) {
	var content_panel = Ext.getCmp("content");
	var tabs = content_panel.query(xtype);
	if (tabs.length) {
		content_panel.setActiveTab(tabs[0]);
		return;
	} 
	content_panel.setActiveTab(content_panel.add({
		title: title,
		xtype: xtype,
		closable: true
	}));
}

