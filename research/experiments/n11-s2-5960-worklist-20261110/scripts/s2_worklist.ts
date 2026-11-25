// Pure-TS enumeration of the S2 {59,60} closure worklist (q61 session 2026-11-10).
// Geometry/legal strictly follow verify_five_terminal_loss7.py: exact integer
// Bareiss det4 over (x^2+y^2, x, y, 1); legal(mask) = FULL & ~(mask | union of
// forbidden over stone triples). Universe: 94 S5 positions (78 first-win + 16
// second-win) embedded verbatim from the K0675 s6 sweep oracle.
// Reproduces: best-S3 blocker dist (13,244 total), 32 classA quads (T1 check),
// per-blocker child/orbit requirements, serve distribution, maximal frontier,
// and the mirror identity of the {60,59} / {60,61} worklists (1,447 D4 orbits).
// All results conditional on the 78-first-win oracle; no game outcome asserted.
// Empty board / two-stone roots remain UNKNOWN.
async function main() {
const N = 121;
const FULL = (1n << 121n) - 1n;
const fwHex = ["00000000000000003800800000000001","00000000000000003800800000000002","00000000000000003800800000000004","00000000000000003800800000000008","00000000000000003800800000000010","00000000000000003800800000000040","00000000000000003800800000000080","00000000000000003800800000000100","00000000000000003800800000000200","00000000000000003800800000000400","00000000000000003800800000000800","00000000000000003800800000001000","00000000000000003800800000004000","00000000000000003800800000010000","00000000000000003800800000040000","00000000000000003800800000080000","00000000000000003800800000200000","00000000000000003800800000400000","00000000000000003800800040000000","00000000000000003800800100000000","00000000000000003800800200000000","00000000000000003800800400000000","00000000000000003800800800000000","00000000000000003800802000000000","00000000000000003800804000000000","00000000000000003800810000000000","00000000000000003800820000000000","00000000000000003800840000000000","00000000000000003800880000000000","00000000000000003800900000000000","00000000000000003800a00000000000","00000000000000003800c00000000000","00000000000000003801800000000000","00000000000000003802800000000000","00000000000000003808100000000000","00000000000000003808200000000000","00000000000000043800800000000000","00000000000000043808000000000000","00000000000000083808000000000000","00000000000000103800800000000000","00000000000000103808000000000000","00000000000000203800000000000001","00000000000000203800000000000002","00000000000000203800000000000004","00000000000000203800000000000008","00000000000000203800000000000010","00000000000000203800000000000040","00000000000000203800000000000080","00000000000000203800000000000100","00000000000000203800000000000200","00000000000000203800000000000400","00000000000000203800000000001000","00000000000000203800000000002000","00000000000000203800000000004000","00000000000000203800000000020000","00000000000000203800000000040000","00000000000000203800000000080000","00000000000000203800000000100000","00000000000000203800000000200000","00000000000000203800000001000000","00000000000000203800000002000000","00000000000000203800000010000000","00000000000000203800000020000000","00000000000000203800000040000000","00000000000000203800000100000000","00000000000000203800000400000000","00000000000000203800001000000000","00000000000000203800002000000000","00000000000000203800004000000000","00000000000000203800008000000000","00000000000000203800010000000000","00000000000000203800040000000000","00000000000000203800080000000000","00000000000000203800800000000000","00000000000000203801000000000000","00000000000000203802000000000000","00000000000000203804000000000000","00000000000000203808000000000000"];
const swHex = ["00000000000000003800800000000020","00000000000000003800800000800000","00000000000000003800800010000000","00000000000000083800800000000000","00000000000000203800000000000020","00000000000000203800000000000800","00000000000000203800000000008000","00000000000000203800000000010000","00000000000000203800000000400000","00000000000000203800000000800000","00000000000000203800000004000000","00000000000000203800000008000000","00000000000000203800000080000000","00000000000000203800000200000000","00000000000000203800000800000000","00000000000000203800020000000000"];

const B = (h: string) => BigInt('0x' + h);
const FW = fwHex.map(B);
const SW = swHex.map(B);
const UNI = [...FW, ...SW];
const FWset = new Set(FW.map(String));
const SWset = new Set(SW.map(String));
const UNIset = new Set(UNI.map(String));

function det4(ps: number[]): number {
  const a = ps.map(p => { const x = p % 11, y = Math.floor(p / 11); return [x*x + y*y, x, y, 1]; });
  let sign = 1, div = 1;
  for (let k = 0; k < 3; k++) {
    if (a[k][k] === 0) {
      let p = -1;
      for (let j = k+1; j < 4; j++) if (a[j][k] !== 0) { p = j; break; }
      if (p < 0) return 0;
      [a[k], a[p]] = [a[p], a[k]]; sign = -sign;
    }
    const piv = a[k][k];
    for (let i = k+1; i < 4; i++) for (let j = k+1; j < 4; j++)
      a[i][j] = (a[i][j]*piv - a[i][k]*a[k][j]) / div;
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
  for (let d = 0; d < N; d++)
    if (d !== a && d !== b && d !== c && det4([a,b,c,d]) === 0) m |= 1n << BigInt(d);
  forbMemo.set(key, m);
  return m;
}

function legalOf(stones: number[]): bigint {
  let banned = 0n;
  for (const s of stones) banned |= 1n << BigInt(s);
  for (let i = 0; i < stones.length; i++)
    for (let j = i+1; j < stones.length; j++)
      for (let k = j+1; k < stones.length; k++)
        banned |= forbidden(stones[i], stones[j], stones[k]);
  return FULL & ~banned;
}

const popcount = (m: bigint) => m.toString(2).replace(/0/g, '').length;
const bitsOf = (m: bigint) => { const out: number[] = []; for (let d = 0; d < N; d++) if ((m >> BigInt(d)) & 1n) out.push(d); return out; };

// --- reproduce the classA enumeration (q60) ---
const legalS1 = legalOf([60]);
const classAQuads: number[][] = [];  // [q, r, t]
let totalBlockers = 0;
const dist: Record<number, number> = {};
for (let q = 0; q < N; q++) {
  if (!((legalS1 >> BigInt(q)) & 1n)) continue;
  const legalS2 = legalOf([60, q]);
  const qbit = 1n << BigInt(q);
  let bestCount = Infinity, bestR = -1;
  for (let r = 0; r < N; r++) {
    if (!((legalS2 >> BigInt(r)) & 1n)) continue;
    const S3 = (1n << 60n) | qbit | (1n << BigInt(r));
    let fcov = 0n;
    for (const f of FW) if ((f & S3) === S3) fcov |= (f & ~S3);
    const count = popcount(legalOf([60, q, r]) & ~fcov);
    if (count < bestCount) { bestCount = count; bestR = r; if (count === 0) break; }
  }
  const r = bestR;
  const S3 = (1n << 60n) | qbit | (1n << BigInt(r));
  let fcov = 0n, ucov = 0n;
  for (const f of FW) if ((f & S3) === S3) fcov |= (f & ~S3);
  for (const u of UNI) if ((u & S3) === S3) ucov |= (u & ~S3);
  const blockersMask = legalOf([60, q, r]) & ~fcov;
  const classAMask = blockersMask & ucov;
  for (const t of bitsOf(classAMask)) classAQuads.push([q, r, t]);
  totalBlockers += popcount(blockersMask);
  dist[popcount(blockersMask)] = (dist[popcount(blockersMask)] || 0) + 1;
}

// --- per-S4 child decomposition ---
function decomposeS4(stones: number[]) {
  const mask = stones.reduce((m, s) => m | (1n << BigInt(s)), 0n);
  const children = bitsOf(legalOf(stones));
  const fw: number[] = [], sw: number[] = [], unk: bigint[] = [];
  for (const c of children) {
    const child = mask | (1n << BigInt(c));
    if (FWset.has(String(child))) fw.push(c);
    else if (SWset.has(String(child))) sw.push(c);
    else unk.push(child);
  }
  return { children: children.length, fw, sw, unk };
}

// D4 transforms of the 11x11 board (index = y*11+x), 8 elements
const TX: ((x: number, y: number) => [number, number])[] = [
  (x, y) => [x, y],
  (x, y) => [y, 10 - x],
  (x, y) => [10 - x, 10 - y],
  (x, y) => [10 - y, x],
  (x, y) => [10 - x, y],
  (x, y) => [x, 10 - y],
  (x, y) => [y, x],
  (x, y) => [10 - y, 10 - x],
];
function transformMask(m: bigint, g: number): bigint {
  let out = 0n;
  for (const p of bitsOf(m)) {
    const [nx, ny] = TX[g](p % 11, Math.floor(p / 11));
    out |= 1n << BigInt(ny * 11 + nx);
  }
  return out;
}
function canon(m: bigint): bigint {
  let best = m;
  for (let g = 1; g < 8; g++) { const t = transformMask(m, g); if (t < best) best = t; }
  return best;
}

// --- main analysis ---
const perQuad = [];
const unknownUnion = new Set<string>();
let t1Violation = 0;
for (const [q, r, t] of classAQuads) {
  const S4 = [60, q, r, t];
  const d = decomposeS4(S4);
  if (d.fw.length > 0) t1Violation++;
  for (const u of d.unk) unknownUnion.add(String(u));
  perQuad.push({ s4: S4, children: d.children, swChildren: d.sw.length, swTs: d.sw, unknown: d.unk.length });
}
// S4-C
const s4c = decomposeS4([51, 59, 60, 61]);
for (const u of s4c.unk) unknownUnion.add(String(u));

// orbit count of unknown union
const orbitCanon = new Set<string>();
for (const s of unknownUnion) orbitCanon.add(String(canon(BigInt(s))));

// --- S2 {59,60} closure worklist (best S3 r = 61) ---
function worklist(q: number, r: number) {
  const S3m = (1n << 60n) | (1n << BigInt(q)) | (1n << BigInt(r));
  let fc = 0n;
  for (const f of FW) if ((f & S3m) === S3m) fc |= (f & ~S3m);
  const blks = bitsOf(legalOf([60, q, r]) & ~fc);
  const perBlocker: { t: number; orbits: string[] }[] = [];
  const serve = new Map<string, number[]>(); // orbit -> blocker ts
  for (const t of blks) {
    const mask = S3m | (1n << BigInt(t));
    const orbs = new Set<string>();
    for (const c of bitsOf(legalOf([60, q, r, t]))) {
      const child = mask | (1n << BigInt(c));
      if (UNIset.has(String(child))) continue;
      const ck = String(canon(child));
      orbs.add(ck);
      if (!serve.has(ck)) serve.set(ck, []);
      serve.get(ck)!.push(t);
    }
    perBlocker.push({ t, orbits: [...orbs] });
  }
  const serveDist: Record<number, number> = {};
  for (const ts of serve.values()) serveDist[ts.length] = (serveDist[ts.length] || 0) + 1;
  const maximal = perBlocker.filter(({ t, orbits }) =>
    !perBlocker.some(({ t: t2, orbits: o2 }) => t2 !== t && orbits.length < o2.length &&
      orbits.every(o => o2.includes(o))));
  return { blockers: blks.length, orbits: serve.size, serveDist, perBlocker, maximal };
}
const w59 = worklist(59, 61);
const w61 = worklist(61, 59);
const orbitSet59 = new Set(w59.perBlocker.flatMap(p => p.orbits));
const orbitSet61 = new Set(w61.perBlocker.flatMap(p => p.orbits));
let inter5961 = 0;
for (const o of orbitSet59) if (orbitSet61.has(o)) inter5961++;
const perBlockerOrbitSizes = w59.perBlocker.map(p => p.orbits.length).sort((a, b) => a - b);

return {
  dist,
  totalBlockers,
  classACount: classAQuads.length,
  t1Violation,
  perQuad: perQuad.map(p => ({ s4: p.s4, children: p.children, sw: p.swChildren, swTs: p.swTs, unknown: p.unknown })),
  s4c: { children: s4c.children, fw: s4c.fw, sw: s4c.sw, unknown: s4c.unk.length,
         unknownTs: s4c.unk.map(u => bitsOf(u)) },
  unknownUnionSize: unknownUnion.size,
  unknownOrbits: orbitCanon.size,
  worklist59: {
    blockers: w59.blockers, orbits: w59.orbits, serveDist: w59.serveDist,
    maximal: w59.maximal.length,
    perBlockerOrbitMin: perBlockerOrbitSizes[0],
    perBlockerOrbitMedian: perBlockerOrbitSizes[Math.floor(perBlockerOrbitSizes.length / 2)],
    perBlockerOrbitMax: perBlockerOrbitSizes[perBlockerOrbitSizes.length - 1],
  },
  worklist61: { blockers: w61.blockers, orbits: w61.orbits },
  mirrorIdentity: inter5961 === orbitSet59.size && orbitSet59.size === orbitSet61.size,
  empty_board: "UNKNOWN",
};
}
