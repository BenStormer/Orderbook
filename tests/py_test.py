import orderbook

def test_market_buy():
    exchange = orderbook.Exchange()

    orders = [(True, 10, -1)]
    for order in orders:
        exchange.place_order("AAPL", order[0], order[1], order[2])
    assert len(exchange.orderbooks) == 1
    assert len(exchange.orderbooks[0].bids) == 1
    assert exchange.orderbooks[0].bids[0] == orderbook.Order(True, 10, -1)

def test_market_sell():
    exchange = orderbook.Exchange()

    orders = [(False, 10, -1)]
    for order in orders:
        exchange.place_order("AAPL", order[0], order[1], order[2])
    assert len(exchange.orderbooks) == 1
    assert len(exchange.orderbooks[0].asks) == 1
    assert exchange.orderbooks[0].asks[0] == orderbook.Order(False, 10, -1)

def test_limit_buy():
    exchange = orderbook.Exchange()

    orders = [(True, 10, 50)]
    for order in orders:
        exchange.place_order("AAPL", order[0], order[1], order[2])
    assert len(exchange.orderbooks) == 1
    assert len(exchange.orderbooks[0].bids) == 1
    assert exchange.orderbooks[0].bids[0] == orderbook.Order(True, 10, 50)

def test_limit_sell():
    exchange = orderbook.Exchange()

    orders = [(False, 10, 50)]
    for order in orders:
        exchange.place_order("AAPL", order[0], order[1], order[2])
    assert len(exchange.orderbooks) == 1
    assert len(exchange.orderbooks[0].asks) == 1
    assert exchange.orderbooks[0].asks[0] == orderbook.Order(False, 10, 50)

def test_market_buy_and_sell():
    exchange = orderbook.Exchange()

    orders = [(True, 10, -1), (False, 10, -1)]
    for order in orders:
        exchange.place_order("AAPL", order[0], order[1], order[2])
    assert len(exchange.orderbooks) == 1
    assert len(exchange.orderbooks[0].bids) == 1
    assert len(exchange.orderbooks[0].asks) == 1

def test_successful_limit_buy_and_sell():
    exchange = orderbook.Exchange()

    orders = [(True, 10, 50), (False, 10, 50)]
    for order in orders:
        exchange.place_order("AAPL", order[0], order[1], order[2])
    assert len(exchange.orderbooks) == 1
    assert len(exchange.orderbooks[0].bids) == 0
    assert len(exchange.orderbooks[0].asks) == 0

def test_unsuccessful_limit_buy_and_sell():
    exchange = orderbook.Exchange()

    orders = [(True, 10, 40), (False, 10, 60)]
    for order in orders:
        exchange.place_order("AAPL", order[0], order[1], order[2])
    assert len(exchange.orderbooks) == 1
    assert len(exchange.orderbooks[0].bids) == 1
    assert len(exchange.orderbooks[0].asks) == 1

def test_limit_buy_market_sell():
    exchange = orderbook.Exchange()

    orders = [(True, 10, 50), (False, 10, -1)]
    for order in orders:
        exchange.place_order("AAPL", order[0], order[1], order[2])
    assert len(exchange.orderbooks) == 1
    assert len(exchange.orderbooks[0].bids) == 0
    assert len(exchange.orderbooks[0].asks) == 0

def test_limit_sell_market_buy():
    exchange = orderbook.Exchange()

    orders = [(False, 10, 50), (True, 10, -1)]
    for order in orders:
        exchange.place_order("AAPL", order[0], order[1], order[2])
    assert len(exchange.orderbooks) == 1
    assert len(exchange.orderbooks[0].bids) == 0
    assert len(exchange.orderbooks[0].asks) == 0

def test_ten_limit_buys_four_limit_sells():
    exchange = orderbook.Exchange()

    orders = [(True, 10, 10),
              (True, 10, 20),
              (True, 10, 30),
              (True, 10, 40),
              (True, 10, 50),
              (True, 10, 60),
              (True, 10, 70),
              (True, 10, 80),
              (True, 10, 90),
              (True, 10, 100),
              (False, 10, 100),
              (False, 10, 90),
              (False, 10, 80),
              (False, 10, 70)]
    for order in orders:
        exchange.place_order("AAPL", order[0], order[1], order[2])
    assert len(exchange.orderbooks) == 1
    assert len(exchange.orderbooks[0].bids) == 6
    assert len(exchange.orderbooks[0].asks) == 0
    assert exchange.orderbooks[0].bids[0].price == 60
    assert exchange.orderbooks[0].bids[5].price == 10
    
def test_five_limit_buys_three_market_sells():
    exchange = orderbook.Exchange()

    orders = [(True, 10, 10),
              (True, 10, 20),
              (True, 10, 30),
              (True, 10, 40),
              (True, 10, 50),
              (False, 27, -1),
              (False, 6, -1),
              (False, 1, -1)]
    for order in orders:
        exchange.place_order("AAPL", order[0], order[1], order[2])
    assert len(exchange.orderbooks) == 1
    assert len(exchange.orderbooks[0].bids) == 2
    assert len(exchange.orderbooks[0].asks) == 0
    assert exchange.orderbooks[0].bids[0].price == 20
    assert exchange.orderbooks[0].bids[0].quantity == 40 - (27 + 6 + 1)  
    assert exchange.orderbooks[0].bids[1].price == 10
    assert exchange.orderbooks[0].bids[1].quantity == 10

def test_two_orderbooks_simple():
    exchange = orderbook.Exchange()

    orders_apple = [(True, 10, -1),
                    (True, 10, 50)]
    for order in orders_apple:
        exchange.place_order("AAPL", order[0], order[1], order[2])

    orders_google = [(True, 10, -1),
                     (True, 10, 50)]
    for order in orders_google:
        exchange.place_order("GOOG", order[0], order[1], order[2])
    
    assert len(exchange.orderbooks) == 2

    assert exchange.orderbook_names["AAPL"] == 0
    assert len(exchange.orderbooks[0].bids) == 2
    assert exchange.orderbooks[0].bids[0].price == 50
    assert exchange.orderbooks[0].bids[1].price == -1
    assert len(exchange.orderbooks[0].asks) == 0

    assert exchange.orderbook_names["GOOG"] == 1
    assert len(exchange.orderbooks[1].bids) == 2
    assert exchange.orderbooks[1].bids[0].price == 50
    assert exchange.orderbooks[1].bids[1].price == -1
    assert len(exchange.orderbooks[1].asks) == 0

def test_two_orderbooks_complicated():
    exchange = orderbook.Exchange()

    orders_apple = [(True, 10, 50),
                    (False, 10, 100),
                    (True, 5, -1),
                    (False, 5, -1)]
    for order in orders_apple:
        exchange.place_order("AAPL", order[0], order[1], order[2])

    orders_google = [(True, 10, 50),
                    (False, 10, 100),
                    (True, 5, -1),
                    (False, 5, -1)]
    for order in orders_google:
        exchange.place_order("GOOG", order[0], order[1], order[2])
    
    assert len(exchange.orderbooks) == 2

    assert exchange.orderbook_names["AAPL"] == 0
    assert len(exchange.orderbooks[0].bids) == 1
    assert exchange.orderbooks[0].bids[0].quantity == 5
    assert len(exchange.orderbooks[0].asks) == 1
    assert exchange.orderbooks[0].asks[0].quantity == 5

    assert exchange.orderbook_names["GOOG"] == 1
    assert len(exchange.orderbooks[1].bids) == 1
    assert exchange.orderbooks[1].bids[0].quantity == 5
    assert len(exchange.orderbooks[1].asks) == 1
    assert exchange.orderbooks[1].asks[0].quantity == 5