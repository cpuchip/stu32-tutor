/* probe: what a process inside stu32-calc's container can do (calc/acceptance.py). Built static, mounted
 * read only at /probe and run as the entry point under run.sh's flags; never part of the image.
 * It tries to write in three places and to reach the network two ways, and prints one JSON line:
 * each attempt's errno name, "ok" when it succeeded. */
#define _GNU_SOURCE
#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

static const char *write_at(const char *path)
{
    int fd = open(path, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd < 0) return strerrorname_np(errno);
    ssize_t n = write(fd, "x", 1);
    close(fd);
    return n == 1 ? "ok" : strerrorname_np(errno);
}

static const char *reach(int type)
{
    int s = socket(AF_INET, type, 0);
    if (s < 0) return strerrorname_np(errno);
    struct sockaddr_in a = {.sin_family = AF_INET, .sin_port = htons(53)};
    inet_pton(AF_INET, "1.1.1.1", &a.sin_addr);
    int r = type == SOCK_STREAM ? connect(s, (struct sockaddr *)&a, sizeof a)
                                : (int)sendto(s, "x", 1, 0, (struct sockaddr *)&a, sizeof a);
    const char *out = r < 0 ? strerrorname_np(errno) : "ok";
    close(s);
    return out;
}

static const char *readable(const char *path)
{
    return access(path, R_OK) == 0 ? "ok" : strerrorname_np(errno);
}

int main(void)
{
    printf("{\"licenses\":\"%s %s %s\",", readable("/licenses/abacus-firmware-MIT.txt"),
           readable("/licenses/casimir-MIT.txt"), readable("/licenses/intel-dfp-BSD-3.txt"));
    printf("\"uid\":%d,\"write_root\":\"%s\",\"write_opt\":\"%s\",\"write_tmp\":\"%s\","
           "\"tcp_1.1.1.1:53\":\"%s\",\"udp_1.1.1.1:53\":\"%s\"}\n",
           (int)getuid(), write_at("/probe-written"), write_at("/opt/stu32/probe-written"),
           write_at("/tmp/probe-written"), reach(SOCK_STREAM), reach(SOCK_DGRAM));
    return 0;
}
