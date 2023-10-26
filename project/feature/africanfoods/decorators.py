from functools import wraps
from .error_handler import AfricanfoodNotFound
from .model import Africanfood
def validate_africanfood_existence(func):
    @wraps(func)
    def africanfoods(africanfood_id):
        africanfood = Africanfood.query.get(africanfood_id)
        if africanfood is None:
            raise AfricanfoodNotFound()
        return func(africanfood_id)
    return africanfoods