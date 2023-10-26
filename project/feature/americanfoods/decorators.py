from functools import wraps
from .error_handler import AmericanfoodNotFound
from .model import Americanfood
def validate_americanfood_existence(func):
    @wraps(func)
    def americanfoods(americanfood_id):
        americanfood =Americanfood.query.get(americanfood_id)
        if americanfood is None:
            raise AmericanfoodNotFound()
        return func(americanfood_id)
    return americanfoods