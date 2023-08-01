.PHONY: all
all: orderbook

orderbook: src/orderbook.cpp
	g++ -o src/orderbook src/orderbook.cpp

.PHONY: install
install:
	mkdir -p bin
	cp -p src/orderbook bin

.PHONY: clean
clean:
	rm -f bin/orderbook
	rm -f src/orderbook