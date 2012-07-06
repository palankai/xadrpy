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
                flex: 2
            },this.dateCfg),
            Ext.apply({
                xtype: 'timefield',
                format: 'H:i:s',
                submitFormat: 'H:i:s',
                width: 80,
                flex: 1
            },this.timeCfg)
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
    		this.dateField.setValue(value.split(" ")[0]);
    		this.timeField.setValue(value.split(" ")[1]);
    	}
    },

    getSubmitData: function(){
        var value = this.getValue()
        var format = this.getFormat()
        console.log(value, format, Ext.Date.format(value, format));
        return value ? Ext.Date.format(value, format) : null;
    },

    getFormat: function(){
        return (this.dateField.submitFormat || this.dateField.format) + " " + (this.timeField.submitFormat || this.timeField.format)
    }
});