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
    "templates": [],
    "styles": [],
    "libs": [],
    "scripts": [],
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
    "name": None,
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

BASE_THEME_TRANSLATION = {
    "title": None,
    "description": None,
    "thumbnail": None
}

THEME_LOADERS = getattr(settings, "THEME_LOADERS", ("xadrpy.contrib.themes.loaders.StaticThemeLoader",))

DEFAULT_THEME = getattr(settings, "DEFAULT_THEME", "regeneracy")
DEFAULT_LIBRARIES = getattr(settings, "DEFAULT_LIBRARIES", [])


THEMES = (
    {"name": 'html5', "type": "xadrpy", "layouts": ["index.html"], "styles": ["style.css", "xreset.css"], "libs": ["x-all"] },
    {"name": "offrecord", "type": "xadrpy" },
    {"name": "regeneracy", "type": "xadrpy" },
    {"name": 'lazybreeze', "type": "xadrpy", "layouts": ["index.html"], "skins": ["style.css"]}
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
