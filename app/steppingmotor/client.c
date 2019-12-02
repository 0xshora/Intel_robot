#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

void client(char *host, in_port_t port, char *msg){
  int s;
  struct sockaddr_in sv_skt;

  if((s = socket(AF_INET, SOCK_STREAM, 0)) < 0){
    perror("socket");
    exit(1);
  }

  sv_skt.sin_family = AF_INET;
  sv_skt.sin_addr.s_addr = inet_addr(host);
  sv_skt.sin_port = htons(port);

  if(connect(s, (struct sockaddr *)&sv_skt, sizeof(sv_skt)) < 0){
    perror("connect");
    close(s);
    exit(1);
  }

  if(write(s, msg, strlen(msg)) < 0){
    perror("write");
    close(s);
    exit(1);
  }

  close(s);
}

