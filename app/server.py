#coding: UTF-8
import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#host = "192.168.0.209"
host = "127.0.0.1"
port = 50002
s.bind((host, port))
s.listen(1)


clients = []

try:
    s.settimeout(10)
    connection, address = s.accept()
    clients.append((connection, address))
    while(True):
        time.sleep(0.5)
        try:
            connection.settimeout(3)
            from_client = connection.recv(4096).decode()
            print("クライアントから受信したメッセージ=>{}".format(from_client))
            #to_client = "あなたは[{}]というメッセージを送信しましたね?".format(from_client)
            #connection.send(to_client.encode("UTF-8"))
        except Exception as e:
            print(e)
            continue
except Exception as e:
    print(clients)
    print(e)
    connection.close()
    s.close()
