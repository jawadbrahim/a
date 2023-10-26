from functools import wraps
from .error_handler import IcecreamNotFound
from .model import Icecream
def validate_icecream_existence(func):
    @wraps(func)
    def icecreams(icecream_id):
        icecream = Icecream.query.get(icecream_id)
        if icecream is None:
            raise IcecreamNotFound()
        return func(icecream_id)
    return icecreams