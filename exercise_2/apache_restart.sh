#!/bin/bash
LOGFILE=/home/user/public_html/domain.com/cron/restart.log
function float_to_int() {
echo $1 | cut -d. -f1
}
check=$(uptime | awk -F' *,? *' '{print $12}')
now=$(date)
checkk=$(float_to_int $check)
if [[ $checkk > 40 ]]; then
        echo $now $checkk >> $LOGFILE 2>&1
        /usr/bin/systemctl restart httpd.service
fi