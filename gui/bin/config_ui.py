 from gui.main_window import MainWindow
 
 def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=5002, help='QConnection port')
    args = parser.parse_args()
    
    app = QtWidgets.QApplication([])

    win = MainWindow(port=args.port)
    win.resize(1000, 500)
    win.show()

    sys.exit(app.exec_())

if __name__ in "__main__":
    main()
