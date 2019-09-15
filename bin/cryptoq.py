import os
import zmq
import time
import argparse
from multiprocessing import Process

from qpython import qconnection
from qpython.qtype import QException

from cryptofeed.backends.zmq import BookZMQ, TradeZMQ
from cryptofeed import FeedHandler
from cryptofeed.exchanges import Coinbase, Kraken, KrakenFutures, Binance, Poloniex, Bitfinex, Bitstamp, Gemini
from cryptofeed.defines import TRADES, L2_BOOK


from utils import read_cfg, trade_convert, book_convert


parser = argparse.ArgumentParser()
parser.add_argument("--q-port", dest="port", type=int, default=5002, help='QConnection port')
parser.add_argument("--kdb-port", dest="kdbport", type=int, default=5555, help='ZMQ port for kdb+ capture')
parser.add_argument("--gui-port", dest="guiport", type=int, default=5556, help='ZMQ port for gui')
parser.add_argument("--config", type=str, default='conf\\subscriptions.yaml', help='path to the config file')
parser.add_argument("--depth", type=int, default=1, help='Order Book depth')
args = parser.parse_args()

PORT = args.port
DEPTH = args.depth
CONFIG = args.config
KDBPORT = args.kdbport
GUIPORT = args.guiport


# create connection object
q = qconnection.QConnection(host='localhost', port=PORT, pandas=True)
# initialize connection
q.open()


def receiver(port):
	ctx = zmq.Context.instance()
	s = ctx.socket(zmq.SUB)
	s.setsockopt(zmq.SUBSCRIBE, b'')
	s.bind(f'tcp://127.0.0.1:{port}')

	while True:
		data = s.recv_string()
		
		if data[0] == "b":
			qStr = book_convert(data, DEPTH)
		elif data[0] == "t":
			qStr = trade_convert(data)
		else:
			print("Cannot recognize data message")
		try:
			q.sendSync(qStr, param=None)
		except QException as e:
			print(f"Error executing query {qStr} against server. {e}")


def main():
	print(f'q connection port: {PORT}\nkdb (zmq) port: {KDBPORT}\ngui (zmq) port: {GUIPORT}\ndepth: {DEPTH}\nconfig: {CONFIG}')
	print(f"IPC version: {q.protocol_version}. Is connected: {q.is_connected()}")
	
	subscriptions = read_cfg(CONFIG)
    
	try:
        
		p = Process(target=receiver, args=(KDBPORT,))
		p.start()

		f = FeedHandler()

		if "coinbase" in subscriptions.keys():
			f.add_feed(Coinbase(
				channels=[L2_BOOK, TRADES], 
				pairs=subscriptions['coinbase'], 
				callbacks={
					TRADES: [TradeZMQ(port=KDBPORT), TradeZMQ(port=GUIPORT)],
					L2_BOOK: [BookZMQ(depth=DEPTH, port=KDBPORT), BookZMQ(depth=DEPTH, port=GUIPORT)]}))
		
        
        if "kraken" in subscriptions.keys():
			f.add_feed(Kraken(
				channels=[L2_BOOK, TRADES], 
				pairs=subscriptions['kraken'], 
				callbacks={
					TRADES: [TradeZMQ(port=KDBPORT), TradeZMQ(port=GUIPORT)],
					L2_BOOK: [BookZMQ(depth=DEPTH, port=KDBPORT), BookZMQ(depth=DEPTH, port=GUIPORT)]}))
		
        
        if "kraken_futures" in subscriptions.keys():
			f.add_feed(KrakenFutures(
				channels=[L2_BOOK, TRADES], 
				pairs=subscriptions['kraken_futures'], 
				callbacks={
					TRADES: [TradeZMQ(port=KDBPORT), TradeZMQ(port=GUIPORT)],
					L2_BOOK: [BookZMQ(depth=DEPTH, port=KDBPORT), BookZMQ(depth=DEPTH, port=GUIPORT)]}))
		
        
        if "binance" in subscriptions.keys():
			f.add_feed(Binance(
				channels=[L2_BOOK, TRADES], 
				pairs=subscriptions['binance'], 
				callbacks={
					TRADES: [TradeZMQ(port=KDBPORT), TradeZMQ(port=GUIPORT)],
					L2_BOOK: [BookZMQ(depth=DEPTH, port=KDBPORT), BookZMQ(depth=DEPTH, port=GUIPORT)]}))
		
        
        if "poloniex" in subscriptions.keys():
			f.add_feed(Poloniex(
				channels=[L2_BOOK, TRADES], 
				pairs=subscriptions['poloniex'], 
				callbacks={
					TRADES: [TradeZMQ(port=KDBPORT), TradeZMQ(port=GUIPORT)],
					L2_BOOK: [BookZMQ(depth=DEPTH, port=KDBPORT), BookZMQ(depth=DEPTH, port=GUIPORT)]}))
		
        
        if "bitfinex" in subscriptions.keys():
			f.add_feed(Bitfinex(
				channels=[L2_BOOK, TRADES], 
				pairs=subscriptions['bitfinex'], 
				callbacks={
					TRADES: [TradeZMQ(port=KDBPORT), TradeZMQ(port=GUIPORT)],
					L2_BOOK: [BookZMQ(depth=DEPTH, port=KDBPORT), BookZMQ(depth=DEPTH, port=GUIPORT)]}))
		
        
        if "bitstamp" in subscriptions.keys():
			f.add_feed(Bitstamp(
				channels=[L2_BOOK, TRADES], 
				pairs=subscriptions['bitstamp'], 
				callbacks={
					TRADES: [TradeZMQ(port=KDBPORT), TradeZMQ(port=GUIPORT)],
					L2_BOOK: [BookZMQ(depth=DEPTH, port=KDBPORT), BookZMQ(depth=DEPTH, port=GUIPORT)]}))
		
        
        if "gemini" in subscriptions.keys():
			f.add_feed(Gemini(
				channels=[L2_BOOK, TRADES], 
				pairs=subscriptions['gemini'], 
				callbacks={
					TRADES: [TradeZMQ(port=KDBPORT), TradeZMQ(port=GUIPORT)],
					L2_BOOK: [BookZMQ(depth=DEPTH, port=KDBPORT), BookZMQ(depth=DEPTH, port=GUIPORT)]}))

		f.run()

	except KeyboardInterrupt:
		pass

	finally:
		p.terminate()
		
		# save trades and quotes tables to disk
		data_path = os.getcwd()+"/data"
		data_path = data_path.replace("\\", "/")
        trades_path = f"`:{data_path}/trades set trades"
        quotes_path = f"`:{data_path}/quotes set quotes"
        print(f"saving to disk quotes -> {quotes_path} trades -> {trades_path}")
		q.sendSync(trades_path)
		q.sendSync(quotes_path)
		q.close()


if __name__ == '__main__':
	main()
