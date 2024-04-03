import argparse
import socket
import struct
import sys


def run_server(ip, port):
    '''
    Receive connections to (ip, port) and print messages sent by them.
    '''
    server = socket.socket()
    server.bind((ip, port))
    server.listen(1000)
    while True:
        conn, _ = server.accept()
        encoded_message = conn.recv(1024)
        message_length = struct.unpack("<I", encoded_message[:4])[0]
        message = encoded_message[4: 4 + message_length].decode()
        print("Received data: " + message)


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
