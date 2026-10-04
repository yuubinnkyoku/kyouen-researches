#!/bin/bash
# Prove that the merge refuses a WIN/LOSS conflict instead of last-wins.
# A cache is proof material: silently keeping one of two contradictory
# verdicts would let a bogus refutation survive.
set -u
D=$(mktemp -d)
trap 'rm -rf "$D"' EXIT
S=/mnt/d/ghq/github.com/yuubinnkyoku/kyouen-researches/research/experiments/n11-search-methods/scripts/dfpn_s5_merge.sh

cat > "$D/base.csv" <<'EOF'
# s5 verdict cache: n=11 schema=1 (canonical key -> WIN/LOSS, UNKNOWN never stored)
s5verdict,100,0,5,2,10
s5verdict,200,0,5,2,10
EOF

# Worker A says key 100 is LOSS; worker B says the same key is WIN.
cat > "$D/wa.csv" <<'EOF'
# s5 verdict cache: n=11 schema=1 (canonical key -> WIN/LOSS, UNKNOWN never stored)
s5verdict,100,0,5,2,11
EOF
cat > "$D/wb.csv" <<'EOF'
# s5 verdict cache: n=11 schema=1 (canonical key -> WIN/LOSS, UNKNOWN never stored)
s5verdict,100,0,5,1,12
EOF

echo "=== case 1: clean merge (two workers agreeing) ==="
bash "$S" "$D/out1.csv" "$D/base.csv" "$D/wa.csv"
rc=$?
echo "rc=$rc"
[ "$rc" = 0 ] || echo "FAIL: clean merge should succeed"

echo
echo "=== case 2: WIN/LOSS conflict must be refused ==="
bash "$S" "$D/out2.csv" "$D/base.csv" "$D/wa.csv" "$D/wb.csv"
rc=$?
echo "rc=$rc"
if [ "$rc" = 0 ]; then
  echo "FAIL: conflict was merged silently"
  exit 1
fi
if [ -f "$D/out2.csv" ]; then
  echo "FAIL: out2.csv was written despite the conflict"
  exit 1
fi
echo "conflict refused, nothing written: OK"

echo
echo "=== case 3: UNKNOWN rows are dropped, not merged ==="
cat > "$D/wu.csv" <<'EOF'
# s5 verdict cache: n=11 schema=1 (canonical key -> WIN/LOSS, UNKNOWN never stored)
s5verdict,300,0,5,0,0
s5verdict,400,0,5,2,5
EOF
bash "$S" "$D/out3.csv" "$D/base.csv" "$D/wu.csv"
echo "UNKNOWN row must not appear:"
grep -c '300,0' "$D/out3.csv" || true

echo
echo "MERGE_GUARD_OK"