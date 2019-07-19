import zmq
import time
import argparse
from datetime import datetime
from multiprocessing import Process

from qpython import qconnection
from qpython.qtype import QException

from cryptofeed.backends.zmq import BookZMQ, TradeZMQ
from cryptofeed import FeedHandler
from cryptofeed.exchanges import Coinbase
from cryptofeed.defines import TRADES, L2_BOOK


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help='QConnection port')
args = parser.parse_args()


q = qconnection.QConnection(host='localhost', port=int(args.port), pandas=True)
q.open()
print(f"is connected to {q}: {q.is_connected()}")


def book_receiver(port):
    addr = 'tcp://127.0.0.1:{}'.format(port)
    print(f'book receiver address: {addr}')
    ctx = zmq.Context.instance()
    s = ctx.socket(zmq.PULL)
    s.connect(addr)
    while True:
        data = s.recv_json()
        qStr = book_convert(data)
        try:
            q.sendSync(qStr, param=None)
        except QException as e:
            print(f"Error executing query {qStr} against server. {e}")


def trade_receiver(port):
    addr = 'tcp://127.0.0.1:{}'.format(port)
    print(f'trade receiver address: {addr}')
    ctx = zmq.Context.instance()
    s = ctx.socket(zmq.PULL)
    s.connect(addr)

    while True:
        data = s.recv_json()
        qStr = trade_convert(data)
        try:
            q.sendSync(qStr, param=None)
        except QException as e:
            print(f"Error executing query {qStr} against server. {e}")


def trade_convert(data):
    hwt = str(datetime.utcnow().isoformat()).replace("T","D").replace("-",".")
    ts = str(datetime.fromtimestamp(data['data']['timestamp']).isoformat()).replace("T","D").replace("-",".")
    exch = data['data']['feed']
    pair = data['data']['pair']
    side = data['data']['side']
    price = data['data']['price']
    amount = data['data']['amount']
    order_id = data['data']['id']
    return f"`trades insert (`timestamp${hwt};`timestamp${ts};" \
            f"`{exch};`$\"{pair}\";`{side};`float${amount};" \
            f"`float${price};`int${order_id})"


def book_convert(data):
    hwt = str(datetime.utcnow().isoformat()).replace("T","D").replace("-",".")
    ts = str(datetime.fromtimestamp(data['data']['timestamp']).isoformat()).replace("T","D").replace("-",".")
    bid_price = list(data['data']['bid'])[0]
    bid_size = float(data['data']['bid'][bid_price])
    ask_price = list(data['data']['ask'])[0]
    ask_size = float(data['data']['ask'][ask_price])
    return f"`quotes insert (`timestamp${hwt};`timestamp${ts};" \
            f"`{data['feed']};`$\"{data['pair']}\";`float${bid_size};" \
            f"`float${bid_price};`float${ask_price};`float${ask_size})"

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
            f.add_feed(
                Coinbase(
                    channels=[L2_BOOK, TRADES], 
                    pairs=coinbase_tickers, 
                    callbacks={
                        TRADES: TradeZMQ(port=5555), 
                        L2_BOOK: BookZMQ(depth=1, port=5556)}))
            f.run()

        finally:
            p1.terminate()
            p2.terminate()    
            
if __name__ in "__main__":
    main()
