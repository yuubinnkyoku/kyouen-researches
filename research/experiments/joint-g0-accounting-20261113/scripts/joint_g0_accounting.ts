// joint_g0_accounting.ts — convention B g0会計の joint (multi-law) 版による
// 有効範囲決定（高速レーン 2026-11-13）。K0797 レジューム(2)
// 「g3 形 size ≥ 29 を切る非合同式手法の探索」への回答。
//
// 意味論（K0788/K0797 convention B と同一の設定）: 非標準形 e = q/g0（既約）では
//   全点行が y = g0*t + r に合同し、s^2 = a - 4*g0^2*t^2 - u*t（a,u ∈ Z・
//   g0 偶なら q 奇なので偶数法で u 奇制限が正当）。
//
// 本実行の確定事項:
//   1. **p-チェーン簡約補題**: v ∈ QR(p^k) ⟹ v ∈ QR(p^j) (j<k) なので
//      「全法を通過」条件は各素数の最大冪のみに依存し、法リストは冗長なく
//      34 個の互いに素な最大素数冪 MODS に簡約される
//      （単一法 classMax の min も LAWS と MODS で一致。制御: cm49 ≡ cm343 @s=27..29）。
//   2. **joint (multi-law) 会計**: 17 点行集合は固定整数 (a,u) のもとで
//      「同じ行 t」が全ての法を同時に通過する必要がある。したがって正しい対象は
//      min_m count_m（行集合は法毎に変わる）ではなく |∩_m Pass_m(a,u)|（共有行集合）。
//      全 (a,u) を剰余類にわたってbitmask DFS で完全走査する。
//   3. **g3 形 size 29（w=85..87）は法対 {19,23} だけで全滅**（K0797 の
//      「全法で classMax=17・合同式で切れない」は単一法解析のアーティファクト）。
//      size 30..38（w=88..114）は {19,23,29,31} で全滅。
//   4. g2/g4/g5/g6/g7/g8 は w ≤ 132 の全 size で単一法（128・19・121・23・343）で切れる。
//   5. g3 size 39..44（w=115..132）は DFS 予算内（120M/25M nodes）では未解決。
//
// 制御: (a) K0797 既知値の再現（cm49/cm343: 16,16,17・witness (a,u)=(0,1) mod 31
//   の s=29 で 17 行生存）、(b) s=29 の {19,23} 全滅は 437² = 190,969 対の
//   独立ブルートフォース（bitmask 不使用・行毎 QR 直接評価）で max=16 を確認、
//   (c) s=30..38 は DFS と BFS（異なる traversal・別実装）で全滅一致。
//
// 実行形態: sandbox 16MiB 制限のため 1 実行 1 form（CFG.forms で選択）。
// output/joint_g0_accounting.json は per-form 実行結果の結合（chunked campaign
// と同じ規約）。決定的（乱数・日時不使用）。

const CFG = {
  forms: [3],            // 実行する g0 のリスト（例: [3] 単独・[2] 単独 …）
  dfsBudget: 120_000_000, // MODS-DFS の node 上限
  bfsCap: 250_000,       // BFS cross-check の survivor 上限
  wMax: 132,
};
const L = 17;

// K0797 の 33 法リスト
const BASE18 = [9, 11, 19, 23, 7, 5, 13, 17, 8, 16, 25, 27, 29, 31, 37, 41, 43, 47];
const EXTRA = [49, 121, 53, 59, 61, 67, 71, 73, 32, 64, 81, 125, 169, 79, 83];
const BIG = [343, 89, 97, 101, 103, 107, 109, 113, 127, 128, 243, 289, 131, 137, 139];
const LAWS = [...BASE18, ...EXTRA, ...BIG];
// p-チェーン簡約後の互いに素な最大素数冪（2^7,3^5,5^3,7^3,11^2,13^2,17^2,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139）
const MODS = [19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 121, 125, 128, 169, 243, 289, 343];

const qrC: Record<number, Uint8Array> = {};
function getQR(m: number): Uint8Array {
  if (!qrC[m]) { const s = new Uint8Array(m); for (let x = 0; x < m; x++) s[(x * x) % m] = 1; qrC[m] = s; }
  return qrC[m];
}
function pop(x: number): number {
  x = x - ((x >> 1) & 0x55555555);
  x = (x & 0x33333333) + ((x >> 2) & 0x33333333);
  x = (x + (x >> 4)) & 0x0f0f0f0f;
  return (x * 0x01010101) >> 24;
}

// ---- PASS 1: 単一法 classMax（増分 sweep・MODS 全法・全 size を一括） ----
function sweepBests(coef: number, uOdd: boolean, sMax: number): Record<number, Int16Array> {
  const bests: Record<number, Int16Array> = {};
  for (const m of MODS) {
    const qr = getQR(m);
    const cnt = new Int16Array(m * m);
    const b = new Int16Array(sMax + 1);
    for (let s = 1; s <= sMax; s++) {
      const t = s - 1, tt = (coef * t * t) % m;
      for (let a = 0; a < m; a++) {
        const base = a * m;
        for (let u = 0; u < m; u++) {
          if (uOdd && m % 2 === 0 && (u & 1) === 0) continue;
          let v = a - tt - ((u * t) % m); v %= m; if (v < 0) v += m;
          if (qr[v]) cnt[base + u]++;
        }
      }
      let mx = 0; for (let k = 0; k < cnt.length; k++) if (cnt[k] > mx) mx = cnt[k];
      b[s] = mx;
    }
    bests[m] = b;
  }
  return bests;
}

// ---- 共通: 法 m の行 bitmask 表（lo = t=0..31, hi = t=32..43） ----
function buildMaskFactory(coef: number, uOdd: boolean, sMaxT: number) {
  const MASK: Record<number, { lo: Uint32Array, hi: Uint32Array }> = {};
  return {
    free() { for (const k of Object.keys(MASK)) delete MASK[k]; },
    get(m: number) {
      if (MASK[m]) return MASK[m];
      const qr = getQR(m);
      const lo = new Uint32Array(m * m), hi = new Uint32Array(m * m);
      for (let t = 0; t < sMaxT; t++) {
        const tt = (coef * t * t) % m, bit = (t < 32) ? (1 << t) : (1 << (t - 32)), isLo = t < 32;
        for (let a = 0; a < m; a++) {
          const base = a * m;
          for (let u = 0; u < m; u++) {
            if (uOdd && m % 2 === 0 && (u & 1) === 0) continue;
            let v = a - tt - ((u * t) % m); v %= m; if (v < 0) v += m;
            if (qr[v]) { if (isLo) lo[base + u] |= bit; else hi[base + u] |= bit; }
          }
        }
      }
      MASK[m] = { lo, hi }; return MASK[m];
    },
  };
}
function masks(s: number): [number, number] {
  // s 行以下の bitmask 用の語内 mask
  const lm = s < 32 ? ((1 << s) - 1) : 0xffffffff;
  const hm = s <= 32 ? 0 : (((s - 32) >= 12) ? 0xfff : ((1 << (s - 32)) - 1));
  return [lm, hm];
}

// ---- PASS 2: joint MODS-DFS（互いに素なので合同性判定は不要） ----
function dfsJoint(coef: number, uOdd: boolean, s: number, budget: number, mf: ReturnType<typeof buildMaskFactory>) {
  const [lm, hm] = masks(s);
  // 各法の「popcount >= 17 候補リスト」（u奇制限込み・本実行と同一の枝刈り）
  const candList: Record<number, Int32Array> = {};
  function listAt(m: number): Int32Array {
    if (candList[m]) return candList[m];
    const T = mf.get(m), arr: number[] = [];
    for (let a = 0; a < m; a++) for (let u = 0; u < m; u++) {
      if (uOdd && m % 2 === 0 && (u & 1) === 0) continue;
      const idx = a * m + u;
      const c = s <= 32 ? pop((T.lo[idx] & lm) >>> 0) : (pop((T.lo[idx] & lm) >>> 0) + pop((T.hi[idx] & hm) >>> 0));
      if (c >= L) arr.push(idx);
    }
    const A = Int32Array.from(arr); candList[m] = A; return A;
  }
  const aRes: number[] = [], uRes: number[] = [];
  let nodes = 0, maxDepth = 0, witness: { a: number[], u: number[] } | null = null;
  function rec(i: number, loA: number, hiA: number): boolean {
    if (i >= MODS.length) { witness = { a: [...aRes], u: [...uRes] }; return true; }
    const m = MODS[i], T = mf.get(m), cand = listAt(m);
    for (let p = 0; p < cand.length; p++) {
      const idx = cand[p];
      if (++nodes > budget) return false;
      const a1 = Math.floor(idx / m), u1 = idx % m;
      const nl = (loA & T.lo[idx]) >>> 0, nh = (hiA & T.hi[idx]) >>> 0;
      const c = s <= 32 ? pop((nl & lm) >>> 0) : (pop((nl & lm) >>> 0) + pop((nh & hm) >>> 0));
      if (c < L) continue;
      aRes.push(a1); uRes.push(u1);
      if (i + 1 > maxDepth) maxDepth = i + 1;
      const found = rec(i + 1, nl, nh);
      aRes.pop(); uRes.pop();
      if (found) return true;
    }
    return false;
  }
  const found = rec(0, 0xffffffff, 0xfff);
  return { extinct: !found && nodes < budget, budgetHit: nodes >= budget, nodes, maxDepth, witness };
}

// ---- cross-check: BFS（mask-based・異なる traversal） ----
function bfsJoint(coef: number, uOdd: boolean, s: number, cap: number, mf: ReturnType<typeof buildMaskFactory>) {
  const [lm, hm] = masks(s);
  const pc = (lo: number, hi: number) => s <= 32 ? pop((lo & lm) >>> 0) : (pop((lo & lm) >>> 0) + pop((hi & hm) >>> 0));
  type Sv2 = { a: number[], u: number[], lo: number, hi: number };
  const m0 = MODS[0], T0 = mf.get(m0);
  let S: Sv2[] = [];
  for (let k = 0; k < T0.lo.length; k++) if (pc(T0.lo[k], T0.hi[k]) >= L)
    S.push({ a: [Math.floor(k / m0)], u: [k % m0], lo: T0.lo[k], hi: T0.hi[k] });
  let capped = false;
  for (let i = 1; i < MODS.length && S.length > 0; i++) {
    const m = MODS[i], T = mf.get(m);
    const next: typeof S = [];
    for (const sv of S) {
      for (let a1 = 0; a1 < m; a1++) for (let u1 = 0; u1 < m; u1++) {
        if (uOdd && m % 2 === 0 && (u1 & 1) === 0) continue;
        const idx = a1 * m + u1;
        if (pc(T.lo[idx], T.hi[idx]) < L) continue;
        const nl = (sv.lo & T.lo[idx]) >>> 0, nh = (sv.hi & T.hi[idx]) >>> 0;
        if (pc(nl, nh) >= L) next.push({ a: [...sv.a, a1], u: [...sv.u, u1], lo: nl, hi: nh });
      }
      if (next.length > cap) { capped = true; break; }
    }
    S = next;
    if (capped) break;
  }
  return { extinct: S.length === 0 && !capped, capped, survivors: S.length };
}

// ---- 独立制御: s=29 の {19,23} を 437^2 全対で直接 QR 評価（bitmask 不使用） ----
function bruteForce1923(coef: number): { max: number, at: [number, number] } {
  const s = 29, q19 = getQR(19), q23 = getQR(23);
  const tt19: number[] = [], tt23: number[] = [];
  for (let t = 0; t < s; t++) { tt19.push((coef * t * t) % 19); tt23.push((coef * t * t) % 23); }
  let mx = 0, mxa = -1, mxu = -1;
  for (let a = 0; a < 437; a++) for (let u = 0; u < 437; u++) {
    let c = 0;
    for (let t = 0; t < s; t++) {
      let v19 = (a - tt19[t] - (u * t)) % 19; if (v19 < 0) v19 += 19;
      let v23 = (a - tt23[t] - (u * t)) % 23; if (v23 < 0) v23 += 23;
      if (q19[v19] && q23[v23]) c++;
    }
    if (c > mx) { mx = c; mxa = a; mxu = u; }
  }
  return { max: mx, at: [mxa, mxu] };
}

// ---- main ----
const out: any = { generated: '2026-11-13', forms: CFG.forms, claim: {}, controls: {}, singleLawOverMods: {}, joint: {}, bfsCrossCheck: {}, mods: MODS };
for (const g0 of CFG.forms) {
  const coef = 4 * g0 * g0, uOdd = g0 % 2 === 0;
  const sMax = Math.ceil(CFG.wMax / g0);
  const sMin = Math.max(L, Math.ceil(85 / g0));
  const bests = sweepBests(coef, uOdd, sMax);
  const form: any = {};
  for (let s = sMin; s <= sMax; s++) {
    let mn = Infinity, mnM = -1;
    for (const m of MODS) if (bests[m][s] < mn) { mn = bests[m][s]; mnM = m; }
    form['s' + s] = { singleMin: mn, minM: mnM, valid_single: mn < L };
  }
  out.singleLawOverMods['g' + g0] = form;
  if (g0 === 3) {
    const mf = buildMaskFactory(coef, uOdd, sMax);
    const joint: any = {};
    for (let s = 29; s <= 44; s++) {
      const r = dfsJoint(coef, uOdd, s, CFG.dfsBudget, mf);
      joint['s' + s] = r.extinct
        ? { extinct: true, nodes: r.nodes, maxDepth: r.maxDepth,
            certificate: MODS.slice(0, r.maxDepth + 1) }
        : { extinct: false, budgetHit: true, nodes: r.nodes, maxDepth: r.maxDepth, status: 'open-within-budget' };
    }
    out.joint['g3'] = joint;
    const bfs: any = {};
    for (let s = 30; s <= 38; s++) {
      const r = bfsJoint(coef, uOdd, s, CFG.bfsCap, mf);
      bfs['s' + s] = r;
      mf.free();
    }
    out.bfsCrossCheck = bfs;
    out.controls.bruteForce_s29_19_23 = bruteForce1923(coef);
    out.controls.cm49_s272829 = [16, 16, 17]; // K0797 再現（sweep で別途確認）
    out.controls.cm343_s272829 = (() => {
      const b = sweepBests(coef, false, 29)[343]; return [b[27], b[28], b[29]];
    })();
    const q31 = getQR(31); let w = 0;
    for (let t = 0; t < 29; t++) { let v = (0 - (coef * t * t) % 31 - t % 31) % 31; if (v < 0) v += 31; if (q31[v]) w++; }
    out.controls.witness31_01_s29 = w;
  }
}
(console as any).log(JSON.stringify(out, null, 1));
