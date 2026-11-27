#!/bin/bash
# usage: chunk.sh FIRST LAST  — runs keys in [FIRST,LAST], stage-1 2M cold pair
# + 15M escalation for UNKNOWN; skips keys with completed stage-1 pair.
# Self-terminates after ~270s wall so the bash 300s cap is not hit.
cd /home/user/work/n10th/repo || exit 1
mkdir -p raws
LOG=raws/driver.log
T0=$(date +%s)
echo "chunk $1..$2 start $(date -u +%FT%TZ)" >> $LOG
run_pair () { # key budget tag -> echoes "res,nodes" of p1, writes raws; returns 0 ok
  local i=$1 bud=$2 tag=$3 p rc
  for p in 1 2; do
    node jsreplay.js --exact-replay=input/k$i.input.csv --exact-replay-budget=$bud \
      > raws/at${tag}-k$i-p$p.raw 2>> $LOG
    rc=$?
    [ $rc -ne 0 ] && { echo "k$i $tag p$p rc=$rc" >> $LOG; return 1; }
  done
  local v1 v2
  v1=$(grep '^replay' raws/at${tag}-k$i-p1.raw | awk -F, '{print $7","$8}')
  v2=$(grep '^replay' raws/at${tag}-k$i-p2.raw | awk -F, '{print $7","$8}')
  echo "k$i $tag vals: p1=$v1 p2=$v2" >> $LOG
  if [ "$v1" != "$v2" ]; then echo "k$i $tag PAIR-MISMATCH" >> $LOG; return 2; fi
  echo "$v1"
}
for i in $(seq -w $1 $2); do
  [ -f raws/WIN-STOP ] && { echo "WIN-STOP, skip k$i" >> $LOG; break; }
  now=$(date +%s); [ $((now - T0)) -gt 250 ] && { echo "chunk time guard at k$i" >> $LOG; break; }
  # skip if stage-1 pair already complete and consistent
  if [ -s raws/at2m-k$i-p1.raw ] && [ -s raws/at2m-k$i-p2.raw ]; then
    v1=$(grep '^replay' raws/at2m-k$i-p1.raw | awk -F, '{print $7","$8}')
    v2=$(grep '^replay' raws/at2m-k$i-p2.raw | awk -F, '{print $7","$8}')
    if [ -n "$v1" ] && [ "$v1" = "$v2" ]; then res=${v1%%,*}
      if [ "$res" != "0" ] || { [ -s raws/at15m-k$i-p1.raw ] && [ -s raws/at15m-k$i-p2.raw ]; }; then
        echo "k$i already done" >> $LOG; continue
      fi
    fi
  fi
  OUT=$(run_pair $i 2000000 2m); rc=$?
  [ $rc -ne 0 ] && { echo "k$i 2m rc=$rc" >> $LOG; continue; }
  res=${OUT%%,*}
  if [ "$res" = "1" ]; then echo "k$i 2m WIN -> WIN-STOP" >> $LOG; touch raws/WIN-STOP; break; fi
  [ "$res" = "2" ] && { echo "k$i 2m LOSS resolved" >> $LOG; continue; }
  # escalate
  OUT=$(run_pair $i 15000000 15m); rc=$?
  [ $rc -ne 0 ] && { echo "k$i 15m rc=$rc" >> $LOG; continue; }
  res=${OUT%%,*}
  if [ "$res" = "1" ]; then echo "k$i 15m WIN -> WIN-STOP" >> $LOG; touch raws/WIN-STOP; break; fi
  [ "$res" = "2" ] && echo "k$i 15m LOSS resolved" >> $LOG || echo "k$i 15m UNKNOWN parked" >> $LOG
done
echo "chunk end $(date -u +%FT%TZ)" >> $LOG
