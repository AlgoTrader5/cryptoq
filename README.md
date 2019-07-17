# cryptoq
stores streaming trade and quote data from cryptofeed to kdb


Requirements:
newest version of q
qpython (python library to interact with q)
cryptofeed (python library to stream cryptocurrency market data) https://github.com/bmoscon/cryptofeed
```
pip install qpython
```

start a q instance, specifiying a port and loading trade and quote table schemas
make sure q executable path is configured to QHOME environment variable or 
specify full path
```q
q schemas.q -p 5002

// table names
q)tables[]
`quotes`trades


```

start python script to record market data
```python
python taq.py
```

and then run in the q prompt to see quotes or trade data
```
q)trades
utc_datetime                  exch_datetime                 exch     sym     ..
-----------------------------------------------------------------------------..
2019.07.17D17:57:48.265899000 2019.07.17D12:57:47.341000000 COINBASE ETH-USD ..
2019.07.17D17:57:51.484030000 2019.07.17D12:57:52.275000000 COINBASE ETH-USD ..
q)
```







