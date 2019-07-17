'''
taken from https://kx.com/blog/combining-high-frequency-cryptocurrency-venue-data-using-kdb/
'''
from cryptofeed.callback import TradeCallback
from cryptofeed import FeedHandler
from cryptofeed.exchanges import Coinbase
from cryptofeed.defines import TRADES

from datetime import datetime
from qpython import qconnection

# outside q instance open the port: q.exe -p 5002
# in q instance open the port: \p 5002
q = qconnection.QConnection(host='localhost', port=5002, pandas=True)
q.open()

q.sync("""trades:([]
	utc_datetime:`timestamp$();
	exch_datetime:`timestamp$();
	exch:`symbol$();
	sym:`symbol$();
	side:`symbol$();
	amount:`float$();
	price:`float$();
	order_id:`long$())""")

q.sync("""quotes:([]
	utc_datetime:`timestamp$();
	exch_datetime:`timestamp$();
	exch:`symbol$();
	sym:`symbol$();
	bnum:`int$();
	bsize:`float$();
	bid:`float$();
	ask:`float$();
	asize:`float$();
	anum:`int$())""")

async def trade(feed, pair, id, timestamp, side, amount, price):
	hwt = str(datetime.utcnow().isoformat()).replace("T","D").replace("-",".")
	ts = str(datetime.fromtimestamp(timestamp).isoformat()).replace("T","D").replace("-",".")
	q.sync(f"`trades insert (`timestamp${hwt};`timestamp${ts};`$\"{pair}\";`{side};{amount};{price};`{feed};{id})")


def main():
	f = FeedHandler()
	f.add_feed(Coinbase(channels=[TRADES], pairs=['ETH-USD'], callbacks={TRADES: TradeCallback(trade)}))
	f.run()



if __name__ == '__main__':
	main()

