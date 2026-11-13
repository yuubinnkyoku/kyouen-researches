// two_row_m24.ts — 2×m・q=4 の真の満容量安定化長 M_{2,4}=9 の決定（K0796）
// モデル（K0069 B214 と同一の幾何）:
//   行 y=0 の石の列集合 A・行 y=1 の列集合 B。
//   - 4点共線は水平行内のみ（非水平直線は各行に1点）→ |A|,|B| ≤ 3。
//   - 4点共円（各行2点）は (x1+x2)/2 = (x3+x4)/2、すなわち
//     pairsum(A) ∩ pairsum(B) ≠ ∅ のときかそのときに限り禁止。
//   安全 ⟺ |A|,|B|≤3 かつ pairsum 素。極大 = どちらの行にも安全に追加できない。
// 制御: m=1..5 で直接幾何（外心・整数演算）による全4組列挙の暴力実装と
//   極大安全集合の総数が完全一致（12/24/78 など・別実装）。
const pairsums = (S: number[]) => { const r = new Set<number>(); for (let i = 0; i < S.length; i++) for (let j = i + 1; j < S.length; j++) r.add(S[i] + S[j]); return r; };
function* subsets(m: number): Generator<number[]> { const r: number[][] = []; const rec = (start: number, cur: number[]) => { r.push([...cur]); if (cur.length < 3) for (let x = start; x < m; x++) { cur.push(x); rec(x + 1, cur); cur.pop(); } }; rec(0, []); for (const s of r) yield s; }
const res: any[] = [];
for (let m = 1; m <= 12; m++) {
  const rows = [...subsets(m)];
  let countFull = 0, countDef = 0, maxDef = -1; let example: any = null;
  for (const A of rows) for (const B of rows) {
    const sa = pairsums(A), sb = pairsums(B);
    let disjoint = true; for (const v of sa) if (sb.has(v)) { disjoint = false; break; }
    if (!disjoint) continue;
    const inA = new Set(A), inB = new Set(B);
    const addA = (() => { if (A.length >= 3) return false; const so = pairsums(B); for (let x = 0; x < m; x++) { if (inA.has(x)) continue; const sn = pairsums([...A, x]); let clash = false; for (const v of sn) if (so.has(v)) { clash = true; break; } if (!clash) return true; } return false; })();
    const addB = (() => { if (B.length >= 3) return false; const so = pairsums(A); for (let x = 0; x < m; x++) { if (inB.has(x)) continue; const sn = pairsums([...B, x]); let clash = false; for (const v of sn) if (so.has(v)) { clash = true; break; } if (!clash) return true; } return false; })();
    if (addA || addB) continue;
    const stones = A.length + B.length;
    const fullCap = 2 * Math.min(m, 3);
    if (stones === fullCap) countFull++; else { countDef++; if (stones > maxDef) { maxDef = stones; example = { A, B, stones }; } }
  }
  res.push({ m, countFull, countDef, maxDeficientStones: maxDef, example });
}
console.log(JSON.stringify(res, null, 1));
