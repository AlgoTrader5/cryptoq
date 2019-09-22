import sys
import argparse
from PyQt5 import QtWidgets
from main_window import MainWindow

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config-file", dest="config", type=str, help='subscriptions config yaml file')
    args = parser.parse_args()
    
    app = QtWidgets.QApplication([])

    win = MainWindow(config=args.config)
    win.resize(1000, 500)
    win.show()

    sys.exit(app.exec_())

if __name__ in "__main__":
    main()
