from pydantic import BaseModel, validator
from typing import Optional
class CategoryPydantic(BaseModel):
    id: int
    title: str

class FoodPydantic(BaseModel):
    id: Optional[int] =None
    title: str
    description: str
    picture: str
    ingredients: str
    category: CategoryPydantic = None  

    @validator('category', pre=True, always=True)
    def validate_category(cls, value):
        if isinstance(value, dict):
            return CategoryPydantic(**value)
        return value