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

int main( void ) {
	
	int fd;
	char filename[ 20 ];
	char buf[ 10 ];
	int res;
	int range = 0;

	// I2Cデータバスをオープン
	sprintf( filename, "/dev/i2c-1" );

	fd = open( filename, O_RDWR );
	if ( fd < 0 ) {
		printf( "Failed to open\n" );
		exit( 1 );
	}

	if ( ioctl( fd, I2C_SLAVE, ( 0xE0 >> 1 ) ) < 0 ) {  // 0xE0(0x11100000) >> 1 = 0x70(0x01110000)
		printf( "Failed get slave address\n" );
		exit( 1 );
	}

	{ // read from 0xE0
		// コマンドレジスタ0に 0x51:Real Ranging Mode - Result in centimeters を送ることによって測距が始まる
		buf[ 0 ] = 0x00;
		buf[ 1 ] = 0x51;

		if ( ( write( fd, buf, 2 ) ) != 2 ) {
			printf( "Failed to set a ranging mode\n" );
			exit( 1 );
		}
		// Wait for the measurement
		// 音波だから、"行って" "帰ってくる" のに時間がかかる
		usleep( 66000 );

		// 測距開始
		buf[ 0 ] = 0x00;
		if ( ( write( fd, buf, 1 ) ) != 1 ) {
			printf( "cannot write to srf02\n" );
			exit( 1 );
		}

		if ( ( read( fd, buf, 4 ) ) != 4 ) {
			printf( "cannot read from srf02\n" );
			exit( 1 );
		}
		range = buf[ 2 ] << 8;

		// 上位と下位をくっつける
		range |= buf[ 3 ];

		printf( "0xE0 Range=%d cm\n", range );
	}

	// 閉じる！！
	close( fd );

	return 0;	
}
