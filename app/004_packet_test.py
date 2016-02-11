import socket
import time


def send_msg(msg):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        host = '127.0.0.1'
        port = 50001
        s.connect((host, port))
        s.sendall(msg.encode(encoding='ascii'))


def main():
    text = "p 1000"
    send_msg(text)
    time.sleep(10)
    text = "s"
    send_msg(text)


if __name__ == '__main__':
    main()
