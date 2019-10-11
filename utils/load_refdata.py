# -*- coding: utf-8 -*-
import os
import sys
import time
import argparse
from pprint import pprint
import asyncio
import ccxt
import ccxt.async_support as ccxta  # noqa: E402
from qpython import qconnection
from qpython.qtype import QException


root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')


# parse args from command line
parser = argparse.ArgumentParser()
parser.add_argument("--q-port", dest="q_port", type=int, default=5002, help='QConnection port')
args = parser.parse_args()

# create connection object
q = qconnection.QConnection(host='localhost', port=args.q_port, pandas=True)
# initialize connection
q.open()
print(f"IPC version: {q.protocol_version}. Is connected: {q.is_connected()}")


async def async_client(exchange):
    client = getattr(ccxta, exchange)()
    markets = await client.load_markets()
    await client.close()
    return {exchange: markets}


async def multi_tickers(exchanges):
    input_coroutines = [async_client(exchange) for exchange in exchanges]
    markets = await asyncio.gather(*input_coroutines, return_exceptions=True)
    return markets


def insert_data(exch, sym, refdata):
    if exch=='kraken' and '.d' in sym:
        return
    try:
        makerFee = refdata['maker'] if not isinstance(refdata['maker'], type(None)) else 0.0
        takerFee = refdata['taker'] if not isinstance(refdata['taker'], type(None)) else 0.0
    except KeyError as e:
        makerFee = 0.0
        takerFee = 0.0

    try:
        minTick = refdata['limits']['price']['min'] \
                if refdata['limits']['price']['min'] else 0.0
        minSize = refdata['limits']['amount']['min'] \
                if refdata['limits']['amount']['min'] else 0.0
    except KeyError as e:
        minTick = 0.0
        minSize = 0.0


    qStr = f"`refdata insert (`$\"{sym}\";`$\"{exch}\";" \
            f"`float${minTick};`float${minSize};" \
            f"`float${makerFee};`float${takerFee})"
    
    try:
        q.sendSync(qStr, param=None)
    except QException as e:
        print(f"Error executing query {qStr} against server. {e}")

        


def main():
    from pprint import pprint

    # Consider review request rate limit in the methods you call
    exchanges = [
        "bitmex", "bittrex", "bitfinex", "bitstamp", "binance",
        "poloniex", "hitbtc", "coinbasepro", "kraken", "gemini",
        "okex", "exx"
    ]

    tic = time.time()
    markets = asyncio.get_event_loop().run_until_complete(multi_tickers(exchanges))
    print("async call spend:", time.time() - tic)
    time.sleep(1)
    
    # write to kdb
    for market in markets:
        for exchange, refdata in market.items():
            for sym, ref in refdata.items():
                insert_data(exchange, sym, ref)
    
    q.sendSync("show `sym xdesc select count sym by exch from refdata")
    q.close()
    time.sleep(3)
    
if __name__ == '__main__':
    main()

