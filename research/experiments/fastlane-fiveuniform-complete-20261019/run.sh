#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
c++ -std=c++17 -O3 enumerate.cpp -o /tmp/kyouen_fiveuniform_enumerate
c++ -std=c++17 -O3 independent.cpp -o /tmp/kyouen_fiveuniform_independent
/tmp/kyouen_fiveuniform_enumerate > all_patterns_results.txt
/tmp/kyouen_fiveuniform_independent > independent_results.txt
/tmp/kyouen_fiveuniform_enumerate 12 g6patterns_raw.txt > n12_only.txt
python3 verify_all.py
python3 count_membership.py
python3 orbit_audit.py > /dev/null
printf '%s\n' 'PASS: exhaustive enumeration, independent recursion, coefficient counts, orbit and witness audit'
