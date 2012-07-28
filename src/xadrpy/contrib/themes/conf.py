from django.conf import settings

BASE_CONFIG = {
    "name": None,
    "type": None,
}

BASE_THEME = {
    "name": None,
    "type": None,
    "doctype": ["HTML5"],
    "thumbnail": None,
    "title": None,
    "description": None,
    "translated": {},
    "features": [],
    "layouts": [],
    "skins": [],
    "templates": {},
    "media": {},
    "styles": [],
    "scripts": [],
    "libs": [],
    "supported": [],
}

BASE_LAYOUT = {
    "name": None,
    "source": None,
    "title": None,
    "description": None,
    "thumbnail": None,
    "styles": [],
    "scripts": [],
    "libs": [],
    "translated": {}
}

BASE_SKIN = {
    "name": None,
    "source": None,
    "title": None,
    "description": None,
    "thumbnail": None,
    "translated": {}
}

BASE_TEMPLATE = {
    "source": None,
    "title": None,
    "description": None,
    "thumbnail": None,
    "translated": {}
}

BASE_MEDIA = {
    "source": None,
    "title": None,
    "description": None,
    "thumbnail": None,
    "translated": {}
}


BASE_LIBRARY = {
    "name": None,
    "type": None,
    "title": None,
    "description": None,
    "version": None,
    "thumbnail": None,
    "scripts": [],
    "styles": [],
    "translated": {},
    "autoload": False,
}

BASE_FILES = { 'html': [], 'style': [], 'script': [], 'media': [] }

BASE_FILE = {
    "name": None,
    "file_name": None,
    "file": None,
    "files": [],
    "files_tripple": [None,None,None],
    "base_file": None,
    "middle_file": None,
    "top_file": None,
    "required": True,
}

BASE_FILE_DEFAULTS = {
    'html': BASE_FILE,
    'style': dict(BASE_FILE,**{ "media": None, }),
    'script': BASE_FILE,
    'media': BASE_FILE,
}


BASE_THEME_TRANSLATION = {
    "title": None,
    "description": None,
    "thumbnail": None
}

THEME_LOADERS = getattr(settings, "THEME_LOADERS", ("xadrpy.contrib.themes.loaders.StaticThemeLoader",))

DEFAULT_THEME = getattr(settings, "DEFAULT_THEME", "sparkling")
DEFAULT_LIBRARIES = getattr(settings, "DEFAULT_LIBRARIES", [])


THEMES = (
#    {"name": 'html5', "type": "xadrpy", "layouts": ["index.html"], "styles": ["style.css", "xreset.css"], "libs": ["x-all"] },
#    {"name": "offrecord", "type": "xadrpy" },
#    {"name": "regeneracy", "type": "xadrpy" },
#    {"name": 'lazybreeze', "type": "xadrpy", "layouts": ["index.html"], "skins": ["style.css"]},
    {"name": 'sparkling', 
        "type": "xadrpy", 
        "doctype": ["xhtml", "xhtml-strict"],
        "supported": ["pages", "blogs"],
        "layouts": ["index.html"], 
        "skins": ["style.css"], 
        "styles": ["style.css"], 
        "libs": ["x-all"],
        "templates": {
            "base": "base",
            "page": "page",
            "column": "column",
            "entry_excerpt": "entry_excerpt",
            "entry": "entry",
        },
        "media": {
            "favicon": "favicon",
        },
        "files": {
            "html": [
                {"name": "base", "file_name": "base.html", },
                {"name": "page", "file_name": "page.html", },
                {"name": "column", "file_name": "column.html", },
                {"name": "entry", "file_name": "entry.html", },
                {"name": "entry_list", "file_name": "entry_list.html", },
                {"name": "entry_excerpt", "file_name": "includes/entry_excerpt.html", },
                {"name": "sidebar", "file_name": "includes/sidebar.html", },
                {"name": "mainmenu", "file_name": "includes/mainmenu.html", },
                {"name": "head", "file_name": "includes/head.html", },
                {"name": "footer", "file_name": "includes/footer.html", },
            ],
            "style": [
                {"name": "style", "file_name": "style.css", },
            ],
            "script": [
                {"name": "script", "file_name": "test.js", },
            ],
            "media": [
                {"name": "pic", "file_name": "images/img01.jpg", },
                {"name": "favicon", "file_name": ["favicon.png","favicon.gif","favicon.ico"], "required": False},
                {"name": "apple_touch_icon", "file_name": ["apple-touch-icon.png","apple-touch-icon.jpg","apple-touch-icon.gif"], "required": False},
            ]
        }
    },
)

LIBRARIES = (
    {"name": "x-all", 
     "type": "xadrpy", 
     "scripts": ["modernizr-2.0.6.min.js", "jquery.min.js", "jquery-ui/jquery-ui.full.min.js", 
                 "plugins.js", "jquery.cookie.js", "jquery.form.js", "jquery.metadata.js",
                 "json2.js", "hoverIntent.js", "jquery.bgiframe.min.js", "superfish/superfish.js",
                 "superfish/supersubs.js", "superfish/init.js"], 
     "styles": ["jquery-ui/css/ui-lightness/jquery-ui.full.css", "superfish/css/superfish.css"],
     "autoload": False},
)

META_HANDLER = "xadrpy.contrib.themes.libs.ThemeMetaHandler"
