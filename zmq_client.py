import zmq
import time
import argparse
from multiprocessing import Process

from qpython import qconnection
from qpython.qtype import QException

from cryptofeed.backends.zmq import BookZMQ, TradeZMQ
from cryptofeed import FeedHandler
from cryptofeed.exchanges import Coinbase, Kraken
from cryptofeed.defines import TRADES, L2_BOOK

from utils import read_cfg, trade_convert, book_convert


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help='QConnection port')
args = parser.parse_args()


# create connection object
q = qconnection.QConnection(host='localhost', port=int(args.port), pandas=True)
# initialize connection
q.open()



def book_receiver(port):
    addr = 'tcp://127.0.0.1:{}'.format(port)
    print(f'book receiver address: {addr}')
    ctx = zmq.Context.instance()
    s = ctx.socket(zmq.SUB)
    s.setsockopt(zmq.SUBSCRIBE, b'')

    s.bind(addr)
    while True:
        data = s.recv_string()
        qStr = book_convert(data)
        try:
            q.sendSync(qStr, param=None)
        except QException as e:
            print(f"Error executing query {qStr} against server. {e}")


def trade_receiver(port):
    addr = 'tcp://127.0.0.1:{}'.format(port)
    print(f'trade receiver address: {addr}')
    ctx = zmq.Context.instance()
    s = ctx.socket(zmq.SUB)
    s.setsockopt(zmq.SUBSCRIBE, b'')

    s.bind(addr)
    while True:
        data = s.recv_string()
        qStr = trade_convert(data)
        try:
            q.sendSync(qStr, param=None)
        except QException as e:
            print(f"Error executing query {qStr} against server. {e}")


def main():
        import os
        
        subscriptions = read_cfg("conf//subscriptions.yaml")
        coinbase_tickers = subscriptions['coinbase']['pairs']
        kraken_tickers = subscriptions['kraken']['pairs']

        print(f"IPC version: {q.protocol_version}. Is connected: {q.is_connected()}")

        try:
            p1 = Process(target=trade_receiver, args=(5555,))
            p2 = Process(target=book_receiver, args=(5556,))
            p3 = Process(target=trade_receiver, args=(5557,))
            p4 = Process(target=book_receiver, args=(5558,))
            
            p1.start()
            p2.start()
            p3.start()
            p4.start() 

            f = FeedHandler()
            
            f.add_feed(Coinbase(
                channels=[L2_BOOK, TRADES], 
                pairs=coinbase_tickers, 
                callbacks={
                    TRADES: TradeZMQ(port=5555), 
                    L2_BOOK: BookZMQ(depth=1, port=5556)}))
            
            f.add_feed(Kraken(
                channels=[L2_BOOK, TRADES], 
                pairs=kraken_tickers, 
                callbacks={
                    TRADES: TradeZMQ(port=5557), 
                    L2_BOOK: BookZMQ(depth=1, port=5558)}))


            f.run()

        finally:
            p1.terminate()
            p2.terminate()
            p3.terminate()
            p4.terminate()
            
            # save trades and quotes tables to disk
            data_path = "d:/repos/cryptoq/data"
            q.sendSync(f"`:{data_path}/trades set trades")
            q.sendSync(f"`:{data_path}/quotes set quotes")
            q.close()
            
if __name__ in "__main__":
    main()
