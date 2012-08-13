from xadrpy.core.access.base import rights

rights.register("admin_reset_password", u"Reset someone user password")
rights.register("admin_add_user", u"Can add new user")
rights.register("admin_edit_user", u"Can edit user")
rights.register("admin_delete_user", u"Can delete user")
rights.register("admin_grant", u"Can modify grants")
