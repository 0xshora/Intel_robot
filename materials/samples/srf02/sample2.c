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

int main( void ) {
	
    int fd[SRF_NUM];
	char filename[ 20 ];
	char buf[ 10 ];
	int res;
	int range[SRF_NUM] = {0};
	int count[SRF_NUM] = {0};
	int tmpE0[sample]={0},tmpE2[sample]={0},tmpE4[sample]={0},tmpE6[sample]={0};
	// I2Cデータバスをオープン
	sprintf( filename, "/dev/i2c-1" );

	fd[0] = open( filename, O_RDWR );
	if ( fd[0] < 0 ) {
		printf( "Failed to open\n" );
		exit( 1 );
	}
	fd[1] = open( filename, O_RDWR );
	if ( fd[1] < 0 ) {
		printf( "Failed to open\n" );
		exit( 1 );
	}
	fd[2] = open( filename, O_RDWR );
	if ( fd[2] < 0 ) {
		printf( "Failed to open\n" );
		exit( 1 );
	}
	fd[3] = open( filename, O_RDWR );
	if ( fd[3] < 0 ) {
		printf( "Failed to open\n" );
		exit( 1 );
	}

	if ( ioctl( fd[0], I2C_SLAVE, ( 0xE0 >> 1 ) ) < 0 ) {  // 0xE0(0x11100000) >> 1 = 0x70(0x01110000)
		printf( "Failed get slave address\n" );
		exit( 1 );
	}
	if ( ioctl( fd[1], I2C_SLAVE, ( 0xE2 >> 1 ) ) < 0 ) {  // 0xE0(0x11100000) >> 1 = 0x70(0x01110000)
		printf( "Failed get slave address\n" );
		exit( 1 );
	}
	if ( ioctl( fd[2], I2C_SLAVE, ( 0xE4 >> 1 ) ) < 0 ) {  // 0xE0(0x11100000) >> 1 = 0x70(0x01110000)
		printf( "Failed get slave address\n" );
		exit( 1 );
	}
	if ( ioctl( fd[3], I2C_SLAVE, ( 0xE6 >> 1 ) ) < 0 ) {  // 0xE0(0x11100000) >> 1 = 0x70(0x01110000)
		printf( "Failed get slave address\n" );
		exit( 1 );
	}

while(1){
	{ // read from 0xE0
		// コマンドレジスタ0に 0x51:Real Ranging Mode - Result in centimeters を送ることによって測距が始まる
		buf[ 0 ] = 0x00;
		buf[ 1 ] = 0x51;

		if ( ( write( fd[0], buf, 2 ) ) != 2 ) {
			printf( "Failed to set a ranging mode\n" );
			exit( 1 );
		}
		// Wait for the measurement
		// 音波だから、"行って" "帰ってくる" のに時間がかかる
		usleep( 66000 );

		// 測距開始
		buf[ 0 ] = 0x00;
		if ( ( write( fd[0], buf, 1 ) ) != 1 ) {
			printf( "cannot write to srf02\n" );
			exit( 1 );
		}

		if ( ( read( fd[0], buf, 4 ) ) != 4 ) {
			printf( "cannot read from srf02\n" );
			exit( 1 );
		}
		range[0] = buf[ 2 ] << 8;

		// 上位と下位をくっつける
		range[0] |= buf[ 3 ];

		tmpE0[count[0]]=range[0];
		if(count[0]==sample){
		    range[0]=true_range(tmpE0);
		    printf("[E0]: %d cm\n",range[0]);
		    count[0]=0;
		    reset(tmpE0);
		}else{
		    count[0]++;
		}

		//printf( "0xE0 Range=%d cm\n", range );
	}
	{ // read from 0xE0
		// コマンドレジスタ0に 0x51:Real Ranging Mode - Result in centimeters を送ることによって測距が始まる
		buf[ 0 ] = 0x00;
		buf[ 1 ] = 0x51;

		if ( ( write( fd[1], buf, 2 ) ) != 2 ) {
			printf( "Failed to set a ranging mode\n" );
			exit( 1 );
		}
		// Wait for the measurement
		// 音波だから、"行って" "帰ってくる" のに時間がかかる
		usleep( 66000 );

		// 測距開始
		buf[ 0 ] = 0x00;
		if ( ( write( fd[1], buf, 1 ) ) != 1 ) {
			printf( "cannot write to srf02\n" );
			exit( 1 );
		}

		if ( ( read( fd[1], buf, 4 ) ) != 4 ) {
			printf( "cannot read from srf02\n" );
			exit( 1 );
		}
		range[1] = buf[ 2 ] << 8;

		// 上位と下位をくっつける
		range[1] |= buf[ 3 ];
		
		tmpE2[count[1]]=range[1];
		if(count[1]==sample){
		    range[1]=true_range(tmpE2);
		    printf("	[E2]: %d cm\n",range[1]);
		    count[1]=0;
		    reset(tmpE2);
		}else{
		    count[1]++;
		}


		//printf( "0xE0 Range=%d cm\n", range );
	}
	{ // read from 0xE0
		// コマンドレジスタ0に 0x51:Real Ranging Mode - Result in centimeters を送ることによって測距が始まる
		buf[ 0 ] = 0x00;
		buf[ 1 ] = 0x51;

		if ( ( write( fd[2], buf, 2 ) ) != 2 ) {
			printf( "Failed to set a ranging mode\n" );
			exit( 1 );
		}
		// Wait for the measurement
		// 音波だから、"行って" "帰ってくる" のに時間がかかる
		usleep( 66000 );

		// 測距開始
		buf[ 0 ] = 0x00;
		if ( ( write( fd[2], buf, 1 ) ) != 1 ) {
			printf( "cannot write to srf02\n" );
			exit( 1 );
		}

		if ( ( read( fd[2], buf, 4 ) ) != 4 ) {
			printf( "cannot read from srf02\n" );
			exit( 1 );
		}
		range[2] = buf[ 2 ] << 8;

		// 上位と下位をくっつける
		range[2] |= buf[ 3 ];
		
		tmpE4[count[2]]=range[2];
		if(count[2]==sample){
		    range[2]=true_range(tmpE4);
		    printf("		[E4]: %d cm\n",range[2]);
		    count[2]=0;
		    reset(tmpE4);
		}else{
		    count[2]++;
		}

		  //printf( "0xE0 Range=%d cm\n", range );
	}
	{ // read from 0xE0
		// コマンドレジスタ0に 0x51:Real Ranging Mode - Result in centimeters を送ることによって測距が始まる
		buf[ 0 ] = 0x00;
		buf[ 1 ] = 0x51;

		if ( ( write( fd[3], buf, 2 ) ) != 2 ) {
			printf( "Failed to set a ranging mode\n" );
			exit( 1 );
		}
		// Wait for the measurement
		// 音波だから、"行って" "帰ってくる" のに時間がかかる
		usleep( 66000 );

		// 測距開始
		buf[ 0 ] = 0x00;
		if ( ( write( fd[3], buf, 1 ) ) != 1 ) {
			printf( "cannot write to srf02\n" );
			exit( 1 );
		}

		if ( ( read( fd[3], buf, 4 ) ) != 4 ) {
			printf( "cannot read from srf02\n" );
			exit( 1 );
		}
		range[3] = buf[ 2 ] << 8;

		// 上位と下位をくっつける
		range[3] |= buf[ 3 ];

		tmpE4[count[2]]=range[3];
		if(count[3]==sample){
		    range[3]=true_range(tmpE4);
		    printf("		    [E6]: %d cm\n",range[3]);
		    count[3]=0;
		    reset(tmpE4);
		}else{
		    count[3]++;
		}
		//printf( "0xE0 Range=%d cm\n", range );
	}
}
	// 閉じる！！
	close( fd[0] );
	close( fd[1] );
	close( fd[2] );
	close( fd[3] );

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

