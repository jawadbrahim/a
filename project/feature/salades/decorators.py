from functools import wraps
from .error_handler import SaladeNotFound
from .model import Salade
def validate_salade_existence(func):
    @wraps(func)
    def salades(salade_id):
        salade = Salade.query.get(salade_id)
        if salade is None:
            raise SaladeNotFound()
        return func(salade_id)
    return salades