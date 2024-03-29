//モータスピードを指定時間でスロープで上げ下げする

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "wiringPi.h"
#include "wiringPiSPI.h"

int L6470_SPI_CHANNEL;
int BUFSIZE = 32;
#define SLOPE_TIME 1000000

// 関数プロトタイプ。
void L6470_write(unsigned char data);
void L6470_init(void);
void L6470_run(long speed);
void L6470_run_both(long speed);
void L6470_run_turn(long speed);
void L6470_run_turn_moving(long speed, int right, float scale);
void L6470_softstop();
void L6470_softhiz();
void L6470_speed_change(long speed, int postspeed);
//change the speed from "speed" to postspeed

int main(int argc, char **argv)
{
    int i, j;
    long speed = 0;

    char *str = (char *)malloc(BUFSIZE * sizeof(char));
    char c;
    long s;
    float sl;
    long S = 0;

    printf("***** start spi test program *****\n");

    // SPI channel 0 を 1MHz で開始。
    //if (wiringPiSPISetup(L6470_SPI_CHANNEL, 1000000) < 0)
    if (wiringPiSPISetup(0, 1000000) < 0)
    {
        printf("SPI Setup failed:\n");
    }
    if (wiringPiSPISetup(1, 1000000) < 0)
    {
        printf("SPI Setup failed:\n");
    }

    // L6470の初期化。
    L6470_SPI_CHANNEL = 0;
    L6470_init();
    L6470_SPI_CHANNEL = 1;
    L6470_init();

	printf("Start      --> Press space\n");
    printf("Speed Up   --> Press p \n");
    printf("Speed Down --> Press q \n");
    printf("Turn Right --> Press r \n");
    printf("Turn Light --> Press l \n");
    printf("Stop       --> Press s \n");
    printf("End        --> Press e \n");

    while ((c = getchar()) != EOF)
    {

        // printf("speed?? (Maximum: +-40000)\n");
        // scanf("%ld", &s);
        // printf("slope time? \n");
        // scanf("%f", &sl);

		

        if (c == 'p')
			//speed up
        {
            speed += 1000;
            L6470_run_both(speed);
            // printf("*** Speed %ld ***\n", speed);
        }

        if (c == 'q')
			//speed down
        {
            speed -= 1000;
            L6470_run_both(speed);
            // printf("*** Speed %ld ***\n", speed);
        }

        if (c == 'r' || c == 'l') { //turn right or left
            if (speed != 0) {
                printf("This machine have to stop before turn\n");
                // stop function
                speed = 0;
                L6470_run_both(speed);
                printf("*** Speed %ld ***\n", speed);
                L6470_softstop();
                L6470_softhiz();

				if (c == 'r') {
					int right_true = 1;
					float scale = 3.0; //default scale
					L6470_run_turn_moving(speed, right_true, scale);
					// printf("*** Turn right : Speed %ld ***\n", speed);
					// speed = 0;
					// L6470_softstop();
					// L6470_softhiz();
					}
				 else {
					int right_false = 0;
					float scale = 3.0;
					L6470_run_turn_moving(speed, right_false, scale);
					// printf("*** Turn right : Speed %ld ***\n", speed);
					// speed = 0;
					// L6470_softstop();
					// L6470_softhiz();
				}


		   	} else {
				if (c == 'r') {
					speed = 10000;
					L6470_run_turn(speed);
					// printf("*** Turn right : Speed %ld ***\n", speed);
					// speed = 0;
					// L6470_softstop();
					// L6470_softhiz();
				} else {
					speed = -10000;
					L6470_run_turn(speed);
					// printf("*** Turn right : Speed %ld ***\n", speed);
					// speed = 0;
					// L6470_softstop();
					// L6470_softhiz();
					}
				}   
        }

        if (c == 's') { 		    

			// if the robot moves in the positive direction
			if (speed > 0) {
				int j;
				for (j = speed; j >= 0; j = j - 100) {
					speed = j;

					usleep(SLOPE_TIME);
					printf("%d\n", j);
					L6470_run_both(speed);
					L6470_softstop();
					L6470_softhiz();
				}

			} else {
				int j;
				for (j = speed; j <=0; j = j + 100) {
					speed = j;
					usleep(SLOPE_TIME);
					printf("%d\n", j);
					L6470_run_both(speed);
					L6470_softstop();
					L6470_softhiz();
				}
			}
		
			L6470_speed_change(speed, 0);	
        }
        if (c == 'e')
        {
            printf("Good job !\n");
	    speed = 0;
            L6470_run_both(speed);
            printf("*** Speed %ld ***\n", speed);
            L6470_softstop();
            L6470_softhiz();
            return 0;
        }
    }

    return 0;
}

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
	} else  if (speed > postspeed){
		//if moving, move more slowly
		int i;
		for (i = speed; i >= postspeed; i -= 100) {
			speed = i;
			usleep(SLOPE_TIME);
			L6470_run_both(speed);
		}
	}

    L6470_SPI_CHANNEL = 0;
    L6470_run(speed);
    L6470_SPI_CHANNEL = 1;
    L6470_run(-1 * speed);
}


void L6470_run_turn(long speed, int right)
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
	L6470_run(speed/scale);
   } else {
	L6470_SPI_CHANNEL = 0;
	L6470_run(speed/scale);
	L6470_SPI_CHANNEL = 1;
	L6470_run(speed);
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
