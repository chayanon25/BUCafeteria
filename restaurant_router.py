from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from schemas import RestaurantCreate, RestaurantBase, RestaurantOut
from models import get_async_session, Restaurants, Locations


router = APIRouter(prefix="/restaurant", tags=["restaurant"])

@router.post("/")
async def createRestaurant(
  create_restaurant: RestaurantCreate,
  session: AsyncSession = Depends(get_async_session)):
  name = create_restaurant.name
  description = create_restaurant.description
  image_url = create_restaurant.image_url
  location = create_restaurant.location
  
  location_id = await get_or_create_location(location, session)
  
  opening_hours = create_restaurant.opening_hours
  phone = create_restaurant.phone
  
  new_restaurants = Restaurants(
    name=name,
    description=description,
    image_url=image_url,
    location_id=location_id,
    opening_hours=opening_hours,
    phone=phone
  )
  session.add(new_restaurants)
  await session.flush()
  
  await session.commit()
  return {"restaurant": "Restaurant created"}

@router.get("/")
async def getRestaurants(session: AsyncSession = Depends(get_async_session)):
  
  result = await session.execute(select(Restaurants))
  
  restaurants = result.scalars().all()

  return restaurants

async def get_or_create_location(name: str, session: AsyncSession):
  result = await session.execute(select(Locations).where(Locations.name == name))
  location = result.scalar_one_or_none()
  if not location:
    location = Locations(name=name)
    session.add(location)
    await session.flush()
  return location.id