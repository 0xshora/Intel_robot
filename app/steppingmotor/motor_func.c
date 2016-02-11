#include <stdio.h>

#include <unistd.h>
#include "wiringPi.h"
#include "wiringPiSPI.h"

int L6470_SPI_CHANNEL;
int BUFSIZE = 32;

#define SLOPE_TIME 10000
#define MAX_DIFF 1000
#define MINUS_MAX_DIFF -1000
#define MAX_SPEED 50000
#define MIN_SPEED -50000
#define MIN_ROLL 100
#define MINUS_MIN_ROLL -100
#define MINUS_MAX_ROLL -10000
#define MAX_SCALE 3
#define MIN_SCALE 0.5



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
/*
void new_speed_change(long speed, long postspeed)
{
	int diff = postspeed - speed;

	// int MAX_DIFF = 1000;
	// int MINUS_MAX_DIFF = -1000;

	int CNT = 30;
	int i;
	long tmp_speed = speed;
	if ((diff / CNT < MAX_DIFF) && (diff / CNT > MAX_DIFF)){
		for (i = 0; i < CNT; i++) {
			usleep(SLOPE_TIME);
			L6470_run_both(tmp_speed);
			tmp_speed += diff / CNT;
		}
	} else if (diff > 0){
		int time = (int)(diff / MAX_DIFF);
		for (i = 0; i < time; i++) {
			usleep(SLOPE_TIME);
			L6470_run_both(tmp_speed);
			tmp_speed += MAX_DIFF;
		}
	} else {
		int time = (int)(diff / MINUS_MAX_DIFF);
		for (i = 0; i < time; i++) {
			usleep(SLOPE_TIME);
			L6470_run_both(tmp_speed);
			tmp_speed += MINUS_MAX_DIFF;
		}
	}
	tmp_speed = postspeed;
	usleep(SLOPE_TIME);
	L6470_run_both(tmp_speed);
	if (postspeed == 0) {
		L6470_softstop();
		L6470_softhiz();
	}
}
*/
void L6470_turn_speed_change(long speed, int postspeed)
{
    printf("speed: %d, postspeed: %d\n", speed, postspeed);
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
    L6470_SPI_CHANNEL = 0;
    L6470_run(speed);
    L6470_SPI_CHANNEL = 1;
    L6470_run(speed);
}

void L6470_run_turn_moving(long speed, int right, float scale)
{
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
