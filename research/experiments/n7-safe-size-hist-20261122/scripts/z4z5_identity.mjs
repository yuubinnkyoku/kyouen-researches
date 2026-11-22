// z4z5_identity.mjs — independent identity gates for the safe-subset histogram:
//   Z_n(4) = C(N,4) - F_n                         (a 4-set is safe iff it is not a forbidden quartet)
//   Z_n(5) = C(N,5) - |{5-sets containing >= 1 forbidden quartet}|
// The 5-set coverage is computed by DIRECT set construction from the quartet
// catalog (quartet + one extra cell, deduplicated by a Set of canonical keys),
// with NO reference to the DFS histogram machinery. Each line also carries the
// published Z_n(4) / Z_n(5) values (K1228 n=3..6 spectrum, K1230 n=7) and a
// match flag, so the gate is self-checking.
//
// Usage: node z4z5_identity.mjs <quartets_dir> [n ...]
//   reads <quartets_dir>/quartets_n<N>.txt (forbidgen det/brute-force catalog,
//   header line "n=..." skipped) for each n given as an argument (default 3..7).
// Determinism: no randomness, no timing in the output.

import * as fs from 'node:fs';

const qdir = process.argv[2];
const ns = process.argv.slice(3).map(Number);
if (!qdir || ns.some(x => !x)) { console.error('usage: node z4z5_identity.mjs <quartets_dir> [n ...]'); process.exit(1); }
if (ns.length === 0) ns.push(3, 4, 5, 6, 7);

// Published Z_n(4), Z_n(5): K1228 (n=3..6 spectrum), K1230 (n=7 histogram).
const PUBLISHED = {
  3: [112, 56], 4: [1626, 2360], 5: [11824, 37272], 6: [56414, 301952], 7: [205512, 1633048],
};

for (const n of ns) {
  const N = n * n;
  const qt = fs.readFileSync(`${qdir}/quartets_n${n}.txt`, 'utf8').split('\n').filter(t => t && !t.startsWith('n='));
  const quads = qt.map(r => r.split(' ').map(Number));
  const F = quads.length;
  // Z(4): C(N,4) - F
  const C4 = Com(N, 4);
  const z4 = C4 - F;
  // Z(5): C(N,5) - covered 5-sets
  const C5 = Com(N, 5);
  const seen = new Set();
  for (const [a, b, c, d] of quads) {
    for (let x = 0; x < N; x++) {
      if (x === a || x === b || x === c || x === d) continue;
      const s = [a, b, c, d, x].sort((u, v) => u - v);
      seen.add(s.join(','));
    }
  }
  const z5 = C5 - seen.size;
  const [pub4, pub5] = PUBLISHED[n] ?? [null, null];
  console.log(JSON.stringify({
    n, N, F, C4, z4_identity: z4, z4_published: pub4, z4_match: pub4 === null ? null : pub4 === z4,
    C5, covered5: seen.size, z5_identity: z5, z5_published: pub5, z5_match: pub5 === null ? null : pub5 === z5,
  }));
}
function Com(m, k) {
  if (k < 0 || m < k) return 0;
  let r = 1;
  for (let i = 0; i < k; i++) r = r * (m - i) / (i + 1);
  return r;
}
