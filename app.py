from collections.abc import AsyncGenerator
import uuid
from datetime import datetime
 
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Text, Boolean, DateTime, Column, Enum
 
import os
from dotenv import load_dotenv
 
load_dotenv()
 
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_HOST = os.getenv("MYSQL_HOST")
DB_NAME = os.getenv("MYSQL_DB")
 
DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
 
class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "users"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum("user","admin", name="user_roles"), default="user", nullable=False)
    created_at_str = user.created_at.strftime("%Y-%m-%d %H:%M:%S")

class Categories(Base):
    __tablename__ = "categories"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), unique=True, nullable=False)

class Locations(Base):
    __tablename__ = "locations"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)

class Restaurants(Base):
    __tablename__ = "restaurants"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    category_id = Column(CHAR(36), ForeignKey("categories.id"))
    location_id = Column(CHAR(36), ForeignKey("locations.id") nullable=False)
    opening_hours = Column(String(100))
    phone = Column(String(50))
    image_url = Column(String(255))

class Menu_items(Base):
    __tablename__ = "menu_items"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    restaurants_id = Column(CHAR(36), ForeignKey="restaurants.id" nullable=False)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    price = Column(DECIMAL(10, 2) nullable=False)
    image_url = Column(String(255))

class Review(Base):
    __tablename__ = "review"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    restaurants_id = Column(CHAR(36), ForeignKey="restaurants.id" nullable=False)
    user_id = Column(CHAR(36), ForeignKey="users.id" nullable=False)
    rating = Column(Integer)
    comment = Column(Text)
    created_at_str = user.created_at.strftime("%Y-%m-%d %H:%M:%S")
