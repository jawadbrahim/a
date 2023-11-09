from functools import wraps
from .error_handler import SweetNotFound
from project.model.sweets import Sweet
def validate_sweet_existence(func):
    @wraps(func)
    def sweets(sweet_id):
        sweet = Sweet.query.get(sweet_id)
        if sweet is None:
            raise SweetNotFound()
        return func(sweet_id)
    return sweets