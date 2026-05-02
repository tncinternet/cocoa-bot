def selling_price(price, diff, fx):
    return (price - diff) * fx

def price_change(current, previous, fx):
    delta = current - previous
    return delta * fx, delta