# cryptoq
stores streaming trade and quote data from cryptofeed to kdb

Requirements:
* python 3.6 >=
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
q.exe q/schemas.q -p 5002
```
in the q prompt, you can see quotes and trades tables
```q
q)tables[]
`quotes`trades
```
in command prompt, change into cryptoq directory and subscribe to market data and send over tcp
```python
python zmq_client.py (modified version from cryptofeed demo_zmq.py)
```
in command prompt, run scripts separately for trades and quotes
```python
python record_trade.py
def main():
    trade_kdb = KdbClient(zmqhost='127.0.0.1', zmqport=5555, kdbhost='localhost', kdbport=5002)
    trade_kdb.run()

if __name__ == '__main__':
    main()
    
    
python record_book.py
def main():
    book_kdb = KdbClient(zmqhost='127.0.0.1', zmqport=5556, kdbhost='localhost', kdbport=5002)
    book_kdb.run()

if __name__ == '__main__':
    main()
```
in q window, you can see trades and quotes data
```q
q)trades
utc_datetime                  exch_datetime                 exch     sym      side amount     price    order_id
---------------------------------------------------------------------------------------------------------------
2019.07.17D22:03:28.561529000 2019.07.17D17:03:24.427000000 COINBASE EOS-USD  sell 42.8       3.956    396979  
2019.07.17D22:03:28.760387000 2019.07.17D17:03:24.641000000 COINBASE ETH-USD  buy  5          215.52   50223672
2019.07.17D22:03:28.762372000 2019.07.17D17:03:24.641000000 COINBASE ETH-USD  buy  15.61874   215.53   50223673
2019.07.17D22:03:29.105701000 2019.07.17D17:03:24.987000000 COINBASE ETH-USD  buy  5          215.52   50223674
2019.07.17D22:03:29.196769000 2019.07.17D17:03:25.760000000 COINBASE DAI-USDC sell 6.03765    0.992532 147320  
2019.07.17D22:03:29.279228000 2019.07.17D17:03:25.152000000 COINBASE BTC-USD  sell 0.01056728 9860     70194746
2019.07.17D22:03:30.065150000 2019.07.17D17:03:25.939000000 COINBASE BTC-USD  buy  0.05440595 9864.39  70194747
2019.07.17D22:03:30.524360000 2019.07.17D17:03:26.405000000 COINBASE XRP-USD  buy  67         0.315    2431849 
2019.07.17D22:03:30.704920000 2019.07.17D17:03:26.580000000 COINBASE LTC-BTC  sell 1.1969     0.009416 6068676 
2019.07.17D22:03:31.379680000 2019.07.17D17:03:27.259000000 COINBASE DAI-USDC sell 22.06721   0.992532 147321  
2019.07.17D22:03:32.061706000 2019.07.17D17:03:27.921000000 COINBASE LINK-USD buy  38.8       2.4657   581567 

q)quotes
utc_datetime                  exch_datetime                 exch     sym      bsize      bid        ask        asize    
------------------------------------------------------------------------------------------------------------------------
2019.07.18D23:11:50.343151000 2019.07.18D18:11:49.920316000 COINBASE ZRX-BTC  4103.811   2.244e-005 2.25e-005  6292.148 
2019.07.18D23:11:50.347144000 2019.07.18D18:11:49.929257000 COINBASE BTC-USDC 1.281527   10649.47   10660.17   0.1716854
2019.07.18D23:11:50.348136000 2019.07.18D18:11:49.932251000 COINBASE BTC-USD  0.00234715 10651.21   10659.03   0.621531 
2019.07.18D23:11:50.349134000 2019.07.18D18:11:49.933245000 COINBASE BTC-USD  0.00234715 10651.21   10659.03   0.621531 
2019.07.18D23:11:50.350131000 2019.07.18D18:11:49.934245000 COINBASE LINK-USD 1310.99    2.67597    2.67997    8.45     
2019.07.18D23:11:50.351136000 2019.07.18D18:11:49.942233000 COINBASE BTC-USD  0.1663128  10651.21   10659.03   0.621531 
2019.07.18D23:11:50.352127000 2019.07.18D18:11:49.966159000 COINBASE XLM-USD  1061       0.088705   0.08872    51574    
2019.07.18D23:11:50.353123000 2019.07.18D18:11:49.967157000 COINBASE ETC-USD  269.7492   6.031      6.04       50       
2019.07.18D23:11:50.354121000 2019.07.18D18:11:49.968154000 COINBASE LINK-USD 1310.99    2.67597    2.67997    8.45     
2019.07.18D23:11:50.355119000 2019.07.18D18:11:49.983112000 COINBASE BTC-USD  0.1663128  10651.21   10659.03   0.621531 
```







