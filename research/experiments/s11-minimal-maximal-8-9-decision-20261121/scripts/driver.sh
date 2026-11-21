#!/bin/bash
# Driver v5: SAT-hunting config (--sat) for SAT-expected instances, default for UNSAT records.
cd /home/user/work/s11
mkdir -p runs
KS=/home/user/knowledge/kyouen-research/_s11-lane
run() {
  name=$1; opts=$2
  echo "=== START $name opts='$opts' $(date -Is)" >> runs/log.txt
  start=$(date +%s)
  ./kissat $opts cnf_$name.cnf > runs/$name.out 2> runs/$name.err
  rc=$?
  end=$(date +%s)
  echo "=== END $name rc=$rc secs=$((end-start)) $(date -Is)" >> runs/log.txt
  grep -E '^s ' runs/$name.out >> runs/log.txt 2>/dev/null
  cp runs/log.txt $KS/log_snapshot.txt
  cp runs/$name.out $KS/last_$name.out 2>/dev/null
}
run n11_k10 "--sat"
run n11_k9fund "--sat"
run n9_k9 "--sat"
run n9_k8 ""
run n11_k8fund "--sat"
run n11_k9 ""
run n11_k8 ""
run n11_k9fund ""
echo "=== ALL DONE $(date -Is)" >> runs/log.txt
cp runs/log.txt $KS/log_snapshot.txt
