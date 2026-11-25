#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
sha256sum -c SHA256SUMS
g++ -std=c++20 -O3 -Wall -Wextra solve_s7_min.cpp -o /tmp/n11-s7-four-solver-$$
trap 'rm -f /tmp/n11-s7-four-solver-$$' EXIT
/tmp/n11-s7-four-solver-$$ missing_s7.txt /tmp/n11-s7-four-replay-$$
python3 build_certificate.py --prefix /tmp/n11-s7-four-replay-$$ --output /tmp/n11-s7-four-replay-$$.json
cmp s7_win_four_min_certificate.json /tmp/n11-s7-four-replay-$$.json
python3 verify_s7_certificate.py --certificate s7_win_four_min_certificate.json --workers "${WORKERS:-4}"
rm -f /tmp/n11-s7-four-replay-$$.*
