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
from qpython import qconnection

# outside q instance open the port: q.exe -p 5002
# in q instance open the port: \p 5002 
# to close q instance, use // command
q = qconnection.QConnection(host='localhost', port=5002, pandas=True)
q.open()


async def trade(feed, pair, id, timestamp, side, amount, price):
	hwt = str(datetime.utcnow().isoformat()).replace("T","D").replace("-",".")
	ts = str(datetime.fromtimestamp(timestamp).isoformat()).replace("T","D").replace("-",".")
	q.sendSync(f"`trades insert (`timestamp${hwt};`timestamp${ts};`{feed};`$\"{pair}\";`{side};{amount};{price};{id})")
	

def main():
	f = FeedHandler()
	f.add_feed(Coinbase(channels=[TRADES], pairs=['ETH-USD'], callbacks={TRADES: TradeCallback(trade)}))
	f.run()



if __name__ == '__main__':
	main()

