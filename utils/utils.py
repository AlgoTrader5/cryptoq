import yaml
import json
from datetime import datetime

def read_cfg(fn: str) -> dict:    
    cfg = None
    with open(fn, 'r') as f:
        try:
            cfg = yaml.safe_load(f)
            f.close()
        except yaml.YAMLError as e:
            print(e)
    return cfg

def load_quote_schema(depth: int) -> str:
    """ Returns quote table schema to be loaded at start of q session.
    
    >>> load_quote_schema(2)
    
    'quotes:([]utc_datetime:`timestamp$();exch_datetime:`timestamp$();exch:`symbol$();sym:`symbol$(); \
             bsize:`float$();bid:`float$();ask:`float$();asize:`float$();bsize1:`float$();bid1:`float$(); \
             ask1:`float$();asize1:`float$())'
    """
    qstr = "quotes:([]" \
            "utc_datetime:`timestamp$();exch_datetime:`timestamp$();" \
            "exch:`symbol$();sym:`symbol$()"
    if depth > 1:
        for i in range(depth):
            if i == 0:
                qstr += ";bsize:`float$();bid:`float$();ask:`float$();asize:`float$()"
            else:
                qstr += f";bsize{i}:`float$();bid{i}:"
                qstr += f"`float$();ask{i}:`float$();asize{i}:`float$()"
        qstr += ")"
    else:
        qstr += ";bsize:`float$();bid:`float$();ask:`float$();asize:`float$())"
    return qstr

def trade_convert(topic, data: str) -> str:
    exch = topic.split("-")[0]
    pair = topic.split(" ", 2)[0].split("-", 2)[-1]

    data = json.loads(data)

    hwt = str(datetime.utcnow().isoformat()).replace("T","D").replace("-",".")
    try:
        ts = str(datetime.fromtimestamp(data['timestamp']).isoformat()).replace("T","D").replace("-",".")
    except Exception as e:
        # kraken futures
        ts = str(datetime.fromtimestamp(data['timestamp']/1000).isoformat()).replace("T","D").replace("-",".")
    
    side   = data['side']
    price  = data['price']
    amount = data['amount']
    
    # somtimes exchanges do not provide trade ID
    if data['id']:
        trade_id = data['id'] 
    else:
        trade_id = 0
    
    return f"`trades insert (`timestamp${hwt};`timestamp${ts};" \
            f"`{exch};`$\"{pair}\";`{side};`float${amount};" \
            f"`float${price};`$\"{trade_id}\")"


def book_convert(topic: str, data: str, depth: int) -> str:
    feed = topic.split("-")[0]
    pair = topic.split(" ", 2)[0].split("-", 2)[-1]

    # data = data.split(" ", 1)[1]
    data = json.loads(data)
    hwt = str(datetime.utcnow().isoformat()).replace("T","D").replace("-",".")

    if isinstance(data['timestamp'], str):
        ts = str(datetime.fromtimestamp(int(data['timestamp'])).isoformat()).replace("T","D").replace("-",".")
    else:
        ts = str(datetime.fromtimestamp(data['timestamp']).isoformat()).replace("T","D").replace("-",".")

    qstr = f"`quotes insert (`timestamp${hwt};`timestamp${ts};`{feed};`$\"{pair}\""
    if depth == 1:
        bid_price = list(data['bid'])[0]
        bid_size  = float(data['bid'][bid_price])
        ask_price = list(data['ask'])[0]
        ask_size  = float(data['ask'][ask_price])
        qstr += f";`float${bid_size};`float${bid_price};`float${ask_price};`float${ask_size})"
    else:
        for i in range(depth):
            bid_price = list(data['bid'])[i]
            bid_size  = float(data['bid'][bid_price])
            ask_price = list(data['ask'])[i]
            ask_size  = float(data['ask'][ask_price])
            qstr += f";`float${bid_size};`float${bid_price}"
            qstr += f";`float${ask_price};`float${ask_size}"
        qstr += ")"
    return qstr
