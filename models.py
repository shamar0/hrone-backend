from pydantic import BaseModel

from typing import List

class Size(BaseModel):
    size: str
    quantity: int

class Product(BaseModel):
    name: str
    price: float
    sizes: List[Size]

class ProductDetails(BaseModel):
    name: str
    id: str

class Items(BaseModel):
    productDetails: ProductDetails
    qty: int

class Order(BaseModel):
    userId: str
    items: List[Items]
    total: float

class ItemsReq(BaseModel):
    productId: str
    qty: int

class OrderReq(BaseModel):
    userId: str
    items: List[ItemsReq]