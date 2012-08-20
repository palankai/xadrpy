Theming
=======

Theming package provides a solution for theme handling.

Approach
--------

- You can define one or more themes (with layouts and skins). 
- The Theming recognizes these definitions.
- Provides selecting layouts, skins

Background
++++++++++

You can reference the layout with '@layout_name' formula. The `Loader` resolve '@layout_name' and ensure proper layout html file.
The context processor set `theming_layout` variable to base / selected layout. 

Installation
------------

.. code-block:: python

	TEMPLATE_LOADERS = (
		'xadrpy.core.theming.loaders.Loader', #Be the first
		...
	)

	TEMPLATE_CONTEXT_PROCESSORS = (
		...
		'xadrpy.core.theming.context_processors.theming',
		...
	)
	
	INSTALLED_APPS = (
		...
		'xadrpy',
		...
		'xadrpy.core.theming',
		...
	)


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
					{"file": "style.css", "media": "all"},
					{"file": "style2.css", "condition": "if IE"},
				)
				"scripts": (
					"skin-scripts.js",			#relative path for required js files
				),
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
The context processor set the selected (with route/page...) layout to `theming_layout` context var. You can redefine it from your views. 

.. code-block:: html
	
	{% extends "theming_layout" %}
	...

.. code-block:: html

	{% extends "@layout_name" %}
	...
	
or

.. code-block:: python
	
	render_to_response("@layout_name", ...)
	...

but the best solution: define a base.html in your template root and it contains just one line: {% extends "theming_layout" %}. You can use proper "base.html".