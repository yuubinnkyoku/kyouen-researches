// 11050円（奇奇実現 (2x-105)^2+(2y-105)^2=11050）の幅w窓センサス。
// 用法: node circle11050_window_census.mjs [wmin wmax]
// 出力: 各幅について34点以上を含む窓の全列挙（窓位置・点数・列パターン）。
// K0791 の窓計数機械と同じ幾何（全48点・24列・行スパン105）の独立再実装。
const R = 11050;
const full = [];
for (let u = -105; u <= 105; u += 2) for (let v = -105; v <= 105; v += 2)
  if (u * u + v * v === R) full.push([(u + 105) / 2, (v + 105) / 2]);
if (full.length !== 48) throw new Error('circle point count != 48');
const wmin = parseInt(process.argv[2] || '83', 10), wmax = parseInt(process.argv[3] || String(wmin), 10);
const out = { circle: '(2x-105)^2+(2y-105)^2=11050', points: full.length, widths: {} };
for (let w = wmin; w <= wmax; w++) {
  const wins = [];
  for (let a = Math.min(...full.map(p => p[0])) - (w - 1); a <= Math.max(...full.map(p => p[0])); a++) {
    const inpts = full.filter(([x]) => x >= a && x <= a + w - 1);
    if (inpts.length >= 34) {
      const cols = [...new Set(inpts.map(p => p[0]))].sort((p, q) => p - q);
      wins.push({ a, n: inpts.length, cols: cols.length, pattern: cols.map(c => c - a) });
    }
  }
  out.widths[w] = { windowsWithAtLeast34: wins.length, windows: wins };
  console.log(JSON.stringify({ w, windowsWithAtLeast34: wins.length }));
  for (const win of wins) console.log('  a=' + win.a + ' n=' + win.n + ' pattern=' + JSON.stringify(win.pattern));
}
if (process.argv[4] === '--json') console.log(JSON.stringify(out));
