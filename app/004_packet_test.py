import socket
import time


def send_msg(msg):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 50001
    s.connect((host, port))
        # s.sendall(msg.encode(encoding='ascii'))
    s.send(msg)


def main():
    text = "r 10000"
    send_msg(text)
    time.sleep(3)
    text = "r -10000"
    send_msg(text)


    time.sleep(3)

    text = "s"
    send_msg(text)


if __name__ == '__main__':
    main()
