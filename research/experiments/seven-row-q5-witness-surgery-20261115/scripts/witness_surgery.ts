// witness_surgery.ts - (7,5) m=33 -> 7x34 witness surgery + exhaustive verification
// Pure TypeScript, exact integer arithmetic (all intermediates < 2^53).
// No repo code, no census, no SAT, no random.
//
// Method:
//   depth-1: enumerate single-stone relocations s -> sp where sp lies on a curve
//     through the unique uncovered cell T of the base witness at width 34,
//     carrying exactly q-2 = 3 base stones (completeness: T is uncovered in the
//     base config, so no curve through T has q-1 stones; any post-move blocking
//     curve of T must be a 3-stone curve plus the moved stone).
//   depth-2: from each safe depth-1 state, enumerate second relocations sp2 lying
//     on 3-stone curves through every still-uncovered cell (necessary condition),
//     then brute-verify each candidate with the exhaustive routines.
//   NOT covered (no absence claim): 2-move extensions where both new stones sit
//     on one 2-stone curve through T.
//   The incremental U-sets (bmapOf/newlyBlocked) accelerate the search only;
//   adopted witnesses are re-verified exclusively by the exhaustive routines
//   (findUnsafeSubset enumeration + per-cell maximality).

type P = [number, number];
const q = 5, w = 7, W = 34, need = q - 1;
const kk = (x: number, y: number) => x * 100 + y;

function cross3(o: P, a: P, b: P): number {
  return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0]);
}
function circleParams(A: P, B: P, C: P): [number, number, number, number] {
  const a11 = 2*(B[0]-A[0]), a12 = 2*(B[1]-A[1]);
  const a21 = 2*(C[0]-A[0]), a22 = 2*(C[1]-A[1]);
  const b1 = B[0]*B[0]+B[1]*B[1]-A[0]*A[0]-A[1]*A[1];
  const b2 = C[0]*C[0]+C[1]*C[1]-A[0]*A[0]-A[1]*A[1];
  const D = a11*a22 - a12*a21;
  const N1 = b1*a22 - b2*a12;
  const N2 = a11*b2 - a21*b1;
  const R2 = (D*A[0]-N1)**2 + (D*A[1]-N2)**2;
  return [D, N1, N2, R2];
}
function onCircle(p: P, cp: [number, number, number, number]): boolean {
  const [D, N1, N2, R2] = cp;
  return (D*p[0]-N1)**2 + (D*p[1]-N2)**2 === R2;
}

// ---------- exhaustive verification (ground truth) ----------

function findUnsafeSubset(stones: P[], qn: number): P[] | null {
  // enumerates all qn-subsets; returns one lying on a common line/circle, else null
  const n = stones.length; const idx: number[] = [];
  function onCommonCurve(sub: P[]): boolean {
    for (let i = 0; i < sub.length; i++) for (let j = i+1; j < sub.length; j++) for (let k2 = j+1; k2 < sub.length; k2++) {
      if (cross3(sub[i], sub[j], sub[k2]) === 0) {
        let ok = true;
        for (let m2 = 0; m2 < sub.length; m2++) if (cross3(sub[i], sub[j], sub[m2]) !== 0) { ok = false; break; }
        if (ok) return true;
      } else {
        const cp = circleParams(sub[i], sub[j], sub[k2]);
        let ok = true;
        for (let m2 = 0; m2 < sub.length; m2++) if (!onCircle(sub[m2], cp)) { ok = false; break; }
        if (ok) return true;
      }
    }
    return false;
  }
  function rec(start: number, depth: number): P[] | null {
    if (depth === qn) { const sub = idx.map(i => stones[i]); return onCommonCurve(sub) ? sub : null; }
    for (let i = start; i < n; i++) {
      idx.push(i); const r = rec(i+1, depth+1); idx.pop();
      if (r) return r;
    }
    return null;
  }
  return rec(0, 0);
}

function unblockedCells(stones: P[], wn: number, Wn: number, qn: number): P[] {
  const nd = qn - 1;
  const occ = new Set(stones.map(s => kk(s[0], s[1])));
  const U: P[] = [];
  for (let x = 0; x < Wn; x++) for (let y = 0; y < wn; y++) {
    if (occ.has(kk(x, y))) continue;
    const e: P = [x, y];
    let blocked = false;
    for (const s of stones) {
      let cnt = 0;
      for (const t of stones) if (cross3(e, s, t) === 0) cnt++;
      if (cnt >= nd) { blocked = true; break; }
    }
    if (!blocked) outer:
    for (let i = 0; i < stones.length; i++) {
      for (let j = i+1; j < stones.length; j++) {
        if (cross3(e, stones[i], stones[j]) === 0) continue;
        const cp = circleParams(e, stones[i], stones[j]);
        let cnt = 0;
        for (const t of stones) if (onCircle(t, cp)) cnt++;
        if (cnt >= nd) { blocked = true; break outer; }
      }
    }
    if (!blocked) U.push(e);
  }
  return U;
}

// ---------- search accelerator (not authoritative) ----------
// inventory(cfg): all lines/circles of cfg carrying exactly 3 or 4 stones, with
//   per-cell index. bmapOf(inv, cfg)[s]: cells losing ALL blocking when s is
//   removed (empty cells exclusively blocked via s, plus s's own position if it
//   would be uncovered after removal). newlyBlocked(inv, sp, s): cells that are
//   (re)blocked after the swap s -> sp = cells of 3-stone curves through sp
//   avoiding s, plus cells of 4-stone curves through sp containing s (those keep
//   4 stones after the swap). U(s -> sp) = ({T} u B(s)) \ newly \\ {sp}.
//   Known to disagree with brute force on rare inputs; every candidate win is
//   re-verified with the exhaustive routines above before adoption.

const BASE: P[] = [[8,0],[18,0],[30,0],[5,1],[24,1],[28,1],[32,1],[0,2],[9,2],[22,2],[28,2],[14,3],[15,3],[21,3],[30,3],[16,4],[20,4],[26,4],[30,4],[3,5],[21,5],[22,5],[25,5],[15,6],[16,6],[18,6],[25,6]] as P[];
const WIN_A: P[] = BASE.filter(t => !(t[0]===25&&t[1]===5) && !(t[0]===20&&t[1]===4)).concat([[8,5],[2,4]] as P[]);
const WIN_B: P[] = BASE.filter(t => !(t[0]===25&&t[1]===5) && !(t[0]===20&&t[1]===4)).concat([[23,5],[2,4]] as P[]);

function verifyWitness(cfg: P[]) {
  const rows = [0,0,0,0,0,0,0]; for (const s of cfg) rows[s[1]]++;
  return {
    safe: findUnsafeSubset(cfg, q) === null,
    maximal: unblockedCells(cfg, w, W, q).length === 0,
    deficient: Math.min(...rows) <= q - 2,
    unblocked35: unblockedCells(cfg, w, W + 1, q),
  };
}

function main() {
  const U34 = unblockedCells(BASE, w, W, q);
  if (U34.length !== 1 || U34[0][0] !== 33 || U34[0][1] !== 0) throw new Error("base sanity fail");
  for (const [name, cfg] of [["winA", WIN_A], ["winB", WIN_B]] as [string, P[]][]) {
    const r = verifyWitness(cfg);
    if (!r.safe || !r.maximal || !r.deficient) throw new Error(name + " FAIL " + JSON.stringify(r));
  }
  return "both witnesses PASS safe+maximal+deficient at 7x34; M_{7,5} >= 35";
}
main();
