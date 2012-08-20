from django.conf import settings

SELECTED_THEME = getattr(settings, "SELECTED_THEME", None)
STATIC_URL = getattr(settings, "STATIC_URL")

_SIMPLE_STYLE_TAG = '<link rel="stylesheet" type="text/css" href="'+STATIC_URL+'%(file)s" />'
_MEDIA_STYLE_TAG = '<link rel="stylesheet" type="text/css" href="'+STATIC_URL+'%(file)s" media="%(media)s" />'

_CONDITION = "<!--[%s]>%s<![endif]-->"

_SCRIPT_TAG = '<script type="text/javascript" src="'+STATIC_URL+'%s"></script>'