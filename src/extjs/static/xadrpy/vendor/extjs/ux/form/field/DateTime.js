Ext.define('Ext.ux.form.field.DateTime', {
    extend:'Ext.form.FieldContainer',
    mixins: {
        field: 'Ext.form.field.Field'
    },
    alias: 'widget.datetimefield',
    layout: 'hbox',
    width: 200,
    height: 22,
    combineErrors: true,
    msgTarget :'side',

    dateCfg:{},
    timeCfg:{},

    initComponent: function() {
        var me = this;
        me.buildField();
        me.callParent();
        this.dateField = this.down('datefield')
        this.timeField = this.down('timefield')
        this.hiddenField = this.down('hiddenfield')
        me.initField();
    },

    //@private
    buildField: function(){
        this.items = [
            Ext.apply({
                xtype: 'datefield',
                format: 'Y-m-d',
                submitFormat: 'Y-m-d',
                width: 100,
                flex: 2,
                submitValue: false,
                scope: this,
                listeners: {
                	change: function() {
                		this.hiddenField.setValue(this.getSubmitData());
                	}
                }
            },this.dateCfg),
            Ext.apply({
                xtype: 'timefield',
                format: 'H:i:s',
                submitFormat: 'H:i:s',
                width: 80,
                flex: 1,
                submitValue: false,
                scope: this,
                listeners: {
                	change: function() {
                		this.hiddenField.setValue(this.getSubmitData());
                	}
                }
            },this.timeCfg),
            Ext.apply({
            	xtype: 'hiddenfield',
            	name: this.name
            })
        ]
    },

    getValue: function() {
        var value,date = this.dateField.getSubmitValue(),time = this.timeField.getSubmitValue();
        if(date){
            if(time){
                var format = this.getFormat()
                value = Ext.Date.parse(date + ' ' + time,format)
            }else{
                value = this.dateField.getValue()
            }
        }
        return value
    },

    setValue: function(value){
    	if( value ) {
    		this.hiddenField.setValue(value);
    		this.dateField.setValue(value.split(" ")[0]);
    		this.timeField.setValue(value.split(" ")[1]);
    	}
    },

    getSubmitData: function(){
        var value = this.getValue()
        var format = this.getFormat()
        var submit_data = value ? Ext.Date.format(value, format) : null;
        this.hiddenField.setValue(submit_data);
        return submit_data;
    },

    getFormat: function(){
        return (this.dateField.submitFormat || this.dateField.format) + " " + (this.timeField.submitFormat || this.timeField.format)
    }
});