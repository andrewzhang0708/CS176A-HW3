#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

// By Junjie Liu and Andrew Zhang, edited from HW2.

void error(const char *);

int main(int argc, char *argv[])
{
   int sock, n;
   unsigned int length;
   struct sockaddr_in server, from;
   struct hostent *hp;
   char buffer[256];
   
   if (argc != 3)
   { 
        printf("Usage: server port\n");
        exit(1);
   }
   sock= socket(AF_INET, SOCK_DGRAM, 0);
   if (sock < 0)
   {
        error("socket");
   }

   server.sin_family = AF_INET;
   hp = gethostbyname(argv[1]);
   if (hp==0)
   {
        error("Unknown host");
   }

   bcopy((char *)hp->h_addr, 
        (char *)&server.sin_addr,
         hp->h_length);
   server.sin_port = htons(atoi(argv[2]));
   length=sizeof(struct sockaddr_in);
   printf("Enter string: ");
   bzero(buffer,256);
   fgets(buffer,255,stdin);
   n=sendto(sock,buffer,
            strlen(buffer),0,(const struct sockaddr *)&server,length);
   if (n < 0)
   {
        error("Sendto");
   }

   while(1){
        bzero(buffer, 256);
        n = recvfrom(sock, buffer, 256, 0, (struct sockaddr *)&from, &length);
        if(n < 0) error("recvfrom");
    
        printf("From server: ");
        fflush(stdout);
        write(1, buffer, n);

        buffer[n] = '\0';
        if(n > 0 && buffer[n-1] == '\n'){
            buffer[n-1] = '\0';
        }

        if(strncmp(buffer, "Sorry", 5) == 0 || (strlen(buffer) == 1 && buffer[0] >= '0' && buffer[0] <= '9')){
            exit(0);
        }
    }

    printf("\n");
   close(sock);
   return 0;
}

void error(const char *msg)
{
    perror(msg);
    exit(0);
}
