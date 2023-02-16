#include <time.h>
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <sys/time.h>

#define OGS_TIME_TO_BCD(x) \
    (((((x) % 10) << 4) & 0xf0) | (((x) / 10) & 0x0f))

#define OGS_NAS_TIME_TO_BCD(x) OGS_TIME_TO_BCD(x)


int get_time_of_day(struct timeval *tv) {
    int rc = gettimeofday(tv, NULL);

    return (rc);
}

void get_gmtime(time_t s, struct tm *tm) {
    memset(tm, 0, sizeof(*tm));

    (void)gmtime_r(&s, tm);
}

void get_localtime(time_t s, struct tm *tm) {

    memset(tm, 0, sizeof(*tm));

    (void)localtime_r(&s, tm);
}


int main () {
    struct timeval tv;
    struct tm gmt, local;
    uint8_t local_time_zone;

    int rc = get_time_of_day(&tv);

    get_gmtime(tv.tv_sec, &gmt);

    get_localtime(tv.tv_sec, &local);

    if (local.tm_gmtoff >= 0) {
        local_time_zone = OGS_NAS_TIME_TO_BCD(local.tm_gmtoff / 900);
    } else {
        local_time_zone = OGS_NAS_TIME_TO_BCD((-local.tm_gmtoff) / 900);
        local_time_zone |= 0x08;
    }

    printf(" Year %d \n", OGS_NAS_TIME_TO_BCD(gmt.tm_year % 100));
    printf(" Month %d\n", OGS_NAS_TIME_TO_BCD(gmt.tm_mon+1));
    printf(" Day %d\n", OGS_NAS_TIME_TO_BCD(gmt.tm_mday));
    printf(" Hour %d\n", OGS_NAS_TIME_TO_BCD(gmt.tm_hour));
    printf(" Minute %d\n", OGS_NAS_TIME_TO_BCD(gmt.tm_min));
    printf(" Sec %d\n", OGS_NAS_TIME_TO_BCD(gmt.tm_sec));
    printf(" Local TimeZone %d\n", local_time_zone);

    return (0);
}

