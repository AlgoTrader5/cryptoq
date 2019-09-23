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
        self.radio_buttons = []
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.create_radio_box_group())
        layout.addWidget(self.symbol_list)
        layout.addWidget(self.create_button_box_group())
        layout.addWidget(self.subscriptions_list)
        self.setLayout(layout)


    def on_add_clicked(self, i):
        print('on add', i)

    def on_clear_clicked(self, i):
        print('on clear', i)

    def on_load_clicked(self, i):
        print('on load', i)


    def create_button_box_group(self):
        '''
        create box group containing push buttons 
        '''
        self.add_btn = QtWidgets.QPushButton("add")
        self.add_btn.clicked.connect(self.on_add_clicked)
        self.clear_btn = QtWidgets.QPushButton("clear")
        self.clear_btn.clicked.connect(self.on_clear_clicked)
        self.load_btn = QtWidgets.QPushButton("load")
        self.load_btn.clicked.connect(self.on_load_clicked)
        
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.add_btn)
        vbox.addWidget(self.clear_btn)
        vbox.addWidget(self.load_btn)
        vbox.addStretch(1)

        group_box = QtWidgets.QGroupBox()
        group_box.setLayout(vbox)
        return group_box
    

    def create_radio_box_group(self):
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
            
