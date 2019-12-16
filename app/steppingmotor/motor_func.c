#include <stdio.h>

#include <unistd.h>
#include "wiringPi.h"
#include "wiringPiSPI.h"

int L6470_SPI_CHANNEL;
int BUFSIZE = 32;

#define SLOPE_TIME 10000
#define MAX_DIFF 1000
#define MINUS_MAX_DIFF -1000
#define MAX_SPEED 5000
#define MIN_SPEED -5000
#define MAX_ROLL 2000
#define MIN_ROLL 100
#define MINUS_MIN_ROLL -100
#define MINUS_MAX_ROLL -2000
#define MAX_SCALE 3
#define MIN_SCALE 0.5

void L6470_softstop();
void L6470_softhiz();
// 関数プロトタイプ。
void L6470_write(unsigned char data);
void L6470_init(void);
void L6470_run(long speed);
void L6470_run_both(long speed);
void L6470_run_turn(long speed);
void L6470_run_turn_moving(long speed, int right, float scale);
void L6470_softstop();
void L6470_softhiz();
void L6470_speed_change(long speed, int postspeed); //change the speed from "speed" to postspeed
void getargs(int * argc, char * argv[], char * buf);

void L6470_write(unsigned char data)
{
    wiringPiSPIDataRW(L6470_SPI_CHANNEL, &data, 1);
    //wiringPiSPIDataRW(0, &data, 1);
    //wiringPiSPIDataRW(1, &data, 1);
}


void L6470_init()
{
    // MAX_SPEED設定。
    /// レジスタアドレス。
    L6470_write(0x07);
    // 最大回転スピード値(10bit) 初期値は 0x41
    L6470_write(0x00);
    L6470_write(0x25);

    // KVAL_HOLD設定。
    /// レジスタアドレス。
    L6470_write(0x09);
    // モータ停止中の電圧設定(8bit)
    L6470_write(0xFF);

    // KVAL_RUN設定。
    /// レジスタアドレス。
    L6470_write(0x0A);
    // モータ定速回転中の電圧設定(8bit)
    L6470_write(0xFF);

    // KVAL_ACC設定。
    /// レジスタアドレス。
    L6470_write(0x0B);
    // モータ加速中の電圧設定(8bit)
    L6470_write(0xFF);

    // KVAL_DEC設定。
    /// レジスタアドレス。
    L6470_write(0x0C);
    // モータ減速中の電圧設定(8bit) 初期値は 0x8A
    L6470_write(0x40);

    // OCD_TH設定。
    /// レジスタアドレス。
    L6470_write(0x13);
    // オーバーカレントスレッショルド設定(4bit)
    L6470_write(0x0F);

    // STALL_TH設定。
    /// レジスタアドレス。
    L6470_write(0x14);
    // ストール電流スレッショルド設定(4bit)
    L6470_write(0x7F);

    //start slopeデフォルト
    /// レジスタアドレス。
    L6470_write(0x0e);
    L6470_write(0x00);

    //デセラレーション設定
    /// レジスタアドレス。
    L6470_write(0x10);
    L6470_write(0x29);
}

void L6470_run(long speed)
{
    unsigned short dir;
    unsigned long spd;
    unsigned char spd_h;
    unsigned char spd_m;
    unsigned char spd_l;

    // 方向検出。
    if (speed < 0)
    {
        dir = 0x50;
        spd = -1 * speed;
    }
    else
    {
        dir = 0x51;
        spd = speed;
    }

    // 送信バイトデータ生成。
    spd_h = (unsigned char)((0x0F0000 & spd) >> 16);
    spd_m = (unsigned char)((0x00FF00 & spd) >> 8);
    spd_l = (unsigned char)(0x00FF & spd);

    // コマンド（レジスタアドレス）送信。
    L6470_write(dir);
    // データ送信。
    L6470_write(spd_h);
    L6470_write(spd_m);
    L6470_write(spd_l);
}

void L6470_run_both(long speed)
{
    L6470_SPI_CHANNEL = 0;
    L6470_run(speed);
    L6470_SPI_CHANNEL = 1;
    L6470_run(-1 * speed);
}

void L6470_turn_speed_change(long speed, int postspeed)
{
    printf("speed: %ld, postspeed: %d\n", speed, postspeed);
    if (postspeed > MAX_SPEED)
    {
        postspeed = MAX_SPEED;
    }
    else if (postspeed < MIN_SPEED)
    {
        postspeed = MIN_SPEED;
    }
    //change the speed from "speed" to postspeed
    if (speed < postspeed)
    {
        //if moving, move faster
        int i;
        for (i = speed; i <= postspeed; i += 100)
        {
            speed = i;
            usleep(SLOPE_TIME);
			L6470_SPI_CHANNEL = 0;
    		L6470_run(speed);
    		L6470_SPI_CHANNEL = 1;
    		L6470_run(speed);
        }
    }
    else if (speed > postspeed)
    {
        //if moving, move more slowly

        int i;
        for (i = speed; i >= postspeed; i -= 100)
        {
            speed = i;
            usleep(SLOPE_TIME);
			L6470_SPI_CHANNEL = 0;
    		L6470_run(speed);
    		L6470_SPI_CHANNEL = 1;
    		L6470_run(speed);
        }
    }

    if (postspeed == 0)
    {
        L6470_softstop();
        L6470_softhiz();
    }

    L6470_SPI_CHANNEL = 0;
    L6470_run(speed);
    L6470_SPI_CHANNEL = 1;
    L6470_run(-1 * speed);
}

void L6470_speed_change(long speed, int postspeed)
{
	if ((int)speed == 0) {
        printf("koko\n");
        L6470_softstop();
        L6470_softhiz();
        return ;
    }
    if (postspeed > MAX_SPEED)
    {
        postspeed = MAX_SPEED;
    }
    else if (postspeed < MIN_SPEED)
    {
        postspeed = MIN_SPEED;
    }
	//change the speed from "speed" to postspeed
	if (speed < postspeed) {
		//if moving, move faster
		int i;
		for (i = speed; i <= postspeed; i += 100) {
			speed = i;
			usleep(SLOPE_TIME);
			L6470_run_both(speed);
		}
	} else if (speed > postspeed){
		//if moving, move more slowly
		int i;
		for (i = speed; i >= postspeed; i -= 100) {
			speed = i;
			usleep(SLOPE_TIME);
			L6470_run_both(speed);
		}
	}

	if (postspeed == 0) {
		L6470_softstop();
		L6470_softhiz();
	}


    L6470_SPI_CHANNEL = 0;
    L6470_run(speed);
    L6470_SPI_CHANNEL = 1;
    L6470_run(-1 * speed);
}


void L6470_run_turn(long speed)
{
	if (speed > MAX_ROLL) {
        speed = MAX_ROLL;
    }
    else if ((speed < MIN_SPEED) && (speed > 0)) {
        speed = MIN_SPEED;
    }
    else if ((speed > MINUS_MIN_ROLL) && (speed <= 0)) {
        speed = MINUS_MIN_ROLL;
    }
    else if (speed < MINUS_MAX_ROLL) {
        speed = MINUS_MAX_ROLL;
    }
    L6470_SPI_CHANNEL = 0;
    L6470_run(speed);
    L6470_SPI_CHANNEL = 1;
    L6470_run(speed);
}

void L6470_run_turn_moving(long speed, int right, float scale)
{
	if (scale > MAX_SCALE) {
        scale = MAX_SCALE;
    }
    else if (scale < MIN_SCALE) {
        scale = MIN_SCALE;
    }
   if (right == 1) {
	L6470_SPI_CHANNEL = 0;
	L6470_run(speed);
	L6470_SPI_CHANNEL = 1;
	L6470_run(-1 * (long)speed/scale);
   } else {
	L6470_SPI_CHANNEL = 0;
	L6470_run((long)speed/scale);
	L6470_SPI_CHANNEL = 1;
	L6470_run(-1 * speed);
   }

}

void L6470_softstop()
{
    unsigned short dir;
    printf("***** SoftStop. *****\n");
    dir = 0xB0;
    // コマンド（レジスタアドレス）送信。
    L6470_write(dir);
    delay(1000);
}

void L6470_softhiz()
{
    unsigned short dir;
    printf("***** Softhiz. *****\n");
    dir = 0xA8;
    // コマンド（レジスタアドレス）送信。
    L6470_write(dir);
    delay(1000);
}
