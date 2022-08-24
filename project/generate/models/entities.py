from pydantic import BaseModel


class Country(BaseModel):
    name: str


class Category(BaseModel):
    id: int | None
    title: str
    link: str


class Product(BaseModel):
    name: str
    category: Category
    country: Country
    price: str
    link: str
    photo: str

