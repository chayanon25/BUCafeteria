from pydantic import BaseModel
from typing import Optional

# Location
class LocationBase(BaseModel):
  name: str

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
  location: str
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

#Review

class ReviewBase(BaseModel):
  rating: int
  comment: Optional[str]

class ReviewCreate(ReviewBase):
  restaurant_id: str
  user_id: str

class ReviewOut(ReviewBase):
  id: str
  user_id: str
  restaurant_id: str
  created_at: str

  class Config:
    orm_mode = True

#User
class UserBase(BaseModel):
    username: str
    role: Optional[str] = "user"

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: str

    class Config:
        orm_mode = True