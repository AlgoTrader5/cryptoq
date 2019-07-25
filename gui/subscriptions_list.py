#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtGui


class SubscriptionsList(QtWidgets.QTableWidget):
	contract_signal = QtCore.pyqtSignal(object)

	def __init__(self, subscriptions, parent=None):
		super(SubscriptionsList, self).__init__(parent)
		self.subscriptions = subscriptions
		self.init_table()

	def on_item_clicked(self, item):
		print(item.text())
		# self.contract_signal.emit()

	def dropEvent(self, event):
		index = self.indexAt(event.pos())
		print('index:', index, index.row())

	def init_table(self):
		# drag and drop funcionality
		# self.setAcceptDrops(True)
		# self.setDragDropOverwriteMode(False)

		self.headers = ['sym','quote','base','exchange']
		self.setColumnCount(len(self.headers))
		self.setHorizontalHeaderLabels(self.headers)
		self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
		self.verticalHeader().setVisible(False)
		self.setSortingEnabled(True)
		
		for exch, contracts in self.subscriptions.items():
			for sym in contracts:
				self.insertRow(0)
				self.setItem(0, 0, QtWidgets.QTableWidgetItem(sym))
				self.setItem(0, 1, QtWidgets.QTableWidgetItem(sym.split("-")[0]))
				self.setItem(0, 2, QtWidgets.QTableWidgetItem(sym.split("-")[1]))
				self.setItem(0, 3, QtWidgets.QTableWidgetItem(exch))
		self.resizeColumnsToContents()
