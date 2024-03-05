from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float
    tax: float = None


h = dict(name="Foo", price=50.2, tax=20.2, hi="The Foo Wrestlers", ri="hi")
item = Item(**h)
print(item)
