#!/bin/bash
# stage1-only 2M sweep for given key range (escalation suppressed after WIN)
cd /home/user/work/n10th/repo || exit 1
mkdir -p raws
LOG=raws/driver.log
T0=$(date +%s)
echo "stage1 chunk $1..$2 start $(date -u +%FT%TZ)" >> $LOG
for i in $(seq -w $1 $2); do
  now=$(date +%s); [ $((now - T0)) -gt 250 ] && { echo "stage1 time guard at k$i" >> $LOG; break; }
  v1=$(grep '^replay' raws/at2m-k$i-p1.raw 2>/dev/null | awk -F, '{print $7","$8}')
  v2=$(grep '^replay' raws/at2m-k$i-p2.raw 2>/dev/null | awk -F, '{print $7","$8}')
  if [ -n "$v1" ] && [ "$v1" = "$v2" ]; then echo "k$i 2m already done ($v1)" >> $LOG; continue; fi
  for p in 1 2; do
    node jsreplay.js --exact-replay=input/k$i.input.csv --exact-replay-budget=2000000 \
      > raws/at2m-k$i-p$p.raw 2>> $LOG || { echo "k$i 2m p$p rc=$?" >> $LOG; break; }
  done
  v1=$(grep '^replay' raws/at2m-k$i-p1.raw | awk -F, '{print $7","$8}')
  v2=$(grep '^replay' raws/at2m-k$i-p2.raw | awk -F, '{print $7","$8}')
  echo "k$i 2m vals: p1=$v1 p2=$v2" >> $LOG
  [ "$v1" != "$v2" ] && echo "k$i 2m PAIR-MISMATCH" >> $LOG
done
echo "stage1 chunk end $(date -u +%FT%TZ)" >> $LOG
