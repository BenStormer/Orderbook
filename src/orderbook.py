"""
ADDITIONAL IMPROVEMENTS:
- Create system for logging all transactions that have occurred

TODO:
- Create Exchange with all orderbooks
    - init with all orderbooks
    - Function for printing exchange
- Create order class
    - init with ID, price, buy/sell side, quantity, time placed, market/limit
    - Function for printing (__str__)
"""
from datetime import datetime, timezone
import time

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
        self.price = price if price else -1 # -1 = market order
        self.time = datetime.now(timezone.utc)
        Order.id += 1

    def __str__(self) -> str:
        """
        Constructs a readable printout of the order.
        """
        return (f"Order {self.id} placed at "
                f"{self.time.strftime('%H:%M:%S, %B %d %Y')}:\n"
                f"\t{'Buy' if self.buy else 'Sell'} {self.quantity} at "
                f"{'market price' if self.price == -1 else f'${self.price:.2f}'}")

    def compact_str(self) -> str:
        """
        Constructs a compact printout of the order.
        """
        return (f"| Order: {self.id:>5} | "
                f"{'Buy' if self.buy else 'Sell':>4} | "
                f"{self.quantity:>8} | "
                f"{f'market price' if self.price == -1 else f'${self.price:.2f}':>12} | "
                f"{self.time.strftime('%H:%M:%S, %m/%d/%y')} |")

"""
- Create Orderbook class
    - Function for cancelling orders
        - Use order id to index map to figure out where to delete
"""
class Orderbook:
    """
    Represents all orders for a stock.
    
    Args:
        ticker (str): Ticker for a given stock
    """
    def __init__(self, ticker: str):
        """
        Constructs an orderbook for a given stock.

        Args:
            ticker (str): Ticker for a given stock
        """
        self.ticker = ticker
        self.bids = [] # List of bids sorted by price from high to low
        self.asks = [] # List of asks sorted by price from low to high


    def __str__(self):
        string = f"{self.ticker:^70}\n"
        string += '-'*70 + '\n'
        string += (f"| {'Order ID':^12} | "
                   f"{'Side':^4} | "
                   f"{'Quantity':^8} | "
                   f"{'Price Type':^12} | "
                   f"{'Time Placed':^18} |") + '\n'
        string += '-'*70 + '\n'
        if self.bids:
            for bid in self.bids:
                string += bid.compact_str() + '\n'
        if self.asks:
            for ask in self.asks:
                string += ask.compact_str() + '\n'
        string += '-'*70 + '\n'
        num_bids = len(self.bids)
        num_asks = len(self.asks)
        string += (f"BIDS: {num_bids}, "
                   f"ASKS: {num_asks}, "
                   f"TOTAL: {num_bids + num_asks}\n")
        return string


    def get_price(self, order: Order, index: int) -> int:
        """
        Gets the price listed for an index in the orderbook.

        Args:
            buy (bool): Represents a buy (True) or sell (False) order
            index (int): The index of interest in the orderbook

        Returns:
            price (int): Numerical value of price or -1 denoting market price
        """
        if self.buy:
            return self.bids[index].price
        else:
            return self.asks[index].price


    def place_order(self, order: Order):
        """
        Places an order and executes (if possible) or queues it.

        Args:
            order (Order): Order to be placed
        """
        self.buy_order(order) if order.buy else self.sell_order(order)


    def queue_order(self, order):
        """
        Queue an order into the orderbook.

        Args:
            order (Order): The ordered to be queued
        """
        if order.buy:
            if len(self.bids) == 0 or order.price == -1:
                self.bids.append(order)
            else:
                insert_index = 0
                last_index = len(self.bids) - 1
                while order.price < self.bids[insert_index].price:
                    insert_index += 1
                    if insert_index > last_index:
                        break
                self.bids.insert(insert_index - 1, order)
        else:
            if len(self.asks) == 0 or order.price == 1:
                self.asks.append(order)
            else:
                insert_index = 0
                last_index = len(self.asks) - 1
                while order.price > self.asks[insert_index].price:
                    insert_index += 1
                    if insert_index > last_index:
                        break
                self.asks.insert(insert_index - 1, order)


    def buy_order(self, order: Order):
        """
        Purchase stock(s) at market price.

        Args:
            order (Order): The buy order
        """
        while order.quantity > 0 and self.asks:
            # Limit order
            if order.price != -1 and self.asks[0].price > order.price:
                self.queue(order)
                return
            ask_quantity = self.asks[0].quantity
            if order.quantity < ask_quantity:
                self.asks[0].quantity -= order.quantity
                return
            elif order.quantity == ask_quantity:
                del self.asks[0]
                return
            else:
                # Check if only market orders remain
                if self.asks[0].price == -1 and order.price == -1:
                    self.queue_order(order)
                    return
                order.quantity -= ask_quantity
                del self.asks[0]
        self.queue_order(order)


    def sell_order(self, order: Order):
        """
        Sell stock(s) at market price.

        Args:
            order (Order): The sell order
        """
        while order.quantity > 0 and self.bids:
            # No bids are high enough to sell to
            if order.price != -1 and self.bids[0].price < order.price:
                self.queue(order)
                return
            bid_quantity = self.bids[0].quantity
            if order.quantity < bid_quantity:
                self.bids[0].quantity -= order.quantity
                return
            elif order.quantity == bid_quantity:
                del self.bids[0]
                return
            else:
                # Check if only market orders remain
                if self.bids[0].price == -1 and order.price == -1:
                    self.queue_order(order)
                    return
                order.quantity -= bid_quantity
                del self.bids[0]
        self.queue_order(order)


def main():
    print()
    test_order = Order(buy=True, quantity=50, price=370)
    test_order2 = Order(buy=True, quantity=2, price=380)
    test_order3 = Order(buy=True, quantity=4)
    test_order4 = Order(buy=False, quantity=70)
    AAPL = Orderbook("AAPL")
    AAPL.place_order(test_order)
    AAPL.place_order(test_order2)
    AAPL.place_order(test_order3)
    AAPL.place_order(test_order4)
    print(AAPL)

main()
