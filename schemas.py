from pydantic import BaseModel
from typing import Optional

# Location
class LocationBase(BaseModel):
  name: str
  description: Optional[str]

class LocationCreate(LocationBase):
  pass

class LocationOut(LocationBase):
  id: str

  class Config:
    orm_mode = True

# Restaurant
class RestaurantBase(BaseModel):
  name: str
  description: Optional[str]
  image_url: Optional[str]

class RestaurantCreate(RestaurantBase):
  location_id: Optional[str] = None
  new_location: Optional[LocationCreate] = None

  opening_hours: Optional[str] = None
  phone: Optional[str] = None

class RestaurantOut(RestaurantBase):
  id: str
  location: LocationOut

  class Config:
    orm_mode = True

#Category
class CategoryBase(BaseModel):
  name: str

class CategoryCreate(CategoryBase):
  pass

class CategoryOut(CategoryBase):
  id: str
  class Config:
    orm_mode = True

#Menu
class MenuBase(BaseModel):
  name: str
  price: float
  description: Optional[str]
  image_url: Optional[str]

class MenuCreate(MenuBase):
  restaurant_id: str
  category_id: Optional[str] = None
  new_category: Optional[CategoryCreate] = None

class MenuOut(MenuBase):
  id: str
  restaurant_id: str
  category: CategoryOut

  class Config:
    orm_mode = True