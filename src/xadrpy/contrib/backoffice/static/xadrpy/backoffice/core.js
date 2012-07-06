Ext.Loader.setConfig({
    enabled : true,
    disableCaching : CONFIG.debug,
    paths : CONFIG.namespaces
});
Ext.Loader.setPath("Ext.ux", STATIC_URL+"xadrpy/vendor/extjs/ux");
Ext.define("backoffice.Module", {
	extend: 'Ext.app.Controller',
});

