from xadrpy.auth.base import permissions

permissions.register("admin_reset_password", u"Reset someone user password")
permissions.register("admin_add_user", u"Can add new user")
permissions.register("admin_edit_user", u"Can edit user")
permissions.register("admin_delete_user", u"Can delete user")
permissions.register("admin_grant", u"Can modify grants")
