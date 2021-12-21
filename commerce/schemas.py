import datetime

from ninja import Schema
from pydantic import UUID4

class prodectImage(Schema):
    image: str
    is_default_image: bool
class CategoryOut(Schema):
    id: UUID4
    name: str
    description: str
    image: str


class LabelOut(Schema):
    id: UUID4
    name: str


class ProductOut(Schema):
    id: UUID4
    is_featured: bool
    name: str
    description: str
    size: str
    qty: int
    price: int
    discounted_price: int
    category: CategoryOut = None
    label: LabelOut =None
    created: datetime.datetime
    updated: datetime.datetime
    images: list[prodectImage]



class ProductCreate(Schema):
    is_featured: bool
    name: str
    description: str
    size: str
    qty: int
    cost: int
    price: int
    discounted_price: int
    category_id: UUID4
    label_id: UUID4


class AddToCartPayload(Schema):
    product_id: UUID4
    qty: int



