import zmq
from datetime import datetime
from qpython import qconnection
from qpython.qtype import QException


class KdbQuoteRecorder:
    def __init__(self, zmqhost='127.0.0.1', zmqport=5556, kdbhost='localhost', kdbport=5002):
        self.kdbhost = kdbhost
        self.kdbport = kdbport
        self.zmqhost = zmqhost
        self.zmqport = zmqport
        self.addr = f"tcp://{self.zmqhost}:{self.zmqport}"
        self.ctx = zmq.Context.instance()
        self.con = self.ctx.socket(zmq.PULL)
        self.con.connect(self.addr)

        self.q = qconnection.QConnection(host=self.kdbhost, port=self.kdbport, pandas=True)
        self.q.open()
        print(f"is connected to {self.q}: {self.q.is_connected()}")

    def run(self):
        while self.q.is_connected():
            try:
                data = self.con.recv_json()
                qStr = self.data_convert(data)
                self.exequery(qStr)
            except Exception as e:
                print(f'ERROR QUERY: {qStr} {e}')

    def stop(self):
        self.q.close()

    def data_convert(self, data):
        hwt = str(datetime.utcnow().isoformat()).replace("T","D").replace("-",".")
        ts = str(datetime.fromtimestamp(data['data']['timestamp']).isoformat()).replace("T","D").replace("-",".")
        bid_price = list(data['data']['bid'])[0]
        bid_size = float(data['data']['bid'][bid_price])
        ask_price = list(data['data']['ask'])[0]
        ask_size = float(data['data']['ask'][ask_price])
        return f"`quotes insert (`timestamp${hwt};`timestamp${ts};" \
                f"`{data['feed']};`$\"{data['pair']}\";`float${bid_size};`float${bid_price};" \
                f"`float${ask_price};`float${ask_size})"

    def exequery(self, qStr, param=None):
        ''' used for insert/delete queries against server'''
        try:
            self.q.sendSync(qStr, param)
        except QException as e:
            print(f"Error executing query {qStr} against server. {e}")

def main():
    try:
        kdb = KdbQuoteRecorder(zmqhost='127.0.0.1', zmqport=5556, kdbhost='localhost', kdbport=5002)
        kdb.run()
    finally:
        print('stop')
        kdb.stop()

if __name__ == '__main__':
    main()
