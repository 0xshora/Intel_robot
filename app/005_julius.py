# ref: http://www.asahi-net.or.jp/~cb9i-kn/geek/20170513totext.html
# before run this file,
# $julius -C bb2.jconf -module &
import socket
import string

host = 'localhost'   
port = 10500         
<<<<<<< HEAD

=======
>>>>>>> 901c483df50e7d1f87949567453c38fca772f027

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

data = ""
while True:
<<<<<<< HEAD


    while (string.find(data, "\n.") == -1):
        data = data + sock.recv(1024)

 
=======
    while (string.find(data, "\n.") == -1):
        data = data + sock.recv(1024)

>>>>>>> 901c483df50e7d1f87949567453c38fca772f027
    strTemp = ""
    for line in data.split('\n'):
        index = line.find('WORD="')
        if index != -1:
            line = line[index+6:line.find('"', index+6)]
            strTemp = strTemp + line
<<<<<<< HEAD
    if strTemp != "":
        print("Result:" + strTemp)
=======

    print("Result:" + strTemp)
>>>>>>> 901c483df50e7d1f87949567453c38fca772f027
    data = ""
