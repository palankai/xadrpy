from exceptions import AuthenticationError

def permission(func=None,required=[]):
    def inner(func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated():
                raise AuthenticationError()
            return func(request, *args, **kwargs)
    if func:
        return inner(func)
    else:
        return inner
