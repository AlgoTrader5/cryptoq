from qpython import qconnection
from qpython.qtype import QException


class KdbClient(object):
	def __init__(self, host, port):
		self.q = qconnection.QConnection(host=host, port=port, pandas=True)
		self.q.open()
		try:
			print('is connected to %s: %s'% (str(self.q), self.q.is_connected()))
		except QException as e:
			print("Error connecting to kdb:\n%s"% e)

	
	def query(self, qStr, param=None):
		''' used for querying data from server'''
		try:
			self.q.query(qconnection.MessageType.SYNC, qStr, param)
			msg = self.q.receive(data_only=False, raw=False)
			return msg.data
		except QException as e:
			print(f"Error querying from {qStr} server:\n{e}")

	
	def exequery(self, qStr, param=None):
		''' used for insert/delete queries against server'''
		try:
			self.q.sendSync(qStr, param)
		except QException as e:
			print(f"Error executing against {qStr} server:\n{e}")

	def close(self):
		print(f"closing connection to {self.q}")
		try:
			self.q.close()
		except QException as e:
			print(f"Error closing kdb:\n{e}")
