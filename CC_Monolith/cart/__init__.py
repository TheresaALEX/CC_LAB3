import json
from products import Product
from cart import dao


class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @classmethod
    def load(cls, data):
        return cls(data['id'], data['username'], data['contents'], data['cost'])


def get_cart(username: str) -> list:
    cart_details = dao.get_cart(username)
   
    if not cart_details:
        return []

    items = []
    for cart_detail in cart_details:
        try:
            contents = json.loads(cart_detail['contents'])  # Safe parsing of contents
            items.extend(contents)  # Directly extend items with contents from the cart detail
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error decoding contents: {e}")
            continue

    # Remove duplicates by using a set and fetch products in one go
    product_ids = set(items)
    products_info = [products.get_product(product_id) for product_id in product_ids]

    return products_info


def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    dao.delete_cart(username)