from functools import wraps
from .error_handler import SauceNotFound
from .model import Sauce
def validate_sauce_existence(func):
    @wraps(func)
    def sauces(sauce_id):
        sauce = Sauce.query.get(sauce_id)
        if sauce is None:
            raise SauceNotFound()
        return func(sauce_id)
    return sauces