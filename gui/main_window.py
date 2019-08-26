#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://stackoverflow.com/questions/9957195/updating-gui-elements-in-multithreaded-pyqt
import os
import sys
import yaml
import argparse
import webbrowser
from datetime import datetime
from decimal import Decimal
from pprint import pprint

from qpython import qconnection
from qpython.qtype import QException

from queue import Queue, Empty
from PyQt5 import QtCore, QtWidgets, QtGui

from contracts_tab import ContractsTab
from cryptofeed.defines import BITSTAMP, BITFINEX, COINBASE, GEMINI, HITBTC, POLONIEX, KRAKEN, BINANCE, EXX, HUOBI, HUOBI_US, HUOBI_DM, OKCOIN, OKEX, COINBENE, BYBIT, FTX
from cryptofeed.pairs import gen_pairs

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, port, config):
        super(MainWindow, self).__init__()

        # create connection object
        self.q = qconnection.QConnection(host='localhost', port=port, pandas=True)
        # initialize connection
        self.q.open()

        # windows
        self.central_widget = None
        self.exchange_window = None
        self.contracts_window = None
        self.strategy_window = None


        self._client_dict = {
            'coinbase': gen_pairs(COINBASE),
            'kraken': gen_pairs(KRAKEN),
            'poloniex': gen_pairs(POLONIEX),
            'binance': gen_pairs(BINANCE),
            'bitstamp': gen_pairs(BITSTAMP),
            'bitfinex': gen_pairs(BITFINEX),
            'gemini': gen_pairs(GEMINI),
            'hitbtc': gen_pairs(HITBTC),
            'exx': gen_pairs(EXX),
            'huobi': gen_pairs(HUOBI),
            'okcoin': gen_pairs(OKCOIN),
            'okex': gen_pairs(OKEX),
            'coinbene': gen_pairs(COINBENE),
            'bybit': gen_pairs(BYBIT)
        }

        self._subscription_dict = self._read_config(config)
        # self._strategy_dict = self._read_config('D:\\Apps\\Romer\\conf\\config_client.yaml')

        
        # 1. set up gui windows
        self.setGeometry(50, 50, 600, 400)
        self.setWindowTitle('ConfigUI')
        self.init_menu()
        # self.init_status_bar()
        self.init_central_area()


    def _read_config(self, file_path):
        '''examples
        
        subscriptions:
        {'CBPRO': ['BTC-USD',
                    ...
                    'ZEC-BTC']}
        '''
        subscriptions = None
        try:
            with open(file_path, encoding='utf8') as fd:
                subscriptions = yaml.safe_load(fd)
        except IOError:
            print(f"{file_path} is missing")

        return subscriptions

    def _save_config(self, file_path):
        subscriptions = None
        try:
            with open(file_path, encoding='utf8') as fd:
                subscriptions = yaml.safe_load(fd)
        except IOError:
            print(f"{file_path} is missing")

        return subscriptions


    #################################################################################################
    # -------------------------------- Event Handler   --------------------------------------------#
    #################################################################################################

    def update_status_bar(self, message):
        self.statusBar().showMessage(message)

    def open_proj_folder(self):
        webbrowser.open('C:/repos/')

    def closeEvent(self, a0: QtGui.QCloseEvent):
        print('close main window')

    #################################################################################################
    # ------------------------------ Event Handler Ends --------------------------------------------#
    #################################################################################################




    #################################################################################################
    # -------------------------------- User Interface  --------------------------------------------#
    #################################################################################################

    def init_menu(self):
        menubar = self.menuBar()
        sysMenu = menubar.addMenu('File')
        # open folder
        sys_folderAction = QtWidgets.QAction('Folder', self)
        sys_folderAction.setStatusTip('Open_Folder')
        sys_folderAction.triggered.connect(self.open_proj_folder)
        sysMenu.addAction(sys_folderAction)
        sysMenu.addSeparator()
        # sys|exit
        sys_exitAction = QtWidgets.QAction('Exit', self)
        sys_exitAction.setShortcut('Ctrl+Q')
        sys_exitAction.setStatusTip('Exit_App')
        sys_exitAction.triggered.connect(self.close)
        sysMenu.addAction(sys_exitAction)


    def init_central_area(self):
        self.central_widget = QtWidgets.QWidget()
        hbox = QtWidgets.QHBoxLayout()
        # -------------------------------- bottom Left ------------------------------------------#
        tab_widget = QtWidgets.QTabWidget()
        tab1 = QtWidgets.QWidget()          # contract
        tab2 = QtWidgets.QWidget()          # strategy
        tab_widget.addTab(tab1, 'Contract')
        tab_widget.addTab(tab2, 'Strategy')

        # --------------------------------  CONTRACT TAB ------------------------------------------#
        self.contract_tab = ContractsTab(self._client_dict, self._subscription_dict)
        contract_tab_layout = QtWidgets.QHBoxLayout()
        contract_tab_layout.addWidget(self.contract_tab)
        tab1.setLayout(contract_tab_layout)

        # --------------------------------  STRATEGY TAB ------------------------------------------#
        # self.strategy_config_window = StrategyConfigWindow(self.db_client)
        tab2_layout = QtWidgets.QVBoxLayout()
        # tab2_layout.addWidget(self.strategy_config_window)
        tab2.setLayout(tab2_layout)

        hbox.addWidget(tab_widget)
        self.central_widget.setLayout(hbox)
        self.setCentralWidget(self.central_widget)

    #################################################################################################
    # ------------------------------ User Interface End --------------------------------------------#
    #################################################################################################

