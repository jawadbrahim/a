from functools import wraps
from .error_handler import AsianfoodNotFound
from .model import Asianfood
def validate_asianfood_existence(func):
    @wraps(func)
    def asianfoods(asianfood_id):
        asianfood = Asianfood.query.get(asianfood_id)
        if asianfood is None:
            raise AsianfoodNotFound()
        return func(asianfood_id)
    return asianfoods