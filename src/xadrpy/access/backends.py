from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        try:
            for user in User.objects.filter(email=username):
                if user.check_password(password):
                    return user
        except User.DoesNotExist:
            pass
        return None

class UserBackend(ModelBackend):
    def authenticate(self, user_id=None, user=None ):
        if user:
            return user
        if not user_id:
            return None
        return self.get_user(user_id)
