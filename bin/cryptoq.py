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
from cryptofeed.exchanges import (Binance, Bitmex, Bitfinex, Bittrex, Bitstamp, Bybit, 
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
		
		if "binance" in subscriptions.keys():
			f.add_feed(Binance(
                max_depth=KDBDEPTH,
				channels=[L2_BOOK, TRADES], 
				pairs=subscriptions['binance'], 
				callbacks={
					TRADES: [TradeZMQ(port=KDBPORT), TradeZMQ(port=GUIPORT)],
					L2_BOOK: [BookZMQ(depth=KDBDEPTH, port=KDBPORT), BookZMQ(depth=GUIDEPTH, port=GUIPORT)]}))
            
            
		if "bitmex" in subscriptions.keys():
			f.add_feed(Bitmex(
                max_depth=KDBDEPTH,
				channels=[L2_BOOK, TRADES], 
				pairs=subscriptions['bitmex'], 
				callbacks={
					TRADES: [TradeZMQ(port=KDBPORT), TradeZMQ(port=GUIPORT)],
					L2_BOOK: [BookZMQ(depth=KDBDEPTH, port=KDBPORT), BookZMQ(depth=GUIDEPTH, port=GUIPORT)]}))
			
            
		if "bitfinex" in subscriptions.keys():
			f.add_feed(Bitfinex(
                max_depth=KDBDEPTH,
				channels=[L2_BOOK, TRADES], 
				pairs=subscriptions['bitfinex'], 
				callbacks={
					TRADES: [TradeZMQ(port=KDBPORT), TradeZMQ(port=GUIPORT)],
					L2_BOOK: [BookZMQ(depth=KDBDEPTH, port=KDBPORT), BookZMQ(depth=GUIDEPTH, port=GUIPORT)]}))
            
            
		if "bittrex" in subscriptions.keys():
			f.add_feed(Bitrex(
                max_depth=KDBDEPTH,
				channels=[L2_BOOK, TRADES], 
				pairs=subscriptions['bittrex'], 
				callbacks={
					TRADES: [TradeZMQ(port=KDBPORT), TradeZMQ(port=GUIPORT)],
					L2_BOOK: [BookZMQ(depth=KDBDEPTH, port=KDBPORT), BookZMQ(depth=GUIDEPTH, port=GUIPORT)]}))
		
		
		if "bitstamp" in subscriptions.keys():
			f.add_feed(Bitstamp(
                max_depth=KDBDEPTH,
				channels=[L2_BOOK, TRADES], 
				pairs=subscriptions['bitstamp'], 
				callbacks={
					TRADES: [TradeZMQ(port=KDBPORT), TradeZMQ(port=GUIPORT)],
					L2_BOOK: [BookZMQ(depth=KDBDEPTH, port=KDBPORT), BookZMQ(depth=GUIDEPTH, port=GUIPORT)]}))
            
            
		if "bybit" in subscriptions.keys():
			f.add_feed(Bybit(
                max_depth=KDBDEPTH,
				channels=[L2_BOOK, TRADES], 
				pairs=subscriptions['bybit'], 
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
            
            
		if "coinbene" in subscriptions.keys():
			f.add_feed(Coinbene(
                max_depth=KDBDEPTH,
				channels=[L2_BOOK, TRADES], 
				pairs=subscriptions['coinbene'], 
				callbacks={
					TRADES: [TradeZMQ(port=KDBPORT), TradeZMQ(port=GUIPORT)],
					L2_BOOK: [BookZMQ(depth=KDBDEPTH, port=KDBPORT), BookZMQ(depth=GUIDEPTH, port=GUIPORT)]}))
            
            
		if "deribit" in subscriptions.keys():
			f.add_feed(Deribit(
                max_depth=KDBDEPTH,
				channels=[L2_BOOK, TRADES], 
				pairs=subscriptions['deribit'], 
				callbacks={
					TRADES: [TradeZMQ(port=KDBPORT), TradeZMQ(port=GUIPORT)],
					L2_BOOK: [BookZMQ(depth=KDBDEPTH, port=KDBPORT), BookZMQ(depth=GUIDEPTH, port=GUIPORT)]}))
            
            
		if "exx" in subscriptions.keys():
			f.add_feed(EXX(
                max_depth=KDBDEPTH,
				channels=[L2_BOOK, TRADES], 
				pairs=subscriptions['exx'], 
				callbacks={
					TRADES: [TradeZMQ(port=KDBPORT), TradeZMQ(port=GUIPORT)],
					L2_BOOK: [BookZMQ(depth=KDBDEPTH, port=KDBPORT), BookZMQ(depth=GUIDEPTH, port=GUIPORT)]}))
            
            
		if "ftx" in subscriptions.keys():
			f.add_feed(FTX(
                max_depth=KDBDEPTH,
				channels=[L2_BOOK, TRADES], 
				pairs=subscriptions['ftx'], 
				callbacks={
					TRADES: [TradeZMQ(port=KDBPORT), TradeZMQ(port=GUIPORT)],
					L2_BOOK: [BookZMQ(depth=KDBDEPTH, port=KDBPORT), BookZMQ(depth=GUIDEPTH, port=GUIPORT)]}))
            
            
		if "gemini" in subscriptions.keys():
			f.add_feed(Gemini(
                max_depth=KDBDEPTH,
				channels=[L2_BOOK, TRADES], 
				pairs=subscriptions['gemini'], 
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
		
		
		if "kraken_futures" in subscriptions.keys():
			f.add_feed(KrakenFutures(
                max_depth=KDBDEPTH,
				channels=[L2_BOOK, TRADES], 
				pairs=subscriptions['kraken_futures'], 
				callbacks={
					TRADES: [TradeZMQ(port=KDBPORT), TradeZMQ(port=GUIPORT)],
					L2_BOOK: [BookZMQ(depth=KDBDEPTH, port=KDBPORT), BookZMQ(depth=GUIDEPTH, port=GUIPORT)]}))
		

		if "okcoin" in subscriptions.keys():
			f.add_feed(OKCoin(
                max_depth=KDBDEPTH,
				channels=[L2_BOOK, TRADES], 
				pairs=subscriptions['okcoin'], 
				callbacks={
					TRADES: [TradeZMQ(port=KDBPORT), TradeZMQ(port=GUIPORT)],
					L2_BOOK: [BookZMQ(depth=KDBDEPTH, port=KDBPORT), BookZMQ(depth=GUIDEPTH, port=GUIPORT)]}))
		
		
		if "okex" in subscriptions.keys():
			f.add_feed(OKEx(
                max_depth=KDBDEPTH,
				channels=[L2_BOOK, TRADES], 
				pairs=subscriptions['okex'], 
				callbacks={
					TRADES: [TradeZMQ(port=KDBPORT), TradeZMQ(port=GUIPORT)],
					L2_BOOK: [BookZMQ(depth=KDBDEPTH, port=KDBPORT), BookZMQ(depth=GUIDEPTH, port=GUIPORT)]}))
		
		
		if "poloniex" in subscriptions.keys():
			f.add_feed(Poloniex(
                max_depth=KDBDEPTH,
				channels=[L2_BOOK, TRADES], 
				pairs=subscriptions['poloniex'], 
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
