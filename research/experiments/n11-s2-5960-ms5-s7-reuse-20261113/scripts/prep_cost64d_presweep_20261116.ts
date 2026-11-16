// cost-64d prep: independent candidate enumeration + parent derivation for row
// 00000000000000403800000008002000 at the canonical head 1419.
// Exact integer arithmetic only; fourth implementation (pre-sweep audit was the third).
const N = 11;
function hexBits(h: string): number[] {
  const v = BigInt('0x' + h); const out: number[] = [];
  for (let i = 0; i < 121; i++) if ((v >> BigInt(i)) & 1n) out.push(i);
  return out;
}
function toHex(bits: number[]): string {
  let v = 0n; for (const b of bits) v |= 1n << BigInt(b);
  return v.toString(16).padStart(32, '0');
}
// forbidden quadruple: lifted 4x4 det [x*x+y*y, x, y, 1] == 0 (concyclic or collinear)
function forbidden(a: number[], b: number[], c: number[], d: number[]): boolean {
  const L = (p: number[]) => [p[0] * p[0] + p[1] * p[1], p[0], p[1]];
  const A = L(a), B = L(b), C = L(c), D = L(d);
  const det3 = (u: number[], v: number[], w: number[]) =>
    u[0] * (v[1] * w[2] - v[2] * w[1]) -
    u[1] * (v[0] * w[2] - v[2] * w[0]) +
    u[2] * (v[0] * w[1] - v[1] * w[0]);
  const t = det3(B, C, D) - det3(A, C, D) + det3(A, B, D) - det3(A, B, C);
  return t === 0;
}
function legalCandidates(hex: string): number[] {
  const stones = hexBits(hex).map(i => [i % N, Math.floor(i / N)]);
  const out: number[] = [];
  for (let b = 0; b < 121; b++) {
    const y = Math.floor(b / N), x = b % N;
    if (stones.some(s => s[0] === x && s[1] === y)) continue;
    let ok = true;
    outer:
    for (let i = 0; i < stones.length; i++)
      for (let j = i + 1; j < stones.length; j++)
        for (let k = j + 1; k < stones.length; k++)
          if (forbidden(stones[i], stones[j], stones[k], [x, y])) { ok = false; break outer; }
    if (ok) out.push(b);
  }
  return out;
}
const T = [
  (x: number, y: number): [number, number] => [x, y],
  (x: number, y: number): [number, number] => [N - 1 - y, x],
  (x: number, y: number): [number, number] => [N - 1 - x, N - 1 - y],
  (x: number, y: number): [number, number] => [y, N - 1 - x],
  (x: number, y: number): [number, number] => [N - 1 - x, y],
  (x: number, y: number): [number, number] => [x, N - 1 - y],
  (x: number, y: number): [number, number] => [y, x],
  (x: number, y: number): [number, number] => [N - 1 - y, N - 1 - x],
];
function canon(hex: string): string {
  const pts = hexBits(hex).map(i => [i % N, Math.floor(i / N)]);
  let best = 'ffffffffffffffffffffffffffffffff';
  for (const t of T) {
    const h = toHex(pts.map(([x, y]) => { const [nx, ny] = t(x, y); return ny * N + nx; }));
    if (h < best) best = h;
  }
  return best;
}
const ROW = '00000000000000403800000008002000';
const PARENT_P = '00000000000000403800000008000000';
// pre-registered bits from class2-lane-next-target-presweep-audit-20261116.json (head pin a66f35c8)
const PREREG = [0,1,2,3,4,5,6,8,9,10,11,16,17,21,25,29,30,32,38,42,43,44,46,53,54,66,69,74,75,76,78,79,80,83,85,86,87,88,89,92,95,96,97,98,99,100,101,102,103,105,106,107,108,109,110,111,113,114,115,116,117,118,119,120];
// ranking CSV at head 1419 (open S5 parents): s5_hex,classes,remaining_s6_orbits,remaining_s7_edge_cost
import { readFileSync } from 'node:fs';
const rank = new Map<string, { classes: number, rows: number, cost: number }>();
for (const line of readFileSync(new URL('../output/class-frontier-s5-ranking-after-cost65j-receipts-20261116.csv', import.meta.url), 'utf8').split(/\r?\n/).slice(1)) {
  if (!line.trim()) continue;
  const [h, cl, r, c] = line.split(',');
  rank.set(h, { classes: Number(cl), rows: Number(r), cost: Number(c) });
}
const cands = legalCandidates(ROW);
const stones = hexBits(ROW);
const report: any = {
  row: ROW,
  stones: stones,
  popcount: stones.length,
  own_candidate_count: cands.length,
  prerereg_count: PREREG.length,
  candidates_match_prereg: JSON.stringify(cands) === JSON.stringify(PREREG),
  row_contains_P: hexBits(PARENT_P).every(b => stones.includes(b)),
  P_ranking: rank.get(PARENT_P) || null,
  deletions: [] as any[],
};
for (const s of stones) {
  const del = toHex(stones.filter(b => b !== s));
  const c = canon(del);
  const r = rank.get(c) || null;
  report.deletions.push({ removed_stone: s, deletion_hex: del, canon: c, open_at_1419: r });
}
console.log(JSON.stringify(report, null, 1));
