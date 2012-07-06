var BackOffice;

Ext.application({
    name: 'backoffice',
    appFolder: STATIC_URL+'xadrpy/backoffice',
    
    launch: function() {
    	BackOffice = this;

    	Ext.QuickTips.init();    	

    	var eventStore = Ext.create('Extensible.calendar.data.MemoryEventStore', {
            // defined in ../data/Events.js
            data: []
        });
    	
        var viewport = Ext.create('Ext.container.Viewport', {
            layout: 'border',
            id: 'viewport',
            title: 'BackOffice',
            iconCls: 'icon-add',
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
            	title: 'BackOffice',
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
                },
                {
                        xtype: 'extensible.calendarpanel',
                        title: 'Naptár',
                        eventStore: eventStore,
                        width: 700,
                        height: 500,
                        activeItem: 1,
                        editModal: true
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

