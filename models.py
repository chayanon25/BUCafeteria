from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy import String, Text, Enum, DateTime, DECIMAL, Integer, ForeignKey
from datetime import datetime
import uuid

from database import engine

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(Enum("user", "admin", name="user_roles"), default="user", nullable=False)
    created_at: Mapped[str] = mapped_column(str, default=datetime.now().strftime("%Y-%M-%d %H-%M-%S"))

    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="user")


class Categories(Base):
    __tablename__ = "categories"

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    restaurants: Mapped[list["Restaurants"]] = relationship("Restaurants", back_populates="category")


class Locations(Base):
    __tablename__ = "locations"

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text)

    restaurants: Mapped[list["Restaurants"]] = relationship("Restaurants", back_populates="location")


class Restaurants(Base):
    __tablename__ = "restaurants"

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text)
    category_id: Mapped[str] = mapped_column(CHAR(36), ForeignKey("categories.id"))
    location_id: Mapped[str] = mapped_column(CHAR(36), ForeignKey("locations.id"), nullable=False)
    opening_hours: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(50))
    image_url: Mapped[str] = mapped_column(String(255))

    category: Mapped["Categories"] = relationship("Categories", back_populates="restaurants")
    location: Mapped["Locations"] = relationship("Locations", back_populates="restaurants")
    menu_items: Mapped[list["MenuItems"]] = relationship("MenuItems", back_populates="restaurant")
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="restaurant")


class MenuItems(Base):
    __tablename__ = "menu_items"

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    restaurant_id: Mapped[str] = mapped_column(CHAR(36), ForeignKey("restaurants.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=False)
    image_url: Mapped[str] = mapped_column(String(255))

    restaurant: Mapped["Restaurants"] = relationship("Restaurants", back_populates="menu_items")


class Review(Base):
    __tablename__ = "review"

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    restaurant_id: Mapped[str] = mapped_column(CHAR(36), ForeignKey("restaurants.id"), nullable=False)
    user_id: Mapped[str] = mapped_column(CHAR(36), ForeignKey("users.id"), nullable=False)
    rating: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now().strftime("%Y-%M-%d %H-%M-%S")

    restaurant: Mapped["Restaurants"] = relationship("Restaurants", back_populates="reviews")
    user: Mapped["Users"] = relationship("Users", back_populates="reviews")