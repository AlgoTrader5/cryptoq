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
    qStr = "quotes:([]" \
            "utc_datetime:`timestamp$();exch_datetime:`timestamp$();" \
            "exch:`symbol$();sym:`symbol$()"
    if depth > 1:
        for i in range(depth):
            if i == 0:
                qStr += ";bsize:`float$();bid:`float$();ask:`float$();asize:`float$()"
            else:
                qStr += f";bsize{i}:`float$();bid{i}:"
                qStr += f"`float$();ask{i}:`float$();asize{i}:`float$()"
        qStr += ")"
    else:
        qStr += ";bsize:`float$();bid:`float$();ask:`float$();asize:`float$())"

    return qStr

def trade_convert(data: str) -> str:
    exch = data.split("-")[0]
    pair = data.split(" ", 2)[0].split("-", 2)[-1]

    data = data.split(" ", 1)[1]
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
    
    if data['id']:
        trade_id = data['id'] 
    else:
        trade_id = 0
    return f"`trades insert (`timestamp${hwt};`timestamp${ts};" \
            f"`{exch};`$\"{pair}\";`{side};`float${amount};" \
            f"`float${price};`$\"{trade_id}\")"


def book_convert(data: str, depth: int) -> str:
    feed = data.split("-")[0]
    pair = data.split(" ", 2)[0].split("-", 2)[-1]

    data = data.split(" ", 1)[1]
    data = json.loads(data)
    hwt = str(datetime.utcnow().isoformat()).replace("T","D").replace("-",".")

    if isinstance(data['timestamp'], str):
        ts = str(datetime.fromtimestamp(int(data['timestamp'])).isoformat()).replace("T","D").replace("-",".")
    else:
        ts = str(datetime.fromtimestamp(data['timestamp']).isoformat()).replace("T","D").replace("-",".")

    qStr = f"`quotes insert (`timestamp${hwt};`timestamp${ts};`{feed};`$\"{pair}\""
    if depth == 1:
        bid_price = list(data['bid'])[0]
        bid_size  = float(data['bid'][bid_price])
        ask_price = list(data['ask'])[0]
        ask_size  = float(data['ask'][ask_price])
        qStr += f";`float${bid_size};`float${bid_price};`float${ask_price};`float${ask_size})"
    else:
        for i in range(depth):
            bid_price = list(data['bid'])[i]
            bid_size  = float(data['bid'][bid_price])
            ask_price = list(data['ask'])[i]
            ask_size  = float(data['ask'][ask_price])
            qStr += f";`float${bid_size};`float${bid_price}"
            qStr += f";`float${ask_price};`float${ask_size}"

        qStr += ")"
    return qStr
