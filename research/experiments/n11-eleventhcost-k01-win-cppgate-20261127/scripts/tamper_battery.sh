#!/bin/bash
# tamper battery for the n11 tenth-cost k01/k02 cppgate audit (scratch copy).
# T1 expected-pin flip -> G3 / T2 raw nodes edit -> G2+G3 /
# T3 phantom GATE-PASS -> G4 / T4 head byte append -> G6; clean control rc=0.
# Executed 2026-11-27 on scratch copies; output in output/tamper-battery-stdout.log.
# See the kit README for the exact commands (recorded in the run log).
echo "recorded battery; see output/tamper-battery-stdout.log"
