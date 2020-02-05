import os
import zmq
import time
import argparse

from cryptofeed import FeedHandler
from cryptofeed.backends.zmq import BookZMQ, TradeZMQ
from cryptofeed.defines import TRADES, L2_BOOK
from cryptofeed.exchanges import BinanceUS, Coinbase

from utils.utils import read_cfg, trade_convert, book_convert, load_quote_schema

def get_args():
        parser = argparse.ArgumentParser()
        parser.add_argument("--port",  dest="port", type=int,default=5556, help='ZMQ port')
        parser.add_argument("--config",             type=str,default='conf\\subscriptions.yaml', help='path to the config file')
        parser.add_argument("--depth", dest="depth",type=int,default=1, help='Order Book depth')
        return parser.parse_args()

args = get_args()

CONFIG = args.config
PORT   = args.port
DEPTH  = args.depth


def main():
        print(f"zmq port    : {PORT}" \
          f"\ndepth         : {DEPTH}" \
          f"\nconfig        : {CONFIG}")


        subscriptions = read_cfg(CONFIG)

        try:
                f = FeedHandler()

                if "binance_us" in subscriptions.keys():
                        f.add_feed(BinanceUS(max_depth=DEPTH, channels=[L2_BOOK, TRADES], pairs=subscriptions['binance_us'],
                                callbacks={TRADES: [TradeZMQ(port=PORT)], L2_BOOK: [BookZMQ(depth=DEPTH, port=PORT)]}))

                if "coinbase" in subscriptions.keys():
                        f.add_feed(Coinbase(max_depth=DEPTH, channels=[L2_BOOK, TRADES], pairs=subscriptions['coinbase'],
                                callbacks={TRADES: [TradeZMQ(port=PORT)], L2_BOOK: [BookZMQ(depth=DEPTH, port=PORT)]}))

                f.run()

        except KeyboardInterrupt:
                pass


if __name__ == '__main__':
        main()
