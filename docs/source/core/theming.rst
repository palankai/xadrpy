Theming
=======

Theming package provides a solution for theme handling.

Approach
--------

- You can define one or more themes (with layouts and skins). 
- The Theming recognizes these definitions.
- Provides selecting layouts, skins

Installation
------------

.. code-block:: python

	MIDDLEWARE_CLASSES = (
		...
	    'xadrpy.core.theming.middleware.ThemingMiddleware',
	    ...
	)
	
	TEMPLATE_CONTEXT_PROCESSORS = (
		...
		'xadrpy.core.theming.context_processors.theming',
		...
	)
	
	INSTALLED_APPS = (
		...
		'xadrpy.core.theming',
		...
	)

after installed run: 

.. code-block:: bash

	$ python manage.py syncdb

Theme definition
----------------

.. code-block:: python

	THEME = {
		# description elements
		'title': "Title of the theme",
		'description': 'Description of the theme. (Long plain text)',
		'thumbnail': 'relative path in static directory of image - it will be resized',
		'translation': {
			'en': { 							#language code
				'title': "Title of the theme for this language",
				'description': 'Description of the theme. (Long plain text) for this language',
				'thumbnail': 'relative path in static directory of image - it will be resized - for this language'
			},
			'hu': { 							#language code
												#Without title, thumbnail we use the main title
				'description': '', 				#Disable description in this language
			},
		},
		
		# theme elements
		'doctype': ['xhtml','xhtml-strict'], 	#list of doctypes
		'static_path': "", 						#relative path in STATIC directories
		'template_path': "", 					#relative path in TEMPLATES direcories,
		'layouts': ( 							# you can leave blank (or don't give it) if you don't want to define layouts
			("vehicle", { 						#The reference name of the layout
				"title": "",					#you can give description elements - see 
				"file: "",						#template file relative path
				"rewrite": {
												#you can give some rewrites for this layout 					
				   		},
				}),
			),
		'skins':( 								#you can leave empty if you don't want to define skins
			("base", { 							#The reference name of the skin
				"title: "",						#you can give description elements
				"styles": (
					("style.css", {"media": "all"}),
					("style2.css", {"condition": "if IE"}),
				)
				"scripts": [
					"skin-scripts.js",			#relative path for required js files
				],
				"rewrite": {
												#you can give some rewrites for this skin - see layout rewrites
				},
			}),
		),
		'base': "base.html",					#base layout
		"rewrite":{
			"page.html": "my-page.html",		#you can give some redefinitions for templates
			}
		}

Rewrite order:
++++++++++++++

- main rewrite
- layout rewrite
- skin rewrite 

Registering
-----------

.. code-block:: python
	
	# in your xtensions.py
	from xadrpy.theming.libs import theme_store
	
	THEME = {... see above ...}
	
	theme_store.register(THEME)

Using
-----
You can reference the selected layout: "${theming:layout}"

.. code-block:: html
	
	{% extends "${theming:layout}" %}
	...
	
or

.. code-block:: python
	
	render_to_response("${theming:layout}", ...)
	...

but the best solution: define a base.html in your template root and it containts just one line: {% extends "${theming:layout}" %}. You can use proper "base.html".