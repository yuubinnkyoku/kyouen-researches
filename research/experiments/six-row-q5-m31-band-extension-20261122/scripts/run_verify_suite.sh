#!/bin/bash
# Deterministic 3-system verification suite for the (6,5) 6x31 witness + controls.
set -u
RUN="$1"; mkdir -p "output/verify-suite/$RUN"
sg() { node scripts/surgery_gen.js --verify "$@"; }
py() { python3 "$@"; }
W=6; M=31; Q=5
# 1) witness — three systems
sg $W $M $Q w6x31q5_L2shift1.json > "output/verify-suite/$RUN/w_sysa.txt" 2>&1; echo "rc_a=$?" >> "output/verify-suite/$RUN/w_sysa.txt"
py scripts/det_q_verify.py $W $M $Q < w6x31q5_L2shift1.json > "output/verify-suite/$RUN/w_sysb.txt" 2>&1; echo "rc_b=$?" >> "output/verify-suite/$RUN/w_sysb.txt"
py scripts/append_criterion.py $W 50 $Q < w6x31q5_L2shift1.json > "output/verify-suite/$RUN/w_sysc.txt" 2>&1; echo "rc_c=$?" >> "output/verify-suite/$RUN/w_sysc.txt"
# 2) tamper controls (must FAIL)
for t in 1 2; do
  sg $W $M $Q verify/nc_tamper$t.json > "output/verify-suite/$RUN/tamper${t}_sysa.txt" 2>&1; echo "rc_a=$?" >> "output/verify-suite/$RUN/tamper${t}_sysa.txt"
  py scripts/det_q_verify.py $W $M $Q < verify/nc_tamper$t.json > "output/verify-suite/$RUN/tamper${t}_sysb.txt" 2>&1; echo "rc_b=$?" >> "output/verify-suite/$RUN/tamper${t}_sysb.txt"
  py scripts/append_criterion.py $W 50 $Q < verify/nc_tamper$t.json > "output/verify-suite/$RUN/tamper${t}_sysc.txt" 2>&1; echo "rc_c=$?" >> "output/verify-suite/$RUN/tamper${t}_sysc.txt"
done
# 3) five-in-a-row control (must FAIL)
sg $W $M $Q verify/nc_line.json > "output/verify-suite/$RUN/nc_line_sysa.txt" 2>&1; echo "rc_a=$?" >> "output/verify-suite/$RUN/nc_line_sysa.txt"
py scripts/det_q_verify.py $W $M $Q < verify/nc_line.json > "output/verify-suite/$RUN/nc_line_sysb.txt" 2>&1; echo "rc_b=$?" >> "output/verify-suite/$RUN/nc_line_sysb.txt"
py scripts/append_criterion.py $W 50 $Q < verify/nc_line.json > "output/verify-suite/$RUN/nc_line_sysc.txt" 2>&1; echo "rc_c=$?" >> "output/verify-suite/$RUN/nc_line_sysc.txt"
# 4) positive control: published L2 6x30 witness (must PASS at m=30)
sg $W 30 $Q verify/L2_stones.json > "output/verify-suite/$RUN/posctrl_sysa.txt" 2>&1; echo "rc_a=$?" >> "output/verify-suite/$RUN/posctrl_sysa.txt"
py scripts/det_q_verify.py $W 30 $Q < verify/L2_stones.json > "output/verify-suite/$RUN/posctrl_sysb.txt" 2>&1; echo "rc_b=$?" >> "output/verify-suite/$RUN/posctrl_sysb.txt"
py scripts/append_criterion.py $W 50 $Q < verify/L2_stones.json > "output/verify-suite/$RUN/posctrl_sysc.txt" 2>&1; echo "rc_c=$?" >> "output/verify-suite/$RUN/posctrl_sysc.txt"
