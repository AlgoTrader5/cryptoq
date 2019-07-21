import argparse

from qpython import qconnection
from qpython.qtype import QException

# parse args from command line
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

if __name__ in "__main__":
	main()
