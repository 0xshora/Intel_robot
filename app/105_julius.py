# ref: http://www.asahi-net.or.jp/~cb9i-kn/geek/20170513totext.html
# before run this file,
# $julius -C bb2.jconf -module &
import socket
import string

host = 'localhost'   
port = 10500         


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
sock.bind((host, port))
sock.listen(1)

clients = []

try:
    sock.settimeout(10)
    connection, address = sock.accept()
    clients.append((connection, address))

    data = ""
    while True:
        try:
            connection.settimeout(3)
            from_client  = connection.recv(4096).decode()
        except exception as e:
            traceback.print_exc()
            continue
        
        


        while (string.find(data, "\n.") == -1):
            data = data + sock.recv(1024)

     
        strTemp = ""
        for line in data.split('\n'):
            index = line.find('WORD="')
            if index != -1:
                line = line[index+6:line.find('"', index+6)]
                strTemp = strTemp + line

        print("Result:" + strTemp)
        data = ""
except exception as e:
    traceback.print_exc()
    connection.close()
    sock.close()

