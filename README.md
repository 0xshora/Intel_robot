# Intel_robot
This is a laboratory work for the department of Computer Science at Keio

The verision using the cameras is under origin syora_branch
app/003_main.py

app/steppingmotor/motor
app/steppingmotor/srf02

The video for this robot is here:
coming soon (planning in February)

<!----- Conversion time: 6.105 seconds.


Using this Markdown file:

1. Cut and paste this output into your source file.
2. See the notes and action items below regarding this conversion run.
3. Check the rendered output (headings, lists, code blocks, tables) for proper
   formatting and use a linkchecker before you publish this page.

Conversion notes:

* Docs to Markdown version 1.0β17
* Sat Feb 01 2020 23:31:23 GMT-0800 (PST)
* Source doc: https://docs.google.com/open?id=1mXgkGcQOsxyJWULs_N1-OCw2hLTOVjDFN_qxd51_Ckc
* This is a partial selection. Check to make sure intra-doc links work.
* This document has images: check for >>>>>  gd2md-html alert:  inline image link in generated source and store images to your server.

WARNING:
You have 6 H1 headings. You may want to use the "H1 -> H2" option to demote all headings by one level.

----->


<p style="color: red; font-weight: bold">>>>>>  gd2md-html alert:  ERRORs: 0; WARNINGs: 1; ALERTS: 5.</p>
<ul style="color: red; font-weight: bold"><li>See top comment block for details on ERRORs and WARNINGs. <li>In the converted Markdown or HTML, search for inline alerts that start with >>>>>  gd2md-html alert:  for specific instances that need correction.</ul>

<p style="color: red; font-weight: bold">Links to alert messages:</p><a href="#gdcalert1">alert1</a>
<a href="#gdcalert2">alert2</a>
<a href="#gdcalert3">alert3</a>
<a href="#gdcalert4">alert4</a>
<a href="#gdcalert5">alert5</a>

<p style="color: red; font-weight: bold">>>>>> PLEASE check and correct alert issues and delete this message and the inline alerts.<hr></p>



# 知的ロボットインターフェース　2班

<p style="text-align: right">
工藤　大山　土田　白坂　石井</p>



# ロボットの名称

忠犬ハチ公

写真、動画:  [https://photos.app.goo.gl/hJGTFqUHYKH6EjwG7](https://photos.app.goo.gl/hJGTFqUHYKH6EjwG7)


# ロボットのコンセプト

まるで自分の犬のようにユーザーと遊ぶことができる犬ロボット。人の顔を見つけると近づいてくるとても人懐っこい性格である。ボール遊びをしたり、はたまたジャンケンをすることができるというとてもかしこい犬で、主人を楽しませることも忘れない。親しい人の顔には特別に笑顔でワンと吠えることもある。その賢さと愛らしさから、人は彼を忠犬ハチ公と呼ぶようになった。


# ロボットのハードウェア構成

基本的にはシンプルな構成となっている。



<p id="gdcalert1" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/-0.png). Store image on your image server and adjust path/filename if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert2">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/-0.png "image_tooltip")


12V 鉛蓄電池からステッピングモータ２つ分の給電をし、それらはラズパイからSPI通信で接続したモータドライバによって制御している。

また、測距センサ(SRF02)はラズパイからI2C通信し、接続している。

モニタとはラズパイのHDMI端子からHDMIケーブルを用いて接続している。

ラズパイのUSB端子にUSB Hub を接続し、Hubからはスピーカー、USBカメラ 2台、Arduinoに接続している。

ラズパイそのものの給電はモバイルバッテリから行っており、USB Hubの給電もモバイルバッテリより行っている。

特徴

・タイヤの回転中心と機体の底面中心がほぼ一致しており、回転による位置のずれがない

・ロボット全体が290*300*340 (高さ、横幅、奥行) と比較的コンパクトにまとまっている


# ロボットのソフトウェア構成

ディレクトリ構成は以下のようになった。尚、ここに示したのは主要なもので、拡張子がないものはディレクトリである。

/home/ri/Intel_robot

├── app

│   ├── 103_emmergencystop.py

│   ├── 201_main.py

│   └── steppingmotor

│       ├── motor.c

│       └── srf02.c

└── data

    ├── haarcascades

    └── wav_file

＜ステッピングモーター＞

　基本的にはwiringPi.hを用いてステッピングモーターに指令を出している。以下の表1のようなコマンドをを持っている。

表1 ステッピングモーターのコマンド集


<table>
  <tr>
   <td>命令
   </td>
   <td>説明
   </td>
  </tr>
  <tr>
   <td>p 回転数
   </td>
   <td><回転数>で指定された回転数を両輪の回転数とする
   </td>
  </tr>
  <tr>
   <td>r 回転数
   </td>
   <td><回転数>で指定された回転数で回転する. 負の数を与えると逆回転になる
   </td>
  </tr>
  <tr>
   <td>s
   </td>
   <td>一時停止する
   </td>
  </tr>
  <tr>
   <td>e
   </td>
   <td>停止し、プロセスを終了する
   </td>
  </tr>
</table>


s命令やp命令で回転数を変える時、速度を徐々に変えるように設定されている。具体的には回転数を100ずつ徐々に変えるようになっている。また、故障を防ぐため最大回転数を指定しており、5000回転より上の回転数にはならないようになっている。

ポート番号50001でサーバーを立てており、char 型の配列bufを受け付けている。このbufに入ったコマンドで先ほどのモーターが動く仕組みになっている。今回のロボットでは、pythonで書かれたカメラと測距センサーの値を加味したプログラムからコマンドを受け付けている。

----------------------------------------------------------------------------------------------------------------

<201_main.py>

　このプログラムによってカメラ画像の取得とロボットの行動を決定し、ステッピングモーターに指令を送っている。カメラ画像から人物検出に関しては、opencvのcascadeを使用している。(使用したcascade:[ https://github.com/opencv/opencv/tree/master/data/haarcascades](https://github.com/opencv/opencv/tree/master/data/haarcascades) のhaarcascade_frontalface_default.xml) 取得したbounding boxにおける左上のx、y座標とheight、widthから中心のx座標とbounding boxの大きさを計算し、それを元に行動を決定する。

　初期状態である人が検知されていない状態ではロボットは停止する。人が検出できた場合、以下のようなフローチャートで行動が決定される。まず、bounding boxの大きさが閾値以上であれば顔が近くにあると判断、つまり人に近づけたと判断し停止する。それ以外の場合、画面の横幅の4分の1から4分の3までに顔の中心があれば前進するが、左端や右端に中心があった場合、方向に応じて左折や右折を行う。

　また、当初は測距センサーの値を用いて障害物へ対応しようとしたが、測距センサーの精度が悪かった為使用せず、代わりに手動で急停止を行うスクリプト:103_emmergencystop.pyを用意した。 

----------------------------------------------------------------------------------------------------------------

＜測距センサー＞

　まず、I2Cデータバスを4つのセンサに対してオープンする。なお、本事件ではSRF02をセンサとして使用した。各センサはコマンドレジスタ0にReal Ranging Mode - Result in centimetersを意味する0x51の信号を送ることで測距を開始する。このセンサは音波を利用して距離を測定しているので、音波の往復のために最低でも66000μsec待つ必要がある。そしてコマンドレジスタ2に測距離データの上位バイト、コマンドレジスタ３に測距離データの下位バイトをそれぞれリクエストし、それぞれのデータを１つにまとめることで距離データを獲得する。　

　しかし、このセンサはセンサ自体を動かした瞬間や、センサの前を物体が横切った瞬間などに上下限を超える不適切な値を提示してしまうので、このバグを取り除くための仕組みを施した。

　まず、それぞれのセンサに対し連続して送られてくる距離データを格納しておくための配列を用意した。この配列のサイズをNとし、N個の距離データを格納するたびにそれらN個のデータの中から最も信頼できる距離データとして中央値となるデータを採用し、配列を初期化した。中央値を採用することによって、不適切な値を取り除くことが可能となった。Nを大きくしすぎると。距離データの獲得に時間がかかりすぎるという問題が発生するため、今回はN＝４で実装を行った。

---------------------------------------------------------------------------------------------------------------------------

<プロセス間通信>

　モーターを制御するプログラム（motor.c）と人を認識し、追いかけるプログラム（201_main.py）の連携は、ソケットによる通信を用いて行った。まず、201_main.pyにおいて人の顔を認識したら、ソケットを作成し、モーターへの指令を50001番ポートへと送る。motor.cにおいては、50001番ポートで201_main.pyからの指令を待ち受け、指令が送られてきたらそれに合わせてモーターのスピードや回転の向きを変化させる。なお、トランスポート層のプロトコルはTCPを用いた。


# ロボットの動作の特徴

＜ロボットの特徴＞

・自動で人を追いかけることができる

・どのような行動をするか音声で確認することができる。

・滑らかにスタート、ストップができる。

・緊急停止ボタンを押さなくてもプログラムで停止可能。

・行動を画像で表現しているので、将来的には行動ベースでロボットの感情の表現が可能。

・人を顔で検出しているので、追いかけさせるには顔を近づけることが必要。

・測距センサーを使用していないので、障害物には弱い。


# 各人のアプリケーション


## 工藤　ボール遊び

テニスボールを追いかけるアプリを作った。以下のようなアルゴリズムで動いている。

①1つのカメラを用いてRGB値からテニスボールを探し、座標・輪郭を割り出す(図1)

②その座標が半分より右側にあれば右側に回転し、左側にあれば逆回転をし、調整をする。(図2)

③座標が真ん中になったら直進する

④輪郭が大きくなったところで止まる。



<p id="gdcalert2" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/-1.png). Store image on your image server and adjust path/filename if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert3">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/-1.png "image_tooltip")


図1 RGB値から輪郭・座標を割り出している様子



<p id="gdcalert3" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/-2.png). Store image on your image server and adjust path/filename if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert4">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/-2.png "image_tooltip")


<p id="gdcalert4" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/-3.png). Store image on your image server and adjust path/filename if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert5">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/-3.png "image_tooltip")




<p id="gdcalert5" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/-4.png). Store image on your image server and adjust path/filename if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert6">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/-4.png "image_tooltip")


図2 テニスボールの位置によって回転し、直進している様子


## 工夫した点

実際にはテニスボールの認識以外の緑色のノイズにも反応してしまうため、複数の検出によってのみ反応させるという閾値をもうけた。また、モーターとのプロセス間通信で遅延が発生しており、物体認識精度が落ちるという現象があったため、最低限のプロセス間通信のみをするように命令数を減らすようなアルゴリズムにした。他にも音声認識を用いたプログラムを作ろうと試みたが、音声辞書を作るところで時間がかかってしまい、作成には至らなかった。


<!-- Docs to Markdown version 1.0β17 -->
