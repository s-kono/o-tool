#!/bin/bash

set -u

export LANG=C
export LC_CTYPE=en_US.utf8
export PATH=/sbin:/bin:/usr/sbin:/usr/bin

readonly URL_iCalGoogle_JHoliday="https://calendar.google.com/calendar/ical/ja.japanese%23holiday@group.v.calendar.google.com/public/basic.ics"
# https://ja.wikipedia.org/wiki/ICalendar

readonly URL_csvCAO_JHoliday=https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv
# https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html

readonly TODAY_YYYYMMDD=$( date +%Y%m%d )

curl -sSm 5 "${URL_iCalGoogle_JHoliday}" \
| tr -d '\r' \
| grep -E "^(DTSTART|SUMMARY)" \
| awk -F: '{print $NF}' \
| xargs -L 2 \
| sort -n \
| awk '$1 >= '${TODAY_YYYYMMDD}' {print $0}'

sleep 1

curl -sSm 5 "${URL_csvCAO_JHoliday}" \
| tr -d '\r' \
| sed -n '2,$p' \
| nkf -w \
| tr , ' ' \
| while read _d _n; do
    echo "$( date +%Y%m%d -d${_d} ) ${_n}"
done \
| awk '$1 >= '${TODAY_YYYYMMDD}' {print $0}'

exit
