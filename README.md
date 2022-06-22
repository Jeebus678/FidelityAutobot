The purpose of this program is to provide simple order automation for fidelity investments using the selenium API. Fidelity doesn't provide an API for trading, so this is my workaround for automation. 

Currently this is work-in-progress with only support for creating simple buy/sell orders.

``` 
usage: main.py [-T TICKER] [-q QUANTITY] [-b | -s] [-S | -D] [-m | -l]
               [-p PRICE] [-d | -g] [-h]

A program for creating fidelity orders.

Required arguments:
  -T TICKER, --ticker TICKER
                        Define order ticker
  -q QUANTITY, --quantity QUANTITY
                        Set order quantity [-1 to select all]
  -b, --buy             Sets order to buy
  -s, --sell            Sets order to sell
  -S, --shares          Sets order to shares
  -D, --dollars         Sets order to dollars

Optional arguments:
  -m, --market          Sets order to market [default]
  -l, --limit           Sets order to limit
  -p PRICE, --price PRICE
                        Sets limit price
  -d, --day             Sets limit order to day
  -g, --gtc             Sets limit order to good-till-cancelled
  -h, --help            Show this help message and exit
```

Config file should look like this:
``` Python
account = {
    "user": "your_username",
    "pass": "your_password",
    "id": "account_number"
}
```

And configure the chrome webdriver to include the proper path
``` Python
driver = webdriver.Chrome(options=cfg.chrome_options, executable_path='PATH_TO_CHROMEDRIVER')
```
