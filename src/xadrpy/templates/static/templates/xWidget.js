(function($) {
	var methods = {};
	var xWidget_options = {}
	
	$.fn.xWidget = function( method ) {
		if ( methods[method] ) {
			return methods[method].apply( this, Array.prototype.slice.call( arguments, 1 ));
		} else if ( typeof method === 'object' || ! method ) {
			return xWidget.apply( this, arguments );
		} else {
			$.error( 'Method ' +  method + ' does not exist on jQuery.xDataTable' );
		}  		
	};

	$.extend({
		xWidget : {}
	});
	
	function xWidget( options ) {
		var $this = $(this);
		$this.load(options.url);
	}
	
})(jQuery);
