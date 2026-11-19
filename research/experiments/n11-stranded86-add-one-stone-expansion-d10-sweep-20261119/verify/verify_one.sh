#!/bin/bash
# usage: verify_one.sh <rootHex> <outSubdir>
set -e
H=$1; D=$2
S=$D/win7-root-$H-extraction-summary-20261119.json
CERT=$D/win7-root-$H-20261119.n11
if [ ! -f "$CERT" ] && [ -f "$CERT.gz.b64" ]; then
  # 第9root（3,069,801 bytes）は .n11 を gzip+base64 した .n11.gz.b64 として出版。
  # 復元: base64 -d win7-root-$H-20261119.n11.gz.b64 | gunzip > win7-root-$H-20261119.n11
  # 復元後 SHA-256 は extraction-summary / MANIFEST の pin と一致すること。
  base64 -d "$CERT.gz.b64" | gunzip > "$CERT"
fi
MOB=$(jq -r .legal_next_moves $S)
MOVES=$(jq -r '.completed_move_list|join(",")' $S)
node scripts/verify_win7_certificate_bigint_independent.mjs "$CERT" "$MOB" > "$D/win7-root-$H-independent-verification-20261119.json" 2> "$D/bigint.err"
node --experimental-strip-types scripts/verify_bit7_win7_cert.ts --cert "$CERT" --root "$H" --root-check --subroots "$MOVES" --consumed-out "$D/consumed-$H.txt" > "$D/win7-root-$H-bareiss-subroots-20261119.jsonl" 2> "$D/bareiss.err"
python3 - "$D" "$H" <<'PYEOF'
import json, sys
D, H = sys.argv[1], sys.argv[2]
cert = open(f'{D}/win7-root-{H}-20261119.n11').read().splitlines()
rows = set(cert[2:])
consumed = [l.strip() for l in open(f'{D}/consumed-{H}.txt') if l.strip()]
cu = set(consumed)
audit = {'exact_union': rows == cu, 'missing': len(rows - cu), 'extra': len(cu - rows),
         'certificate_rows': len(rows), 'consumed_lines': len(consumed), 'consumed_unique': len(cu)}
json.dump(audit, open(f'{D}/win7-root-{H}-bareiss-union-audit-20261119.json', 'w'), indent=2)
# cross-method equality with bigint record
v = json.load(open(f'{D}/win7-root-{H}-independent-verification-20261119.json'))
bl = [json.loads(l) for l in open(f'{D}/win7-root-{H}-bareiss-subroots-20261119.jsonl')]
br, bb = bl[0], bl[1]
stats = list(bb['stats'].values())
agree = (sum(x['seen'] for x in stats) == v['visited_states_across_subroots']
         and sum(x['terminals'] for x in stats) == v['terminal_count']
         and sum(x['opponentEdges'] for x in stats) == v['loser_reply_edges']
         and [min(x['range'][0] for x in stats), max(x['range'][1] for x in stats)] == v['terminal_range'])
v['cross_method_state_flow_equal'] = agree
v['certificate_union_exact'] = audit['exact_union'] and audit['missing'] == 0 and audit['extra'] == 0
json.dump(v, open(f'{D}/win7-root-{H}-independent-verification-20261119.json', 'w'), indent=2)
print('OK', H, 'cross_equal=', agree, 'union=', audit['exact_union'], 'rows=', len(rows))
PYEOF
