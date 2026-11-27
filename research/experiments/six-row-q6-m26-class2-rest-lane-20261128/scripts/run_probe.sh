#!/bin/bash
# usage: run_probe.sh <cnf> <rawlog> <cap_s>
# kissat 4.0.4 official linux-amd64 (sha256 21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1),
# unpacked from the official release asset zip (sha256 63282e5168ca040a2018edfba0726bf893a7a6bcdb1db87feb67857e2da697a7).
K=$HOME/lane-work/kissat/kissat-4.0.4-linux-amd64
timeout -s TERM "$3" "$K" "$1" > "$2"
rc=$?
if [ -s "$2" ] && grep -q '^s ' "$2"; then :; fi
exit $rc
