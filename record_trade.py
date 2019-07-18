from record_kdb import KdbClient


def main():
    trade_kdb = KdbClient(zmqhost='127.0.0.1', zmqport=5555, kdbhost='localhost', kdbport=5002)
    trade_kdb.run()

    
if __name__ == '__main__':
    main()
