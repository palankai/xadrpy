from models import Route
import hashlib

__all__ = ['update_signatures']

def update_signatures():
    for route in Route.objects.all():
        route.signature = hashlib.md5(route.get_signature()).hexdigest()
        route.save()