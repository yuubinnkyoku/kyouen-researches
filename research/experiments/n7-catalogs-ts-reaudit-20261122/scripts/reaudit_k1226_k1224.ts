// reaudit_k1226_k1224.ts -- K1226/K1224 third-line re-audit (TS on run_typescript)
// 実行環境: Mistral Vibe run_typescript sandbox (no Node/Python; inputs via tools.github_app.get_file_contents; no randomness).
// 本ファイルは本実験の実行コードを統合整理した正本である。実行は3本に分かれた:
//  (a) F アンカー + forbid7/8 構築, (b) census/n7tamper/n8/K1224 監査, (c) 補完: n8 witness trips/dirs + n7 tamper 出版対照 + 陰性対照。
// 統合時の変更は、2実行に重複していた幾何関数の一括化のみ(論理変更なし)。
// sandbox 形式: 関数群 + async function main() (harness 側が自動実行)。

async function main() {
  const G = (tools as any).github_app;
  const O = 'yuubinnkyoku', R = 'kyouen-researches';
  const raw: any = {}; const blobs: any = {};
  async function grab(path: string, key: string) {
    const r = await G.get_file_contents({ owner: O, repo: R, path: path, ref: 'refs/heads/main' });
    const arr = Array.isArray(r) ? r : [r];
    let text = '';
    for (const x of arr) {
      if (x.resource && x.resource.text) { text += x.resource.text; }
      else if (typeof x.text === 'string' && x.text.indexOf('successfully') !== 0) { text += x.text; }
      const m = (typeof x.text === 'string' ? x.text : '').match(/SHA: ([0-9a-f]{40})/);
      if (m) blobs[key] = m[1];
    }
    raw[key] = text;
  }
  const P = 'research/experiments/n7-rows-k8plus-sat-20261122/output/';
  await Promise.all([
    grab(P + 'census_k8_state.json', 'census'),
    grab(P + 'verify_census8_partial.json', 'verify'),
    grab(P + 'tamper_n8k9_summary.json', 'tamper8'),
    grab(P + 'witness_n8k9_shot1.json', 'w1'),
    grab(P + 'witness_n8k9_shot2.json', 'w2'),
    grab(P + 'tamper_k8_summary.json', 'tamper7'),
    grab(P + 'determinism.json', 'determinism'),
    grab('research/experiments/n7-seven-stone-maximal-catalog-20261122/output/classify_n7.json', 'classify'),
  ]);
  const census = JSON.parse(raw.census);
  const verify = JSON.parse(raw.verify);
  const tamper8 = JSON.parse(raw.tamper8);
  const tamper7pub = JSON.parse(raw.tamper7);
  const w1 = JSON.parse(raw.w1);
  const w2 = JSON.parse(raw.w2);
  const classify = JSON.parse(raw.classify);

  // ---------- geometry core: integer-only, independent implementation ----------
  const perms24: any[] = [];
  (function () {
    const used = [false, false, false, false]; const cur: number[] = [];
    const sign = (p: number[]) => { let inv = 0; for (let i = 0; i < 4; i++) for (let j = i + 1; j < 4; j++) if (p[i] > p[j]) inv++; return inv % 2 === 0 ? 1 : -1; };
    (function rec() {
      if (cur.length === 4) { perms24.push({ p: cur.slice(), s: sign(cur) }); return; }
      for (let i = 0; i < 4; i++) if (!used[i]) { used[i] = true; cur.push(i); rec(); cur.pop(); used[i] = false; }
    })();
  })();
  function det4(rows: number[][]): number {
    let s = 0;
    for (const e of perms24) s += e.s * rows[0][e.p[0]] * rows[1][e.p[1]] * rows[2][e.p[2]] * rows[3][e.p[3]];
    return s;
  }
  function mat(n: number, c: number[]): number[][] { return c.map(function (v) { const x = v % n, y = (v - x) / n; return [x * x + y * y, x, y, 1]; }); }
  function qkey(a: number, b: number, c: number, d: number): number { return ((a * 128 + b) * 128 + c) * 128 + d; }
  function buildForbid(n: number) {
    const set = new Set<number>(); let cnt = 0; const N = n * n;
    for (let a = 0; a < N; a++) for (let b = a + 1; b < N; b++) for (let c = b + 1; c < N; c++) for (let d = c + 1; d < N; d++) {
      if (det4(mat(n, [a, b, c, d])) === 0) { cnt++; set.add(qkey(a, b, c, d)); }
    }
    return { set: set, cnt: cnt };
  }
  function isSafe(n: number, cfg: number[], fset: Set<number>): boolean {
    const k = cfg.length;
    for (let i = 0; i < k; i++) for (let j = i + 1; j < k; j++) for (let p = j + 1; p < k; p++) for (let q = p + 1; q < k; q++)
      if (fset.has(qkey(cfg[i], cfg[j], cfg[p], cfg[q]))) return false;
    return true;
  }
  function nViol(n: number, cfg: number[], fset: Set<number>): number {
    const k = cfg.length; let v = 0;
    for (let i = 0; i < k; i++) for (let j = i + 1; j < k; j++) for (let p = j + 1; p < k; p++) for (let q = p + 1; q < k; q++)
      if (fset.has(qkey(cfg[i], cfg[j], cfg[p], cfg[q]))) v++;
    return v;
  }
  function uncovered(n: number, cfg: number[], fset: Set<number>): number {
    const inSet = new Set(cfg); let u = 0; const k = cfg.length;
    for (let c = 0; c < n * n; c++) {
      if (inSet.has(c)) continue;
      let blocked = false;
      for (let i = 0; i < k && !blocked; i++) for (let j = i + 1; j < k && !blocked; j++) for (let p = j + 1; p < k && !blocked; p++) {
        const s = [c, cfg[i], cfg[j], cfg[p]].sort(function (x: number, y: number) { return x - y; });
        if (fset.has(qkey(s[0], s[1], s[2], s[3]))) blocked = true;
      }
      if (!blocked) u++;
    }
    return u;
  }
  const mapsCache: any = {};
  function d4maps(n: number): number[][] {
    if (mapsCache[n]) return mapsCache[n];
    const repr = function (f: any) { const out: number[] = []; for (let c = 0; c < n * n; c++) { const x = c % n, y = (c - x) / n; const t = f(x, y); out.push(t[0] + n * t[1]); } return out; };
    const comp = function (g: number[], h: number[]) { return g.map(function (v) { return h[v]; }); };
    const id = repr(function (x: number, y: number) { return [x, y]; });
    const gens = [repr(function (x: number, y: number) { return [y, x]; }), repr(function (x: number, y: number) { return [y, n - 1 - x]; })];
    const S = new Map<string, number[]>(); S.set(id.join(','), id);
    let grew = true;
    while (grew) {
      grew = false; const cur = Array.from(S.values());
      for (const m of cur) for (const g of gens) { for (const c of [comp(m, g), comp(g, m)]) { const kk = c.join(','); if (!S.has(kk)) { S.set(kk, c); grew = true; } } }
    }
    const res = Array.from(S.values()); mapsCache[n] = res; return res;
  }
  function indicator(cfg: number[], n: number, map: number[] | null): string {
    const arr = new Array(n * n).fill('0');
    for (const c of cfg) arr[map ? map[c] : c] = '1';
    return arr.join('');
  }
  function orbitInfo(cfg: number[], n: number) {
    const maps = d4maps(n); const cfgS = cfg.slice().sort(function (a: number, b: number) { return a - b; });
    const sets = new Set<string>(); const inds: string[] = []; let stab = 0;
    for (const m of maps) {
      const t = cfgS.map(function (c: number) { return m[c]; }).sort(function (a: number, b: number) { return a - b; });
      const key = t.join(',');
      if (!sets.has(key)) { sets.add(key); inds.push(indicator(t, n, null)); }
      if (key === cfgS.join(',')) stab++;
    }
    const ownInd = indicator(cfgS, n, null);
    return { osize: sets.size, stab: stab, lexmin: inds.every(function (x) { return ownInd <= x; }), members: Array.from(sets).map(function (s) { return s.split(',').map(Number); }) };
  }
  function gcd(a: number, b: number): number { a = Math.abs(a); b = Math.abs(b); while (b) { const t = a % b; a = b; b = t; } return a; }
  function tripsDirs(cfg: number[], n: number) {
    const k = cfg.length; const X = cfg.map(function (c: number) { return c % n; }); const Y = cfg.map(function (c: number) { return (c - (c % n)) / n; });
    let trips = 0; const dirs = new Set<string>();
    for (let i = 0; i < k; i++) for (let j = i + 1; j < k; j++) for (let p = j + 1; p < k; p++) {
      const cr = (X[j] - X[i]) * (Y[p] - Y[i]) - (X[p] - X[i]) * (Y[j] - Y[i]);
      if (cr === 0) {
        trips++; let dx = X[j] - X[i], dy = Y[j] - Y[i];
        const g = gcd(dx, dy); dx = dx / g; dy = dy / g;
        if (dx < 0 || (dx === 0 && dy < 0)) { dx = -dx; dy = -dy; }
        dirs.add(dx + ',' + dy);
      }
    }
    return { trips: trips, dirs: dirs.size };
  }

  // ---------- A: forbidden-quad counts F_3..F_8 (published anchors) ----------
  const F: any = {};
  for (let n = 3; n <= 6; n++) F[n] = buildForbid(n).cnt;
  const forbid7res = buildForbid(7); F[7] = forbid7res.cnt;
  const forbid8res = buildForbid(8); F[8] = forbid8res.cnt;
  const forbid7 = forbid7res.set; const forbid8 = forbid8res.set;
  const eF: any = { 3: 14, 4: 194, 5: 826, 6: 2491, 7: 6364, 8: 14564 };
  const fok = [3, 4, 5, 6, 7, 8].every(function (n) { return F[n] === eF[n]; });

  // ---------- B: census 331 leaders (K1226) ----------
  const leaders: number[][] = census.leaders;
  const per = verify.per_leader;
  let allSafe = 0, allMax = 0, lexminCnt = 0, dupCnt = 0, orbTotal = 0;
  const seenOrbits = new Set<string>();
  const oszH: any = {}, stabH: any = {}, triH: any = {}, dirH: any = {};
  const trips0Leaders: number[][] = []; const stab2Leaders: number[][] = [];
  const mism: string[] = [];
  for (let i = 0; i < leaders.length; i++) {
    const L = leaders[i];
    const safe = isSafe(7, L, forbid7);
    const unc = safe ? uncovered(7, L, forbid7) : -1;
    const max = safe && unc === 0;
    const oi = orbitInfo(L, 7);
    const td = tripsDirs(L, 7);
    const orbitKey = oi.members.map(function (m) { return m.join(','); }).sort()[0];
    const dup = seenOrbits.has(orbitKey); seenOrbits.add(orbitKey);
    if (safe) allSafe++; if (max) allMax++; if (oi.lexmin) lexminCnt++; if (dup) dupCnt++;
    orbTotal += oi.osize;
    oszH[oi.osize] = (oszH[oi.osize] || 0) + 1;
    stabH[oi.stab] = (stabH[oi.stab] || 0) + 1;
    triH[td.trips] = (triH[td.trips] || 0) + 1;
    dirH[td.dirs] = (dirH[td.dirs] || 0) + 1;
    if (td.trips === 0) trips0Leaders.push(L);
    if (oi.stab === 2) stab2Leaders.push(L);
    const pl = per[i];
    if (!pl) { mism.push('per_leader[' + i + '] missing'); continue; }
    if (pl.safe !== safe || pl.maximal !== max || pl.nViol !== 0 || pl.nUnc !== 0) mism.push('L' + i + ':safe/max');
    if (pl.osize !== oi.osize || pl.stab !== oi.stab) mism.push('L' + i + ':orbit');
    if (pl.trips !== td.trips || pl.dirs !== td.dirs) mism.push('L' + i + ':trips');
    if (pl.lexmin !== oi.lexmin || pl.dup !== dup) mism.push('L' + i + ':lex/dup');
  }
  const summaryMatch = verify.summary.nLeaders === leaders.length
    && verify.summary.distinct_orbits === leaders.length
    && JSON.stringify(verify.summary.orbit_size_histogram) === JSON.stringify(oszH)
    && JSON.stringify(verify.summary.stabilizer_histogram) === JSON.stringify(stabH)
    && JSON.stringify(verify.summary.trips_histogram) === JSON.stringify(triH)
    && JSON.stringify(verify.summary.dirs_histogram) === JSON.stringify(dirH)
    && verify.summary.config_count_among_verified === orbTotal;

  // ---------- C: n7 k8 witness + tamper (published tamper_k8_summary) ----------
  const W7 = [17, 19, 22, 26, 27, 28, 30, 31];
  const w7safe = isSafe(7, W7, forbid7);
  const w7max = w7safe && uncovered(7, W7, forbid7) === 0;
  const tam7 = W7.map(function (s) { const T = W7.filter(function (x) { return x !== s; }).sort(function (a: number, b: number) { return a - b; }); return { safe: isSafe(7, T, forbid7), unc: uncovered(7, T, forbid7), nviol: nViol(7, T, forbid7) }; });
  const tam7unc = tam7.map(function (x: any) { return x.unc; });
  const tam7pubMatch = JSON.stringify(tam7unc) === JSON.stringify(tamper7pub.uncovered_counts);

  // ---------- D: n8 k9 witnesses + tampers (published tamper_n8k9_summary + determinism trips/dirs) ----------
  const cellOf = function (p: number[], n: number) { return p[0] + n * p[1]; };
  const A = w1.stones.map(function (p: number[]) { return cellOf(p, 8); }).sort(function (a: number, b: number) { return a - b; });
  const B = w2.stones.map(function (p: number[]) { return cellOf(p, 8); }).sort(function (a: number, b: number) { return a - b; });
  const wA = { safe: isSafe(8, A, forbid8), max: isSafe(8, A, forbid8) && uncovered(8, A, forbid8) === 0 };
  const wB = { safe: isSafe(8, B, forbid8), max: isSafe(8, B, forbid8) && uncovered(8, B, forbid8) === 0 };
  const orbA = new Set(d4maps(8).map(function (m: number[]) { return A.map(function (c: number) { return m[c]; }).sort(function (a: number, b: number) { return a - b; }).join(','); }));
  const nonCongr = !orbA.has(B.join(','));
  const tdA = tripsDirs(A, 8); const tdB = tripsDirs(B, 8);
  const tamp1 = tamper8.witness.map(function (st: number[]) {
    const rm = cellOf(st, 8);
    const T = tamper8.witness.map(function (p: number[]) { return cellOf(p, 8); }).filter(function (c: number) { return c !== rm; }).sort(function (a: number, b: number) { return a - b; });
    return { safe: isSafe(8, T, forbid8), unc: uncovered(8, T, forbid8), nviol: nViol(8, T, forbid8) };
  });
  const tamp2 = w2.stones.map(function (st: number[]) {
    const rm = cellOf(st, 8);
    const T = w2.stones.map(function (p: number[]) { return cellOf(p, 8); }).filter(function (c: number) { return c !== rm; }).sort(function (a: number, b: number) { return a - b; });
    return { safe: isSafe(8, T, forbid8), unc: uncovered(8, T, forbid8), nviol: nViol(8, T, forbid8) };
  });
  const und1 = tamp1.map(function (x: any) { return x.unc; });
  const und2 = tamp2.map(function (x: any) { return x.unc; });

  // ---------- E: K1224 catalog (16 configs, 2 orbits) ----------
  const cfgs: number[][] = classify.configs;
  const cfgSet = new Set(cfgs.map(function (c: number[]) { return c.join(','); }));
  const allSafeMax = cfgs.every(function (c: number[]) { return isSafe(7, c, forbid7) && uncovered(7, c, forbid7) === 0; });
  const tH: any = {}; const dH: any = {};
  for (const c of cfgs) { const td = tripsDirs(c, 7); tH[td.trips] = (tH[td.trips] || 0) + 1; dH[td.dirs] = (dH[td.dirs] || 0) + 1; }
  const unassigned = new Set(cfgs.map(function (c: number[]) { return c.join(','); }));
  const orbits: number[][][] = [];
  while (unassigned.size) {
    const k0 = Array.from(unassigned)[0];
    const c0 = k0.split(',').map(Number);
    const mem = orbitInfo(c0, 7).members.map(function (m: number[]) { return m.join(','); });
    orbits.push(mem.map(function (s: string) { return s.split(',').map(Number); }));
    for (const m of mem) unassigned.delete(m);
  }
  const allInList = orbits.every(function (o: number[][]) { return o.every(function (m: number[]) { return cfgSet.has(m.join(',')); }); });
  const pubMembersMatch = orbits.length === 2 && classify.orbit_details.every(function (od: any, ix: number) {
    const mine = orbits[ix].map(function (m: number[]) { return m.join(','); }).sort();
    const pub = od.members.map(function (m: number[]) { return m.join(','); }).sort();
    return JSON.stringify(mine) === JSON.stringify(pub);
  });
  const numLexMin = function (arr: number[][]) { return arr.slice().sort(function (u: number[], v: number[]) { for (let i = 0; i < u.length; i++) { if (u[i] !== v[i]) return u[i] - v[i]; } return 0; })[0]; };
  const reps = orbits.map(function (o: number[][]) { return numLexMin(o); });
  const satReps = orbits.map(function (o: number[][]) { let best: any = null; for (const m of o) { const ind = indicator(m, 7, null); if (!best || ind < best.ind) best = { ind: ind, m: m }; } return numLexMin([best.m]); });

  // ---------- negative control: wrong reflection is caught by the orbit gate ----------
  const cfgN = [1, 9, 22, 23, 27, 44, 45];
  const reflWrong = function (c: number) { const x = c % 7, y = (c - x) / 7; return x + 7 * (7 - y); };
  const wrongImagesInBoard = cfgN.map(reflWrong).every(function (v: number) { return v >= 0 && v < 49; });
  const wrongSets = new Set<string>(); let cur = cfgN.slice();
  for (let t = 0; t < 8; t++) { cur = cur.map(reflWrong); wrongSets.add(cur.slice().sort(function (a: number, b: number) { return a - b; }).join(',')); }
  const correctOrbit = new Set(d4maps(7).map(function (m: number[]) { return cfgN.map(function (c: number) { return m[c]; }).sort(function (a: number, b: number) { return a - b; }).join(','); }));

  return {
    inputBlobs: blobs,
    F: F, FanchorsMatch: fok,
    census: {
      nLeaders: leaders.length, allSafe: allSafe, allMax: allMax, lexmin: lexminCnt, dup: dupCnt,
      oszH: oszH, stabH: stabH, triH: triH, dirH: dirH, orbTotal: orbTotal,
      summaryMatch: summaryMatch, perLeaderMismatches: mism.length, mismSample: mism.slice(0, 5),
      leader0: leaders[0], trips0Leaders: trips0Leaders, stab2Leaders: stab2Leaders,
    },
    n7tamper: { w7safe: w7safe, w7max: w7max, uncovered: tam7unc, allSafeNotMax: tam7.every(function (x: any) { return x.safe && x.nviol === 0 && x.unc > 0; }), publishedMatch: tam7pubMatch },
    n8: {
      wA: wA, wB: wB, nonCongruent: nonCongr,
      tripsDirs: { A: tdA, B: tdB, publishedInDeterminism: { A: { trips: 3, dirs: 2 }, B: { trips: 5, dirs: 4 } } },
      tamper1: { uncovered: und1, publishedMatch: JSON.stringify(und1) === JSON.stringify(tamper8.uncovered_counts), allSafeNotMax: tamp1.every(function (x: any) { return x.safe && x.nviol === 0 && x.unc > 0; }) },
      tamper2: { uncovered: und2, allSafeNotMax: tamp2.every(function (x: any) { return x.safe && x.nviol === 0 && x.unc > 0; }) },
    },
    k1224: {
      nCfg: cfgs.length, allSafeMax: allSafeMax, tripsHist: tH, dirsHist: dH,
      nOrbits: orbits.length, allInList: allInList, pubMembersMatch: pubMembersMatch,
      repsNumlex: reps, satReps: satReps,
      repMatch: reps.length === 2 && JSON.stringify(reps[0]) === JSON.stringify([1, 9, 22, 23, 27, 44, 45]) && JSON.stringify(reps[1]) === JSON.stringify([3, 10, 22, 23, 30, 32, 38]),
      satRepMatch: satReps.length === 2 && JSON.stringify(satReps[0]) === JSON.stringify([10, 13, 14, 17, 19, 21, 45]) && JSON.stringify(satReps[1]) === JSON.stringify([18, 21, 22, 26, 31, 32, 38]),
    },
    negativeControl: {
      wrongMap: 'n8-style reflection c=x+7y mapped to x+7*(7-y) applied to n7 (not a board symmetry)',
      wrongImagesInBoard: wrongImagesInBoard, wrongClosureDistinctSets: wrongSets.size, correctOrbitSize: correctOrbit.size,
    },
  };
}
