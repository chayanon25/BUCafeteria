from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy import String, Text, Enum, DateTime, DECIMAL, Integer, ForeignKey
from datetime import datetime
import uuid

from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from database import DATABASE_URL

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(Enum("user", "admin", name="user_roles"), default="user", nullable=False)
    created_at: Mapped[str] = mapped_column(String(20), default=datetime.now().strftime("%Y-%M-%d %H-%M-%S"))

    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="user")


class Categories(Base):
    __tablename__ = "categories"

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    menu_items: Mapped[list["MenuItems"]] = relationship("MenuItems", back_populates="category")


class Locations(Base):
    __tablename__ = "locations"

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    restaurants: Mapped[list["Restaurants"]] = relationship("Restaurants", back_populates="location")


class Restaurants(Base):
    __tablename__ = "restaurants"

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text)
    location_id: Mapped[str] = mapped_column(CHAR(36), ForeignKey("locations.id"), nullable=False)
    opening_hours: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(50))
    image_url: Mapped[str] = mapped_column(String(255))

    location: Mapped["Locations"] = relationship("Locations", back_populates="restaurants")
    menu_items: Mapped[list["MenuItems"]] = relationship("MenuItems", back_populates="restaurant")
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="restaurant")


class MenuItems(Base):
    __tablename__ = "menu_items"

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    restaurant_id: Mapped[str] = mapped_column(CHAR(36), ForeignKey("restaurants.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text)
    category_id: Mapped[str] = mapped_column(CHAR(36), ForeignKey("categories.id"))
    price: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=False)
    image_url: Mapped[str] = mapped_column(String(255))

    category: Mapped["Categories"] = relationship("Categories", back_populates="menu_items")
    restaurant: Mapped["Restaurants"] = relationship("Restaurants", back_populates="menu_items")


class Review(Base):
    __tablename__ = "review"

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    restaurant_id: Mapped[str] = mapped_column(CHAR(36), ForeignKey("restaurants.id"), nullable=False)
    user_id: Mapped[str] = mapped_column(CHAR(36), ForeignKey("users.id"), nullable=False)
    rating: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now().strftime("%Y-%M-%d %H-%M-%S"))

    restaurant: Mapped["Restaurants"] = relationship("Restaurants", back_populates="reviews")
    user: Mapped["Users"] = relationship("Users", back_populates="reviews")
    
    
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
 
 
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
 
 
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
 