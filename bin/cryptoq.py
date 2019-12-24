import os
import zmq
import time
import argparse
from multiprocessing import Process

from qpython import qconnection
from qpython.qtype import QException

from cryptofeed import FeedHandler
from cryptofeed.backends.zmq import BookZMQ, TradeZMQ
from cryptofeed.defines import TRADES, L2_BOOK
from cryptofeed.exchanges import (Binance, BinanceUS, Bitmex, Bitfinex, Bittrex, Bitstamp, Bybit, 
                                  Coinbase, Coinbene, Deribit, EXX, FTX, Gemini, Kraken, 
                                  KrakenFutures, OKCoin, OKEx, Poloniex)

from utils.utils import read_cfg, trade_convert, book_convert, load_quote_schema

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("--q-port",    dest="port",     type=int, default=5002, help='QConnection port')
	parser.add_argument("--kdb-port",  dest="kdbport",  type=int, default=5555, help='ZMQ port for kdb+ capture')
	parser.add_argument("--gui-port",  dest="guiport",  type=int, default=5556, help='ZMQ port for gui')
	parser.add_argument("--config",                     type=str, default='conf\\subscriptions.yaml', help='path to the config file')
	parser.add_argument("--kdb-depth", dest="kdbdepth", type=int, default=5, help='Order Book depth for kdb+')
	parser.add_argument("--gui-depth", dest="guidepth", type=int, default=1, help='Order Book depth for gui')
	return parser.parse_args()

args = get_args()

PORT     = args.port
CONFIG   = args.config
KDBPORT  = args.kdbport
GUIPORT  = args.guiport
KDBDEPTH = args.kdbdepth
GUIDEPTH = args.guidepth

# create connection object
q = qconnection.QConnection(host='localhost', port=PORT, pandas=True)
# initialize connection
q.open()

# create quotes table in kdb+
q.sendSync(load_quote_schema(KDBDEPTH))

def receiver(port):
	ctx = zmq.Context.instance()
	s = ctx.socket(zmq.SUB)
	s.setsockopt(zmq.SUBSCRIBE, b'')
	s.bind(f'tcp://127.0.0.1:{port}')

	while True:
		data = s.recv_string()
        
		msg_type = data.split("-")[1].split('-')[0]
		if msg_type == "book":
			qStr = book_convert(data, KDBDEPTH)
		elif msg_type == "trades":
			qStr = trade_convert(data)
		else:
			print("Cannot recognize data message", data)
            return
        
		try:
			q.sendSync(qStr, param=None)
		except QException as e:
			print(f"Error executing query {qStr} against server. {e}")


def main():
	print(f"\nq connection port : {PORT}" \
          f"\nzmq (kdb) port    : {KDBPORT}" \
          f"\nzmq (gui) port    : {GUIPORT}" \
          f"\nkdb depth         : {KDBDEPTH}" \
          f"\ngui depth         : {GUIDEPTH}" \
          f"\nconfig            : {CONFIG}")
    
	print(f"IPC version: {q.protocol_version}. Is connected: {q.is_connected()}")
	
	subscriptions = read_cfg(CONFIG)
	
	try:
		
		p = Process(target=receiver, args=(KDBPORT,))
		p.start()

		f = FeedHandler()
		
		if "binance_us" in subscriptions.keys():
			f.add_feed(BinanceUS(
                max_depth=KDBDEPTH,
				channels=[L2_BOOK, TRADES], 
				pairs=subscriptions['binance_us'], 
				callbacks={
					TRADES: [TradeZMQ(port=KDBPORT), TradeZMQ(port=GUIPORT)],
					L2_BOOK: [BookZMQ(depth=KDBDEPTH, port=KDBPORT), BookZMQ(depth=GUIDEPTH, port=GUIPORT)]}))
            
		if "coinbase" in subscriptions.keys():
			f.add_feed(Coinbase(
                max_depth=KDBDEPTH,
				channels=[L2_BOOK, TRADES], 
				pairs=subscriptions['coinbase'], 
				callbacks={
					TRADES: [TradeZMQ(port=KDBPORT), TradeZMQ(port=GUIPORT)],
					L2_BOOK: [BookZMQ(depth=KDBDEPTH, port=KDBPORT), BookZMQ(depth=GUIDEPTH, port=GUIPORT)]}))

		if "kraken" in subscriptions.keys():
			f.add_feed(Kraken(
				channels=[L2_BOOK, TRADES], 
				pairs=subscriptions['kraken'], 
				callbacks={
					TRADES: [TradeZMQ(port=KDBPORT), TradeZMQ(port=GUIPORT)],
					L2_BOOK: [BookZMQ(depth=KDBDEPTH, port=KDBPORT), BookZMQ(depth=GUIDEPTH, port=GUIPORT)]}))

		f.run()

	except KeyboardInterrupt:
		pass

	finally:
		p.terminate()
		
		# save trades and quotes tables to disk
		data_path = os.getcwd()
		data_path = data_path.replace("\\", "/")
		trades_path = f"`:{data_path}/trades set trades"
		quotes_path = f"`:{data_path}/quotes set quotes"
		print(f"saving to disk quotes -> {quotes_path} trades -> {trades_path}")
		q.close()


if __name__ == '__main__':
	main()
