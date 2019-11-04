import socket

def send_msg(msg, host='127.0.0.1', port='50001'):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(msg.encode(encoding='ascii'))
