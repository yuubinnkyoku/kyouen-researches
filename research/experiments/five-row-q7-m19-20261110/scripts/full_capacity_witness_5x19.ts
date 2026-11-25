// full_capacity_witness_5x19.ts
// 5x19, q=7 (7 stones on a common circle or line = forbidden).
// (a) regenerate the >=7-point circle census (same-row-pair method:
//     every circle with >=7 points among 5 rows has <=2 pts/row, hence
//     contains a same-row pair; complete enumeration).
// (b) search a safe (6,6,6,6,6) config; maximality is automatic since
//     each empty point's row line already holds 6 stones.
// (c) verify safety with exact integer arithmetic via three paths:
//     A: circles from triples of stones, key = normalized (center, r^2);
//     B: cocircular 4-subset counting (threshold C(7,4)=35);
//     C: max stones on the 95 regenerated census curves + row lines.
// (d) density: fraction of random full-capacity configs that are safe.
// (e) blocker feasibility for the remaining (3/4/5-deficient-row) classes.
// All circle-membership tests use exact integers:
//   (nX - qx*den)^2 + (nY - qy*den)^2 == ref
// A float-division variant of this test was caught reporting an UNSAFE
// candidate as safe (7 stones on the circle centered (11,1)); the
// independent 4-subset path B detected it. Never use floats here.

const W = 19, H = 5;
const pts: number[][] = [];
for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) pts.push([x, y]);
const g0 = (a: number, b: number): number => { a = Math.abs(a); b = Math.abs(b); while (b) { const t = a % b; a = b; b = t; } return a || 1; };
function mulberry32(a: number) {
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const normCenterKey = (x1:number,y1:number,x2:number,y2:number,x3:number,y3:number) => {
  const d = 2*(x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2));
  if (d === 0) return null;
  const A1=x1*x1+y1*y1,A2=x2*x2+y2*y2,A3=x3*x3+y3*y3;
  const numX = A1*(y2-y3)+A2*(y3-y1)+A3*(y1-y2);
  const numY = A1*(x3-x2)+A2*(x1-x3)+A3*(x2-x1);
  let den=d, nX=numX, nY=numY;
  let g = g0(g0(den,nX),nY);
  if (den<0) g=-g;
  den/=g; nX/=g; nY/=g;
  const rdx = nX-x1*den, rdy = nY-y1*den;
  let r2n = rdx*rdx+rdy*rdy, r2d = den*den;
  const g2 = g0(r2n,r2d); r2n/=g2; r2d/=g2;
  return { key: den+'|'+nX+'|'+nY+'|'+r2n+'|'+r2d, den, nX, nY, ref: rdx*rdx+rdy*rdy };
};

// ---- (a) census
const census: number[][][] = [];
{
  const seen = new Set<string>();
  for (let y = 0; y < H; y++) {
    const rowPts = pts.filter(p => p[1] === y);
    for (let i = 0; i < rowPts.length; i++) for (let j = i+1; j < rowPts.length; j++) {
      const p = rowPts[i], q = rowPts[j];
      for (const r of pts) {
        if (r === p || r === q) continue;
        const c = normCenterKey(p[0],p[1],q[0],q[1],r[0],r[1]);
        if (!c || seen.has(c.key)) continue;
        const on: number[][] = [];
        for (const s of pts) {
          const dx = c.nX-s[0]*c.den, dy = c.nY-s[1]*c.den;
          if (dx*dx+dy*dy === c.ref) on.push(s);
        }
        if (on.length >= 7) { seen.add(c.key); census.push(on); }
      }
    }
  }
}
const censusBySize: Record<string, number> = {};
for (const c of census) censusBySize[c.length] = (censusBySize[c.length]||0)+1;
const rowDist: Record<string, number> = {};
for (const c of census) {
  const counts = [0,0,0,0,0];
  c.forEach(p => counts[p[1]]++);
  rowDist[counts.join('')] = (rowDist[counts.join('')]||0)+1;
}

// ---- safety checks
function safePathA(stones: number[][]): number {
  // exact: circles from stone triples; returns worst circle stone count
  // (7 if a line reaches 7 stones)
  const n = stones.length;
  const circles = new Map<string, { den:number; nX:number; nY:number; ref:number }>();
  for (let i = 0; i < n; i++) for (let j = i+1; j < n; j++) for (let k = j+1; k < n; k++) {
    const c = normCenterKey(stones[i][0],stones[i][1],stones[j][0],stones[j][1],stones[k][0],stones[k][1]);
    if (!c || circles.has(c.key)) continue;
    circles.set(c.key, { den: c.den, nX: c.nX, nY: c.nY, ref: c.ref });
  }
  let worst = 0;
  for (const cc of circles.values()) {
    let cnt = 0;
    for (const s of stones) {
      if ((cc.nX-s[0]*cc.den)**2 + (cc.nY-s[1]*cc.den)**2 === cc.ref) cnt++;
    }
    if (cnt > worst) worst = cnt;
  }
  const lineCnt = new Map<string, number>();
  for (let i = 0; i < n; i++) for (let j = i+1; j < n; j++) for (let k = j+1; k < n; k++) {
    const [x1,y1]=stones[i],[x2,y2]=stones[j],[x3,y3]=stones[k];
    if ((x2-x1)*(y3-y1)-(x3-x1)*(y2-y1) !== 0) continue;
    let A=y2-y1,B=x1-x2,C=A*x1+B*y1;
    const g=g0(g0(A,B),C); A/=g;B/=g;C/=g;
    if (A<0||(A===0&&B<0)){A=-A;B=-B;C=-C;}
    const key=A+','+B+','+C;
    const v=(lineCnt.get(key)||0)+1;
    if (v>=35) return 7; // C(7,3)=35 triples on a line => 7 collinear
    lineCnt.set(key,v);
  }
  return worst;
}
function safePathB(stones: number[][]): number {
  // independent: cocircular 4-subset counting; returns max quads per circle
  // (>= C(7,4)=35 means a 7-stone circle)
  const n = stones.length;
  const quadCnt = new Map<string, number>();
  let maxQ = 0;
  for (let a=0;a<n;a++) for (let b=a+1;b<n;b++) for (let c2=b+1;c2<n;c2++) for (let d2=c2+1;d2<n;d2++) {
    const P=[stones[a],stones[b],stones[c2],stones[d2]];
    const M=P.map(([x,y])=>[x,y,x*x+y*y,1]);
    let D=0;
    for (let r0=0;r0<4;r0++){
      const sub:number[][]=[];
      for (let r=0;r<4;r++) if(r!==r0) sub.push([M[r][0],M[r][1],M[r][2]]);
      const d3=(s:number[][])=>s[0][0]*(s[1][1]*s[2][2]-s[1][2]*s[2][1])-s[0][1]*(s[1][0]*s[2][2]-s[1][2]*s[2][0])+s[0][2]*(s[1][0]*s[2][1]-s[1][1]*s[2][0]);
      D += ((r0%2===0)?1:-1)*d3(sub);
    }
    if (D!==0) continue;
    let done=false;
    for (let t1=0;t1<4&&!done;t1++) for (let t2=t1+1;t2<4&&!done;t2++) for (let t3=t2+1;t3<4&&!done;t3++) {
      const [x1,y1]=P[t1],[x2,y2]=P[t2],[x3,y3]=P[t3];
      if ((x2-x1)*(y3-y1)-(x3-x1)*(y2-y1)===0) continue;
      const c = normCenterKey(x1,y1,x2,y2,x3,y3);
      if (!c) continue;
      const v=(quadCnt.get(c.key)||0)+1;
      if(v>maxQ)maxQ=v;
      quadCnt.set(c.key,v);
      done=true;
    }
  }
  return maxQ;
}
const rowsToStones = (rows: number[][]) => {
  const st: number[][] = [];
  rows.forEach((r,y)=>r.forEach(x=>st.push([x,y])));
  return st;
};

// ---- (b) search
let witnessRows: number[][] | null = null;
let searchAttempts = 0;
{
  const rand = mulberry32(0x5F1919);
  for (let att = 1; att <= 100 && !witnessRows; att++) {
    searchAttempts = att;
    const rows: number[][] = [];
    for (let y = 0; y < H; y++) {
      const xs = Array.from({length: W}, (_, i) => i);
      for (let i = W-1; i > 0; i--) { const j = Math.floor(rand()*(i+1)); const t = xs[i]; xs[i]=xs[j]; xs[j]=t; }
      rows.push(xs.slice(0,6).sort((a,b)=>a-b));
    }
    if (safePathA(rowsToStones(rows)) <= 6) witnessRows = rows;
  }
}

// ---- (c) verification of witness
const stones = rowsToStones(witnessRows!);
const worstA = safePathA(stones);
const maxQuadsB = safePathB(stones);
let worstCensus = 0;
for (const c of census) {
  let cnt = 0;
  for (const s of stones) if (c.some(q => q[0]===s[0] && q[1]===s[1])) cnt++;
  if (cnt > worstCensus) worstCensus = cnt;
}
const rowCounts = witnessRows!.map(r => r.length);
const maximality = rowCounts.every(c => c === 6); // every empty point: row line would reach 7

// ---- (d) density
let densitySafe = 0; const DN = 200;
{
  const rand = mulberry32(0xC0FFEE);
  for (let t = 0; t < DN; t++) {
    const rows: number[][] = [];
    for (let y = 0; y < H; y++) {
      const xs = Array.from({length: W}, (_, i) => i);
      for (let i = W-1; i > 0; i--) { const j = Math.floor(rand()*(i+1)); const tt = xs[i]; xs[i]=xs[j]; xs[j]=tt; }
      rows.push(xs.slice(0,6).sort((a,b)=>a-b));
    }
    if (safePathA(rowsToStones(rows)) <= 6) densitySafe++;
  }
}

// ---- (e) remaining-class blocker feasibility
function classStats(D: number[]) {
  const F = [0,1,2,3,4].filter(y => !D.includes(y));
  let noBlocker = 0, needOtherDef = 0, total = 0, minThrough = Infinity;
  for (const p of pts) {
    if (!D.includes(p[1])) continue;
    total++;
    let capThrough = 0, fullOnlyThrough = 0, through = 0;
    for (const c of census) {
      if (!c.some(s => s[0]===p[0] && s[1]===p[1])) continue;
      through++;
      const rho = [0,0,0,0,0];
      c.forEach(s => rho[s[1]]++);
      const cap = (y: number) => D.includes(y) ? 5 : 6;
      let m = 0;
      for (let y = 0; y < 5; y++) m += Math.min(rho[y], cap(y));
      m -= 1; // p itself empty
      if (m >= 6) capThrough++;
      let m2 = 0;
      for (const y of F) m2 += Math.min(rho[y], cap(y));
      m2 += Math.min(rho[p[1]], cap(p[1])) - 1; // own-row second point
      if (m2 >= 6) fullOnlyThrough++;
    }
    if (through < minThrough) minThrough = through;
    if (capThrough === 0) noBlocker++;
    if (fullOnlyThrough === 0) needOtherDef++;
  }
  return { deficient_rows: D, points_in_deficient_rows: total,
    points_with_no_potential_blocker: noBlocker,
    points_whose_blockers_require_other_deficient_row_stones: needOtherDef,
    min_census_circles_through_a_point: minThrough };
}
const classes = [
  [0,1,2],[0,1,3],[0,1,4],[0,2,3],[0,2,4],[1,2,3],
  [0,1,2,3],[0,1,2,4],[0,1,3,4],
  [0,1,2,3,4]
].map(classStats);

const result = {
  board: "5x19", rule: "q=7 (7 stones on a common circle or line forbidden)",
  witness: {
    rows: witnessRows,
    stone_count: 30,
    row_occupancy: "(6,6,6,6,6) full capacity",
    safety_pathA_worst_circle_stones: worstA,
    safety_pathB_max_cocircular_quads: maxQuadsB,
    safety_pathB_threshold_C74: 35,
    safety_pathC_worst_census_curve_stones: worstCensus,
    row_lines_stone_counts: rowCounts,
    maximality: maximality,
    maximality_argument: "every empty point lies on a row line that already holds exactly 6 stones; adding it makes 7 collinear on that line",
    search_seed: "0x5F1919", search_attempts: searchAttempts
  },
  density_random_full_capacity: { samples: DN, safe: densitySafe, fraction: densitySafe / DN },
  census_regenerated: { circles_ge7: census.length, by_size: censusBySize, row_distributions: rowDist,
    method: "same-row-pair enumeration (pigeonhole: >=7 points over 5 rows with <=2/row forces a same-row pair)",
    matches_K0726: census.length === 95 && censusBySize['7'] === 8 && censusBySize['8'] === 87 },
  remaining_deficient_classes: classes
};
console.log(JSON.stringify(result, null, 1));
