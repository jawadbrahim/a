from functools import wraps
from .error_handler import ArabicfoodNotFound
from project.model.arabicfoods import Arabicfood
def validate_arabicfood_existence(func):
    @wraps(func)
    def arabicfoods(arabicfood_id):
        arabicfood = Arabicfood.query.get(arabicfood_id)
        if arabicfood is None:
            raise ArabicfoodNotFound()
        return func(arabicfood_id)
    return arabicfoods