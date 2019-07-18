import zmq
import time
from pprint import pprint
from multiprocessing import Process

from cryptofeed.backends.zmq import BookZMQ, TradeZMQ
from cryptofeed import FeedHandler
from cryptofeed.exchanges import Coinbase, Kraken, Poloniex, Binance
from cryptofeed.defines import L3_BOOK, TRADES, L2_BOOK


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


def read_cfg(fileName, key=None):
    '''open config file'''
    import yaml
    print(f'reading config {fileName}')
    cfg = {}
    with open(fileName, 'r') as f:
        try:
            config = yaml.safe_load(f)
            f.close()
            # only grab exchange specific config
            if key:
                for k, v in config.items():
                    if key in k:
                        cfg[k] = config[k]
                return cfg
            else:
                return config
        except yaml.YAMLError as e:
            print(e)



def main():
        subscriptions = read_cfg(fileName="subscriptions.yaml")

        coinbase_tickers = subscriptions['coinbase']['pairs'] if 'coinbase' in subscriptions.keys() else None
        kraken_tickers = subscriptions['kraken']['pairs'] if 'kraken' in subscriptions.keys() else None
        poloniex_tickers = subscriptions['poloniex']['pairs'] if 'poloniex' in subscriptions.keys() else None
        binance_tickers = subscriptions['binance']['pairs'] if 'binance' in subscriptions.keys() else None

        try:
            
            # coinbase
            if coinbase_tickers:
                p1 = Process(target=trade_receiver, args=(5555,))
                p2 = Process(target=book_receiver, args=(5556,))
            
            # kraken
            if kraken_tickers:
                p3 = Process(target=trade_receiver, args=(5557,))
                p4 = Process(target=book_receiver, args=(5558,))
            
            # poloniex
            if poloniex_tickers:
                p5 = Process(target=trade_receiver, args=(5559,))
                p6 = Process(target=book_receiver, args=(5560,))
            
            # binance
            if binance_tickers:
                p7 = Process(target=trade_receiver, args=(5561,))
                p8 = Process(target=book_receiver, args=(5562,))

            # coinbase
            if coinbase_tickers:
                p1.start()
                p2.start()
                
            # kraken
            if kraken_tickers:
                p3.start()
                p4.start()
                
            # poloniex
            if poloniex_tickers:
                p5.start()
                p6.start()
                
            # binance
            if binance_tickers:
                p7.start()
                p8.start()


            f = FeedHandler()
            
            # coinbase
            if coinbase_tickers:
                f.add_feed(Coinbase(channels=[L2_BOOK, TRADES], pairs=cbpro_tickers, callbacks={TRADES: TradeZMQ(port=5555), L2_BOOK: BookZMQ(depth=1, port=5556)}))
            
            # kraken
            if kraken_tickers:
                f.add_feed(Kraken(channels=[L2_BOOK, TRADES], pairs=kraken_tickers, callbacks={TRADES: TradeZMQ(port=5557), L2_BOOK: BookZMQ(depth=1, port=5558)}))
            
            # poloniex
            if poloniex_tickers:
                f.add_feed(Poloniex(channels=[L2_BOOK, TRADES], pairs=poloniex_tickers, callbacks={TRADES: TradeZMQ(port=5559), L2_BOOK: BookZMQ(depth=1, port=5560)}))
            
            # binance
            if binance_tickers:
                f.add_feed(Binance(channels=[L2_BOOK, TRADES], pairs=binance_tickers, callbacks={TRADES: TradeZMQ(port=5561), L2_BOOK: BookZMQ(depth=1, port=5562)}))

            f.run()

        finally:
            # coinbase
            if coinbase_tickers:
                p1.terminate()
                p2.terminate()
            
            # kraken
            if kraken_tickers:
                p3.terminate()
                p4.terminate()

            # poloniex
            if poloniex_tickers:
                p5.terminate()
                p6.terminate()

            # binance
            if binance_tickers:
                p7.terminate()
                p8.terminate()

