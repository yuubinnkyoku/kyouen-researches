#!/usr/bin/env node
// gen_n9_cnf.mjs - 9x9 K_9 upper-bound SAT campaign generator (2026-11-15).
// Reproduces:
//  (1) F_n census for n=7,8,9 via two independent implementations
//      (system A: difference-triangle linear forms; system B: normalized curve catalog)
//  (2) third-system verification of the 18-stone witness W9 (census violations,
//      direct 4x4 integer determinants over all C(18,4) subsets, addcost maximality,
//      D4 orbit, row counts, point degrees)
//  (3) at-least-K sequential-counter CNF for K=18 (positive control: W9 satisfies
//      with zero violated clauses) and K=19 (expected UNSAT, pending kissat; a SAT
//      model would refute the external upper bound 18 and give K_9 >= 19).
// All checks are asserted; the script prints ALL CHECKS PASSED on success.
// Deterministic: no randomness, no timestamps; output is byte-identical per run.
//
// Usage: node gen_n9_cnf.mjs [outdir]   (default: ../output relative to this file)
// Writes: n9_census_cnf_20261115.json, n9_ge18.cnf, n9_ge19.cnf
// Next step (bash/kissat lane): node scripts/gen_n9_cnf.mjs && kissat <outdir>/n9_ge19.cnf

import { writeFileSync, mkdirSync } from "node:fs";
import { join, dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

function gcd2(a, b) {
    a = Math.abs(a);
    b = Math.abs(b);
    while(b){
      const t = a % b;
      a = b;
      b = t;
    }
    return a || 1;
  }

function det3(m) {
    return m[0] * (m[4] * m[8] - m[5] * m[7]) - m[1] * (m[3] * m[8] - m[5] * m[6]) + m[2] * (m[3] * m[7] - m[4] * m[6]);
  }

function C4(s) {
    return s < 4 ? 0 : s * (s - 1) * (s - 2) * (s - 3) / 24;
  }

function buildBoard(n) {
    const N = n * n;
    const px = new Uint8Array(N), py = new Uint8Array(N), pw = new Uint16Array(N);
    for(let p = 0; p < N; p++){
      const x = p % n, y = p / n | 0;
      px[p] = x;
      py[p] = y;
      pw[p] = x * x + y * y;
    }
    return {
      n,
      N,
      px,
      py,
      pw
    };
  }

function censusA(n) {
    const bd = buildBoard(n);
    const N = bd.N, px = bd.px, py = bd.py, pw = bd.pw;
    const qa = [], qb = [], qc = [], qd = [], kind = [];
    for(let a = 0; a < N - 3; a++){
      const wa = pw[a], xa = px[a], ya = py[a];
      for(let b = a + 1; b < N - 2; b++){
        const bw = pw[b] - wa, bx = px[b] - xa, by = py[b] - ya;
        for(let c = b + 1; c < N - 1; c++){
          const cw = pw[c] - wa, cx = px[c] - xa, cy = py[c] - ya;
          const c1 = bx * cy - by * cx, c2 = by * cw - bw * cy, c3 = bw * cx - bx * cw;
          const cross = bx * cy - by * cx;
          for(let d = c + 1; d < N; d++){
            if (c1 * (pw[d] - wa) + c2 * (px[d] - xa) + c3 * (py[d] - ya) === 0) {
              qa.push(a);
              qb.push(b);
              qc.push(c);
              qd.push(d);
              kind.push(cross === 0 ? 1 : 2);
            }
          }
        }
      }
    }
    let lines = 0, circles = 0;
    for (const k of kind){
      if (k === 1) lines++;
      else circles++;
    }
    return {
      n,
      N,
      qa,
      qb,
      qc,
      qd,
      F: qa.length,
      collinearQuads: lines,
      cocircularQuads: circles
    };
  }

function censusB(n) {
    const bd = buildBoard(n);
    const N = bd.N, px = bd.px, py = bd.py, pw = bd.pw;
    const lineCnt = new Map(), circCnt = new Map();
    for(let a = 0; a < N - 2; a++){
      for(let b = a + 1; b < N - 1; b++){
        const dx1 = px[b] - px[a], dy1 = py[b] - py[a];
        for(let c = b + 1; c < N; c++){
          const dx2 = px[c] - px[a], dy2 = py[c] - py[a];
          if (dx1 * dy2 - dy1 * dx2 === 0) {
            let A = dy1, B = -dx1, C = -(A * px[a] + B * py[a]);
            const g = gcd2(gcd2(A, B), C);
            A /= g;
            B /= g;
            C /= g;
            if (A < 0 || A === 0 && B < 0) {
              A = -A;
              B = -B;
              C = -C;
            }
            const key = A + "," + B + "," + C;
            lineCnt.set(key, (lineCnt.get(key) || 0) + 1);
          } else {
            const D = det3([
              px[a],
              py[a],
              1,
              px[b],
              py[b],
              1,
              px[c],
              py[c],
              1
            ]);
            const Nu = det3([
              -pw[a],
              py[a],
              1,
              -pw[b],
              py[b],
              1,
              -pw[c],
              py[c],
              1
            ]);
            const Nv = det3([
              px[a],
              -pw[a],
              1,
              px[b],
              -pw[b],
              1,
              px[c],
              -pw[c],
              1
            ]);
            const Nt = det3([
              px[a],
              py[a],
              -pw[a],
              px[b],
              py[b],
              -pw[b],
              px[c],
              py[c],
              -pw[c]
            ]);
            let c1 = D, c2 = Nu, c3 = Nv, c4 = Nt;
            const g = gcd2(gcd2(gcd2(c1, c2), c3), c4);
            c1 /= g;
            c2 /= g;
            c3 /= g;
            c4 /= g;
            if (c1 < 0) {
              c1 = -c1;
              c2 = -c2;
              c3 = -c3;
              c4 = -c4;
            }
            const key = c1 + "," + c2 + "," + c3 + "," + c4;
            circCnt.set(key, (circCnt.get(key) || 0) + 1);
          }
        }
      }
    }
    const lineBySize = {}, circBySize = {};
    let lineTotal = 0, circTotal = 0, lineQuads = 0, circQuads = 0;
    for (const [key, cnt] of lineCnt){
      if (cnt < 4) continue;
      const t = key.split(",");
      const A = +t[0], B = +t[1], C = +t[2];
      let s = 0;
      for(let p = 0; p < N; p++)if (A * px[p] + B * py[p] + C === 0) s++;
      lineBySize[s] = (lineBySize[s] || 0) + 1;
      lineTotal++;
      lineQuads += C4(s);
    }
    for (const [key, cnt] of circCnt){
      if (cnt < 4) continue;
      const t = key.split(",");
      const c1 = +t[0], c2 = +t[1], c3 = +t[2], c4 = +t[3];
      let s = 0;
      for(let p = 0; p < N; p++)if (c1 * pw[p] + c2 * px[p] + c3 * py[p] + c4 === 0) s++;
      circBySize[s] = (circBySize[s] || 0) + 1;
      circTotal++;
      circQuads += C4(s);
    }
    return {
      F: lineQuads + circQuads,
      collinearQuads: lineQuads,
      cocircularQuads: circQuads,
      lineCatalog: {
        total: lineTotal,
        bySize: lineBySize
      },
      circleCatalog: {
        total: circTotal,
        bySize: circBySize
      }
    };
  }

function verifyW9(A9) {
    const bd = buildBoard(A9.n);
    const N = bd.N, px = bd.px, py = bd.py, pw = bd.pw;
    const occ = new Uint8Array(N);
    for (const p of W9CELLS)occ[p] = 1;
    let E = 0;
    for(let i = 0; i < A9.qa.length; i++)if (occ[A9.qa[i]] && occ[A9.qb[i]] && occ[A9.qc[i]] && occ[A9.qd[i]]) E++;
    let detZero = 0, checked = 0;
    const m = W9CELLS.length;
    for(let i = 0; i < m - 3; i++)for(let j = i + 1; j < m - 2; j++)for(let k = j + 1; k < m - 1; k++)for(let l = k + 1; l < m; l++){
      const a = W9CELLS[i];
      const d = det3([
        px[W9CELLS[j]] - px[a],
        py[W9CELLS[j]] - py[a],
        pw[W9CELLS[j]] - pw[a],
        px[W9CELLS[k]] - px[a],
        py[W9CELLS[k]] - py[a],
        pw[W9CELLS[k]] - pw[a],
        px[W9CELLS[l]] - px[a],
        py[W9CELLS[l]] - py[a],
        pw[W9CELLS[l]] - pw[a]
      ]);
      checked++;
      if (d === 0) detZero++;
    }
    const addcost = {};
    let addMin = 1e9;
    for(let e = 0; e < N; e++){
      if (occ[e]) continue;
      let c = 0;
      for(let i = 0; i < A9.qa.length; i++){
        const s = occ[A9.qa[i]] + occ[A9.qb[i]] + occ[A9.qc[i]] + occ[A9.qd[i]];
        if (s === 3 && (e === A9.qa[i] || e === A9.qb[i] || e === A9.qc[i] || e === A9.qd[i])) c++;
      }
      addcost[c] = (addcost[c] || 0) + 1;
      if (c < addMin) addMin = c;
    }
    const n = A9.n;
    const tf = [
      [
        1,
        0,
        0,
        0,
        1,
        0
      ],
      [
        0,
        -1,
        n - 1,
        1,
        0,
        0
      ],
      [
        -1,
        0,
        n - 1,
        0,
        -1,
        n - 1
      ],
      [
        0,
        1,
        0,
        -1,
        0,
        n - 1
      ],
      [
        1,
        0,
        0,
        0,
        -1,
        n - 1
      ],
      [
        -1,
        0,
        n - 1,
        0,
        1,
        0
      ],
      [
        0,
        1,
        0,
        1,
        0,
        0
      ],
      [
        0,
        -1,
        n - 1,
        -1,
        0,
        n - 1
      ]
    ];
    const imgs = new Set();
    for (const f of tf){
      const s = W9CELLS.map((p)=>{
        const x = p % n, y = p / n | 0;
        return (f[0] * x + f[1] * y + f[2]) * n + (f[3] * x + f[4] * y + f[5]);
      }).sort((p, q)=>p - q).join(",");
      imgs.add(s);
    }
    const rowCount = [];
    for(let y = 0; y < n; y++){
      let c = 0;
      for(let x = 0; x < n; x++)if (occ[y * n + x]) c++;
      rowCount.push(c);
    }
    const deg = new Int32Array(N);
    for(let i = 0; i < A9.qa.length; i++){
      deg[A9.qa[i]]++;
      deg[A9.qb[i]]++;
      deg[A9.qc[i]]++;
      deg[A9.qd[i]]++;
    }
    let dmin = 1e9, dmax = -1, dsum = 0;
    const dminCells = [], dmaxCells = [];
    for(let p = 0; p < N; p++){
      dsum += deg[p];
      if (deg[p] < dmin) {
        dmin = deg[p];
        dminCells.length = 0;
        dminCells.push(p);
      } else if (deg[p] === dmin) dminCells.push(p);
      if (deg[p] > dmax) {
        dmax = deg[p];
        dmaxCells.length = 0;
        dmaxCells.push(p);
      } else if (deg[p] === dmax) dmaxCells.push(p);
    }
    return {
      cells: W9CELLS,
      censusViolations: E,
      det4x4Zero: detZero,
      det4x4Checked: checked,
      addcostHistogram: addcost,
      addcostMin: addMin,
      d4OrbitSize: imgs.size,
      rowCount,
      degreeMin: dmin,
      degreeMax: dmax,
      degreeSum: dsum,
      degreeMinCells: dminCells,
      degreeMaxCells: dmaxCells
    };
  }

function fnv1a64(s) {
    let h = 0xcbf29ce484222325n;
    for(let i = 0; i < s.length; i++){
      h ^= BigInt(s.charCodeAt(i));
      h = BigInt.asUintN(64, h * 0x100000001b3n);
    }
    return h.toString(16).padStart(16, "0");
  }

function genCNF(A9, K, w9Cells) {
    const N = A9.N;
    const cum = [
      0
    ];
    for(let i = 1; i <= N; i++)cum[i] = cum[i - 1] + Math.min(i, K);
    const nVars = N + cum[N];
    const auxId = (i, j)=>N + cum[i - 1] + j;
    const clauses = [];
    for(let i = 1; i <= N; i++){
      for(let j = 1; j <= Math.min(i, K); j++){
        const A = auxId(i, j);
        const B = j <= i - 1 ? auxId(i - 1, j) : 0;
        const C = j >= 2 ? auxId(i - 1, j - 1) : 0;
        const c1 = [
          -A
        ];
        if (B) c1.push(B);
        c1.push(i);
        clauses.push(c1);
        if (j >= 2) {
          const c2 = [
            -A
          ];
          if (B) c2.push(B);
          c2.push(C);
          clauses.push(c2);
        }
        if (B) clauses.push([
          -B,
          A
        ]);
        if (j >= 2) clauses.push([
          -i,
          -C,
          A
        ]);
        else clauses.push([
          -i,
          A
        ]);
      }
    }
    for(let i = 0; i < A9.qa.length; i++)clauses.push([
      -(A9.qa[i] + 1),
      -(A9.qb[i] + 1),
      -(A9.qc[i] + 1),
      -(A9.qd[i] + 1)
    ]);
    const unit = auxId(N, K);
    clauses.push([
      unit
    ]);
    const nClauses = clauses.length;
    let text = "p cnf " + nVars + " " + nClauses + "\n";
    for (const cl of clauses)text += cl.join(" ") + " 0\n";
    const assign = new Uint8Array(nVars + 1);
    const occ = new Uint8Array(N);
    for (const p of w9Cells)occ[p] = 1;
    let pref = 0;
    for(let i = 1; i <= N; i++){
      assign[i] = occ[i - 1];
      if (occ[i - 1]) pref++;
      for(let j = 1; j <= Math.min(i, K); j++)assign[auxId(i, j)] = pref >= j ? 1 : 0;
    }
    let viol = 0, unitViolated = false;
    for (const cl of clauses){
      let sat = false;
      for (const lit of cl){
        const v = lit > 0 ? assign[lit] : 1 - assign[-lit];
        if (v) {
          sat = true;
          break;
        }
      }
      if (!sat) {
        viol++;
        if (cl.length === 1 && cl[0] === unit) unitViolated = true;
      }
    }
    return {
      text,
      nVars,
      nClauses,
      bytes: text.length,
      fnv1a64: fnv1a64(text),
      w9Violated: viol,
      w9UnitViolated: unitViolated
    };
  }

function buildReport(A7, B7, A8, B8, A9, B9, w9, g18, g19) {
    return {
      schema: "n9-census-cnf-1",
      date: "2026-11-15",
      board: "9x9",
      generator: "scripts/gen_n9_cnf.mjs",
      boards: {
        "7": {
          F: A7.F,
          collinearQuads: A7.collinearQuads,
          cocircularQuads: A7.cocircularQuads,
          systemsAgree: true,
          lineCatalog: B7.lineCatalog,
          circleCatalog: B7.circleCatalog
        },
        "8": {
          F: A8.F,
          collinearQuads: A8.collinearQuads,
          cocircularQuads: A8.cocircularQuads,
          systemsAgree: true,
          lineCatalog: B8.lineCatalog,
          circleCatalog: B8.circleCatalog
        },
        "9": {
          F: A9.F,
          collinearQuads: A9.collinearQuads,
          cocircularQuads: A9.cocircularQuads,
          systemsAgree: true,
          lineCatalog: B9.lineCatalog,
          circleCatalog: B9.circleCatalog
        }
      },
      w9: w9,
      cnf: {
        encoding: "cell var p+1 (1..81); sequential at-least-K counter, aux id = 81 + cum[i-1] + j with cum[i] = sum_{i'<=i} min(i',K); a[i][j] <-> a[i-1][j] OR (x_i AND a[i-1][j-1]) with a[i-1][j]=FALSE for j>i-1 and a[i-1][j-1]=TRUE for j=1; four clause types per (i,j) with TRUE/FALSE constants substituted; forbidden-quad clauses -(a+1) -(b+1) -(c+1) -(d+1); unit a[81][K]",
        ge18: {
          nVars: g18.nVars,
          nClauses: g18.nClauses,
          bytes: g18.bytes,
          fnv1a64: g18.fnv1a64,
          w9SatisfiesWithZeroViolations: true
        },
        ge19: {
          nVars: g19.nVars,
          nClauses: g19.nClauses,
          bytes: g19.bytes,
          fnv1a64: g19.fnv1a64,
          w9ViolatedClauses: g19.w9Violated,
          w9ViolationIsUnitOnly: g19.w9UnitViolated,
          expectation: "UNSAT would prove K_9 <= 18 in-repo; a SAT model decodes to a 19-stone configuration refuting the external upper bound"
        }
      }
    };
  }

function computeAll() {
    const A7 = censusA(7), B7 = censusB(7), A8 = censusA(8), B8 = censusB(8), A9 = censusA(9), B9 = censusB(9);
    const ok = (cond, msg)=>{
      if (!cond) throw new Error("CHECK FAIL: " + msg);
    };
    ok(A7.F === 6364 && B7.F === 6364, "F7");
    ok(A8.F === 14564 && B8.F === 14564, "F8");
    ok(A9.F === 29152 && B9.F === 29152, "F9");
    ok(A7.collinearQuads === B7.collinearQuads && A7.cocircularQuads === B7.cocircularQuads, "split7 agree");
    ok(A8.collinearQuads === B8.collinearQuads && A8.cocircularQuads === B8.cocircularQuads, "split8 agree");
    ok(A9.collinearQuads === B9.collinearQuads && A9.cocircularQuads === B9.cocircularQuads, "split9 agree");
    ok(A9.collinearQuads === 3156 && A9.cocircularQuads === 25996, "split9 values");
    ok(JSON.stringify(B9.lineCatalog) === JSON.stringify({
      total: 92,
      bySize: {
        4: 36,
        5: 24,
        6: 4,
        7: 4,
        8: 4,
        9: 20
      }
    }), "line catalog");
    ok(JSON.stringify(B9.circleCatalog) === JSON.stringify({
      total: 6722,
      bySize: {
        4: 5996,
        5: 248,
        6: 316,
        7: 4,
        8: 146,
        10: 8,
        12: 4
      }
    }), "circle catalog");
    const w9 = verifyW9(A9);
    ok(w9.censusViolations === 0, "w9 E");
    ok(w9.det4x4Zero === 0 && w9.det4x4Checked === 3060, "w9 det");
    ok(w9.addcostMin === 3, "w9 addmin");
    ok(JSON.stringify(w9.addcostHistogram) === JSON.stringify({
      3: 1,
      4: 3,
      5: 7,
      6: 6,
      7: 9,
      8: 11,
      9: 7,
      10: 9,
      11: 6,
      12: 2,
      13: 1,
      14: 1
    }), "w9 addcost hist");
    ok(w9.d4OrbitSize === 8, "w9 d4");
    ok(JSON.stringify(w9.rowCount) === "[3,2,2,1,1,3,2,1,3]", "w9 rows");
    ok(w9.degreeMin === 978 && w9.degreeMax === 1728 && w9.degreeSum === 116608, "w9 degrees");
    ok(JSON.stringify(w9.degreeMinCells) === "[0,8,72,80]" && JSON.stringify(w9.degreeMaxCells) === "[40]", "w9 deg cells");
    const g18 = genCNF(A9, 18, W9CELLS);
    const g19 = genCNF(A9, 19, W9CELLS);
    ok(g18.nVars === 1386 && g18.nClauses === 34274, "cnf18 meta");
    ok(g19.nVars === 1449 && g19.nClauses === 34525, "cnf19 meta");
    ok(g18.bytes === 586502 && g19.bytes === 590502, "cnf bytes");
    ok(g18.w9Violated === 0 && g18.w9UnitViolated === false, "cnf18 w9 control");
    ok(g19.w9Violated === 1 && g19.w9UnitViolated, "cnf19 w9 negative control");
    const report = buildReport(A7, B7, A8, B8, A9, B9, w9, g18, g19);
    return {
      report,
      ge18Text: g18.text,
      ge19Text: g19.text
    };
  }

const W9CELLS = [5,6,8,9,11,18,24,31,44,47,50,52,54,55,70,73,75,79];


// ---- main ----
const res = computeAll();
const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.argv[2] ? resolve(process.argv[2]) : join(here, "..", "output");
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, "n9_ge18.cnf"), res.ge18Text);
writeFileSync(join(outDir, "n9_ge19.cnf"), res.ge19Text);
writeFileSync(join(outDir, "n9_census_cnf_20261115.json"), JSON.stringify(res.report, null, 2) + "\n");
const b9 = res.report.boards["9"];
console.log("census F9=" + b9.F + " (collinear " + b9.collinearQuads + ", cocircular " + b9.cocircularQuads + ")");
console.log("W9: violations=" + res.report.w9.censusViolations + ", det4x4 zero=" + res.report.w9.det4x4Zero + "/" + res.report.w9.det4x4Checked + ", addcostMin=" + res.report.w9.addcostMin);
console.log("ge18: " + res.report.cnf.ge18.nVars + " vars, " + res.report.cnf.ge18.nClauses + " clauses, FNV-1a-64 " + res.report.cnf.ge18.fnv1a64 + ", W9 satisfies (control)");
console.log("ge19: " + res.report.cnf.ge19.nVars + " vars, " + res.report.cnf.ge19.nClauses + " clauses, FNV-1a-64 " + res.report.cnf.ge19.fnv1a64);
console.log("next: kissat n9_ge19.cnf  (UNSAT => K_9 <= 18 in-repo; SAT => decode + verify a 19-stone witness)");
console.log("ALL CHECKS PASSED");
