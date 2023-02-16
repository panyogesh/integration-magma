#include <time.h>
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>

#define OAILOG_ERROR fprintf
#define LOG_NAS_EMM stderr
#define RETURNerror -1
#define RETURNok 0
#define MAX_MINUTE_DIGITS 3
#define TIME_ZONE_IE_MAX_LENGTH 2

int get_time_zone(void) {
  char timestr[20] = {0};
  char string[MAX_MINUTE_DIGITS] = {0};
  time_t t;
  struct tm* tmp;
  struct tm updateTime;
  int hour = 0, minute = 0, timezone = 0;

  t = time(NULL);
  tmp = localtime_r(&t, &updateTime);
  if (tmp == NULL) {
    OAILOG_ERROR(LOG_NAS_EMM, "localtime_r() failed to get local timer info ");
    return RETURNerror;
  }

  if (strftime(timestr, sizeof(timestr), "%z", &updateTime) == 0) {
    OAILOG_ERROR(LOG_NAS_EMM, "EMMAS-SAP - strftime() Failed to get timezone");
    return RETURNerror;
  }

  /* the string shall be in the form of +hhmm (+0530) */
  if (timestr[0] == '-') {
    timezone = 0x08;
  }
  hour = (10 * (timestr[1] - '0')) | (timestr[2] - '0');
  minute = ((10 * (timestr[3] - '0')) | (timestr[4] - '0')) + (hour * 60);
  minute /= 15;

  snprintf(string, sizeof(string), "%02d", minute);
  timezone |= (string[1] - '0') << 4;
  timezone |= (string[0] - '0');

  return (timezone);
}

int emm_send_emm_information()
{
  time_t t;
  struct tm* tmp;
  struct tm updateTime;
  uint8_t formatted;
  char string[MAX_MINUTE_DIGITS] = {0};

  /*
   * optional - Local Time Zone
   */
  int result = get_time_zone();
  if (result != RETURNerror) {
    printf ("\n get_time_zone() -> localtimezone %d, Size(TIME_ZONE_IE_MAX_LENGTH=%d) \n",
            result, TIME_ZONE_IE_MAX_LENGTH);
  }

  t = time(NULL);
  tmp = gmtime_r(&t, &updateTime);
  if (tmp == NULL) {
    OAILOG_ERROR(LOG_NAS_EMM, "gmtime() failed to get local timer info");
    return (RETURNerror);
  }

  /*
   * Time SHALL be encoded as specified in 3GPP 23.040 in SM-TL TPDU format.
   */
  /*
   * updateTime.year is "years since 1900"
   * GSM format is the last 2 digits of the year.
   */
  snprintf(string, sizeof(string), "%02d", updateTime.tm_year + 1900 - 2000);
  formatted = (string[1] - '0') << 4;
  formatted |= (string[0] - '0');

  printf("\n universaltimeandlocaltimezone.year %d \n", formatted);

  /*
   * updateTime.tm_mon is "months since January" in [0-11] range.
   * GSM format is months in [1-12] range.
   */
  snprintf(string, sizeof(string), "%02d", updateTime.tm_mon + 1);
  formatted = (string[1] - '0') << 4;
  formatted |= (string[0] - '0');
  printf("\n universaltimeandlocaltimezone.month %d \n", formatted);

  snprintf(string, sizeof(string), "%02d", updateTime.tm_mday);
  formatted = (string[1] - '0') << 4;
  formatted |= (string[0] - '0');
  printf("\n universaltimeandlocaltimezone.day %d\n", formatted);

  snprintf(string, sizeof(string), "%02d", updateTime.tm_hour);
  formatted = (string[1] - '0') << 4;
  formatted |= (string[0] - '0');
  printf("\n niversaltimeandlocaltimezone.hour=%d \n", formatted);


  snprintf(string, sizeof(string), "%02d", updateTime.tm_min);
  formatted = (string[1] - '0') << 4;
  formatted |= (string[0] - '0');
  printf("\n universaltimeandlocaltimezone.minute %d\n", formatted);

  snprintf(string, sizeof(string), "%02d", updateTime.tm_sec);
  formatted = (string[1] - '0') << 4;
  formatted |= (string[0] - '0');
  printf ("\n universaltimeandlocaltimezone.second %d \n", formatted);


  return (0);
}

int main () {
   emm_send_emm_information();
   return 0;
}
