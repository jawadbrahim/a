from functools import wraps
from .error_handler import EuropeanfoodNotFound
from project.model.europeanfoods import Europeanfood
def validate_europeanfood_existence(func):
    @wraps(func)
    def europeanfoods(europeanfood_id):
        europeanfood = Europeanfood.query.get(europeanfood_id)
        if europeanfood is None:
            raise EuropeanfoodNotFound()
        return func(europeanfood_id)
    return europeanfoods