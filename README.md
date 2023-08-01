# Orderbook
An implementation of a limit-matching orderbook

Inspired by:  
kmanley's orderbook here: https://github.com/kmanley/orderbook,  
ajtulloch's orderbook here: https://github.com/ajtulloch/quantcup-orderbook,  
jeog's orderbook here: https://github.com/jeog/SimpleOrderbook

## Goals:
- [x] Integrate main functionality within Python
  - [x] Place market "buy" and "sell" orders
  - [x] Place limit "buy" and "sell" orders
- [x] Add tests for Python version of orderbook
- [ ] Re-create orderbook in C++ with optimized matching engine
  - General logic should be the same as the Python version
- [ ] Add tests for C++ version of orderbook