from django.conf import settings
from django.core.management.base import CommandError
from django.utils.translation import ugettext as _


def test_is_application_installed(app_name):
    if not app_name in settings.INSTALLED_APPS:
        raise CommandError(_("The '%(app_name)s' app is listed in settings.INSTALLED_APPS") % {"app_name":app_name} )

