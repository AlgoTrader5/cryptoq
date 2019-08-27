# -*- coding: utf-8 -*-
import asyncio
import ccxt
import ccxt.async_support as ccxta  # noqa: E402
import time
import os
import sys
import argparse
from qpython import qconnection
from qpython.qtype import QException


root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')


# parse args from command line
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, help='QConnection port')
args = parser.parse_args()

# create connection object
q = qconnection.QConnection(host='localhost', port=args.port, pandas=True)
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
	makerFee = refdata['maker']
	takerFee = refdata['taker']
	minTick = refdata['limits']['price']['min']
	minSize = refdata['limits']['amount']['min']
	
	qStr = f"`refdata insert (`$\"{sym}\";`$\"{exch}\";" \
			f"`float${minTick};`float${minSize};" \
			f"`float${makerFee};`float${takerFee})"
	try:
		q.sendSync(qStr, param=None)
	except QException as e:
		print(f"Error executing query {qStr} against server. {e}")

		
if __name__ == '__main__':
	from pprint import pprint

	# Consider review request rate limit in the methods you call
	exchanges = [
		"coinex", "bitmex", "bittrex", "bitfinex", "poloniex", "hitbtc", 
		"coinbasepro", "kraken", "binance", "bitstamp", "gemini",
		"okex", "kucoin", "exx"
	]

	tic = time.time()
	markets = asyncio.get_event_loop().run_until_complete(multi_tickers(exchanges))
	print("async call spend:", time.time() - tic)
	
	# write to kdb
	for market in markets:
		for exchange, refdata in market.items():
			for sym, ref in refdata.items():
				insert_data(exchange, sym, ref)
	
	

