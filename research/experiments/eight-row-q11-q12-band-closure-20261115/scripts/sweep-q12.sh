#!/bin/bash
# resume-safe q12 deficient-mode sweep (takeover run 2026-11-22)
# usage: ./sweep-q12.sh <start> <end> <budget_seconds> [base_cap]
# - one JSONL line per width appended to records/sweep-q12.jsonl
# - decided widths (UNSAT/SAT) are skipped without regenerating their CNF (this script wrote them)
# - INDET (timeout) widths are retried with doubled cap on later invocations
# - SAT (rc=10) halts everything immediately with exit code 42
# records schema matches sweep-q11.jsonl: {"q","m","status","conflicts","proc_s","cap","rc","cnf_md5","vars","clauses","tag","solver"}
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
cd "$BASE"
START=${1:?start m}; END=${2:?end m}; BUDGET=${3:?wall budget s}; BASECAP=${4:-60}
KISSAT="$BASE/bin/kissat"
# knowledge mounts may be noexec: fall back to an executable copy outside the mount
if ! "$KISSAT" --version >/dev/null 2>&1; then cp "$BASE/bin/kissat" /tmp/kissat-tko && chmod +x /tmp/kissat-tko && KISSAT=/tmp/kissat-tko; fi
TIME0=$(date +%s)
mkdir -p cnf records satlogs
RECORDS=records/sweep-q12.jsonl
touch "$RECORDS"

MAXPEAK=0
for ((m=START; m<=END; m++)); do
  NOW=$(date +%s)
  if [ $((NOW-TIME0)) -ge $BUDGET ]; then echo "BUDGET_EXIT next=$m"; exit 0; fi

  # resume check (record-first)
  REC=$(grep "\"m\":$m," "$RECORDS" | tail -1)
  R_ST=$(echo "$REC" | sed -n 's/.*"status":"\([A-Z]*\)".*/\1/p')
  if [ -n "$REC" ] && { [ "$R_ST" = "UNSAT" ] || [ "$R_ST" = "SAT" ]; }; then continue; fi

  # generate CNF
  node genfam12.js 8 "$m" 12 --deficient "cnf/q12_$m.cnf" > "satlogs/gen_$m.json" 2>/dev/null || { echo "GEN_FAIL m=$m"; exit 3; }
  VARS=$(sed -n 's/.*"vars":\([0-9]*\).*/\1/p' "satlogs/gen_$m.json")
  CLAUSES=$(sed -n 's/.*"clauses":\([0-9]*\).*/\1/p' "satlogs/gen_$m.json")
  MD5=$(md5sum "cnf/q12_$m.cnf" | awk '{print $1}')

  if [ -n "$REC" ] && [ "$R_ST" = "INDET" ]; then
      R_MD5=$(echo "$REC" | sed -n 's/.*"cnf_md5":"\([0-9a-f]*\)".*/\1/p')
      if [ "$R_MD5" != "$MD5" ]; then CAP=$BASECAP; else
        R_CAP=$(echo "$REC" | sed -n 's/.*"cap":\([0-9]*\).*/\1/p')
        [ "$R_CAP" -ge 4800 ] && { rm -f "cnf/q12_$m.cnf"; continue; }
        CAP=$(( R_CAP * 2 ))
      fi
  else
    CAP=$BASECAP
  fi
  [ "$CAP" -gt 4800 ] && CAP=4800

  timeout "$CAP" "$KISSAT" "cnf/q12_$m.cnf" > "satlogs/q12_$m.log" 2>&1
  RC=$?
  CONFLICTS=$(grep -m1 '^c conflicts:' "satlogs/q12_$m.log" | awk '{print $3}')
  [ -z "$CONFLICTS" ] && CONFLICTS=0
  PROC_RAW=$(grep -m1 '^c process-time:' "satlogs/q12_$m.log" | sed -n 's/.* \([0-9]*\.[0-9]*\) seconds.*/\1/p')
  PROC_S=${PROC_RAW%.*}
  case $RC in
    20) ST=UNSAT ;;
    10) ST=SAT ;;
    124) ST=INDET ;;
    *) ST=UNKNOWN_RC$RC ;;
  esac
  [ "$CONFLICTS" -gt "$MAXPEAK" ] && MAXPEAK=$CONFLICTS
  echo "{\"q\":12,\"m\":$m,\"status\":\"$ST\",\"conflicts\":$CONFLICTS,\"proc_s\":$PROC_S,\"cap\":$CAP,\"rc\":$RC,\"cnf_md5\":\"$MD5\",\"vars\":$VARS,\"clauses\":$CLAUSES,\"tag\":\"tko-1\",\"solver\":\"kissat-4.0.4-linux-amd64\"}" >> "$RECORDS"
  rm -f "cnf/q12_$m.cnf"
  if [ "$ST" = "SAT" ]; then
    echo "SAT_FOUND m=$m log=satlogs/q12_$m.log"
    exit 42
  fi
  if [ "${ST#UNKNOWN}" != "$ST" ]; then echo "ABNORMAL m=$m rc=$RC"; exit 4; fi
done
echo "RANGE_DONE $START..$END maxpeak=$MAXPEAK"
exit 0
