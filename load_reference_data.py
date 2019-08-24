import argparse

from qpython import qconnection
from qpython.qtype import QException
from cryptofeed.pairs import gen_pairs
from cryptofeed.defines import BITSTAMP, BITFINEX, COINBASE, GEMINI, HITBTC, POLONIEX, KRAKEN, BINANCE, EXX, HUOBI, HUOBI_US, HUOBI_DM, OKCOIN, OKEX, COINBENE, BYBIT, FTX


# parse args from command line
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, help='QConnection port')
args = parser.parse_args()

# create connection object
q = qconnection.QConnection(host='localhost', port=args.port, pandas=True)
# initialize connection
q.open()
print(f"IPC version: {q.protocol_version}. Is connected: {q.is_connected()}")


def insert_data(exch, sym, sym2):
	qStr = f"`refdata insert (`symbol${exch};`symbol${sym};`symbol${sym2})"
	try:
		q.sendSync(qStr, param=None)
	except QException as e:
		print(f"Error executing query {qStr} against server. {e}")


def main():
	exch_list = [
		BITSTAMP, BITFINEX, COINBASE, GEMINI, HITBTC, POLONIEX, KRAKEN, BINANCE, 
		EXX, HUOBI, HUOBI_US, HUOBI_DM, OKCOIN, OKEX, COINBENE, BYBIT, FTX
	]
	for exch in exch_list:
		pairs = gen_pairs(exch)
		for k,v in pairs.items():
			print(exch, k, v)
            insert_data(exch, k, v)


if __name__ in "__main__":
	main()
