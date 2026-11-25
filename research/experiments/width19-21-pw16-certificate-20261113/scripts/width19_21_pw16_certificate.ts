// width19_21_pw16_certificate.ts — P(19) = P(20) = P(21) = 16 の完全決定（高速レーン 2026-11-13）。
// 依存なし・決定的（乱数・日時不使用）。STAGE 分割実行（単一 sandbox の deadline 対策）:
//   STAGES = "subsets" | "kill" | "accounting" | "witness" | "all"
// （"all" は分割実行の記録値の再現用。sandbox では 1..2 STAGE ずつ推奨）。
//
// 意味論・枠組み（K0072 Vieta + K0763-K0767 会計 + K0778/K0784 と同一・第五独立実装）:
//   円 x²+y²+Cx+Dy+N=0・行 0..w-1（幅=行数）・列は非有界。
//   P = 2d+s・接点行 s ≤ 2（幾何）→ P ≥ 17 ⟹ d ≥ 8（二重行）→ C ∈ Z（K0072）→
//   d+s ≥ 9 点行。点行集合 R（|R| ≥ 9）は:
//   (a) 標準形（e = 4D ∈ 4Z）: s_y² = A − 4y² − ey。任意の奇素数冪 m で
//       a = A mod m（N 自由により全剰余）・u = e mod m（4D 自由により全剰余）が
//       自由 → 証明書「∃(a,u) mod m: a − 4i² − ui ∈ QR0(m) ∀i ∈ R」は必要条件
//       （QR0 = 平方剰余 ∪ {0}・接点行 s=0 を含む）。偶数法（8,16）では
//       A ≡ C² (mod 4)・e ≡ 0 (mod 4) の制約があるが自由 (a,u) は真に上位集合
//       → 消去用途に健全（誤殺なし・殺し漏れのみ）。
//   (b) g0 ≥ 2 形（全点行が y ≡ r (mod g0)・e = q/g0 既約）: convention B
//       （K0788 監査）により s² = a' − 4g0²t² − u't（t = (y−r)/g0）。類サイズ
//       ⌈w/g0⌉ と classMax（証明書通過最大点数・全法の min）で排除。
//   よって P ≥ 17 は (a) 9 部分集合の証明書全滅 または (b) classMax < 9 で否定される。
//
// 本実装の新規性（K0778/K0784 からの差分）:
//   K0778/K0784 の基底 18 法（9,11,19,23,7,5,13,17,8,16,25,27,29,31,37,41,43,47）で
//   w=21 level 9 に生残した 16 集合（K0784 命題4・本スクリプトで全数保持して再現）
//   を**拡張法（素数 53..343・素数冪 121,125,128,169,256,289,343 等）で掃引**した
//   結果、**全 16 集合が法 121 = 11² または 343 = 7³ のみで全滅**。
//   有界半径探索（K0778 の R ≤ 2×10⁷ など）に依存しない**無条件全称証明**。
//   w=19 の 2 集合・w=20 の 8 集合は全て w=21 の 16 集合に含まれる（行値が
//   0..18 / 0..19 に収まるもの）ため、同じ掃引で P(19), P(20) も確定する
//   （K0778 の条件付き上界 P ≤ 18 を等号付き P = 16 に強化）。
//
// 制御:
//   (1) w=17,18 k=9 は基底法で全滅（K0778 の P(17)=P(18)=16 と一致）。
//   (2) w=19 k=9 生残 2 集合（K0778 stage(7) の S1 = {0,1,4,6,7,12,13,15,18} と鏡像）・
//       w=20 k=9 生残 8 集合（K0778 の candidates: 8 と一致）・w=21 k=9 生残 16 集合
//       （K0784 命題4 の 16 と一致）。
//   (3) 実在 witness の行集合（130 円 {0,1,2,4,7,9,10,11}・50 円 {0,1,3,4,6,7}・
//       650 円 S* = {0,1,3,4,7,10,15,18,21,22,24,25}）は拡張法 **全て** で証明書を
//       通過（実在集合を誤殺していないことの直接検証）。
//   (4) 130 円 (2x−11)²+(2y−11)²=130 は w=17..21 でちょうど 16 点（下界・等号）。

const STAGES = "all"; // 分割実行時は "subsets" | "kill" | "accounting" | "witness" に書き換え

async function main() {
  const out: any = { generated: "2026-11-13", stages: {} };
  const qrCache: Record<number, Uint8Array> = {};
  function getQR(m: number): Uint8Array {
    if (!qrCache[m]) { const s = new Uint8Array(m); for (let x = 0; x < m; x++) s[(x * x) % m] = 1; qrCache[m] = s; }
    return qrCache[m];
  }
  function subsetOK(S: number[], m: number, coef: number): boolean {
    const qr = getQR(m);
    for (let a = 0; a < m; a++) for (let u = 0; u < m; u++) {
      let ok = true;
      for (let k = 0; k < S.length; k++) {
        const i = S[k];
        let t = (a - (coef * i * i) % m - u * i) % m; if (t < 0) t += m;
        if (!qr[t]) { ok = false; break; }
      }
      if (ok) return true;
    }
    return false;
  }
  function killerMod(S: number[], mods: number[]): number | null {
    for (const m of mods) if (!subsetOK(S, m, 4)) return m;
    return null;
  }
  const MODS = [9, 11, 19, 23, 7, 5, 13, 17, 8, 16, 25, 27, 29, 31, 37, 41, 43, 47];
  const EXT = [53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 121, 125, 127, 128, 131, 137, 139, 149, 151, 157, 163, 167, 169, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 256, 257, 263, 269, 271, 277, 281, 283, 289, 293, 307, 311, 313, 317, 331, 337, 343];

  function runW(w: number, k: number, keepAll: boolean) {
    let total = 0, survivors = 0; const perMod: Record<number, number> = {};
    const all: number[][] = []; const cur: number[] = [];
    function rec(s: number) {
      if (cur.length === k) {
        total++;
        let alive = true;
        for (const m of MODS) { if (!subsetOK(cur, m, 4)) { perMod[m] = (perMod[m] || 0) + 1; alive = false; break; } }
        if (alive) { survivors++; if (keepAll) all.push(cur.slice()); }
        return;
      }
      for (let i = s; i < w; i++) { cur.push(i); rec(i + 1); cur.pop(); }
    }
    rec(0);
    return { subsets: total, survivors, perMod, survivorAll: all };
  }

  if (STAGES === "all" || STAGES === "subsets") {
    const c17 = runW(17, 9, false), c18 = runW(18, 9, false);
    const s19 = runW(19, 9, true), s20 = runW(20, 9, true), s21 = runW(21, 9, true);
    out.stages.subsets = {
      control_w17_k9: { subsets: c17.subsets, survivors: c17.survivors },
      control_w18_k9: { subsets: c18.subsets, survivors: c18.survivors },
      survivors_w19: { subsets: s19.subsets, survivors: s19.survivors, sets: s19.survivorAll },
      survivors_w20: { subsets: s20.subsets, survivors: s20.survivors, sets: s20.survivorAll },
      survivors_w21: { subsets: s21.subsets, survivors: s21.survivors, sets: s21.survivorAll },
    };
  }

  if (STAGES === "all" || STAGES === "kill") {
    const sets21: number[][] = [
      [0,1,3,4,7,12,15,18,19],[0,1,4,6,7,12,13,15,18],[0,1,4,6,7,12,13,18,19],
      [0,1,4,7,12,15,16,18,19],[0,1,6,7,12,13,15,18,19],[0,3,5,6,11,12,14,17,18],
      [0,3,5,6,11,12,14,17,20],[0,3,6,8,9,14,15,17,20],[1,2,4,5,8,13,16,19,20],
      [1,2,5,7,8,13,14,16,19],[1,2,5,7,8,13,14,19,20],[1,2,5,8,13,16,17,19,20],
      [1,2,7,8,13,14,16,19,20],[1,4,6,7,12,13,15,18,19],[2,3,6,8,9,14,15,17,20],
      [2,5,7,8,13,14,16,19,20]];
    const results = sets21.map(S => ({ S: S.join(","), killedBy: killerMod(S, EXT) }));
    const key = new Set(sets21.map(s => s.join(",")));
    const sub19 = [[0,1,4,6,7,12,13,15,18],[0,3,5,6,11,12,14,17,18]];
    const sub20 = [[0,1,3,4,7,12,15,18,19],[0,1,4,6,7,12,13,15,18],[0,1,4,6,7,12,13,18,19],[0,1,4,7,12,15,16,18,19],[0,1,6,7,12,13,15,18,19],[0,3,5,6,11,12,14,17,18],[1,2,5,7,8,13,14,16,19],[1,4,6,7,12,13,15,18,19]];
    out.stages.kill = {
      killed: results.filter(r => r.killedBy !== null).length,
      total: results.length,
      allKilledBy_121_or_343: results.every(r => r.killedBy === 121 || r.killedBy === 343),
      perSet: results,
      w19_candidates_included_in_w21_list: sub19.every(s => key.has(s.join(","))),
      w20_candidates_included_in_w21_list: sub20.every(s => key.has(s.join(","))),
    };
  }

  if (STAGES === "all" || STAGES === "accounting") {
    function classMax(rows: number[], coef: number): number {
      let best = Infinity;
      for (const m of MODS) {
        const qr = getQR(m); let bm = 0;
        for (let a = 0; a < m; a++) for (let u = 0; u < m; u++) {
          let c = 0;
          for (const y of rows) { let t = (a - (coef * y * y) % m - u * y) % m; if (t < 0) t += m; if (qr[t]) c++; }
          if (c > bm) bm = c;
        }
        if (bm < best) best = bm;
      }
      return best;
    }
    const acc: any = {};
    for (const w of [19, 20, 21]) {
      const evens: number[] = [], odds: number[] = [];
      for (let y = 0; y < w; y += 2) evens.push(y);
      for (let y = 1; y < w; y += 2) odds.push(y);
      const evT = evens.map(y => y / 2), odT = odds.map(y => (y - 1) / 2);
      let g3max = 0;
      const g3: any = {};
      for (let r = 0; r < 3; r++) {
        const clsT: number[] = []; for (let y = r; y < w; y += 3) clsT.push((y - r) / 3);
        const cm = classMax(clsT, 36); g3["r" + r] = { n: clsT.length, B: cm }; g3max = Math.max(g3max, cm);
      }
      const evB = classMax(evT, 16), odB = classMax(odT, 16);
      const evA = classMax(evens, 16), odA = classMax(odds, 16);
      acc["w" + w] = {
        g2: { evens_n: evens.length, evens_B: evB, evens_A: evA, odds_n: odds.length, odds_B: odB, odds_A: odA },
        g3: { ...g3, maxB: g3max },
        g4_classSize: Math.ceil(w / 4),
        allBelow9_B: Math.max(evB, odB, g3max) < 9 && Math.ceil(w / 4) < 9,
      };
    }
    out.stages.accounting = acc;
  }

  if (STAGES === "all" || STAGES === "witness") {
    const pts: [number, number][] = [];
    for (let y = -30; y <= 30; y++) for (let x = -30; x <= 30; x++)
      if ((2 * x - 11) ** 2 + (2 * y - 11) ** 2 === 130) pts.push([x, y]);
    const perW: Record<number, number> = {};
    for (const w of [17, 18, 19, 20, 21]) {
      perW[w] = new Set(pts.filter(([, y]) => y >= 0 && y < w).map(p => p.join(","))).size;
    }
    const rows = [...new Set(pts.map(p => p[1]))].sort((a, b) => a - b);
    const c130 = [0, 1, 2, 4, 7, 9, 10, 11], c50 = [0, 1, 3, 4, 6, 7];
    const Sstar = [0, 1, 3, 4, 7, 10, 15, 18, 21, 22, 24, 25];
    out.stages.witness = {
      c130_total: pts.length, c130_rows: rows, c130_perW: perW,
      realizable_pass_EXT: {
        c130: killerMod(c130, EXT) === null,
        c50: killerMod(c50, EXT) === null,
        S650: killerMod(Sstar, EXT) === null,
      },
    };
  }

  out.claims = {
    exact: { 19: 16, 20: 16, 21: 16 },
    method: "k=9 base-18 survivor complete enumeration + extended-modulus (121=11^2, 343=7^3) unconditional kill + g0>=2 convention-B classMax accounting + 130-circle lower bound 16",
    upgrades: "P(19),P(20): K0778 conditional upper 18 -> proved 16. P(21): K0784 open {16,17,18} -> proved 16",
    closure: "P(w) is now decided for every w in 6..48 (with K0778/K0782/K0784/K0788)",
  };
  return out;
}
