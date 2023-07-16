# Orderbook
An implementation of a limit-matching orderbook

Inspired by:  
kmanley's orderbook here: https://github.com/kmanley/orderbook,  
ajtulloch's orderbook here: https://github.com/ajtulloch/quantcup-orderbook,  
jeog's orderbook here: https://github.com/jeog/SimpleOrderbook

## Goals:
- [ ] Integrate main functionality within Python
  - [ ] Place market "buy" and "sell" orders
  - [ ] Place limit "buy" and "sell" orders
- [ ] Add tests
- [ ] Re-create orderbook in C++ with optimized matching engine
  - Functionality should be the same as the Python version
- [ ] Create Python interface for users to place orders and interact with
- [ ] Add tests for C++ version of orderbook
