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
    print ("I will quit")
    text = "s"
    send_msg(text)
    time.sleep(5)
    text = "e"
    send_msg(text)


if __name__ == '__main__':
    main()
