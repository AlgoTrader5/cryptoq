import yaml
from datetime import datetime


def read_cfg(fn):    
    print(f'reading config {fn}')
    cfg = None
    with open(fn, 'r') as f:
        try:
            cfg = yaml.safe_load(f)
            f.close()
        except yaml.YAMLError as e:
            print(e)
    return cfg

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


