# cryptoq
stores streaming trade and quote data from cryptofeed to kdb

Requirements:
* 32-bit or 64-bit version of kdb+ https://kx.com/connect-with-us/download/
* qpython (python library to interact with q)
* cryptofeed (python library to stream cryptocurrency market data) https://github.com/bmoscon/cryptofeed


# Getting Started
configure the subscriptions.yaml config file with exchange, channels and products
example:
```yaml
coinbase:
  channels:
    - TRADES
    - L2_BOOK
  pairs:
    - BTC-USD
    - BTC-USDC
```

in command prompt, start q instance specifiying port and schema file
```shell
q schemas.q -p 5002
```

in q, you can see quotes and trades tables
```q
q)tables[]
`quotes`trades
```

in command prompt, run taq.py to record market data
```python
python taq.py
```

in q window, you can see trades data
```q
q)trades
utc_datetime                  exch_datetime                 exch     sym     ..
-----------------------------------------------------------------------------..
2019.07.17D17:57:48.265899000 2019.07.17D12:57:47.341000000 COINBASE ETH-USD ..
2019.07.17D17:57:51.484030000 2019.07.17D12:57:52.275000000 COINBASE ETH-USD ..
```







