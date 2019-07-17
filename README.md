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
utc_datetime                  exch_datetime                 exch     sym      side amount     price      order_id
-----------------------------------------------------------------------------------------------------------------
2019.07.17D22:01:23.618419000 2019.07.17D17:01:18.190000000 COINBASE BTC-USD  buy  0.00384101 9846.59    70194616
2019.07.17D22:01:23.654451000 2019.07.17D16:59:44.444000000 COINBASE BTC-USDC sell 2.400667   9820.73    398738  
2019.07.17D22:01:23.656453000 2019.07.17D17:01:08.860000000 COINBASE ETH-USD  buy  0.0875     215.37     50223503
2019.07.17D22:01:23.657454000 2019.07.17D16:59:21.334000000 COINBASE ETH-USDC sell 14.79564   215.16     175403  
2019.07.17D22:01:23.658454000 2019.07.17D17:01:03.121000000 COINBASE ETH-BTC  sell 0.03051163 0.02187    7956634 
2019.07.17D22:01:23.659455000 2019.07.17D17:01:19.206000000 COINBASE LTC-USD  sell 17.51998   92.89      40660187
2019.07.17D22:01:23.660456000 2019.07.17D17:01:11.704000000 COINBASE LTC-BTC  sell 0.6030337  0.009446   6068665 
```







