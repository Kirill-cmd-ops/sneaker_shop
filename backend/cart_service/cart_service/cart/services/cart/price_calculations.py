def calculate_total_price(items) -> float:
    total_price = 0
    for cart_association in items.sneaker_associations:
        total_price += cart_association.sneaker.price * cart_association.quantity
    return total_price
