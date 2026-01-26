#!/bin/bash

FILE="/sys/class/thermal/thermal_zone0/temp"

if [[ ! -r "$FILE" ]]; then
  echo "sensor=cpu_temp status=error reason=unreadable path=$FILE"
  exit 0
fi

raw=$(<"$FILE")               # millidegrees C
temp_c=$(awk "BEGIN { printf \"%.2f\", $raw/1000 }")

echo "sensor=cpu_temp temp_c=$temp_c"
