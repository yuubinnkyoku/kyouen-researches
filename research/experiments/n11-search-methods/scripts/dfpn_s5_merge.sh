#!/bin/bash
# Deterministically merge s5 worker caches into one canonical cache.
#
# N11-DFPN-COVER-OPTIMUM.md specifies this policy and it is enforced here:
#   * each worker writes its OWN file; nobody appends to a shared cache
#   * the merge is keyed on the canonical key, not on arrival order
#   * ANY key carrying two different verdicts STOPS the merge; nothing is
#     written, because a conflict means the proof material is unsound and a
#     human has to look at it
#   * UNKNOWN is never merged: result must be 1 or 2
#   * the result lands on a temp file and is renamed, so a reader never
#     sees a half-written cache
#
# Usage:
#   dfpn_s5_merge.sh <out.csv> <base.csv> [worker.csv ...]
set -u
if [ "$#" -lt 2 ]; then
  echo "usage: $0 <out.csv> <base.csv> [worker.csv ...]" >&2
  exit 2
fi
OUT=$1; shift
BASE=$1; shift

TMP="${OUT}.tmp.$$"
: > "$TMP"
echo '# s5 verdict cache: n=11 schema=1 (canonical key -> WIN/LOSS, UNKNOWN never stored)' > "$TMP"

# base first, then every worker, all into the staging file
for f in "$BASE" "$@"; do
  [ -f "$f" ] || continue
  grep -v '^#' "$f" >> "$TMP" || true
done

python3 - "$TMP" "$OUT" <<'PY'
import io, sys, collections
src, dst = sys.argv[1], sys.argv[2]
verdicts = collections.OrderedDict()
conflicts = []
rows = 0
for line in io.open(src, encoding='utf-8', errors='replace'):
    line = line.strip()
    if not line or line.startswith('#'):
        continue
    f = line.split(',')
    if len(f) < 6 or f[0] != 's5verdict':
        continue
    if int(f[3]) != 5:
        continue
    r = int(f[4])
    if r not in (1, 2):       # never accept UNKNOWN
        continue
    key = (int(f[1]), int(f[2]))
    if key in verdicts:
        if verdicts[key][0] != r:
            conflicts.append((key, verdicts[key][0], r))
        continue
    verdicts[key] = (r, int(f[5]))
    rows += 1

print('merged keys   : %d' % len(verdicts))
print('WIN           : %d' % sum(1 for v in verdicts.values() if v[0] == 1))
print('LOSS          : %d' % sum(1 for v in verdicts.values() if v[0] == 2))
if conflicts:
    print()
    print('CONFLICT: %d key(s) carry two different verdicts' % len(conflicts))
    for k, a, b in conflicts[:10]:
        print('  key=%s  %s vs %s' % (k, 'WIN' if a == 1 else 'LOSS',
                                    'WIN' if b == 1 else 'LOSS'))
    print('MERGE_REFUSED: nothing written')
    sys.exit(1)

with io.open(dst, 'w', encoding='utf-8') as f:
    f.write('# s5 verdict cache: n=11 schema=1 '
            '(canonical key -> WIN/LOSS, UNKNOWN never stored)\n')
    for key in sorted(verdicts):
        r, nodes = verdicts[key]
        f.write('s5verdict,%d,%d,5,%d,%d\n' % (key[0], key[1], r, nodes))
print('written       : %s' % dst)
print('MERGE_OK')
PY
RC=$?
if [ "$RC" -ne 0 ]; then
  rm -f "$TMP"
  exit 1
fi
# The python body above already wrote the merged cache to $OUT, so there is
# nothing to move. An earlier version ended with `mv -f "$TMP" "$OUT"`,
# which overwrote that correct output with the unfiltered staging file and
# resurrected UNKNOWN rows the filter had just rejected.
rm -f "$TMP"
exit 0