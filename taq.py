'''
Records trade and quote data to kdb+

exchange and product subscriptions configured in subscriptions.yaml 

modified from https://kx.com/blog/combining-high-frequency-cryptocurrency-venue-data-using-kdb/
'''
from cryptofeed.callback import TradeCallback
from cryptofeed import FeedHandler
from cryptofeed.exchanges import Coinbase
from cryptofeed.defines import TRADES

from datetime import datetime
from kdb_client import KdbClient



async def trade(feed, pair, id, timestamp, side, amount, price):
	hwt = str(datetime.utcnow().isoformat()).replace("T","D").replace("-",".")
	ts = str(datetime.fromtimestamp(timestamp).isoformat()).replace("T","D").replace("-",".")
	kdb_client.exequery(f"`trades insert (`timestamp${hwt};`timestamp${ts};`{feed};`$\"{pair}\";`{side};{amount};{price};{id})")
	

def main():
	try:
		kdb_client = KdbClient(host='localhost', port=5002)
		
		f = FeedHandler()
		f.add_feed(Coinbase(channels=[TRADES], pairs=['ETH-USD'], callbacks={TRADES: TradeCallback(trade)}))
		f.run()
	finally:
		kdb_client.close()
		



if __name__ == '__main__':
	main()

