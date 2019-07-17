'''
Records trade and quote data to kdb+
exchange and product subscriptions configured in subscriptions.yaml 
modified from https://kx.com/blog/combining-high-frequency-cryptocurrency-venue-data-using-kdb/
'''
from cryptofeed.callback import TradeCallback, BookCallback
from cryptofeed import FeedHandler
from cryptofeed.exchanges import Coinbase
from cryptofeed.defines import TRADES

import yaml
from datetime import datetime
from kdb_client import KdbClient


kdb_client = KdbClient(host='localhost', port=5002)

async def trade(feed, pair, id, timestamp, side, amount, price):
    hwt = str(datetime.utcnow().isoformat()).replace("T","D").replace("-",".")
    ts = str(datetime.fromtimestamp(timestamp).isoformat()).replace("T","D").replace("-",".")
    amount = float(amount)
    kdb_client.exequery(f"`trades insert (`timestamp${hwt};`timestamp${ts};`{feed};`$\"{pair}\";`{side};{amount};{price};{id})")

async def book(feed, pair, book, timestamp):
    hwt = str(datetime.utcnow().isoformat()).replace("T","D").replace("-",".")
    ts = str(datetime.fromtimestamp(timestamp).isoformat()).replace("T","D").replace("-",".")
    bid_price = list(book['bid'])[-1]
    bid_size = float(book['bid'][bid_price])
    ask_price = list(book['ask'])[0]
    ask_size = float(book['ask'][ask_price])
    kdb_client.exequery(f"`quotes insert (`timestamp${hwt};`timestamp${ts};`{feed};`$\"{pair}\";{bid_size};{bid_price};{ask_price};{ask_size})")


##### Subscriptions Config #####
config = None
try:
    with open('subscriptions.yaml', encoding='utf8') as fd:
        config = yaml.safe_load(fd)
except IOError:
    print("subscriptions file is missing")


def main():
    try:
        f = FeedHandler()
        f.add_feed(Coinbase(channels=[TRADES], pairs=config['coinbase']['pairs'], callbacks={TRADES: TradeCallback(trade)}))
        f.run()
    finally:
        kdb_client.close()
        

if __name__ == '__main__':
    main()

