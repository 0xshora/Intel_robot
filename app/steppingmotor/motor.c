#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include "wiringPi.h"
#include "wiringPiSPI.h"

#define BUFSIZE 32
#define MAXCHAR 256
#define MAXCOM 16
#define SLOPE_TIME 10000
#define MAXDIGIT 100
#define MAX_SPEED 50000
#define MIN_SPEED -50000
#define MAX_ROLL 10000
#define MIN_ROLL 100
#define MINUS_MIN_ROLL -100
#define MINUS_MAX_ROLL -10000
#define MAX_SCALE 3
#define MIN_SCALE 0.5

int L6470_SPI_CHANNEL;

// 関数プロトタイプ。

extern void L6470_write(unsigned char data);
extern void L6470_init(void);
extern void L6470_run(long speed);
extern void L6470_run_both(long speed);
extern void L6470_run_turn(long speed);
extern void L6470_run_turn_moving(long speed, int right, float scale);
extern void L6470_softstop();
extern void L6470_softhiz();
extern void L6470_speed_change(long speed, int postspeed); //change the speed from "speed" to postspeed
extern void new_speed_change(long speed, int postspeed);
extern void getargs(int * argc, char * argv[], char * buf);
extern void L6470_turn_speed_change(long, int);



int main(int argc, char ** argv) {
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
    if (wiringPiSPISetup(0, 1000000) < 0) {
        printf("SPI Setup failed:\n");
    }
    if (wiringPiSPISetup(1, 1000000) < 0) {
        printf("SPI Setup failed:\n");
    }

    // L6470の初期化。
    L6470_SPI_CHANNEL = 0;
    L6470_init();
    L6470_SPI_CHANNEL = 1;
    L6470_init();

    //printf("Speed Change --> p speed(-10000 ~ 10000)\n");
    //printf("Turn Right   --> r scale(0.1 ~ 10)\n");
    //printf("Turn Left    --> l scale(0.1 ~ 10)\n");
    //printf("Stop         --> s\n");
    //printf("End          --> e\n");
    
    int my_argc;
    char **my_argv;
    
    int turn_flg = 0;
 

    //for setting up a tcp server
    int sockfd;
    int new_sockfd;
    unsigned int clit_len;
    unsigned short serv_port = 50001;
    struct sockaddr_in serv_addr;
    struct sockaddr_in clit_addr;

    if ((sockfd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0) {
        fprintf(stderr, "socket() failed\n");
        exit(1);
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    serv_addr.sin_port = htons(serv_port);

    if (bind(sockfd, (struct sockaddr * ) & serv_addr, sizeof(serv_addr)) < 0) {
        fprintf(stderr, "bind() failed\n");
        exit(1);
    }

    if (listen(sockfd, 1) < 0) {
        fprintf(stderr, "listen() failed\n");
        close(sockfd);
        exit(1);
    }

    while (1) {
        clit_len = sizeof(clit_addr);
        if ((new_sockfd = accept(sockfd, (struct sockaddr * ) & clit_addr, & clit_len)) < 0) {
            fprintf(stderr, "accept() failed\n");
            close(sockfd);
            exit(1);
        }

        char buf[256];
        int buf_len;
        int ac = 0;
        char **av;
        av = malloc(sizeof(char *) * MAXCOM);
        int i;
        for (i = 0; i < MAXCOM; i++) {
            av[i] = malloc(sizeof(char) * MAXCHAR);
        }
        memset(buf, 0, 256);

        if ((buf_len = read(new_sockfd, buf, 256)) < 0) {
            fprintf(stderr, "read() failed\n");
            continue;
        }

        getargs(&ac, av, buf);

        fprintf(stderr, "%s:%s\n", av[0], av[1]);

        if (strcmp(av[0], "p") == 0) {
            long sp = atol(av[1]);
            L6470_speed_change(speed, sp);
            speed = sp;
            // printf("*** Speed %ld ***\n", speed);
        }

        if (strcmp(av[0], "r") == 0 || strcmp(av[0], "l") == 0) {
            if (speed != 0) {
                double scale = atof(av[1]);
                if (strcmp(buf, "r") == 0) {
                    int right_true = 1;
                    L6470_run_turn_moving(speed, right_true, scale);
                } else {
                    int right_false = 0;
                    L6470_run_turn_moving(speed, right_false, scale);
                }
            } else {
                long sp = atol(av[1]);
                if (strcmp(buf, "r") == 0) {
					turn_flg = 1;
                    L6470_run_turn(sp);
        			speed = 0;
                } else {
					turn_flg = 1;
                    L6470_run_turn(sp);
                    speed = 0;
                }
            }
        }

        if (strcmp(buf, "s") == 0 && turn_flg == 0) {
            L6470_speed_change(speed, 0);
            speed = 0;
        } else if (strcmp(buf, "s") == 0 && turn_flg == 1) {
			L6470_turn_speed_change(speed, 0);
			speed = 0;
			turn_flg = 0;
		}

        if (strcmp(buf, "e") == 0) {
            L6470_speed_change(speed, 0);
			speed = 0;
            close(new_sockfd);
            close(sockfd);
            exit(0);
        }
    }
	return 0;
}
