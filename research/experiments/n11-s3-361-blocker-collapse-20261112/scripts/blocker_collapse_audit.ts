// Self-contained audit: S3 {59,60,61} blocker collapse via full D4-image matching
// against the K0675 s6 sweep oracle. No network, no manifest: the 94 oracle
// positions are embedded from s5_verdicts.json (first_win_s5 + second_win_s5).
// Anchors asserted: 94 S5 reps of S4 {47,59,60,61}; 7890 raw S6 edges; 3868 S6
// classes; 110 legal S4 children of S3 {59,60,61}; 102 direct W4 closures;
// 8 blockers in 3 V4 classes; per-representative and union accounting.
// Run: Vibe run_typescript harness (async function main auto-invoked).
const FW_HEX = ["00000000000000003800800000000001","00000000000000003800800000000002","00000000000000003800800000000004","00000000000000003800800000000008","00000000000000003800800000000010","00000000000000003800800000000040","00000000000000003800800000000080","00000000000000003800800000000100","00000000000000003800800000000200","00000000000000003800800000000400","00000000000000003800800000000800","00000000000000003800800000001000","00000000000000003800800000004000","00000000000000003800800000010000","00000000000000003800800000040000","00000000000000003800800000080000","00000000000000003800800000200000","00000000000000003800800000400000","00000000000000003800800040000000","00000000000000003800800100000000","00000000000000003800800200000000","00000000000000003800800400000000","00000000000000003800800800000000","00000000000000003800802000000000","00000000000000003800804000000000","00000000000000003800810000000000","00000000000000003800820000000000","00000000000000003800840000000000","00000000000000003800880000000000","00000000000000003800900000000000","00000000000000003800a00000000000","00000000000000003800c00000000000","00000000000000003801800000000000","00000000000000003802800000000000","00000000000000003808100000000000","00000000000000003808200000000000","00000000000000043800800000000000","00000000000000043808000000000000","00000000000000083808000000000000","00000000000000103800800000000000","00000000000000103808000000000000","00000000000000203800000000000001","00000000000000203800000000000002","00000000000000203800000000000004","00000000000000203800000000000008","00000000000000203800000000000010","00000000000000203800000000000040","00000000000000203800000000000080","00000000000000203800000000000100","00000000000000203800000000000200","00000000000000203800000000000400","00000000000000203800000000001000","00000000000000203800000000002000","00000000000000203800000000004000","00000000000000203800000000020000","00000000000000203800000000040000","00000000000000203800000000080000","00000000000000203800000000100000","00000000000000203800000000200000","00000000000000203800000001000000","00000000000000203800000002000000","00000000000000203800000010000000","00000000000000203800000020000000","00000000000000203800000040000000","00000000000000203800000100000000","00000000000000203800000400000000","00000000000000203800001000000000","00000000000000203800002000000000","00000000000000203800004000000000","00000000000000203800008000000000","00000000000000203800010000000000","00000000000000203800040000000000","00000000000000203800080000000000","00000000000000203800800000000000","00000000000000203801000000000000","00000000000000203802000000000000","00000000000000203804000000000000","00000000000000203808000000000000"];
const SW_HEX = ["00000000000000003800800000000020","00000000000000003800800000800000","00000000000000003800800010000000","00000000000000083800800000000000","00000000000000203800000000000020","00000000000000203800000000000800","00000000000000203800000000008000","00000000000000203800000000010000","00000000000000203800000000400000","00000000000000203800000000800000","00000000000000203800000004000000","00000000000000203800000008000000","00000000000000203800000080000000","00000000000000203800000200000000","00000000000000203800000800000000","00000000000000203800020000000000"];
const N = 121, FULL = (1n << 121n) - 1n;
const X = new Int8Array(N), Y = new Int8Array(N), Q = new Int32Array(N);
for (let p = 0; p < N; p++) { X[p] = p % 11; Y[p] = Math.floor(p / 11); Q[p] = X[p]*X[p] + Y[p]*Y[p]; }
const forbMemo = new Map();
function forbidden(a, b, c) {
  const key = (a*121+b)*121+c; let m = forbMemo.get(key); if (m !== undefined) return m;
  m = 0n; const x1=X[a],y1=Y[a],x2=X[b],y2=Y[b],x3=X[c],y3=Y[c];
  const A2 = x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2);
  if (A2 === 0) { const A = y2-y1, Bx = x1-x2;
    for (let z = 0; z < N; z++) if (A*(X[z]-x1)+Bx*(Y[z]-y1) === 0) m |= 1n << BigInt(z);
  } else { const D = 2*A2, Uxn = Q[a]*(y2-y3)+Q[b]*(y3-y1)+Q[c]*(y1-y2),
      Uyn = Q[a]*(x3-x2)+Q[b]*(x1-x3)+Q[c]*(x2-x1), Rx = D*x1-Uxn, Ry = D*y1-Uyn;
    for (let z = 0; z < N; z++) { const dx = D*X[z]-Uxn, dy = D*Y[z]-Uyn;
      if (dx*dx + dy*dy === Rx*Rx + Ry*Ry) m |= 1n << BigInt(z); } }
  m &= ~((1n<<BigInt(a))|(1n<<BigInt(b))|(1n<<BigInt(c))); forbMemo.set(key, m); return m;
}
function legalOf(st) { let banned = 0n;
  for (const s of st) banned |= 1n << BigInt(s);
  for (let i = 0; i < st.length; i++) for (let j = i+1; j < st.length; j++) for (let k = j+1; k < st.length; k++)
    banned |= forbidden(st[i], st[j], st[k]);
  return FULL & ~banned; }
function bitsOf(m) { const o = []; for (let d = 0; d < N; d++) if ((m >> BigInt(d)) & 1n) o.push(d); return o; }
const TX = [(x,y)=>[x,y],(x,y)=>[y,10-x],(x,y)=>[10-x,10-y],(x,y)=>[10-y,x],(x,y)=>[10-x,y],(x,y)=>[x,10-y],(x,y)=>[y,x],(x,y)=>[10-y,10-x]];
function canon(m) { let best = m;
  for (let g = 1; g < 8; g++) { let t = 0n;
    for (const p of bitsOf(m)) { const [nx,ny] = TX[g](p%11, Math.floor(p/11)); t |= 1n << BigInt(ny*11+nx); }
    if (t < best) best = t; } return best; }
function imgs(m) { const out = [];
  for (let g = 0; g < 8; g++) { let t = 0n;
    for (const p of bitsOf(m)) { const [nx,ny] = TX[g](p%11, Math.floor(p/11)); t |= 1n << BigInt(ny*11+nx); }
    out.push(t); } return out; }
function need(cond, msg) { if (!cond) throw new Error('AUDIT FAIL: ' + msg); }
async function main() {
  const FW = FW_HEX.map(h => BigInt('0x'+h)), SW = SW_HEX.map(h => BigInt('0x'+h));
  need(FW.length === 78 && SW.length === 16, 'oracle counts');
  const S4 = BigInt('0x00000000000000003800800000000000');
  const s5reps = [...new Set(bitsOf(legalOf(bitsOf(S4))).map(c => canon(S4 | (1n << BigInt(c)))))];
  need(s5reps.length === 94, 'priority S5 frontier != 94');
  const oracleOrbits = new Set([...FW, ...SW].map(canon));
  for (const k of oracleOrbits) need(s5reps.includes(k), 'oracle orbit not a child of priority S4');
  const judged = new Map(); let rawEdges = 0;
  for (const parent of s5reps) { const st = bitsOf(parent); const leg = legalOf(st);
    rawEdges += bitsOf(leg).length;
    for (const c of bitsOf(leg)) { const s6 = canon(parent | (1n << BigInt(c)));
      if (!judged.has(s6.toString(16))) judged.set(s6.toString(16), bitsOf(legalOf(bitsOf(s6))).length); } }
  need(rawEdges === 7890, 'raw S6 edges != 7890');
  need(judged.size === 3868, 'judged S6 classes != 3868');
  // S3 {59,60,61} frontier
  const TRIPLE = (1n<<59n)|(1n<<60n)|(1n<<61n);
  const legU = bitsOf(legalOf([59,60,61]));
  need(legU.length === 110, 'legal S4 children of S3 != 110');
  const fwSet = new Set(FW.map(p => canon(p).toString(16)));
  const fc = new Set(), swu = new Set();
  for (const o of oracleOrbits) { const isFW = fwSet.has(o.toString(16));
    for (const im of imgs(o)) { if ((im & TRIPLE) === TRIPLE) { const rest = bitsOf(im & ~TRIPLE);
      if (rest.length === 2) { const [u, v] = rest;
        if (legU.includes(u) && legU.includes(v)) { if (isFW) { fc.add(u); fc.add(v); } else { swu.add(u); swu.add(v); } } } } } }
  need(fc.size === 102, 'direct W4 closures != 102');
  const blks = legU.filter(u => !fc.has(u)).sort((a,b)=>a-b);
  need(JSON.stringify(blks) === '[5,23,27,31,89,93,97,115]', 'blocker list mismatch');
  const V4 = (p) => { const x = p%11, y = Math.floor(p/11);
    return [...new Set([[x,y],[10-x,10-y],[10-x,y],[x,10-y]].map(([a,b]) => b*11+a))].sort((a,b)=>a-b); };
  const seen = new Set(); const classes = [];
  for (const u of blks) { if (seen.has(u)) continue; const cl = V4(u).filter(q => blks.includes(q));
    cl.forEach(q => seen.add(q)); classes.push(cl); }
  need(classes.length === 3, 'V4 classes != 3');
  need(JSON.stringify(classes) === '[[5,115],[27,93],[23,31,89,97]]', 'V4 class partition mismatch');
  const reps = [5, 27, 23, 31];
  const per = []; const unionAll = new Set();
  for (const u of reps) { const s4m = TRIPLE | (1n << BigInt(u));
    const s5f = [...new Set(bitsOf(legalOf(bitsOf(s4m))).map(c => canon(s4m | (1n << BigInt(c)))))];
    let oblig = 0; const s6set = new Set();
    for (const p of s5f) { const st = bitsOf(p); const leg = legalOf(st); oblig += bitsOf(leg).length;
      for (const c of bitsOf(leg)) s6set.add(canon(p | (1n << BigInt(c))).toString(16)); }
    let jud = 0, nw = 0, cost = 0;
    for (const k of s6set) { unionAll.add(k);
      if (judged.has(k)) jud++; else { nw++; cost += bitsOf(legalOf(bitsOf(BigInt('0x'+k)))).length; } }
    per.push({ u, s5: s5f.length, oblig, s6all: s6set.size, judged: jud, newS6: nw, newCost: cost }); }
  need(JSON.stringify(per) === JSON.stringify([{u:5,s5:54,oblig:4795,s6all:2191,judged:159,newS6:2032,newCost:159266},{u:27,s5:54,oblig:4698,s6all:2150,judged:77,newS6:2073,newCost:157179},{u:23,s5:100,oblig:9014,s6all:4417,judged:234,newS6:4183,newCost:330227},{u:31,s5:100,oblig:9014,s6all:4417,judged:234,newS6:4183,newCost:330227}]), 'per-representative stats mismatch');
  let uJ = 0, uN = 0, uC = 0;
  for (const k of unionAll) { if (judged.has(k)) uJ++; else { uN++; uC += bitsOf(legalOf(bitsOf(BigInt('0x'+k)))).length; } }
  need(unionAll.size === 8340 && uJ === 460 && uN === 7880 && uC === 616491, 'union accounting mismatch');
  return JSON.stringify({ ok: true, kid_anchor: 'K0766', oracle: { fw: 78, sw: 16 },
    s5: 94, rawEdges: 7890, judgedS6: 3868, legalS4: 110, directW4: fc.size, blockers: blks,
    v4Classes: classes, perRepresentative: per,
    union4: { all: unionAll.size, judged: uJ, newS6: uN, newCost: uC } });
}
