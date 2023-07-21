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
        return (f"Order: {self.id:>5} | "
                f"{'Buy' if self.buy else 'Sell':>4} | "
                f"{self.quantity:>4} | "
                f"{f'market price' if self.price == -1 else f'${self.price:.2f}':>12} | "
                f"{self.time.strftime('%H:%M:%S, %m/%d/%y')}")

"""
- Create Orderbook class
    - Function for cancelling orders
        - Use order id to index map to figure out where to delete
    - Function for printing out the orderbook
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
        self.highest_bid = -1 # Pointer to highest bid price
        self.lowest_ask = -1 # Pointer to lowest ask price


    def __str__(self):
        num_bids = len(self.bids)
        num_asks = len(self.asks)
        print(f"Total number of orders: {num_bids + num_asks}")
        if self.bids:
            print(f"Number of bids: {num_bids}. See details below:")
            for bid in self.bids:
                print(bid.compact_str())
            print()
        if self.asks:
            print(f"Number of asks: {num_asks}. See details below:")
            for ask in self.asks:
                print(ask.compact_str())
            print()


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
        # Check that an appropriate sale is even possible
        if ((order.buy and self.lowest_ask < 0) or
            (not order.buy and self.highest_bid < 0)):
            return self.queue_order(order)

        if order.market:
            return self.market_buy(order) if order.buy else self.market_sell(order)
        # Limit order
        else:
            # Bid > existing ask
            if order.buy and order.price > self.get_price(self.lowest_ask):
                return self.limit_buy(order)
            # Ask < existing bid
            elif order.sell and order.price < self.get_price(self.highest_bid):
                return self.limit_sell(order)
            else:
                return self.queue_order(order)


    def queue_order(self, order):
        """
        Queue an order into the orderbook.

        Args:
            order (Order): The ordered to be queued
        """
        if order.buy:
            if len(self.bids) == 0:
                self.bids.append(order)
            else:
                insert_index = 0
                last_index = len(self.bids) - 1
                while order.price < self.bids[insert_index].price:
                    if insert_index > last_index:
                        break
                    insert_index += 1
                self.bids.insert(insert_index, order)
        else:
            if len(self.asks) == 0:
                self.asks.append(order)
            else:
                insert_index = 0
                last_index = len(self.asks) - 1
                while order.price > self.asks[insert_index].price:
                    if insert_index > last_index:
                        break
                    insert_index += 1
                self.asks.insert(insert_index, order)


    def market_buy(self, order: Order):
        """
        Purchase stock(s) at market price.

        Args:
            order (Order): The buy order
        """
        while order.quantity > 0 and self.asks:
            ask_quantity = self.asks[0].quantity
            if order.quantity < ask_quantity:
                self.asks[0].quantity -= order.quantity
                order.quantity = 0
            elif order.quantity == ask_quantity:
                self.asks.remove(0)
                order.quantity = 0
            else:
                order.quantity -= ask_quantity
                self.asks.remove(0)
        if order.quantity > 0:
            queue_order(order)

# Market sell
# Limit buy
# Limit sell




def main():
    test_order = Order(True, 50, 370)
    test_order2 = Order(False, 2)
    print(test_order.compact_str())
    print(test_order2.compact_str())

main()
