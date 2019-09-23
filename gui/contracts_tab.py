#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui
from subscriptions_list import SubscriptionsList
from symbol_list import SymbolList

class ContractsTab(QtWidgets.QWidget):

    def __init__(self, markets, subscriptions, parent=None):
        super(ContractsTab, self).__init__(parent)
        self.markets = markets
        self.symbol_list = SymbolList(self.markets)
        self.subscriptions_list = SubscriptionsList(subscriptions)
        self.add_btn = QtWidgets.QPushButton("add")
        self.add_btn.clicked.connect(self.on_click)
        
        self.radio_buttons = []
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.create_box_group())
        layout.addWidget(self.symbol_list)
        layout.addWidget(self.add_btn)
        layout.addWidget(self.subscriptions_list)
        self.setLayout(layout)


    def on_click(self, i):
        print('on click', i)
    

    def create_box_group(self):
        '''
        create box group containing radio buttons 
        for each exchange
        '''
        vbox = QtWidgets.QVBoxLayout()
        
        for exch, syms in self.markets.items():
            b = QtWidgets.QRadioButton(exch)
            b.clicked.connect(lambda: self.btnstate(b))
            self.radio_buttons.append(b)
            vbox.addWidget(b)
        
        vbox.addStretch(1)

        group_box = QtWidgets.QGroupBox()
        group_box.setLayout(vbox)
        return group_box
        

    def btnstate(self, b):
        for rb in self.radio_buttons:
            if rb.isChecked():
                self.symbol_list.select_exchange.emit(rb.text())
            
