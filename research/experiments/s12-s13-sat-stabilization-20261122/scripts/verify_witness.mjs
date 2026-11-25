// verify_witness.mjs — independent second verifier for maximal safe sets on the
// n x n standard kyouen board (q = 4). BigInt determinant along a DIFFERENT code
// path than verify_witness.py: Bareiss-fraction-free sweep on the 4x4 matrix
// [x, y, x^2+y^2, 1] (column order differs from the Python verifier too), and
// cocircularity via the determinant of the 3x3 minors of [x, y, 1 | x^2+y^2].
// Usage: node verify_witness.mjs witness.json    ({"n": 12, "stones": [[x,y],...]})
import { readFileSync } from 'node:fs';

const wit = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const n = wit.n, stones = wit.stones.map(([x, y]) => [BigInt(x), BigInt(y)]);
const k = stones.length;

// Bareiss integer-preserving determinant of a 4x4 BigInt matrix.
function bareiss4(M) {
  const A = M.map(r => r.slice());
  let sign = 1n;
  let prev = 1n;
  for (let i = 0; i < 3; i++) {
    if (A[i][i] === 0n) {
      let sw = -1;
      for (let r = i + 1; r < 4; r++) if (A[r][i] !== 0n) { sw = r; break; }
      if (sw < 0) return 0n;
      [A[i], A[sw]] = [A[sw], A[i]];
      sign = -sign;
    }
    for (let r = i + 1; r < 4; r++) {
      for (let c = i + 1; c < 4; c++) {
        A[r][c] = (A[r][c] * A[i][i] - A[r][i] * A[i][c]) / prev;
      }
    }
    prev = A[i][i];
  }
  return sign * A[3][3];
}

function coco4(p1, p2, p3, p4) {
  // matrix columns [x, y, x^2+y^2, 1]
  const M = [p1, p2, p3, p4].map(([x, y]) => [x, y, x * x + y * y, 1n]);
  return bareiss4(M);
}

function coll3(p1, p2, p3) {
  // 3x3 det of [x, y, 1]
  const [x1, y1] = p1, [x2, y2] = p2, [x3, y3] = p3;
  return x1 * (y2 - y3) - y1 * (x2 - x3) + (x2 * y3 - x3 * y2);
}

function combos(arr, r) {
  const res = [];
  const pick = (start, cur) => {
    if (cur.length === r) { res.push(cur.slice()); return; }
    for (let i = start; i < arr.length; i++) { cur.push(arr[i]); pick(i + 1, cur); cur.pop(); }
  };
  pick(0, []);
  return res;
}

const S = new Set(stones.map(([x, y]) => Number(x) + n * Number(y)));
let viol = [], minAbs = null, uncovered = [], certs = 0, blocked = 0;
for (const c of combos(stones, 4)) {
  const d = coco4(...c);
  if (d === 0n) viol.push(c.map(p => [Number(p[0]), Number(p[1])]));
  else {
    const a = d < 0n ? -d : d;
    if (minAbs === null || a < minAbs) minAbs = a;
  }
}
for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) {
  if (S.has(x + n * y)) continue;
  const p = [BigInt(x), BigInt(y)];
  let att = false;
  for (const t of combos(stones, 3)) {
    if (coco4(p, ...t) === 0n) { att = true; blocked++; break; }
  }
  if (!att) uncovered.push([x, y]);
}
const ok = viol.length === 0 && uncovered.length === 0;
console.log(JSON.stringify({
  n, k,
  engine: "bareiss BigInt, column order [x,y,x^2+y^2,1]",
  checked_safe_quadruples: combos.length ? combos(stones, 4).length : 0,
  violating_quadruples: viol.length,
  blocked_empty_points: blocked,
  uncovered_points: uncovered,
  min_abs_nonzero_determinant: minAbs === null ? null : minAbs.toString(),
  verdict: ok ? "SAFE+MAXIMAL" : "NOT-MAXIMAL-SAFE",
}, null, 1));
process.exitCode = ok ? 0 : 1;
