The purpose of this program is to provide simple order automation for fidelity investments using the selenium API. Fidelity doesn't provide an API for trading, so this is a great workaround for automation. 

Currently this is work-in-progress with only support for creating simple buy/sell orders through the `Orders.py` module. 

Usage: 
``` Python 
Orders = order.Order(driver)
Orders.create_trade("TSLA", "buy", 1, "shares")
Orders.create_trade("AAPL", "sell", 100, "dollars") 
Orders.create_trade("GME", "sell", 10, "shares", "limit", 10000000, "gtc") 
```

- Create Orders object & pass webdriver
- Create trades py passing parameters to `create_trade` 
- Offers full support over all basic trade functions, that is: 
      - Buy/Sell orders
      - Limit/Market options 
      - Trade in dollars or shares 
