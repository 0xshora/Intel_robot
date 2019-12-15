import socket
import time

# ref: http://www.asahi-net.or.jp/~cb9i-kn/geek/20170513totext.html
# before run this file,
# $julius -C bb2.jconf -module &
import string

host = 'localhost'   # Raspberry PiのIPアドレス
port = 10500         # juliusの待ち受けポート

# パソコンからTCP/IPで、自分PCのjuliusサーバに接続
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

data = ""
while True:

    # "/RECOGOUT"を受信するまで、一回分の音声データを全部読み込む。
    while (string.find(data, "\n.") == -1):
        data = data + sock.recv(1024)

    # 音声XMLデータから、<WORD>を抽出して音声テキスト文に連結する。
    strTemp = ""
    for line in data.split('\n'):
        index = line.find('WORD="')
        if index != -1:
            line = line[index+6:line.find('"', index+6)]
            strTemp = strTemp + line

    print("結果:" + strTemp)
    voice(strTemp)
    data = ""


def send_msg(msg):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 50001
    s.connect((host, port))
        # s.sendall(msg.encode(encoding='ascii'))
    s.send(msg)


def voice(cmd = None):
    if cmd is None:
        return

    if string.find(cmd, "まがれ") != -1:
        text = "r {}\n".format(5000)
        send_msg(text)
    else if string.find(cmd, "まえにすすめ") != -1:
        text = "p {}\n".format(1000)
        send_msg(text)
    else if string.find(cmd, "うしろにすすめ") != -1:
        text = "p {}\n".format(-1000)
        send_msg(text)
    else if string.find(cmd, "とまれ") != -1:
        text = "s\n"
        send_msg(text)
