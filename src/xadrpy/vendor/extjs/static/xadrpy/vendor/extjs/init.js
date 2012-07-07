//Ext.MessageBox.CRITICAL = 'ext-mb-error';
ResponseHandler = function() {
    /**
     * Megpróbálja átkódolni a json stringet objektummá.
     * Ha a kapott érték string, akkor átkódolja, ha objektum, akkor visszatér vele
     * Ha bármi probléma van, akkor hibát dobunk
     *
     * @param {Object} value
     *
     * @return Object
     *
     * @see Ext.decode
     */
    var _tryDecode = function(value)
    {
        if ((typeof value).toLowerCase() === 'string') {
            var v = null;
            try {
                v = Ext.decode(value);
            } catch (e) {
                throw(
                    'ResponseHandler: '
                    + 'The response is not a json string.'
                );
            }
            return v;
        } else if ((typeof value).toLowerCase() === 'object') {
            return value;
        }
        throw(
            'ResponseHandler: '
            + 'The response is not a string or object.'
        );
    };

    return {

        /**
         * Hiba: nincs bejelentkezve
         * @param {Number}
         */
        FAILURE_AUTH : 2,

        /**
         * Hiba: nem elérhető funkció
         * @param {Number}
         */
        FAILURE_LOCK : 1,

        /**
         * Hiba: nem speciális hiba
         * @param {Number}
         */
        FAILURE_NONE : -1,

        errorTitle: "Error!",
        unexpectError: "Unknown error. The server send the next message:",
        responseStatus: "Response status:",
        responseText: "Response text:",
        unexpectErrorTitle: "Unknown error!",
        clientErrorTitle: "Hibásan kitöltött form",
        clientErrorText: "Figyelem! A piros aláhúzással jelölt mezők rosszul lettek kitöltve. Kérem, ellenőrizze!",



        /**
         * Megvizsgálja, hogy a kapott json objektum tartalmaz-e authorizációs gondokat,
         * és csak akkor tér vissza falsal, ha tartalmaz, és annak értéke false
         *
         * @param {Object|String} response
         *
         * @return {Boolean} csak akkor tér vissza false-al, ha a kapott json tartalmazza az authorized: false-t
         *                    minden egyéb esetben true
         */
        isAuthenticationFailure : function(response)
        {
            var obj = _tryDecode(response);

            if (obj.authorized === false) {
                return true;
            }

            return false;
        },

        /**
         * Megvizsgálja, hogy a kapott json objektum tartalmaz-e lokkolási gondokat,
         * és csak akkor tér vissza trueval, ha tartalmaz, és annak értéke true
         *
         * @param {Object|String} response
         *
         * @return {Boolean} csak akkor tér vissza false-al, ha a kapott json tartalmazza az locked: true-t
         *                    minden egyéb esetben tru
         */
        isLocked : function(response)
        {
            var obj = _tryDecode(response);

            if (obj.locked === true) {
                return true;
            }

            return false;
        },
        /**
         * Visszatér a hiba számával a kapott json tömb alapján
         *
         * @param {String|XmlHttpResponse} response The response to inspect for errors
         *
         * @return {Number}
         */
        getFailureType : function(response)
        {
            var resp = null;

            if (response) {
                if (response.responseText) {
                    resp = _tryDecode(response.responseText);
                } else {
                    resp = _tryDecode(response);
                }
            }

            if (resp.authorized === false) {
                return this.FAILURE_AUTH;
            }

            if (resp.locked === true) {
                return this.FAILURE_LOCK;
            }

            return this.FAILURE_NONE;
        },

        /**
         * Visszatér a dekódolt json stringgel, ha sikerült a lekérés, vagy null-al, ha esetleg nem...
         *
         * @param {String|XmlHttpResponse}
         *
         * @return {Object}
         *
         */
        isSuccess : function(response)
        {
            var resp = null;
            try {
                if(response.response) {
                  resp = response.response;
                }else if (response.responseText) {
                    resp = _tryDecode(response.responseText);
                } else {
                    resp = _tryDecode(response);
                }

                if (resp.success === true) {
                    return resp;
                }
            } catch (e) {

            }

            return null;
        },

        /**
         * Visszatér a dekódolt json stringgel, ha NEM sikerült a lekérés, vagy null-al, ha sikeres...
         *
         * @param {String|XmlHttpResponse}
         *
         * @return {Object}
         *
         */
        isFailure : function(response)
        {
            var resp = null;
            try {
                if(response.response) {
                  resp = response.response;
                }else if (response.responseText) {
                    resp = _tryDecode(response.responseText);
                } else {
                    resp = _tryDecode(response);
                }

                if (resp.success === false) {
                    return resp;
                }
            } catch (e) {

            }

            return null;
        },
        parseData: function(response) {
            var resp = response;
            try {
                if (resp) {
                    if (resp.responseText) {
                        resp = _tryDecode(resp.responseText);
                    } else {
                        resp = _tryDecode(resp);
                    }
                }
                response.data = resp;
            } catch (e) {
            	response.data = null;
            }
        	
        },
        /**
         * Ez az objektum kezeli le a hibákat, melyek a válaszból jöhetnek
         * Ha bármilyen hiba van, akkor megjelenít egy üzenetboxot, melyben benne vannak a hibák
         *
         * Az options objektum paraméterei:
         * 	onLogin : false, or object:
         *  fn : ez a funkció lesz meghívva login után
         *  scope : scope, ami a meghívott fügvénynek át van adva
         *  
		 *	title : egyedi cím megadása a hibaablaknak
         *  errorCallbackParams : errorCallback függvényt kapon, akkor annak adhatunk át paramétereket
         *  fn : ez a funkció lesz meghívva a load után
         *  params : ezekkel a paraméterekkel lesz meghívva
         *
         * @param {String|XmlHttpResponse} response
         * @param {object} options
         */
        handleFailure : function(response, options) {
            var resp = response;
            try {
                if (resp) {
                    if (resp.responseText) {
                        resp = _tryDecode(resp.responseText);
                    } else {
                        resp = _tryDecode(resp);
                    }
                }
                response.error = resp.error;
            } catch (e) {
            }
			
            //meg kell vizsgálni a bejelentkezést?
            if (options && options.onLogin === true) {
                if (ResponseHandler.isAuthenticationFailure(resp)) {
                    if(options) {
                      var ol = options.onLogin;
                    } else {
                      var ol = function() {};
                    }
                    //ha függvényt adunk meg az onLoginnak akkor azt jó lenne meghívni a login után...
					//TODO: login képernyő kellene
                    //Login.show(null, ol);
                    return;
                }
            }

            //abort/megszakítás történt
            if(!response || response.status<2) {
                return true;
            }
            var msg  = Ext.MessageBox;

            var error = {};

            var opt = {};
			
            if (!resp || !resp.error) {
              if(options && options.errorParameter) {
                opt = {
                  title   : (options.title?Ext.util.Format.htmlEncode(options.title):this.unexpectError),
                  message : Ext.util.Format.htmlEncode(options.errorParameter)
                };
              } else {
                error = ResponseHandler.errorDecode(response);
                opt = {
                    title   : error.exception,
                    message : error.text
                };
              }
            } else {
                error = resp.error;
                opt = {
                    title   : Ext.util.Format.htmlEncode(error.exception),
                    message : error.text
                };
            }
            if(!error.level) {
              error.level = 'error';
            }
            
        	var has_failure = options instanceof Ext.data.Request && options.scope.failure || options.scope.failure
            if (!has_failure) {
	            msg.show({
	                title   : opt.title || this.errorTitle,
	                msg     : opt.message,
	                buttons : msg.OK,//Ext.window.MessageBox.OK,
	                icon    : msg[error.level.toUpperCase()],
	                cls     :'msgbox-'+error.level,
	                width   : 400,
	                modal	: true
	            });
            }
            if(resp.errorCallback) {
              var errorCallback = new Ext.data.ScriptTagProxy({
                  timeout : 5000,
                  url: resp.errorCallback,
                  nocache: true,
                  method: "post"
              });
              if(options && options.errorCallbackParams) {
                errorCallback.load(options.errorCallbackParams.params, null, options.errorCallbackParams.fn);
              } else {
                errorCallback.load();
              }
            }
        },
        handleClientFailure: function(response,options) {
          var msg  = Ext.MessageBox;
         
          var resp = (response.response?response.response:response);

          try {
              if (resp) {
                  if (resp.responseText) {
                      resp = _tryDecode(resp.responseText);
                  } else {
                      resp = _tryDecode(resp);
                  }
              }
          } catch (e) {
          }
         
          var error = {};

          var opt = {};
         
          //abort/megszakítás történt
          if(!response || !response.response || response.response.status<2) {
            return true;
          }

          if (response) {
            if(options && options.message) {
              opt = {
                title   : (options.title?Ext.util.Format.htmlEncode(options.title):this.unexpectError),
                message : Ext.util.Format.htmlEncode(options.message)
              };
            } else {
              error = ResponseHandler.errorDecode((response.response?response.response:response));
              opt = {
                  title   : (error.title?error.title:this.clientErrorTitle),
                  message : (error.message?error.message:this.clientErrorText)
              };
            }
            if(!error.level) {
              error.level = 'warning';
            }
            msg.show({
                title   : opt.title || this.errorTitle,
                msg     : opt.message,
                buttons : msg.OK,
                icon    : msg[error.level.toUpperCase()],
                cls     :'msgbox-'+error.level,
                width   : 400
            });
            if(resp.errorCallback) {
              var errorCallback = new Ext.data.ScriptTagProxy({
                  timeout : 5000,
                  url: resp.errorCallback,
                  nocache: true,
                  method: "post"
              });
              if(options && options.errorCallbackParams) {
                errorCallback.load(options.errorCallbackParams.params, null, options.errorCallbackParams.fn);
              } else {
                errorCallback.load();
              }
            }
            return true;
          }
          return false;
        },

        errorDecode : function(response)
        {
            var error = response.error || this.isError(response.responseText);

            if (error === null) {
                return {
                    message   : '<b>'
                                + this.unexpectError
                                +'</b><br />-----<br />'+
                                  '<b>'+this.responseStatus+'</b> '+response.status+'<br />'+
                                  '<b>'+this.responseText+'</b><br />'+
                                  Ext.util.Format.stripTags(response.responseText),
                    code      :  -1,
                    level     : 'critical',
                    title     : this.unexpectErrorTitle
                };
            } else {
                if (error.text) {
                    error.title = error.title || this.errorTitle;
                    error.message = error.text;
                    if(!error.level) {
                      error.level = 'critical';
                    }
                }else if (error.level == 'critical') {
                    error.title = error.title || this.unexpectErrorTitle;
                    error.message = '<b>'
                                    +this.unexpectError
                                    +'</b><br />-----<br />'+
                                      '<b>'+this.responseStatus+'</b> '+response.status+'<br />'+
                                      '<b>'+this.responseText+'</b><br />'+
                                    error.message || Ext.util.Format.stripTags(response.responseText);
                } else if (error.fields) {
                    var str = [];
                    for (var i in error.fields) {
                        str.push('<b>'+i+'</b>:<br /> '+error.fields[i].join('<br />'));
                    }
                    error.message += '<br />'+str.join('<br />');
                }

            }

            return error;
        },
        isError : function(source)
        {
            var obj = null;

            try {
                obj = Ext.decode(source);
            } catch (e) {
                return null;
            }

            if (obj && obj.response && obj.response.type === 'error') {
                var sh = obj.response.value;
                return {
                    message     : sh.message,
                    description : sh.description,
                    code        : sh.code,
                    level       : sh.level
                };
            } else if (obj && obj.error) {
                var sh = obj.error;
                return {
                    message     : sh.message?sh.message:sh.text,
                    title       : sh.title,
                    code        : sh.code,
                    type        : sh.type,
                    file        : sh.file,
                    line        : sh.line,
                    level       : sh.level,
                    fields      : sh.fields || null
                };
            }

            return null;
        },
        
        handleFormFailure: function(form, options) {
        	var error = options.response.error;
        	var field_errors = error.kwargs.field_errors;
        	var non_field_errors = error.kwargs.non_field_errors;

        	var formatted_field_errors = {};
        	for (field_name in field_errors) {
        		formatted_field_errors[field_name]=field_errors[field_name].join("\n");
        	}
        	form.markInvalid(formatted_field_errors);

        	var error_box = Ext.MessageBox.show({
                title   : "Feldolgozási hiba",
                msg     : non_field_errors ? "<ul><li>"+non_field_errors.join("</li><li>")+"</li></ul><br />Kérem ellenőrizze az adatokat!" : "Kérem ellenőrizze az adatokat!",
                buttons : Ext.MessageBox.OK,
                icon    : Ext.MessageBox[error.level.toUpperCase()],
                cls     :'msgbox-'+error.level,
                width   : 400
            });
        	if( !non_field_errors ) {
        		setTimeout(function() { error_box.close(); }, 2000);
        	}
        
        }
        
    };


}();



Ext.define('Ext.data.writer.Form', {
    extend: 'Ext.data.writer.Writer',
    alternateClassName: 'Ext.data.FormWriter',
    alias: 'writer.form',
    //inherit docs
    writeRecords: function(request, data) {
        if (data.length != 1) {
        	Ext.Error.raise('Form writer doesn\'t write multiple records');
        }
        data = data[0];
        for (name in data) {
        	request.params[name] = data[name]
        }
        return request
    }
});




Ext.onReady(function() {
	Ext.require([
	             'Ext.ux.form.field.DateTime'
	          ]);
	Ext.require(["Ext.Ajax","Ext.window.MessageBox","Ext.data.Request"], function() {
		Ext.Ajax.on('requestcomplete', function(con, response, options) {
		        var res = ResponseHandler.isFailure(response);
		        if(res && res.success===false) {
		        		console.log(response, options);
		                ResponseHandler.handleFailure(response,options);                                                                                                                                                                                      
		                return false;                                                                                                                                                                                                                         
		        } else {
		        	ResponseHandler.parseData(response);
		        }                                                                                                                                                                                                                                             
		        return true;                                                                                                                                                                                                                                  
		}, this);                                                                                                                                                                                                                                             
		Ext.Ajax.on('requestexception', function(con, response, options) {                                                                                                                                                                                    
		        var res = ResponseHandler.isFailure(response);                                                                                                                                                                                                
		        if(res && res.success===false) {                                                                                                                                                                                                              
		                ResponseHandler.handleFailure(response,options);                                                                                                                                                                                      
		                return false;                                                                                                                                                                                                                         
		        }                                                                                                                                                                                                                                             
		        return true;                                                                                                                                                                                                                                  
		}, this);
	  Ext.Ajax.on("beforerequest", function(conn, xhr, eopts) {
		  function getCookie(name) {
		        var cookieValue = null;
		        if (document.cookie && document.cookie != '') {
		            var cookies = document.cookie.split(';');
		            for (var i = 0; i < cookies.length; i++) {
		                var cookie = Ext.String.trim(cookies[i]);
		                // Does this cookie string begin with the name we want?
		                if (cookie.substring(0, name.length + 1) == (name + '=')) {
		                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
		                    break;
		                }
		            }
		        }
		        return cookieValue;
		    }
		  
		    function sameOrigin(url) {
		        // url could be relative or scheme relative or absolute
		        var host = document.location.host; // host + port
		        var protocol = document.location.protocol;
		        var sr_origin = '//' + host;
		        var origin = protocol + sr_origin;
		        // Allow absolute or scheme relative URLs to same origin
		        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
		            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
		            // or any other URL that isn't scheme relative or absolute i.e relative.
		            !(/^(\/\/|http:|https:).*/.test(url));
		    }
		    
		    function safeMethod(method) {
		        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
		    }
		    if (!safeMethod(xhr.method) && sameOrigin(xhr.url)) {
		        xhr.headers = {
	        		"X-CSRFToken": getCookie('csrftoken')		
		        }
		    }		  
	  });
	});

});
 