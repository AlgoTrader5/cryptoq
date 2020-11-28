import pandas as pd

from qpython import qconnection
from qpython.qtype import QException

from cryptofeed.defines import TRADES, FUNDING, TICKER, OPEN_INTEREST, L2_BOOK
from cryptofeed.backends.backend import (BackendBookCallback, BackendBookDeltaCallback, 
                                         BackendTradeCallback, BackendTickerCallback, 
                                         BackendFundingCallback, BackendOpenInterestCallback)
    

class KdbCallback:
    def __init__(self, host='127.0.0.1', key=None, numeric_type=float, **kwargs):
        q = qconnection.QConnection(host='localhost', port=5555, pandas=True)
        q.open()
        self.key = key if key else self.default_key
        self.numeric_type = numeric_type

    async def write(self, feed, pair, delta, timestamp):
        print(feed, pair, delta, timestamp)

        
class BookDeltaKdb(KdbCallback, BackendBookDeltaCallback):
    default_key = L2_BOOK

    
class BookKdb(KdbCallback, BackendBookCallback):
    default_key = L2_BOOK

    
class TradeKdb(KdbCallback, BackendTradeCallback):
    default_key = TRADES

    
class TradeKdb(KdbCallback, BackendTradeCallback):
    default_key = TRADES

    
class FundingKdb(KdbCallback, BackendFundingCallback):
    default_key = FUNDING

    
class TickerKdb(KdbCallback, BackendTickerCallback):
    default_key = TICKER

    
class OpenInterestKdb(KdbCallback, BackendOpenInterestCallback):
    default_key = OPEN_INTEREST
