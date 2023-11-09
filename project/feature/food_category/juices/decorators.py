from functools import wraps
from .error_handler import JuiceNotFound
from project.model.juices import Juice
def validate_juice_existence(func):
    @wraps(func)
    def juices(juice_id):
        juice = Juice.query.get(juice_id)
        if juice is None:
            raise JuiceNotFound()
        return func(juice_id)
    return juices