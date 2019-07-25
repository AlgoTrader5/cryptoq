#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtGui


class SymbolList(QtWidgets.QTableWidget):
    select_exchange = QtCore.pyqtSignal(str)

    def __init__(self, clients, parent=None):
        super(ContractsList, self).__init__(parent)
        self.clients = clients
        self.init_table()
        self.select_exchange.connect(self.change_symbols)


    def on_item_clicked(self, item):
        print(item.text())


    def init_table(self):
        # drag and drop funcionality
        # self.setDragEnabled(True)
        # self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # self.setDragDropOverwriteMode(False)
        # self.setDragDropOverwriteMode(False)
        # self.last_drop_row = None
        
        self.headers = ['sym','quote','base','exchange']
        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)
        self.verticalHeader().setVisible(False)
        self.setSortingEnabled(True)

        exch = 'coinbase'
        syms = self.clients[exch]
        for sym in syms:
            self.insertRow(0)
            self.setItem(0, 0, QtWidgets.QTableWidgetItem(sym))
            self.setItem(0, 1, QtWidgets.QTableWidgetItem(sym.split("-")[0]))
            self.setItem(0, 2, QtWidgets.QTableWidgetItem(sym.split("-")[1]))
            self.setItem(0, 3, QtWidgets.QTableWidgetItem(exch))
        self.resizeColumnsToContents()


    def change_symbols(self, exch):
        self.clear()
        self.setRowCount(0)
        self.setHorizontalHeaderLabels(self.headers)
        syms = self.clients[exch]
        for sym in syms:
            self.insertRow(0)
            self.setItem(0, 0, QtWidgets.QTableWidgetItem(sym))
            self.setItem(0, 1, QtWidgets.QTableWidgetItem(sym.split("-")[0]))
            self.setItem(0, 2, QtWidgets.QTableWidgetItem(sym.split("-")[1]))
            self.setItem(0, 3, QtWidgets.QTableWidgetItem(exch))
        self.resizeColumnsToContents()
