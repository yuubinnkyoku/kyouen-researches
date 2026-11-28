#!/bin/bash
# canon.sh — canonical reproduction procedure for t2-blocking-duality-20261128.
# Prereqs: zig cc (0.13.0, tarball sha256 d45312e6...230ea = repo pin), python3.
# Board files (already in repo):
#   research/experiments/projective-blocking-kyouen-20261125/output/board_pg2q{3,4}.txt
#   research/experiments/s-parameter-kyouen-20261125/output/board_ag2q{3,4,5}.txt
#   boards/board_pg2q5.txt in this kit (GF(5) construction, see verify_duality.py).
# Everything is deterministic; run1 and run2 outputs must be byte-identical.
set -e
zig cc -O2 -o blocking_duality scripts/blocking_duality.c

PG=../projective-blocking-kyouen-20261125/output
AG=../s-parameter-kyouen-20261125/output
run2 () { # tag board s : two runs, both with list dump, byte-compare all outputs
  ./blocking_duality -l a_$1 $2 $3 > r1_$1.txt
  ./blocking_duality -l b_$1 $2 $3 > r2_$1.txt
  diff r1_$1.txt r2_$1.txt
  diff a_$1.maximal.txt b_$1.maximal.txt
  diff a_$1.minimal.txt b_$1.minimal.txt
}

# 0) calibration on t=1 boards (published values: 1240 / 247 / 10741 / 36475,
#    size splits per K1367 / K1356+K1366 / K1366 / K1364)
./blocking_duality $AG/board_ag2q4.txt 3
./blocking_duality $PG/board_pg2q3.txt 3
./blocking_duality $PG/board_pg2q4.txt 4
./blocking_duality $AG/board_ag2q5.txt 4

# 1) the six boards (t>=2 sweep + AG(2,3) t=1 small board)
run2 pg2q3s2 $PG/board_pg2q3.txt 2
run2 pg2q4s3 $PG/board_pg2q4.txt 3
run2 ag2q3s2 $AG/board_ag2q3.txt 2
run2 ag2q4s2 $AG/board_ag2q4.txt 2
run2 ag2q5s3 $AG/board_ag2q5.txt 3
run2 pg2q5s4 boards/board_pg2q5.txt 4

# 2) independent python verification of every dumped mask (all six boards;
#    PG(2,5) takes ~3 min) + derived-board regeneration
python3 scripts/verify_duality.py $PG/board_pg2q3.txt pg 3 2 a_pg2q3s2.maximal.txt a_pg2q3s2.minimal.txt both
python3 scripts/verify_duality.py $PG/board_pg2q4.txt pg 4 3 a_pg2q4s3.maximal.txt a_pg2q4s3.minimal.txt both
python3 scripts/verify_duality.py $AG/board_ag2q3.txt ag 3 2 a_ag2q3s2.maximal.txt a_ag2q3s2.minimal.txt both
python3 scripts/verify_duality.py $AG/board_ag2q4.txt ag 4 2 a_ag2q4s2.maximal.txt a_ag2q4s2.minimal.txt both
python3 scripts/verify_duality.py $AG/board_ag2q5.txt ag 5 3 a_ag2q5s3.maximal.txt a_ag2q5s3.minimal.txt both
python3 scripts/verify_duality.py boards/board_pg2q5.txt pg 5 4 a_pg2q5s4.maximal.txt a_pg2q5s4.minimal.txt both

# 3) third system: pure-python brute enumeration (direct definitions,
#    no Gray code) on the four boards with n<=21
for b in "$PG/board_pg2q3.txt 2" "$AG/board_ag2q3.txt 2" "$AG/board_ag2q4.txt 2" "$PG/board_pg2q4.txt 3"; do
  python3 scripts/brute_third.py $b
done

# 4) derived-board rerun: C enumerator on the independently GF-constructed
#    boards (different point labeling) must reproduce identical counts
for d in "$PG/board_pg2q3.txt.derived.txt 2" "$PG/board_pg2q4.txt.derived.txt 3" \
         "$AG/board_ag2q3.txt.derived.txt 2" "$AG/board_ag2q4.txt.derived.txt 2" \
         "$AG/board_ag2q5.txt.derived.txt 3"; do
  ./blocking_duality $d
done
