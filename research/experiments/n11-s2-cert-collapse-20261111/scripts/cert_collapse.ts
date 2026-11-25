// q64 session (2026-11-11). Pure-TS, 78-first-win oracle conditional.
// Reproduces the S2 {59,60} certificate collapse, greedy certificate order,
// S6 census of the greedy head certificates (milestone-2), and the cross-S2
// worklist map of the 8 classA S2s (root 60). Tables are embedded verbatim
// from research/experiments/n11-s2-5960-worklist-20261110/scripts/s2_worklist.ts
// (K0675 oracle: 78 first-win + 16 second-win S5 positions).
// Set DO_S6 = true to recompute the S6 census (heavier; ~1 blocker costs about
// 87 blocker scans). Set DO_CROSS = n to recompute the first n cross-S2
// worklists (each is a full {60,q} sweep; 4 per sandbox run is the practical
// limit). No game outcome asserted anywhere. Empty board / two-stone roots
// remain UNKNOWN.
async function main() {
const DO_S6 = false;
const DO_CROSS = 0; // number of cross-S2 worklists (order: 47, 69, 35, 41, 11, 28, 59, 61)
const fwHex = ["00000000000000003800800000000001","00000000000000003800800000000002","00000000000000003800800000000004","00000000000000003800800000000008","00000000000000003800800000000010","00000000000000003800800000000040","00000000000000003800800000000080","00000000000000003800800000000100","00000000000000003800800000000200","00000000000000003800800000000400","00000000000000003800800000000800","00000000000000003800800000001000","00000000000000003800800000004000","00000000000000003800800000010000","00000000000000003800800000040000","00000000000000003800800000080000","00000000000000003800800000200000","00000000000000003800800000400000","00000000000000003800800040000000","00000000000000003800800100000000","00000000000000003800800200000000","00000000000000003800800400000000","00000000000000003800800800000000","00000000000000003800802000000000","00000000000000003800804000000000","00000000000000003800810000000000","00000000000000003800820000000000","00000000000000003800840000000000","00000000000000003800880000000000","00000000000000003800900000000000","00000000000000003800a00000000000","00000000000000003800c00000000000","00000000000000003801800000000000","00000000000000003802800000000000","00000000000000003808100000000000","00000000000000003808200000000000","00000000000000043800800000000000","00000000000000043808000000000000","00000000000000083808000000000000","00000000000000103800800000000000","00000000000000103808000000000000","00000000000000203800000000000001","00000000000000203800000000000002","00000000000000203800000000000004","00000000000000203800000000000008","00000000000000203800000000000010","00000000000000203800000000000040","00000000000000203800000000000080","00000000000000203800000000000100","00000000000000203800000000000200","00000000000000203800000000000400","00000000000000203800000000001000","00000000000000203800000000002000","00000000000000203800000000004000","00000000000000203800000000020000","00000000000000203800000000040000","00000000000000203800000000080000","00000000000000203800000000100000","00000000000000203800000000200000","00000000000000203800000001000000","00000000000000203800000002000000","00000000000000203800000010000000","00000000000000203800000020000000","00000000000000203800000040000000","00000000000000203800000100000000","00000000000000203800000400000000","00000000000000203800001000000000","00000000000000203800002000000000","00000000000000203800004000000000","00000000000000203800008000000000","00000000000000203800010000000000","00000000000000203800040000000000","00000000000000203800080000000000","00000000000000203800800000000000","00000000000000203801000000000000","00000000000000203802000000000000","00000000000000203804000000000000","00000000000000203808000000000000"];
const swHex = ["00000000000000003800800000000020","00000000000000003800800000800000","00000000000000003800800010000000","00000000000000083800800000000000","00000000000000203800000000000020","00000000000000203800000000000800","00000000000000203800000000008000","00000000000000203800000000010000","00000000000000203800000000400000","00000000000000203800000000800000","00000000000000203800000004000000","00000000000000203800000008000000","00000000000000203800000080000000","00000000000000203800000200000000","00000000000000203800000800000000","00000000000000203800020000000000"];

const B = (h: string) => BigInt('0x' + h);
const FW = fwHex.map(B); const SW = swHex.map(B);
const UNIset = new Set([...FW, ...SW].map(String));
if (FW.length !== 78 || SW.length !== 16 || fwHex.some(h => h.length !== 32) || swHex.some(h => h.length !== 32)) throw new Error('table check failed');
const N = 121;
const FULL = (1n << 121n) - 1n;
function det4(ps: number[]): number {
  const a = ps.map(p => { const x = p % 11, y = Math.floor(p / 11); return [x*x + y*y, x, y, 1]; });
  let sign = 1, div = 1;
  for (let k = 0; k < 3; k++) {
    if (a[k][k] === 0) { let p = -1; for (let j = k+1; j < 4; j++) if (a[j][k] !== 0) { p = j; break; } if (p < 0) return 0; [a[k], a[p]] = [a[p], a[k]]; sign = -sign; }
    const piv = a[k][k];
    for (let i = k+1; i < 4; i++) for (let j = k+1; j < 4; j++) a[i][j] = (a[i][j]*piv - a[i][k]*a[k][j]) / div;
    div = piv;
  }
  return sign * a[3][3];
}
const forbMemo = new Map<string, bigint>();
function forbidden(a: number, b: number, c: number): bigint {
  const key = a + ',' + b + ',' + c;
  let m = forbMemo.get(key);
  if (m !== undefined) return m;
  m = 0n;
  for (let d = 0; d < N; d++) if (d !== a && d !== b && d !== c && det4([a,b,c,d]) === 0) m |= 1n << BigInt(d);
  forbMemo.set(key, m); return m;
}
function legalOf(stones: number[]): bigint {
  let banned = 0n;
  for (const s of stones) banned |= 1n << BigInt(s);
  for (let i = 0; i < stones.length; i++) for (let j = i+1; j < stones.length; j++) for (let k = j+1; k < stones.length; k++) banned |= forbidden(stones[i], stones[j], stones[k]);
  return FULL & ~banned;
}
const popcount = (m: bigint) => m.toString(2).replace(/0/g, '').length;
const bitsOf = (m: bigint) => { const out: number[] = []; for (let d = 0; d < N; d++) if ((m >> BigInt(d)) & 1n) out.push(d); return out; };
const TX: ((x: number, y: number) => [number, number])[] = [
  (x, y) => [x, y], (x, y) => [y, 10 - x], (x, y) => [10 - x, 10 - y], (x, y) => [10 - y, x],
  (x, y) => [10 - x, y], (x, y) => [x, 10 - y], (x, y) => [y, x], (x, y) => [10 - y, 10 - x],
];
function transformMask(m: bigint, g: number): bigint {
  let out = 0n;
  for (const p of bitsOf(m)) { const [nx, ny] = TX[g](p % 11, Math.floor(p / 11)); out |= 1n << BigInt(ny * 11 + nx); }
  return out;
}
function canon(m: bigint): bigint {
  let best = m;
  for (let g = 1; g < 8; g++) { const t = transformMask(m, g); if (t < best) best = t; }
  return best;
}
function worklist(q: number, r: number) {
  const S3m = (1n << 60n) | (1n << BigInt(q)) | (1n << BigInt(r));
  let fc = 0n;
  for (const f of FW) if ((f & S3m) === S3m) fc |= (f & ~S3m);
  const blks = bitsOf(legalOf([60, q, r]) & ~fc);
  const perBlocker: { t: number; orbits: string[] }[] = [];
  for (const t of blks) {
    const mask = S3m | (1n << BigInt(t));
    const orbs = new Set<string>();
    for (const c of bitsOf(legalOf([60, q, r, t]))) {
      const child = mask | (1n << BigInt(c));
      if (UNIset.has(String(child))) continue;
      orbs.add(String(canon(child)));
    }
    perBlocker.push({ t, orbits: [...orbs] });
  }
  return perBlocker;
}
const gName = ['id', 'rot90', 'rot180', 'rot270', 'reflX', 'reflY', 'diagMain', 'diagAnti'];
const gOf = (t: number, g: number) => { const [nx, ny] = TX[g](t % 11, Math.floor(t / 11)); return ny * 11 + nx; };
const pb = worklist(59, 61);
const keyOf = (o: string[]) => [...o].sort().join('|');
const byKey = new Map<string, number[]>();
const orbitsByKey = new Map<string, string[]>();
for (const p of pb) {
  const k = keyOf(p.orbits);
  if (!byKey.has(k)) { byKey.set(k, []); orbitsByKey.set(k, p.orbits); }
  byKey.get(k)!.push(p.t);
}
const classes = [...byKey.values()];
const singletons = classes.filter(v => v.length === 1).map(v => v[0]);
const pairs = classes.filter(v => v.length === 2).map(v => [...v].sort((a, b) => a - b));
const pairVia = pairs.map(([a, b]) => {
  const via: string[] = [];
  for (let g = 1; g < 8; g++) if (gOf(a, g) === b) via.push(gName[g]);
  return { pair: [a, b], via };
});
// universe closure audit (explains why the collapse is not automatic)
const closure: Record<string, number> = {};
for (let g = 1; g < 8; g++) {
  let miss = 0;
  for (const u of [...FW, ...SW]) if (!UNIset.has(String(transformMask(u, g)))) miss++;
  closure[gName[g]] = miss;
}
const cov = new Set<string>();
const todo = [...byKey.keys()];
const greedy: any[] = [];
let cum = 0, cumB = 0;
while (todo.length) {
  let bi = -1, bn = Infinity;
  for (let i = 0; i < todo.length; i++) {
    let n = 0;
    for (const o of orbitsByKey.get(todo[i])!) if (!cov.has(o)) n++;
    if (n < bn) { bn = n; bi = i; }
  }
  const k = todo.splice(bi, 1)[0];
  for (const o of orbitsByKey.get(k)!) cov.add(o);
  cum += bn; cumB += byKey.get(k)!.length;
  greedy.push({ ts: byKey.get(k), added: bn, cumOrbits: cum, cumBlockers: cumB });
}
const out: any = {
  blockers: pb.length,
  distinctCertificates: byKey.size,
  singletonCerts: singletons,
  pairs,
  pairVia,
  universeMissUnderG: closure,
  greedyHead: greedy.slice(0, 14),
  greedyLast: greedy[greedy.length - 1],
  totalOrbits: cov.size,
  empty_board: "UNKNOWN",
};
if (DO_S6) {
  function s6OrbitsOf(t: number) {
    const S4 = [60, 59, 61, t];
    const mask4 = S4.reduce((m, s) => m | (1n << BigInt(s)), 0n);
    const orbits = new Set<string>();
    let oblig = 0;
    for (const c of bitsOf(legalOf(S4))) {
      const child = mask4 | (1n << BigInt(c));
      if (UNIset.has(String(child))) continue;
      oblig++;
      for (const s6 of bitsOf(legalOf([...S4, c]))) orbits.add(String(canon(child | (1n << BigInt(s6)))));
    }
    return { obligations: oblig, s6Orbits: orbits };
  }
  const per: any = {};
  const m2 = new Set<string>();
  for (const t of [5, 27, 71, 82, 104]) {
    const s = s6OrbitsOf(t);
    per[t] = { obligations: s.obligations, s6Orbits: s.s6Orbits.size };
    for (const o of s.s6Orbits) m2.add(o);
  }
  out.s6Milestone2 = { per, union: m2.size };
}
if (DO_CROSS > 0) {
  // best-S3 blockers for a given q under the K0685 convention
  function bestR(q: number): number {
    const legalS2 = legalOf([60, q]);
    let bestCount = Infinity, bestRr = -1;
    for (let r = 0; r < N; r++) {
      if (!((legalS2 >> BigInt(r)) & 1n)) continue;
      const S3 = (1n << 60n) | (1n << BigInt(q)) | (1n << BigInt(r));
      let fcov = 0n;
      for (const f of FW) if ((f & S3) === S3) fcov |= (f & ~S3);
      const count = popcount(legalOf([60, q, r]) & ~fcov);
      if (count < bestCount) { bestCount = count; bestRr = r; if (count === 0) break; }
    }
    return bestRr;
  }
  const cross: any = {};
  for (const q of [47, 69, 35, 41, 11, 28, 59, 61].slice(0, DO_CROSS)) {
    const r = bestR(q);
    const wl = worklist(q, r);
    const orbs = new Set<string>();
    for (const p of wl) for (const o of p.orbits) orbs.add(o);
    cross['q' + q] = { r, blockers: wl.length, orbits: orbs.size };
  }
  out.crossS2 = cross;
}
return out;
}
