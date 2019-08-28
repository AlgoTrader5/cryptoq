```q
q)getCandlestick[`$"BTC-USD";`$"COINBASE";1]

minute| sym     exch     num volume    o        h        l        c        vwap     buyVol    sellVol    buyNum sellNum
------| ---------------------------------------------------------------------------------------------------------------
02:41 | BTC-USD COINBASE 19  0.5967802 10637.79 10641.7  10622.78 10625.89 10628.51 0.1454666 0.4513136  10     9      
02:42 | BTC-USD COINBASE 16  0.9032585 10620.58 10629.73 10620.35 10620.35 10624.06 0.8086228 0.09463569 10     6      
02:43 | BTC-USD COINBASE 15  0.4656438 10622.67 10629.89 10621.46 10625.72 10625.58 0.4280983 0.03754556 10     5      
02:44 | BTC-USD COINBASE 14  0.4015885 10625.99 10626    10621.29 10625.99 10625.74 0.3859287 0.01565982 11     3      
02:45 | BTC-USD COINBASE 24  9.856621  10626    10638.71 10625.99 10638.71 10626.13 9.850947  0.00567491 23     1      
02:46 | BTC-USD COINBASE 16  3.180451  10640    10650    10640    10650    10645.85 2.976496  0.203955   13     3      
02:47 | BTC-USD COINBASE 17  1.938382  10655.55 10655.67 10650.21 10655.67 10653.09 0.1008218 1.83756    11     6      
02:48 | BTC-USD COINBASE 15  6.635837  10655.67 10655.67 10653.74 10653.76 10655.63 0.119175  6.516662   6      9      
02:49 | BTC-USD COINBASE 24  0.6880857 10653.76 10653.76 10640.01 10640.01 10647.14 0.4754764 0.2126093  15     9      
02:50 | BTC-USD COINBASE 20  1.207107  10639.87 10639.87 10630    10637.08 10631.65 1.030817  0.1762903  12     8      
02:51 | BTC-USD COINBASE 15  2.25401   10637.01 10637.5  10630.83 10636.55 10636.5  1.91604   0.33797    11     4      
02:52 | BTC-USD COINBASE 10  0.4985982 10636.55 10647.59 10636.55 10647.3  10641.42 0.4282986 0.07029962 7      3  
```
The refdata portion is still work in progress. The data coming from ccxt is unreliable.
```q
q)select from refdata where exch=`coinbasepro
sym       exch        minTick minSize makerFee takerFee
-------------------------------------------------------
XTZ/BTC   coinbasepro 1e-008  1       0        0.003
REP/USD   coinbasepro 0.01    0.1     0        0.003
BTC/USDC  coinbasepro 0.01    0.001   0        0.003
ZRX/BTC   coinbasepro 1e-008  1       0        0.003
BCH/EUR   coinbasepro 0.01    0.01    0        0.003
ZEC/USDC  coinbasepro 0.01    0.01    0        0.003
LTC/USD   coinbasepro 0.01    0.1     0        0.003
BAT/USDC  coinbasepro 1e-006  1       0        0.003
XLM/USD   coinbasepro 1e-006  1       0        0.003
DNT/USDC  coinbasepro 1e-006  1       0        0.003
LTC/EUR   coinbasepro 0.01    0.1     0        0.003
BTC/GBP   coinbasepro 0.01    0.001   0        0.003
ETC/GBP   coinbasepro 0.001   0.1     0        0.003
EOS/BTC   coinbasepro 1e-006  0.1     0        0.003
LINK/USD  coinbasepro 1e-005  1       0        0.003
ETC/BTC   coinbasepro 1e-006  0.1     0        0.003
MANA/USDC coinbasepro 1e-006  1       0        0.003
REP/BTC   coinbasepro 1e-006  0.1     0        0.003
XLM/BTC   coinbasepro 1e-008  1       0        0.003
ETC/EUR   coinbasepro 0.001   0.1     0        0.003
```
