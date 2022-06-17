The purpose of this program is to provide simple order automation for fidelity investments using the selenium API. Fidelity doesn't provide an API for trading, so this is my workaround for automation. 

Currently this is work-in-progress with only support for creating simple buy/sell orders through the `Orders.py` module. 

Usage: 
``` Python 
usage: main.py [-h] [-T TICKER] [-q QUANTITY] [-b | -s] [-S | -D] [-m | -l]

options:
  -h, --help            show this help message and exit
  -T TICKER, --ticker TICKER
  -q QUANTITY, --quantity QUANTITY
  -b, --buy
  -s, --sell
  -S, --shares
  -D, --dollars
  -m, --market
  -l, --limit
```

Examples: 
``` bash
main.py -T VT --quantity 1 --buy --shares --market 
main.py -T AMC --quantity 10 --sell --dollars --limit  
```
