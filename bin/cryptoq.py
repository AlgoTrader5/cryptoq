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
    parser.add_argument("--q-port",    dest="port",      type=int, default=5002,                       help='QConnection port')
    parser.add_argument("--zmq-port",  dest="zmq_port",  type=int, default=5555,                       help='ZMQ port for kdb+ capture')
    parser.add_argument("--config",                      type=str, default='conf\\subscriptions.yaml', help='path to the config file')
    parser.add_argument("--depth",     dest="depth",     type=int, default=5,                          help='Order Book depth for kdb+')
    return parser.parse_args()

  
args = get_args()

# create connection object
q = qconnection.QConnection(host='localhost', port=args.port, pandas=True)
q.open()

# create quotes table in kdb+
q.sendSync(load_quote_schema(args.depth))


def receiver(port, depth):
    ctx = zmq.Context.instance()
    s = ctx.socket(zmq.SUB)
    s.setsockopt(zmq.SUBSCRIBE, b'')
    s.bind(f'tcp://127.0.0.1:{port}')

    while True:
        data = s.recv_string()
        # example topic might look like: COINBASE-book-LTC-BTC
        topic, msg = data.split(" ", 1)
        msg_type = topic.split("-")[1]
        qstr = ""
        if msg_type == "book":
            qstr = book_convert(topic, msg, depth)
        elif msg_type == "trades":
            qstr = trade_convert(topic, msg)
        else:
            print(f"Cannot recognize data message {data}!!!")
            return
        if qstr:
            try:
                q.sendSync(qstr, param=None)
            except QException as e:
                print(f"Error executing query {qStr} against server. {e}")


def main():
    args = get_args()
    print(f"\nq connection port : {args.port}" \
          f"\nzmq (kdb) port    : {args.zmq_port}" \
          f"\ndepth             : {args.depth}" \
          f"\nconfig            : {args.config}")
    
    subscriptions = read_cfg(args.config)
    print(f"IPC version: {q.protocol_version}. Is connected: {q.is_connected()}")
    
    try:
        p = Process(target=receiver, args=(args.zmq_port, args.depth,))
        p.start()
        f = FeedHandler()
        
        if "binance_us" in subscriptions.keys():
            f.add_feed(BinanceUS(
                max_depth=args.depth,
                channels=[L2_BOOK, TRADES], 
                pairs=subscriptions['binance_us'], 
                callbacks={
                    TRADES: [TradeZMQ(port=args.zmq_port)],
                    L2_BOOK: [BookZMQ(depth=args.depth, port=args.zmq_port)]}))
        
        if "coinbase" in subscriptions.keys():
            f.add_feed(Coinbase(
                max_depth=args.depth,
                channels=[L2_BOOK, TRADES], 
                pairs=subscriptions['coinbase'], 
                callbacks={
                    TRADES: [TradeZMQ(port=args.zmq_port)],
                    L2_BOOK: [BookZMQ(depth=args.depth, port=args.zmq_port)]}))
        
        if "kraken" in subscriptions.keys():
            f.add_feed(Kraken(
                channels=[L2_BOOK, TRADES], 
                pairs=subscriptions['kraken'], 
                callbacks={
                    TRADES: [TradeZMQ(port=args.zmq_port)],
                    L2_BOOK: [BookZMQ(depth=args.depth, port=args.zmq_port)]}))

        f.run()

    except KeyboardInterrupt:
        pass

    finally:
        p.terminate()
        # save trades and quotes tables to disk
        # data_path = os.getcwd()
        # data_path = data_path.replace("\\", "/")
        # trades_path = f"`:{data_path}/trades set trades"
        # quotes_path = f"`:{data_path}/quotes set quotes"
        # print(f"saving to disk quotes -> {quotes_path} trades -> {trades_path}")
        q.close()


if __name__ == '__main__':
    main()
