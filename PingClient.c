#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <sys/time.h>


void error(const char *msg) {
    perror(msg);
    exit(1);
}

double get_time_in_ms() {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return tv.tv_sec * 1000.0 + tv.tv_usec / 1000.0;
}

int main(int argc, char *argv[]) {
    int sock, portno, n;
    struct sockaddr_in server, from;
    struct hostent *hp;
    socklen_t serverlen;
    char buffer[1024];

    const int TIMEOUT_SEC = 1;
    const int NUM_PINGS = 10;

    if (argc != 3) {
        fprintf(stderr, "Usage: %s <hostname> <port>\n", argv[0]);
        exit(1);
    }

    sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0)
        error("socket");

    struct timeval timeout;
    timeout.tv_sec = TIMEOUT_SEC;
    timeout.tv_usec = 0;
    setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, (char *)&timeout, sizeof(timeout));

    hp = gethostbyname(argv[1]);
    if (hp == NULL)
        error("Unknown host");

    portno = atoi(argv[2]);
    bzero((char *)&server, sizeof(server));
    server.sin_family = AF_INET;
    bcopy((char *)hp->h_addr, (char *)&server.sin_addr, hp->h_length);
    server.sin_port = htons(portno);
    serverlen = sizeof(server);

    // printf("PING %s:%d with %d packets:\n", argv[1], portno, NUM_PINGS);

    double rtts[NUM_PINGS];
    int received = 0;

    for (int i = 0; i < NUM_PINGS; i++) {
        double send_time = get_time_in_ms();

        sprintf(buffer, "PING %d %f", i + 1, send_time);

        n = sendto(sock, buffer, strlen(buffer), 0, (struct sockaddr *)&server, serverlen);
        if (n < 0)
            error("sendto");

        bzero(buffer, sizeof(buffer));
        socklen_t fromlen = sizeof(from);
        n = recvfrom(sock, buffer, sizeof(buffer) - 1, 0, (struct sockaddr *)&from, &fromlen);
        double recv_time = get_time_in_ms();

        if (n < 0) {
            printf("Request timeout for seq#=%d\n", i + 1);
            rtts[i] = -1;
        } else {
            buffer[n] = '\0';
            double rtt = recv_time - send_time;
            rtts[i] = rtt;
            received++;
            printf("111PING received from 127.0.0.1: seq#=%d\n",
                   i + 1);
        }
        sleep(1);
    }

    double sum = 0, min = 1e9, max = -1;
    for (int i = 0; i < NUM_PINGS; i++) {
        if (rtts[i] > 0) {
            sum += rtts[i];
            if (rtts[i] < min) min = rtts[i];
            if (rtts[i] > max) max = rtts[i];
        }
    }

    printf("--- %s ping statistics ---\n", argv[1]);
    printf("%d packets transmitted, %d received, %.0f%% packet loss\n",
           NUM_PINGS, received, 100.0 * (NUM_PINGS - received) / NUM_PINGS);

    if (received > 0) {
        printf("rtt min/avg/max = %.3f/%.3f/%.3f ms\n",
               min, sum / received, max);
    }

    close(sock);
    return 0;
}
