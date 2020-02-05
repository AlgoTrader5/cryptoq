from cryptofeed import FeedHandler
from cryptofeed.exchanges import Coinbase

from cryptofeed.defines import TRADES, TICKER, L3_BOOK, L2_BOOK, BOOK_DELTA
from async_kdb_callback import AsyncKdbCallback


def main():
    f = FeedHandler(raw_message_capture=AsyncKdbCallback())
    f.add_feed(Coinbase(pairs=['BTC-USD'], channels=[L2_BOOK, TRADES]))
    f.run()


if __name__ == '__main__':
    main()
