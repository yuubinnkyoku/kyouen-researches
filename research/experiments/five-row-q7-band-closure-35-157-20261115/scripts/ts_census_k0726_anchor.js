// K0726 anchor verification for the (5,7) band-closure lane.
// Fresh, method-independent reimplementation of two census systems:
//   A: horizontal-chord pair (same row) + third point in a different row
//      (completeness: >=7 points on w=5 rows -> some row has >=2 points).
//   B: all C(5m,3) triples with an integer Cramer solve, collinear skipped
//      (independent of the pigeonhole argument).
// All arithmetic is exact integer arithmetic (values < 2^53).
// Anchors: K0726 (5x18: 84 circles {7:4, 8:80}; 5x19: 95 circles {7:8, 8:87},
// 64,980 row-pair constructions, 132,180 non-collinear triples, 83,471 distinct
// circles, +5 row lines) and the band-start records value (5x35: 244 curves).

function gcd2(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { const t = a % b; a = b; b = t; } return a || 1; }
function normKey(a, b, c, d) {
  let g = gcd2(gcd2(gcd2(Math.abs(a), Math.abs(b)), Math.abs(c)), Math.abs(d));
  a /= g; b /= g; c /= g; d /= g;
  if (a < 0 || (a === 0 && b < 0)) { a = -a; b = -b; c = -c; d = -d; }
  return [a + '|' + b + '|' + c + '|' + d, [a, b, c, d]];
}

function censusA(w, m) {  // keep all distinct circles (small m only)
  const keys = new Set(); let constructions = 0, selfCheckFail = 0;
  for (let y = 0; y < w; y++) for (let x1 = 0; x1 < m; x1++) for (let x2 = x1 + 1; x2 < m; x2++) {
    const D = -(x1 + x2); const K1 = x1 * x1 + y * y + D * x1;
    for (let y3 = 0; y3 < w; y3++) { if (y3 === y) continue; const den = y3 - y;
      for (let x3 = 0; x3 < m; x3++) {
        const Enum = K1 - (x3 * x3 + y3 * y3 + D * x3);
        const r = normKey(den, den * D, Enum, -den * K1 - Enum * y);
        const v = r[1];
        const ev = (x, yy) => v[0] * (x * x + yy * yy) + v[1] * x + v[2] * yy + v[3];
        if (ev(x1, y) !== 0 || ev(x2, y) !== 0 || ev(x3, y3) !== 0) selfCheckFail++;
        keys.add(r[0]); constructions++;
      } } }
  const hist = {}; let ge7 = 0;
  for (const key of keys) { const v = key.split('|').map(Number); let cnt = 0;
    for (let yy = 0; yy < w; yy++) for (let x = 0; x < m; x++)
      if (v[0] * (x * x + yy * yy) + v[1] * x + v[2] * yy + v[3] === 0) cnt++;
    if (cnt >= 7) { ge7++; hist[cnt] = (hist[cnt] || 0) + 1; } }
  return { constructions, distinctCirclesAll: keys.size, circlesGe7: ge7, hist, selfCheckFail, rowLines: m >= 7 ? w : 0 };
}

function censusB(w, m) {  // all triples, independent of the pigeonhole argument
  const n = w * m; const px = [], py = [];
  for (let y = 0; y < w; y++) for (let x = 0; x < m; x++) { px.push(x); py.push(y); }
  const det3 = (a, b, c) => a[0] * (b[1] * c[2] - c[1] * b[2]) - a[1] * (b[0] * c[2] - c[0] * b[2]) + a[2] * (b[0] * c[1] - c[0] * b[1]);
  const keys = new Set(); let nonCollinear = 0, collinear = 0, selfCheckFail = 0;
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) for (let k = j + 1; k < n; k++) {
    const x1 = px[i], y1 = py[i], x2 = px[j], y2 = py[j], x3 = px[k], y3 = py[k];
    const r1 = x1 * x1 + y1 * y1, r2 = x2 * x2 + y2 * y2, r3 = x3 * x3 + y3 * y3;
    const a = det3([x1, y1, 1], [x2, y2, 1], [x3, y3, 1]);
    if (a === 0) { collinear++; continue; }
    const b = det3([-r1, y1, 1], [-r2, y2, 1], [-r3, y3, 1]);
    const c = det3([x1, -r1, 1], [x2, -r2, 1], [x3, -r3, 1]);
    const d = det3([x1, y1, -r1], [x2, y2, -r2], [x3, y3, -r3]);
    const r = normKey(a, b, c, d); const v = r[1];
    const ev = (x, yy) => v[0] * (x * x + yy * yy) + v[1] * x + v[2] * yy + v[3];
    if (ev(x1, y1) !== 0 || ev(x2, y2) !== 0 || ev(x3, y3) !== 0) selfCheckFail++;
    keys.add(r[0]); nonCollinear++;
  }
  const hist = {}; let ge7 = 0;
  for (const key of keys) { const v = key.split('|').map(Number); let cnt = 0;
    for (let yy = 0; yy < w; yy++) for (let x = 0; x < m; x++)
      if (v[0] * (x * x + yy * yy) + v[1] * x + v[2] * yy + v[3] === 0) cnt++;
    if (cnt >= 7) { ge7++; hist[cnt] = (hist[cnt] || 0) + 1; } }
  return { nonCollinear, collinear, distinctCirclesAll: keys.size, circlesGe7: ge7, hist, selfCheckFail };
}

function censusAImmediate(w, m) {  // memory-light: count per construction, keep only >=7
  const kept = new Map(); let constructions = 0;
  for (let y = 0; y < w; y++) for (let x1 = 0; x1 < m; x1++) for (let x2 = x1 + 1; x2 < m; x2++) {
    const D = -(x1 + x2); const K1 = x1 * x1 + y * y + D * x1;
    for (let y3 = 0; y3 < w; y3++) { if (y3 === y) continue; const den = y3 - y;
      for (let x3 = 0; x3 < m; x3++) {
        const Enum = K1 - (x3 * x3 + y3 * y3 + D * x3);
        const r = normKey(den, den * D, Enum, -den * K1 - Enum * y);
        constructions++;
        if (kept.has(r[0])) continue;
        const v = r[1]; let cnt = 0;
        for (let yy = 0; yy < w; yy++) for (let x = 0; x < m; x++)
          if (v[0] * (x * x + yy * yy) + v[1] * x + v[2] * yy + v[3] === 0) cnt++;
        if (cnt >= 7) kept.set(r[0], cnt);
      } } }
  const hist = {}; for (const c of kept.values()) hist[c] = (hist[c] || 0) + 1;
  return { constructions, circlesGe7: kept.size, hist, rowLines: m >= 7 ? w : 0, totalCurves: kept.size + (m >= 7 ? w : 0) };
}

const out = {
  m19: { A: censusA(5, 19), B: censusB(5, 19) },
  m18: { A: censusA(5, 18), B: censusB(5, 18) },
  m35_bandStart: censusAImmediate(5, 35)
};
console.log(JSON.stringify(out));
