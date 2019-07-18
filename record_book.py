from kdb_client import KdbClient


def main():
    book_kdb = KdbClient(zmqhost='127.0.0.1', zmqport=5555, kdbhost='localhost', kdbport=5002)
    book_kdb.run()

    
if __name__ == '__main__':
    main()
