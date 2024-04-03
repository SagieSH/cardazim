import argparse
import socket
import struct
import sys
from threading import Thread


def decode_data(encoded_data: bytes) -> str:
    '''
    Decode data encoded with the following format:
    b"< 4 bytes describing the length of the data in little-endian >< The data >"
    '''
    data_length = struct.unpack("<I", encoded_data[:4])[0]
    data = encoded_data[4: 4 + data_length].decode()

    return data


def receive_data(connection: socket.socket):
    '''
    Receive data from the connection and print it.
    '''
    encoded_data = connection.recv(1024)
    print("Received data: " + decode_data(encoded_data))


def run_server(ip: str, port: int):
    '''
    Receive connections to (ip, port) and print data sent by them.
    '''
    server = socket.socket()
    server.bind((ip, port))
    server.listen(1000)
    while True:
        connection, _ = server.accept()
        t = Thread(target=receive_data, args=(connection,))
        t.run()


def get_args():
    parser = argparse.ArgumentParser(description='Start local server.')
    parser.add_argument('ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('port', type=int,
                        help='the server\'s port')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        run_server(args.ip, args.port)
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
