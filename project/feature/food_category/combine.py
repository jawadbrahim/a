
from .pydantic_models import FoodPydantic, CategoryPydantic
from .data_classes import FoodDataclass, CategoryDataclass
from dataclasses import asdict

class PydanticToDataclassConverter:
    @staticmethod
    def food_pydantic_to_dataclass(pydantic_instance: FoodPydantic) -> FoodDataclass:
        return FoodDataclass(**pydantic_instance.dict())

    @staticmethod
    def category_pydantic_to_dataclass(pydantic_instance: CategoryPydantic) -> CategoryDataclass:
        return CategoryDataclass(**pydantic_instance.dict())

class DataclassToPydanticConverter:
    @staticmethod
    def food_dataclass_to_pydantic(dataclass_instance: FoodDataclass) -> FoodPydantic:
        return FoodPydantic(**asdict(dataclass_instance))

    @staticmethod
    def category_dataclass_to_pydantic(dataclass_instance: CategoryDataclass) -> CategoryPydantic:
        return CategoryPydantic(**asdict(dataclass_instance))
