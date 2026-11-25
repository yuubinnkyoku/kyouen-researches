// Pure-TS reproduction of the n11 chain_blockers best-S3 audit + full classA
// decomposition (K0685 wall, q60 session 2026-11-10).
// Geometry/legal strictly follow verify_five_terminal_loss7.py:
//   det4 rows (x^2+y^2, x, y, 1), exact integer Bareiss;
//   legal(mask) = FULL & ~(mask | union over stone triples of forbidden).
// Input: the 94-position S5 universe (78 first-win + 16 second-win) from
//   research/experiments/n11-central-19-cover-20261031/output/s6sweep/s5_verdicts.json
//   (embedded below verbatim as hex).
// Key simplification (proved in-session): W4(s4) <=> s4 is a strict subset of
// some FIRST_WIN78 position. Any F in FW78 with S4 subset F has F\S4 legal in
// S4 automatically (no four stones of a legal 5-position are cocircular or
// collinear). Hence blockers_of(s3) = legal(s3) & ~fcov(s3) where
// fcov(s3) = union over F in FW78 with S3 subset F of (F & ~S3), and
// classA blockers = blockers & ucov(s3) (ucov over all 94 universe positions);
// by T1 these arise only via the 16 second-win positions.
// All results are conditional on the 78-first-win oracle; no game outcome is
// asserted. Empty board / two-stone roots remain UNKNOWN.

const N = 121;
const FULL = (1n << 121n) - 1n;

const fwHex = ["00000000000000003800800000000001","00000000000000003800800000000002","00000000000000003800800000000004","00000000000000003800800000000008","00000000000000003800800000000010","00000000000000003800800000000040","00000000000000003800800000000080","00000000000000003800800000000100","00000000000000003800800000000200","00000000000000003800800000000400","00000000000000003800800000000800","00000000000000003800800000001000","00000000000000003800800000004000","00000000000000003800800000010000","00000000000000003800800000040000","00000000000000003800800000080000","00000000000000003800800000200000","00000000000000003800800000400000","00000000000000003800800040000000","00000000000000003800800100000000","00000000000000003800800200000000","00000000000000003800800400000000","00000000000000003800800800000000","00000000000000003800802000000000","00000000000000003800804000000000","00000000000000003800810000000000","00000000000000003800820000000000","00000000000000003800840000000000","00000000000000003800880000000000","00000000000000003800900000000000","00000000000000003800a00000000000","00000000000000003800c00000000000","00000000000000003801800000000000","00000000000000003802800000000000","00000000000000003808100000000000","00000000000000003808200000000000","00000000000000043800800000000000","00000000000000043808000000000000","00000000000000083808000000000000","00000000000000103800800000000000","00000000000000103808000000000000","00000000000000203800000000000001","00000000000000203800000000000002","00000000000000203800000000000004","00000000000000203800000000000008","00000000000000203800000000000010","00000000000000203800000000000040","00000000000000203800000000000080","00000000000000203800000000000100","00000000000000203800000000000200","00000000000000203800000000000400","00000000000000203800000000001000","00000000000000203800000000002000","00000000000000203800000000004000","00000000000000203800000000020000","00000000000000203800000000040000","00000000000000203800000000080000","00000000000000203800000000100000","00000000000000203800000000200000","00000000000000203800000001000000","00000000000000203800000002000000","00000000000000203800000010000000","00000000000000203800000020000000","00000000000000203800000040000000","00000000000000203800000100000000","00000000000000203800000400000000","00000000000000203800001000000000","00000000000000203800002000000000","00000000000000203800004000000000","00000000000000203800008000000000","00000000000000203800010000000000","00000000000000203800040000000000","00000000000000203800080000000000","00000000000000203800800000000000","00000000000000203801000000000000","00000000000000203802000000000000","00000000000000203804000000000000","00000000000000203808000000000000"];
const swHex = ["00000000000000003800800000000020","00000000000000003800800000800000","00000000000000003800800010000000","00000000000000083800800000000000","00000000000000203800000000000020","00000000000000203800000000000800","00000000000000203800000000008000","00000000000000203800000000010000","00000000000000203800000000400000","00000000000000203800000000800000","00000000000000203800000004000000","00000000000000203800000008000000","00000000000000203800000080000000","00000000000000203800000200000000","00000000000000203800000800000000","00000000000000203800020000000000"];

const B = (h: string) => BigInt('0x' + h);
const FW = fwHex.map(B);
const SW = swHex.map(B);
const UNI = [...FW, ...SW];

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
      a[i][j] = (a[i][j]*piv - a[i][k]*a[k][j]) / div; // exact Bareiss divisions
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

const legalS1 = legalOf([60]);
const bestPerS2: Record<number, { r: number; blockers: number; classA: number; classA_ts: number[] }> = {};
const dist: Record<number, number> = {};
let totalBlockers = 0, totalClassA = 0;

for (let q = 0; q < N; q++) {
  if (!((legalS1 >> BigInt(q)) & 1n)) continue;
  const legalS2 = legalOf([60, q]);
  const qbit = 1n << BigInt(q);
  let best: { count: number; r: number; classA: number; classA_ts: number[] } | null = null;
  for (let r = 0; r < N; r++) {
    if (!((legalS2 >> BigInt(r)) & 1n)) continue;
    const S3 = (1n << 60n) | qbit | (1n << BigInt(r));
    let fcov = 0n, ucov = 0n;
    for (const f of FW) if ((f & S3) === S3) fcov |= (f & ~S3);
    for (const u of UNI) if ((u & S3) === S3) ucov |= (u & ~S3);
    const blockersMask = legalOf([60, q, r]) & ~fcov;
    const count = popcount(blockersMask);
    if (best === null || count < best.count) {
      const classAMask = blockersMask & ucov;
      const ts: number[] = [];
      for (let t = 0; t < N; t++) if ((classAMask >> BigInt(t)) & 1n) ts.push(t);
      best = { count, r, classA: ts.length, classA_ts: ts };
      if (count === 0) break;
    }
  }
  bestPerS2[q] = { r: best!.r, blockers: best!.count, classA: best!.classA, classA_ts: best!.classA_ts };
  dist[best!.count] = (dist[best!.count] || 0) + 1;
  totalBlockers += best!.count;
  totalClassA += best!.classA;
}

const classAPositive = Object.entries(bestPerS2).filter(([, v]) => v.classA > 0)
  .map(([q, v]) => ({ q: +q, best_r: v.r, blockers: v.blockers, classA: v.classA, ts: v.classA_ts }));

console.log(JSON.stringify({
  dist: Object.fromEntries(Object.entries(dist).map(([k, v]) => [k, v]).sort((a, b) => +a[0] - +b[0])),
  total_blockers: totalBlockers,
  total_classA: totalClassA,
  classA_positive_S2s: classAPositive,
  empty_board: "UNKNOWN",
  two_stone_roots: "UNKNOWN",
  note: "conditional on the 78 first-win S5 oracle (K0675); no game outcome asserted",
}, null, 2));
