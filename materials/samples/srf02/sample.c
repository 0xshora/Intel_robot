//
// 2014.07.10
// TSUCHIYA, Akihito
//
// SFR02 測距プログラム
// 2つのセンサを接続する場合
//
// 詳細は「SRF02 I2C Mode.pdf」を参照。
//
// 使用法： $ sudo ./sample
//
#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>
#include "/usr/include/linux/i2c-dev.h"

#define sample 4
#define SRF_NUM 4
int compare_int(const void *a,const void *b);
int true_range(int *tmp);
void reset(int *tmp);

int main(void)
{

	int fd1, fd2, fd3, fd4;
	int count1=0,count2=0;
	int tmpE0[sample]={0},tmpE2[sample]={0},tmpE4[sample]={0},tmpE6[sample]={0};
	char filename[20];
	char buf[10];
	int res;
	int range = 0;

	// I2Cデータバスをオープン
	sprintf(filename, "/dev/i2c-1");
	// 1つめ
	fd1 = open(filename, O_RDWR);
	if (fd1 < 0)
	{
		printf("Error on open\n");
		exit(1);
	}
	// 2つめ
	fd2 = open(filename, O_RDWR);
	if (fd2 < 0)
	{
		printf("Error on open\n");
		exit(1);
	}
	fd3 = open(filename, O_RDWR);
	if (fd3 < 0)
	{
	    	printf("Error on open\n");
		exit(1);
	}
	fd4 = open(filename, O_RDWR);
	if (fd4 < 0)
	{
	    	printf("Error on open\n");
		exit(1);
	}
	if (ioctl(fd1, I2C_SLAVE, (0xE0 >> 1)) < 0)
	{ // 0xE0(0x11100000) >> 1 = 0x70(0x01110000)
		printf("Error on slave address 0xE0\n");
		exit(1);
	}
	
	if (ioctl(fd2, I2C_SLAVE, (0xE2 >> 1)) < 0)
	{ // 0xE0(0x11100000) >> 1 = 0x70(0x01110000)
		printf("Error on slave address 0xE2\n");
		exit(1);
	}
	if (ioctl(fd3, I2C_SLAVE, (0xE4 >> 1)) < 0)
	{
	    printf("Error on slave address 0xE4n\n");
	    exit(1);
	}
	if (ioctl(fd4, I2C_SLAVE, (0xE6 >> 1)) < 0)
	{
	    printf("Error on slave address 0xE6n\n");
	    exit(1);
	}

	while(1){
	// 1つめのセンサに対して
	
	{ // read from 0xE0
		// コマンドレジスタ0に 0x51:Real Ranging Mode - Result in centimeters を送ることによって測距が始まる
		buf[0] = 0x00;
		buf[1] = 0x51;

		if ((write(fd1, buf, 2)) != 2)
		{
			printf("0xE0 Error send the read command\n");
			exit(1);
		}
		// Wait for the measurement
		// 音波だから、"行って" "帰ってくる" のに時間がかかる
		usleep(66000);

		// コマンドレジスタ2に対し測距値データの上位バイトをリクエスト
		buf[0] = 0x02;
		if ((write(fd1, buf, 1)) != 1)
		{
			printf("0xE0 Error on select the Range High Byte\n");
			exit(1);
		}

		if ((read(fd1, buf, 1)) != 1)
		{
			printf("0xE0 Error on read the Range High Byte\n");
			exit(1);
		}
		range = buf[0] << 8;

		// コマンドレジスタ3に対し測距値データの下位バイトをリクエスト
		buf[0] = 0x03;
		if ((write(fd1, buf, 1)) != 1)
		{
			printf("0xE0 Error on select the Range Low Byte\n");
			exit(1);
		}

		if ((read(fd1, buf, 1)) != 1)
		{
			printf("0xE0 Error on read the Range Low Byte\n");
			exit(1);
		}

		// 上位と下位をくっつける
		//printf("0xE0 Range=%d cm\n", range);

	}
                range |= buf[0];
		tmpE0[count2]=range;
		if(count2==sample){
		    range=true_range(tmpE0);
		    printf("[E0]: %d cm\n",range);
		    count2=0;
		    reset(tmpE0);
		}else{
		    count2++;
		}

	{ // read from 0xE2
		buf[0] = 0x00;
		buf[1] = 0x51;

		if ((write(fd2, buf, 2)) != 2)
		{
			printf("0xE2 Error send the read command\n");
			exit(1);
		}
		// Wait for the measurement
		usleep(66000);
	//	usleep(200000);
			
		buf[0] = 0x02;
		if ((write(fd2, buf, 1)) != 1)
		{
			printf("0xE2 Error on select the Range High Byte\n");
			exit(1);
		}

		if ((read(fd2, buf, 1)) != 1)
		{
			printf("0xE2 Error on read the Range High Byte\n");
			exit(1);
		}
		range = buf[0] << 8;

		buf[0] = 0x03;
		if ((write(fd2, buf, 1)) != 1)
		{
			printf("0xE2 Error on select the Range Low Byte\n");
			exit(1);
		}

		if ((read(fd2, buf, 1)) != 1)
		{
			printf("0xE2 Error on read the Range Low Byte\n");
			exit(1);
		}
		range |= buf[0];	

	//	printf("0xE2 Range=%d cm\n", range);
	}
		tmpE2[count2]=range;
		if(count2==sample){
		    range=true_range(tmpE2);
		    printf("	[E2]: %d cm\n",range);
		    count2=0;
		    reset(tmpE2);
		}else{
		    count2++;
		}

	{ // read from 0xE4
		// コマンドレジスタ0に 0x51:Real Ranging Mode - Result in centimeters を送ることによって測距が始まる
		buf[0] = 0x00;
		buf[1] = 0x51;

		if ((write(fd3, buf, 2)) != 2)
		{
			printf("0xE4 Error send the read command\n");
			exit(1);
		}
		// Wait for the measurement
		// 音波だから、"行って" "帰ってくる" のに時間がかかる
		usleep(66000);

		// コマンドレジスタ2に対し測距値データの上位バイトをリクエスト
		buf[0] = 0x02;
		if ((write(fd3, buf, 1)) != 1)
		{
			printf("0xE4 Error on select the Range High Byte\n");
			exit(1);
		}

		if ((read(fd3, buf, 1)) != 1)
		{
			printf("0xE4 Error on read the Range High Byte\n");
			exit(1);
		}
		range = buf[0] << 8;

		// コマンドレジスタ3に対し測距値データの下位バイトをリクエスト
		buf[0] = 0x03;
		if ((write(fd3, buf, 1)) != 1)
		{
			printf("0xE4 Error on select the Range Low Byte\n");
			exit(1);
		}

		if ((read(fd3, buf, 1)) != 1)
		{
			printf("0xE4 Error on read the Range Low Byte\n");
			exit(1);
		}

		// 上位と下位をくっつける
		//printf("0xE0 Range=%d cm\n", range);

	}
                range |= buf[0];
		tmpE4[count2]=range;
		if(count2==sample){
		    range=true_range(tmpE4);
		    printf("		[E4]: %d cm\n",range);
		    count2=0;
		    reset(tmpE4);
		}else{
		    count2++;
		}

{ // read from 0xE6
		// コマンドレジスタ0に 0x51:Real Ranging Mode - Result in centimeters を送ることによって測距が始まる
		buf[0] = 0x00;
		buf[1] = 0x51;

		if ((write(fd4, buf, 2)) != 2)
		{
			printf("0xE6 Error send the read command\n");
			exit(1);
		}
		// Wait for the measurement
		// 音波だから、"行って" "帰ってくる" のに時間がかかる
		usleep(66000);

		// コマンドレジスタ2に対し測距値データの上位バイトをリクエスト
		buf[0] = 0x02;
		if ((write(fd4, buf, 1)) != 1)
		{
			printf("0xE6 Error on select the Range High Byte\n");
			exit(1);
		}

		if ((read(fd4, buf, 1)) != 1)
		{
			printf("0xE6 Error on read the Range High Byte\n");
			exit(1);
		}
		range = buf[0] << 8;

		// コマンドレジスタ3に対し測距値データの下位バイトをリクエスト
		buf[0] = 0x03;
		if ((write(fd4, buf, 1)) != 1)
		{
			printf("0xE6 Error on select the Range Low Byte\n");
			exit(1);
		}

		if ((read(fd4, buf, 1)) != 1)
		{
			printf("0xE6 Error on read the Range Low Byte\n");
			exit(1);
		}

		// 上位と下位をくっつける
		//printf("0xE0 Range=%d cm\n", range);

	}
                range |= buf[0];
		tmpE6[count2]=range;
		if(count2==sample){
		    range=true_range(tmpE6);
		    printf("			[E6]: %d cm\n",range);
		    count2=0;
		    reset(tmpE6);
		}else{
		    count2++;
		}
	}

	// 閉じる！！
	close(fd1);
	close(fd2);
	close(fd3);
	close(fd4);
	return 0;
}
int compare_int(const void *a,const void *b){
    	return *(int *)a-*(int *)b;
}

int true_range(int *tmp){
	qsort(tmp,sample+1,sizeof(int),compare_int);
	return tmp[0];
}

void reset(int *tmp){
    	for(int i=0;i++;i<sample){
	    tmp[i]=0;
	}
}
	


