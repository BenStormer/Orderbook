# Orderbook
A Python implementation of a limit-matching orderbook. This orderbook supports four actions:
  - Market buys
  - Markets sells
  - Limit buys
  - Limit sells

Orders are automatically matched and trades are made if possible.

To run unit tests, first activate the virtual environment by running `source ./venv/bin/activate` after installing the requirements. Then, simply run `pytest` from the root of the repo to run tests.

The main goal of this orderbook was to get familiar with the most basic logic of an orderbook and matching engine, as well as to simply get better at OOP in Python.

## Goals:
- [x] Integrate main functionality within Python
  - [x] Place market "buy" and "sell" orders
  - [x] Place limit "buy" and "sell" orders
- [x] Add unit tests for Python version of orderbook

## Potential Future Work:
- [ ] Allow order cancellation
- [ ] Add logging for trades that occured