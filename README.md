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
q.exe schemas.q -p 5002
```

start python script to record market data
```python
python taq.py
```







