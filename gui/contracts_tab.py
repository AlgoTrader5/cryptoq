#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui
from subscriptions_list import SubscriptionsList
from symbol_list import SymbolList

class ContractsTab(QtWidgets.QWidget):

    def __init__(self, clients, subscriptions, parent=None):
        super(ContractsTab, self).__init__(parent)
        self.symbol_list = SymbolList(clients)
        self.subscriptions_list = SubscriptionsList(subscriptions)
        self.add_btn = QtWidgets.QPushButton("add")
        self.add_btn.clicked.connect(self.on_click)
        
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.create_box_group())
        layout.addWidget(self.symbol_list)
        layout.addWidget(self.add_btn)
        layout.addWidget(self.subscriptions_list)
        self.setLayout(layout)


    def on_click(self, i):
        print('on click', i)
    

    def create_box_group(self):
        group_box = QtWidgets.QGroupBox()
        self.b1 = QtWidgets.QRadioButton("coinbase")
        self.b1.setChecked(True)
        self.b1.toggled.connect(lambda:self.btnstate(self.b1))
        self.b2 = QtWidgets.QRadioButton("kraken")
        self.b2.toggled.connect(lambda:self.btnstate(self.b2))
        self.b3 = QtWidgets.QRadioButton("binance")
        self.b3.toggled.connect(lambda:self.btnstate(self.b3))
        self.b4 = QtWidgets.QRadioButton("poloniex")
        self.b4.toggled.connect(lambda:self.btnstate(self.b4))
        self.b5 = QtWidgets.QRadioButton("bitfinex")
        self.b5.toggled.connect(lambda:self.btnstate(self.b5))
        self.b6 = QtWidgets.QRadioButton("bitstamp")
        self.b6.toggled.connect(lambda:self.btnstate(self.b6))
        self.b7 = QtWidgets.QRadioButton("gemini")
        self.b7.toggled.connect(lambda:self.btnstate(self.b7))
        self.b8 = QtWidgets.QRadioButton("huobi")
        self.b8.toggled.connect(lambda:self.btnstate(self.b8))
        self.b9 = QtWidgets.QRadioButton("okex")
        self.b9.toggled.connect(lambda:self.btnstate(self.b9))
        self.b10 = QtWidgets.QRadioButton("okcoin")
        self.b10.toggled.connect(lambda:self.btnstate(self.b10))
        self.b11 = QtWidgets.QRadioButton("exx")
        self.b11.toggled.connect(lambda:self.btnstate(self.b11))
        self.b12 = QtWidgets.QRadioButton("bybit")
        self.b12.toggled.connect(lambda:self.btnstate(self.b12))


        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.b1)
        vbox.addWidget(self.b2)
        vbox.addWidget(self.b3)
        vbox.addWidget(self.b4)
        vbox.addWidget(self.b5)
        vbox.addWidget(self.b6)
        vbox.addWidget(self.b7)
        vbox.addWidget(self.b8)
        vbox.addWidget(self.b9)
        vbox.addWidget(self.b10)
        vbox.addWidget(self.b11)
        vbox.addWidget(self.b12)
        vbox.addStretch(1)
        group_box.setLayout(vbox)
        return group_box
        

    def btnstate(self,b):
        if b.isChecked():
            self.symbol_list.select_exchange.emit(b.text())



