import asyncio
import argparse
from datetime import datetime
from utils import read_cfg

from cryptofeed.rest import Rest

from qpython import qconnection
from qpython.qtype import QException

from pprint import pprint


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help='QConnection port')
args = parser.parse_args()


# create connection object
q = qconnection.QConnection(host='localhost', port=int(args.port), pandas=True)
# initialize connection
q.open()

print(q)
print(f"IPC version: {q.protocol_version}. Is connected: {q.is_connected()}")


def main():

	subscriptions = read_cfg("conf//subscriptions.yaml")

	r = Rest()

	rest_clients = {
		'coinbase': r.coinbase,
		'binance': r.binance,
		'kraken': r.kraken,
		'poloniex': r.poloniex
	}
	
	for exch, data in subscriptions.items():
		for pair in data['pairs']:
			print(f'Getting trade data for {exch} {pair}')
			trades = rest_clients[exch].trades(pair)
			for trade in trades:
				for t in trade:
					hwt = str(datetime.utcnow().isoformat()).replace("T","D").replace("-",".")
					ts = str(datetime.fromtimestamp(t['timestamp']).isoformat()).replace("T","D").replace("-",".")
					qStr = f"`trades insert (`timestamp${hwt};`timestamp${ts};" \
							f"`{t['feed']};`$\"{t['pair']}\";`{t['side']};`float${t['amount']};" \
							f"`float${t['price']};`int${t['id']})"
					try:
						q.sendSync(qStr, param=None)    
					except QException as e:
						print(f"Error executing query {qStr} against server. {e}")

						
if __name__ in "__main__":
	main()
