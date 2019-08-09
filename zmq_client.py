import os
import zmq
import time
import argparse
from multiprocessing import Process

from qpython import qconnection
from qpython.qtype import QException

from cryptofeed.backends.zmq import BookZMQ, TradeZMQ
from cryptofeed import FeedHandler
from cryptofeed.exchanges import Coinbase, Kraken, Binance, Poloniex
from cryptofeed.defines import TRADES, L2_BOOK

from utils import read_cfg, trade_convert, book_convert


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help='QConnection port')
parser.add_argument("-d", "--depth", help='Order book depth')
args = parser.parse_args()

PORT = int(args.port)
DEPTH = int(args.depth)

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
            qStr = book_convert(data)
        else:
            qStr = trade_convert(data)
        try:
            q.sendSync(qStr, param=None)
        except QException as e:
            print(f"Error executing query {qStr} against server. {e}")


def main():
    subscriptions = read_cfg("conf//subscriptions.yaml")
    coinbase_tickers = subscriptions['coinbase']
    kraken_tickers = subscriptions['kraken']
    binance_tickers = subscriptions['binance']
    poloniex_tickers = subscriptions['poloniex']

    print(f"IPC version: {q.protocol_version}. Is connected: {q.is_connected()}")

    try:
        p = Process(target=receiver, args=(5555,))
        p.start()

        f = FeedHandler()
        
        f.add_feed(Coinbase(
            channels=[L2_BOOK, TRADES], 
            pairs=coinbase_tickers, 
            callbacks={
                TRADES: [TradeZMQ(port=5555), TradeZMQ(port=5556)],
                L2_BOOK: [BookZMQ(depth=DEPTH, port=5555), BookZMQ(depth=DEPTH, port=5556)]}))
        
        f.add_feed(Kraken(
            channels=[L2_BOOK, TRADES], 
            pairs=kraken_tickers, 
            callbacks={
                TRADES: [TradeZMQ(port=5555), TradeZMQ(port=5556)],
                L2_BOOK: [BookZMQ(depth=DEPTH, port=5555), BookZMQ(depth=DEPTH, port=5556)]}))
        
        f.add_feed(Binance(
            channels=[L2_BOOK, TRADES], 
            pairs=binance_tickers, 
            callbacks={
                TRADES: [TradeZMQ(port=5555), TradeZMQ(port=5556)],
                L2_BOOK: [BookZMQ(depth=DEPTH, port=5555), BookZMQ(depth=DEPTH, port=5556)]}))

        f.add_feed(Poloniex(
            channels=[L2_BOOK, TRADES], 
            pairs=poloniex_tickers, 
            callbacks={
                TRADES: [TradeZMQ(port=5555), TradeZMQ(port=5556)],
                L2_BOOK: [BookZMQ(depth=DEPTH, port=5555), BookZMQ(depth=DEPTH, port=5556)]}))

        f.run()

    finally:
        p.terminate()
        
        # save trades and quotes tables to disk
        data_path = "d:/repos/cryptoq/data"
        q.sendSync(f"`:{data_path}/trades set trades")
        q.sendSync(f"`:{data_path}/quotes set quotes")
        q.close()
            
if __name__ in "__main__":
    main()
