// Census-free SAFETY-ONLY checker built on published sat.js primitives
// (circleABC/onCircle/lineABC/onLine). Complements verifyConfig, which also
// requires maximality. Usage: node safety_only.js <q> <stones.json>
// Prints UNSAFE with the offending curve, or SAFE; exit 1 on unsafe.
const S = require("./sat.js");
const fs = require("fs");
const q = parseInt(process.argv[2], 10);
const parsed = JSON.parse(fs.readFileSync(process.argv[3], "utf8"));
const st = (Array.isArray(parsed) ? parsed : parsed.stones).map(p => [p[0], p[1]]);
const N = st.length;
const seenLine = new Set(), seenCirc = new Set();
for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++) {
  const lo = S.lineABC(st[i], st[j]); const lk = lo.join(",");
  if (!seenLine.has(lk)) { seenLine.add(lk);
    let c = 0; for (const [x, y] of st) if (S.onLine(lo, x, y)) c++;
    if (c >= q) { console.log("UNSAFE line " + lk + " count=" + c); process.exit(1); } }
  for (let k = j + 1; k < N; k++) {
    const co = S.circleABC(st[i], st[j], st[k]);
    if (!co) continue;
    const ck = co.join(",");
    if (seenCirc.has(ck)) continue; seenCirc.add(ck);
    let c = 0; for (const [x, y] of st) if (S.onCircle(co, x, y)) c++;
    if (c >= q) { console.log("UNSAFE circle " + ck + " count=" + c); process.exit(1); }
  }
}
console.log("SAFE");
