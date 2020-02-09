from qpython import qconnection
from qpython.qtype import QException


class KdbClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.conn = qconnection.QConnection(host=self.host, port=self.port, pandas=True)

    def open(self):
        self.conn.open()
        print(f'IPC version: {self.conn.protocol_version}. Is connected: {self.conn.is_connected()}')

    def insert(self, qstr):
        try:
            return self.conn.sendSync(qstr, param=None)
        except QException as e:
            print(f"Error executing query {qstr} against server. {e}")
        return


    def close(self):
        self.conn.close()

