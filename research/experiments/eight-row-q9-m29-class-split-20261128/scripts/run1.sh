#!/bin/bash
set -u
W=$1; M=$2; CLS=$3; KROW=$4; MP=$5; TMO=${6:-280}
S3=scripts/sat3.js
TAG="c${CLS}k${KROW/:/}p${MP}"
OUT=out
CNF=$OUT/r${W}x${M}q9_${TAG}.cnf; KSOUT=$OUT/k_${TAG}_m${M}.txt
node --max-old-space-size=6144 $S3 $W $M 9 --class=$CLS --krow=$KROW --minpos=$MP $CNF > $OUT/meta_${TAG}_m${M}.json
T0=$(date +%s.%N); timeout $TMO ./kissat $CNF > $KSOUT 2>&1; KSRC=$?; T1=$(date +%s.%N)
KSEC=$(echo "$T1 $T0" | awk '{printf "%.1f",$1-$2}')
KCONF=$(grep -E "^c conflicts" $KSOUT | tail -1 | awk '{print $3}')
if [ "$KSRC" = "10" ]; then KRES=SAT; elif [ "$KSRC" = "20" ]; then KRES=UNSAT; else KRES=INDET; fi
echo "PIECE w$W m$M class$CLS krow$KROW minpos$MP -> $KRES rc=$KSRC conflicts=${KCONF:-null} sec=$KSEC"
if [ "$KRES" = "SAT" ]; then grep "^v " $KSOUT > $OUT/model_${TAG}_m${M}.txt; fi
rm -f $CNF
