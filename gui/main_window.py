#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://stackoverflow.com/questions/9957195/updating-gui-elements-in-multithreaded-pyqt
import os
import sys
import yaml
import webbrowser
from datetime import datetime
from decimal import Decimal
from pprint import pprint

from queue import Queue, Empty
from PyQt5 import QtCore, QtWidgets, QtGui

from contracts_tab import ContractsTab
from cryptofeed.defines import BITSTAMP, BITFINEX, COINBASE, FTX, GEMINI, HITBTC, POLONIEX, KRAKEN, BINANCE, EXX, HUOBI, HUOBI_US, OKCOIN, OKEX, COINBENE, BYBIT
from cryptofeed.pairs import gen_pairs


root = os.path.dirname(os.getcwd())

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, config):
        super(MainWindow, self).__init__()
        self.config = self._read_config(f'{root}\\conf\\{config}')
        self.markets = {
            'binance': gen_pairs(BINANCE),
            'bitfinex': gen_pairs(BITFINEX),
            'bitstamp': gen_pairs(BITSTAMP),
            'bybit': gen_pairs(BYBIT),
            'coinbase': gen_pairs(COINBASE),
            'coinbene': gen_pairs(COINBENE),
            'exx': gen_pairs(EXX),
            'ftx': gen_pairs(FTX),
            'gemini': gen_pairs(GEMINI),
            'hitbtc': gen_pairs(HITBTC),
            'huobi': gen_pairs(HUOBI),
            'kraken': gen_pairs(KRAKEN),
            'okcoin': gen_pairs(OKCOIN),
            'okex': gen_pairs(OKEX),
            'poloniex': gen_pairs(POLONIEX)
        }
        # windows
        self.central_widget = None
        self.exchange_window = None
        self.contracts_window = None
        
        # 1. set up gui windows
        self.setGeometry(50, 50, 600, 400)
        self.setWindowTitle('ConfigUI')
        self.init_menu()
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
        return


    #################################################################################################
    # -------------------------------- Event Handler   --------------------------------------------#
    #################################################################################################

    def update_status_bar(self, message):
        self.statusBar().showMessage(message)

    def open_proj_folder(self):
        webbrowser.open(root)

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
        tab_widget.addTab(tab1, 'Contract')

        # --------------------------------  CONTRACT TAB ------------------------------------------#
        self.contract_tab = ContractsTab(self.markets, self.config)
        contract_tab_layout = QtWidgets.QHBoxLayout()
        contract_tab_layout.addWidget(self.contract_tab)
        tab1.setLayout(contract_tab_layout)
        
        hbox.addWidget(tab_widget)
        self.central_widget.setLayout(hbox)
        self.setCentralWidget(self.central_widget)

    #################################################################################################
    # ------------------------------ User Interface End --------------------------------------------#
    #################################################################################################

