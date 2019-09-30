
2018.9.21版


README.txt
→ このファイル

RI2018.pdf
→ 実験指導書

0 Parts.docx
→ 配布物一覧

1 How to setup Raspberry pi3 with ubuntuMATE.docx
→ Raspberry piのセットアップ

2 How to build Power Sources.pptx
→ 電源設計

3 How to use Almi Frame & crimp terminal.docx
→ アルミフレームの組み方、圧着端子の付け方

4 Figure_ bracket 4 stepping motor.pptx
→ ステッピングモータ取り付け用のブラケット、図面、寸法

5 5 How to Remote Login.pptx
→ 外部のネットワークからラズパイにログインする方法





julius [ 音声認識エンジンのソースプログラム ]
 |
 +--- dictation-kit-v4.4.zip
 |
 +--- grammar-kit-v4.1.tar.gz
 |
 +--- julius-4.4.2.tar.gz
 |
 +--- Juliusbook-4.1.5-ja.pdf


srf02 [ 超音波距離計のマニュアル類 ]
 |
 +--- SRF02 Technical Specification.pdf
 |    超音波距離計の技術仕様
 |
 +--- SRF02 I2C Mode.pdf
 |    超音波距離計のI2C仕様。I2Cバスへの接続の仕方。コマンド。測距。アドレス変更方法、などなど
 |
 +--- README.txt


motor-stepping [ ステッピングモータドライバキットのマニュアル ](2017年から使用)
 |
 +--- specification-L6470.pdf
 |    コントローラチップの仕様書。命令の一覧など。
 |
 +--- stepping-motor-driver-I6470-manual.pdf
      ドライバキットのマニュアル


motor-dc [ DCモータコントローラのドライバとマニュアル ](2016年まで使用)
 |
 +--- imcs01_driver_JROBO
 |    Raspberry pi2でエラー、警告なしにコンパイルできるようソースに手を加えたもの。
 |    imcs01_driver_3.2_JROBO.tgz を展開したもの。
 |
 +--- README.txt             
 | 
 +--- imcs01_driver_3.2.tar.gz
 |    iXsが提供している Linux kernel3.2用のドライバ＆サンプルプログラム(オリジナル)
 |
 +--- imcs01_driver_3.2_JROBO.tgz
 |    ドライバをRaspbianでコンパイルできるようオリジナルソースに手を加えたもの。
 |
 +--- imcs01_manual_circuit_v1_1.pdf
 |    モータコントローラの回路図
 |
 +--- imcs01_manual_hardware_v1_3.pdf
 |    モータコントローラのハードウェアマニュアル
 |
 +--- imcs01_manual_software_v1_3.pdf
 |    モータコントローラのソフトウェアマニュアル
 |
 +--- imcs01_sample_linux.tar.gz
 |    モータコントローラのサンプルプログラム
 |    imcs01_driver_3.2.tar.gzに収録されているものと同じ？ 
 |
 +--- imds03_manual_dimension_v2.pdf
 |    モータドライバの基板図
 |
 +--- imds03_manual_v2.pdf
      モータドライバのマニュアル


ubuntuMATE[ Raspberry pi用OS ]
 |
 +--- ubuntu-mate-16.04.2-desktop-armhf-raspberry-pi.img.xz
      OSイメージファイル


Win32DiskImager [ ディスクイメージ読み書きツール ]
 |
 +--- Win32DiskImager.exe
      ubuntuMATEのディスクイメージをマイクロSDカードに書き込むために使用します。
      SDカードからイメージ作成も可能なので、バックアップにも使えます。
      


wiringPi [GPIOによる入出力を手軽にプログラムするためのライブラリ]
 |
 +--- WiringPiのソース
      SPI通信、シリアル通信などを手軽にCプログラム実装できます。





samples/opencv [ OpenCVのサンプルプログラム ]
 |
 +--- README.txt
 |
 +--- Makefile     
 |
 +--- sample1.c
 |    1台のカメラから動画をキャプチャし、ウィンドウ表示するサンプルプログラム。
 |
 +--- sample2.c
      1台のカメラから動画をキャプチャし、顔認識するサンプルプログラム。


sample/pthread
 |
 +--- sample_pthread.cpp
 |    大域変数a をスレッドから更新するテスト
 |
 +--- sample_pthread2.cpp
      複数のスレッド立ち上げテスト


samples/srf02 [ 超音波距離計のサンプルプログラム ]
 |
 +--- changeAddr.c
 |    超音波距離計のI2Cスレーブアドレスを変更するプログラム兼サンプルプログラム。
 |
 +--- sample.c
      測距サンプルプログラム


sample/steppingmotor
 |
 +--- motor_slope.c
 |    モータ停止からしだいにモータが回り始め、回転からしだいにモータが停止するデモ
 |
 +--- motor_speed.c
 |    モータを指定したスピードで回転させるデモ
 |
 +--- motor_steps.c
      指定したステップ数（角度）だけ回転させるデモ


samples/wiringpi [ GPIOライブラリ＆ツール ]
 |
 +--- ledtest.c
      サンプルプログラム LEDの点滅





