"""
ADDITIONAL IMPROVEMENTS:
- Create system for logging all transactions that have occurred
- Create system for cancelling order
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

    def __init__(self, buy: bool, quantity: int, price: float | int | None = None):
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
        self.price = float(price) if price else -1  # -1 = market order
        self.time = datetime.now(timezone.utc)
        Order.id += 1

    def __str__(self) -> str:
        """
        Constructs a readable printout of the order.
        """
        return (
            f"Order {self.id} placed at "
            f"{self.time.strftime('%H:%M:%S, %B %d %Y')}:\n"
            f"\t{'Buy' if self.buy else 'Sell'} {self.quantity} at "
            f"{'market price' if self.price == -1 else f'${self.price:.2f}'}"
        )

    def compact_str(self) -> str:
        """
        Constructs a compact printout of the order.
        """
        return (
            f"| Order: {self.id:>5} | "
            f"{'Buy' if self.buy else 'Sell':>4} | "
            f"{self.quantity:>8} | "
            f"{'market price' if self.price == -1 else f'${self.price:.2f}':>12} | "
            f"{self.time.strftime('%H:%M:%S, %m/%d/%y')} |"
        )


class Orderbook:
    """
    Represents all orders for a specific stock.
    """

    def __init__(self, ticker: str):
        """
        Constructs an orderbook for a given stock.

        Args:
            ticker (str): Ticker for a given stock
        """
        self.ticker = ticker
        self.bids: list[Order] = []  # List of bids sorted by price from high to low
        self.asks: list[Order] = []
        # List of asks sorted by price from low to high

    def __str__(self):
        string = f"{self.ticker:^70}\n"
        string += "-" * 70 + "\n"
        string += (
            f"| {'Order ID':^12} | "
            f"{'Side':^4} | "
            f"{'Quantity':^8} | "
            f"{'Price Type':^12} | "
            f"{'Time Placed':^18} |"
        ) + "\n"
        string += "-" * 70 + "\n"
        if self.bids:
            for bid in self.bids:
                string += bid.compact_str() + "\n"
        if self.asks:
            for ask in self.asks:
                string += ask.compact_str() + "\n"
        string += "-" * 70 + "\n"
        num_bids = len(self.bids)
        num_asks = len(self.asks)
        string += (
            f"BIDS: {num_bids}, "
            f"ASKS: {num_asks}, "
            f"TOTAL: {num_bids + num_asks}\n"
        )
        return string

    def get_price(self, order: Order, index: int) -> float | int:
        """
        Gets the price listed for an index in the orderbook.

        Args:
            buy (bool): Represents a buy (True) or sell (False) order
            index (int): The index of interest in the orderbook

        Returns:
            price (int): Numerical value of price or -1 denoting market price
        """
        if order.buy:
            return self.bids[index].price
        else:
            return self.asks[index].price

    def place_order(self, order: Order):
        """
        Places an order and executes (if possible) or queues it.

        Args:
            order (Order): Order to be placed
        """
        if (order.buy and not self.asks) or (not order.buy and not self.bids):
            self.queue_order(order)
            return

        match (order.buy, order.price):
            case True, -1:
                self.market_buy(order)
            case True, _:
                self.limit_buy(order)
            case False, -1:
                self.market_sell(order)
            case False, _:
                self.limit_sell(order)

    def queue_order(self, order):
        """
        Queue an order into the orderbook.

        Args:
            order (Order): The ordered to be queued
        """
        if order.buy:
            if len(self.bids) == 0:
                self.bids.append(order)
            elif order.price == -1:
                self.bids.insert(0, order)
            else:
                insert_index = 0
                last_index = len(self.bids) - 1
                while order.price < self.bids[insert_index].price:
                    insert_index += 1
                    if insert_index > last_index:
                        break
                self.bids.insert(insert_index, order)
        else:
            if len(self.asks) == 0:
                self.asks.append(order)
            elif order.price == -1:
                self.asks.insert(0, order)
            else:
                insert_index = 0
                last_index = len(self.asks) - 1
                while order.price > self.asks[insert_index].price:
                    insert_index += 1
                    if insert_index > last_index:
                        break
                self.asks.insert(insert_index, order)

    def market_buy(self, order: Order):
        """
        Purchase stock(s) at market price.

        Args:
            order (Order): The market buy order
        """
        ask_index = 0
        while order.quantity > 0 and self.asks and ask_index < len(self.asks):
            ask_price = self.asks[ask_index].price
            if ask_price == -1:
                pass
            ask_quantity = self.asks[ask_index].quantity
            if order.quantity < ask_quantity:
                self.asks[ask_index].quantity -= order.quantity
                return
            elif order.quantity == ask_quantity:
                del self.asks[ask_index]
                return
            else:
                order.quantity -= self.asks[ask_index].quantity
                del self.asks[ask_index]
            ask_index += 1
        self.queue_order(order)

    def market_sell(self, order: Order):
        """
        Sell stock(s) at market price.

        Args:
            order (Order): The market sell order
        """
        bid_index = 0
        while order.quantity > 0 and self.bids and bid_index < len(self.bids):
            bid_price = self.bids[bid_index].price
            if bid_price == -1:
                pass
            bid_quantity = self.bids[bid_index].quantity
            if order.quantity < bid_quantity:
                self.bids[bid_index].quantity -= order.quantity
                return
            elif order.quantity == bid_quantity:
                del self.bids[bid_index]
                return
            else:
                order.quantity -= self.bids[bid_index].quantity
                del self.bids[bid_index]
            bid_index += 1
        self.queue_order(order)

    def limit_buy(self, order: Order):
        """
        Purchase stock(s) at limit price.

        Args:
            order (Order): The buy order
        """
        ask_index = 0
        while order.quantity > 0 and self.asks and ask_index > len(self.asks):
            ask_price = self.asks[ask_index].price
            if ask_price > order.price:
                self.queue_order(order)
                return

            ask_quantity = self.asks[ask_index].quantity
            if order.quantity < ask_quantity:
                self.asks[ask_index].quantity -= order.quantity
                return
            elif order.quantity == ask_quantity:
                del self.asks[ask_index]
                return
            else:
                order.quantity -= self.asks[ask_index].quantity
                del self.asks[ask_index]
            ask_index += 1
        self.queue_order(order)

    def limit_sell(self, order: Order):
        """
        Sell stock(s) at limit price.
        """
        bid_index = 0
        while order.quantity > 0 and self.bids and bid_index > len(self.bids):
            bid_price = self.bids[bid_index].price
            if bid_price < order.price:
                self.queue_order(order)
                return

            bid_quantity = self.bids[bid_index].quantity
            if order.quantity < bid_quantity:
                self.bids[bid_index].quantity -= order.quantity
                return
            elif order.quantity == bid_quantity:
                del self.bids[bid_index]
                return
            else:
                order.quantity -= bid_quantity
                del self.bids[bid_index]
            bid_index += 1
        self.queue_order(order)


"""
TODO:
- Create Exchange with all orderbooks
    - init with all orderbooks
    - Function for printing exchange
"""


class Exchange:
    """
    Represents all orderbooks present.
    """

    def __init__(self):
        """
        Initialize the exchange.
        """
        self.orderbook_names = {}
        self.orderbooks = []

    def __str__(self):
        string = ""
        if len(self.orderbooks) == 0:
            string += "No orderbooks are present. Empty exchange."
            return string

        for orderbook in self.orderbooks:
            string += str(orderbook)
        return string

    def create_orderbook(self, ticker: str):
        """
        Create an orderbook.

        Args:
            ticker (str): The ticker for the orderbook
        """
        orderbook = Orderbook(ticker)
        self.orderbook_names[ticker] = len(self.orderbooks)
        self.orderbooks.append(orderbook)

    def place_order(
        self, ticker: str, buy: bool, quantity: int, price: float | int | None
    ):
        """
        Place an order in a specific orderbook.

        Args:
            ticker (str): The ticker for the orderbook
            buy (bool): Represents a buy (True) or sell (False) order
            quantity (int): The number of stocks to buy/sell
            price (Optional[float | int]): The price of the order placed.
        """
        if ticker not in self.orderbook_names:
            self.create_orderbook(ticker)

        orderbook_index = self.orderbook_names[ticker]
        order = Order(buy, quantity, price)
        self.orderbooks[orderbook_index].place_order(order)


def main():
    print()
    exchange = Exchange()
    orders = [
        (True, 50, 370),
        (True, 2, 380),
        (True, 4, None),
        (False, 50, None),
        (False, 2, 500),
    ]
    for order in orders:
        exchange.place_order("AAPL", order[0], order[1], order[2])
    print(exchange)


if __name__ == "__main__":
    main()
