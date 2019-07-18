import zmq
import time
from pprint import pprint
from multiprocessing import Process

from cryptofeed.backends.zmq import BookZMQ, TradeZMQ
from cryptofeed import FeedHandler
from cryptofeed.exchanges import Coinbase
from cryptofeed.defines import TRADES, L2_BOOK


def book_receiver(port):
    addr = 'tcp://127.0.0.1:{}'.format(port)
    print(f'book receiver address: {addr}')
    ctx = zmq.Context.instance()
    s = ctx.socket(zmq.PULL)
    s.connect(addr)
    while True:
        data = s.recv_json()


def trade_receiver(port):
    addr = 'tcp://127.0.0.1:{}'.format(port)
    print(f'trade receiver address: {addr}')
    ctx = zmq.Context.instance()
    s = ctx.socket(zmq.PULL)
    s.connect(addr)
    while True:
        data = s.recv_json()


def read_cfg(fn):
    import yaml
    print(f'reading config {fn}')
    cfg = None
    with open(fn, 'r') as f:
        try:
            cfg = yaml.safe_load(f)
            f.close()
        except yaml.YAMLError as e:
            print(e)
    return cfg



def main():
        subscriptions = read_cfg("conf//subscriptions.yaml")
        coinbase_tickers = subscriptions['coinbase']['pairs']

        try:
            p1 = Process(target=trade_receiver, args=(5555,))
            p2 = Process(target=book_receiver, args=(5556,))
            
            p1.start()
            p2.start()     

            f = FeedHandler()
            f.add_feed(Coinbase(channels=[L2_BOOK, TRADES], pairs=coinbase_tickers, callbacks={TRADES: TradeZMQ(port=5555), L2_BOOK: BookZMQ(depth=1, port=5556)}))
            f.run()

        finally:
            p1.terminate()
            p2.terminate()
            
if __name__ in "__main__":
    main()
