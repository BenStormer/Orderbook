"""
TODO:
- Create Exchange with all orderbooks
    - init with all orderbooks
    - Function for printing exchange
- Create order class
    - init with ID, price, buy/sell side, quantity, time placed, market/limit
    - Function for printing (__str__)
"""
from datetime import datetime, timezone

# Work on smallest part to largest
class Order:
    """
    Represents a singular order.

    Args:
        buy (bool): Represents a buy (True) or sell (False) order
        quantity (int): The number of stocks to buy/sell
        price (Optional[float | int]): The price of the order placed
    """
    id = 1
    def __init__(self, buy: bool, quantity: int, price: float|int|None=None):
        """
        Constructs an order.

        Args:
            buy (bool): Represents a buy (True) or sell (False) order
            quantity (int): The number of stocks to buy/sell
            price (Optional[float | int]): The price of the order placed
        """
        self.id = Order.id
        self.buy = buy
        self.quantity = quantity
        self.price = price
        self.market = True if price else False # False = limit order
        self.time = datetime.now(timezone.utc)
        Order.id += 1

    def __str__(self) -> str:
        """
        Constructs a readable printout of the order.
        """
        return (f"Order {self.id} placed at "
                f"{self.time.strftime('%H:%M:%S, %B %d %Y')}:\n"
                f"\t{'Buy' if self.buy else 'Sell'} {self.quantity} at "
                f"{f'${self.price:.2f}' if self.price else 'market price'}")

    def compact_str(self) -> str:
        """
        Constructs a compact printout of the order.
        """
        return (f"Order: {self.id:>5} | "
                f"{'Buy' if self.buy else 'Sell':>4} | "
                f"{self.quantity:>4} | "
                f"{f'${self.price:.2f}' if self.price else 'market price':>12} | "
                f"{self.time.strftime('%H:%M:%S, %m/%d/%y')}")

"""
- Create Orderbook class
    - init with ticker and list of orders (list of dicts)
        - should also have a hash for mapping order id to index
    - Should track the best ask and best bid (pointers to index)
    - Function for placing an order
        - Should execute order if possible, or place in queue based on price
    - Function for updating pointers (called when order is executed or cancelled)
    - Function for cancelling orders
        - Use order id to index map to figure out where to delete
    - Function for printing out the orderbook
"""


def main():
    test_order = Order(True, 50, 370)
    test_order2 = Order(False, 2)
    print(test_order.compact_str())
    print(test_order2.compact_str())

main()
