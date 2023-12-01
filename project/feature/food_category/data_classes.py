from dataclasses import dataclass
from typing import Optional

@dataclass
class CategoryDataclass:
    id: int
    title: str

@dataclass
class FoodDataclass:
    id: Optional[int]
    title: str
    description: str
    picture: str
    ingredients: str
    category: Optional[CategoryDataclass] = None
