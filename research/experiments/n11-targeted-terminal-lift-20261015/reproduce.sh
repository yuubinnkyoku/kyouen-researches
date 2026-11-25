#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
cd "$(dirname "$0")"
sha256sum -c SHA256SUMS
D=$(mktemp -d)
trap 'rm -rf "$D"' EXIT
CXX=${CXX:-g++}
"$CXX" -std=c++20 -O3 -o "$D/verify_win" scripts/verify_s8_batch_cpp.cpp
"$CXX" -std=c++20 -O3 -o "$D/verify_loss" scripts/verify_s8_loss_batch_cpp.cpp
"$CXX" -std=c++20 -O3 -o "$D/solve_s10" scripts/solve_s10_candidates.cpp
"$CXX" -std=c++20 -O3 -o "$D/lift" scripts/lift_all.cpp
"$CXX" -std=c++20 -O3 -o "$D/rank_s6" scripts/rank_s6_all.cpp
"$CXX" -std=c++20 -O3 -o "$D/reverse" scripts/reverse_closure.cpp
for x in new_s8_171_terminal new_s8_win_sixteen_terminal; do
 "$D/verify_win" "certificates/$x.cert"
 PYTHONPATH=scripts python3 scripts/verify_s8_batch_python.py "certificates/$x.cert"
done
"$D/verify_loss" certificates/new_s8_loss_three_terminal.cert
PYTHONPATH=scripts python3 scripts/verify_s8_loss_batch_python.py certificates/new_s8_loss_three_terminal.cert
PYTHONPATH=scripts python3 scripts/verify_delta_standalone.py data/target_four_s8_s10_probe_cpp.tsv
"$D/solve_s10" data/target_four_s8_s10_unknown.txt "$D/recomputed_cpp.tsv"
diff -u data/target_four_s8_s10_probe_cpp.tsv "$D/recomputed_cpp.tsv"
PYTHONPATH=scripts python3 scripts/merge_s10_workers.py data/s10_merged_51164.tsv "$D/merged.tsv" data/target_four_s8_s10_probe_verified.tsv --geometry
cmp data/s10_merged_51571.tsv "$D/merged.tsv"
# Fail closed: a conflicting worker shard must not alter the destination.
read -r key verdict < data/s10_merged_51164.tsv
if [ "$verdict" = WIN ]; then bad=LOSS; else bad=WIN; fi
printf '%s\t%s\n' "$key" "$bad" > "$D/conflict.tsv"
printf 'sentinel\n' > "$D/sentinel.tsv"
if PYTHONPATH=scripts python3 scripts/merge_s10_workers.py data/s10_merged_51164.tsv "$D/sentinel.tsv" "$D/conflict.tsv" >/dev/null 2>&1; then
 echo 'FAIL conflicting merge accepted' >&2; exit 1
fi
[ "$(cat "$D/sentinel.tsv")" = sentinel ]
PYTHONPATH=scripts python3 scripts/audit_deltas.py
"$D/reverse" data/s10_merged_51571.tsv "$D/rank_s8.tsv"
cmp data/s8_loss_rank_51571.tsv "$D/rank_s8.tsv"
PYTHONPATH=scripts python3 scripts/audit_rank_filter.py
PYTHONPATH=scripts python3 scripts/derive_s7_loss.py certificates/new_s8_loss_three_terminal.cert data/all_s7_loss_2213.txt data/all_s7_win_17.txt "$D/s7delta.txt"
cmp data/new_s7_loss_from_three.txt "$D/s7delta.txt"
"$D/lift" data/s10_merged_51571.tsv data/lift_s8_win_after_49095.txt data/all_s8_loss_294.txt data/all_s7_loss_2232.txt "$D/s7win.txt" "$D/s8win.txt" "$D/s9win.txt"
cmp data/lifted_s7_win_51571.txt "$D/s7win.txt"
cmp data/lifted_s8_win_51571.txt "$D/s8win.txt"
cmp data/lifted_s9_win_51571.txt "$D/s9win.txt"
"$D/rank_s6" data/all_s7_loss_2232.txt data/all_s7_win_17.txt "$D/s6rank.tsv" >/dev/null
cmp data/s6_rank_51571.tsv "$D/s6rank.tsv"
(cd scripts && python3 test_mutations.py verify_s8_loss_batch_python.py "$D/verify_loss" ../certificates/new_s8_loss_three_terminal.cert)
(cd scripts && python3 test_mutations.py verify_s8_batch_python.py "$D/verify_win" ../certificates/new_s8_win_sixteen_terminal.cert)
echo 'PASS full clean-room reproduction'
