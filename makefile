.PHONY: all
all: orderbook

orderbook: src/orderbook.cpp
	g++ -std=c++20 -o src/orderbook src/orderbook.cpp

.PHONY: install
install:
	mkdir -p bin
	cp -p src/orderbook bin

.PHONY: clean
clean:
	rm -f bin/orderbook
	rm -f src/orderbook