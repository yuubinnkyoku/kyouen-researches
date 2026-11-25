#!/bin/bash
CLS="$1"; TMO="$2"; K_ARG="${3:-}"; MP_ARG="${4:-}"
TAG=$(echo "$CLS" | tr -d '[], ')
F=/tmp/inst_${TAG}_${K_ARG}_${MP_ARG}.cnf
node class_sat.js 5 20 7 "$CLS" "$F" ${K_ARG:+"$K_ARG"} ${MP_ARG:+"$MP_ARG"} >/dev/null
T0=$(date +%s%3N)
timeout $TMO ./kissat-4.0.4-linux-amd64 "$F" > /tmp/out_$TAG.txt; RC=$?
T1=$(date +%s%3N)
V=$(grep "^s " /tmp/out_$TAG.txt | head -1)
CFL=$(grep "^c conflicts" /tmp/out_$TAG.txt | awk '{print $3}')
node -e "const rec={w:5,m:20,q:7,defRows:process.argv[1],k:process.argv[2]||null,minpos:process.argv[3]||null,verdict:process.argv[4],rc:Number(process.argv[5]),ms:Number(process.argv[6]),conflicts:process.argv[7]?Number(process.argv[7]):null,timeoutS:Number(process.argv[8])};require('fs').appendFileSync('records.jsonl',JSON.stringify(rec)+'\n');console.log('class '+process.argv[1]+' k='+(process.argv[2]||'-')+' mp='+(process.argv[3]||'-')+' -> '+process.argv[4]+' ('+(rec.ms/1000).toFixed(1)+'s, '+(rec.conflicts||'?')+' conflicts)')" "$CLS" "$K_ARG" "$MP_ARG" "$V" "$RC" "$((T1-T0))" "$CFL" "$TMO"
