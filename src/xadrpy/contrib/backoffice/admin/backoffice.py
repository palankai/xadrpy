from django.conf import settings

NAMESPACES = {
    "backoffice.admin": settings.STATIC_URL+"xadrpy/backoffice.admin"
}

CONTROLLERS = (
    'backoffice.admin.controller.UsersController',
    'backoffice.admin.controller.GroupsController',
    'backoffice.admin.Module',
)

