// PG(2,7) s=3 full spectrum pipeline (declared in research/log/2026-11-27-pg2q7-s3-twocone-spectrum-declaration.md)
// Phase A: cone enumeration to per-layer binary files. Phase B: per-layer radix sort + bottom-up mex DP.
'use strict';
const fs = require('fs');
const path = require('path');
const [,, modeArg, coneArg, fsetArg, dirArg, qArg, sArg] = process.argv;
const q = parseInt(qArg || '7'), s = parseInt(sArg || '3'), n = q * q + q + 1;
const mode = modeArg;                 // 'enum' or 'dp'
const cone = coneArg;                  // 'nc' (non-collinear F) or 'c' (collinear F)
const fset = parseInt(fsetArg || '0');
const dir = dirArg || `/tmp/cone_${cone}_${fset}`;

// ---- board (same construction as two_cone.js; verified by checks below) ----
const pts = [];
for (let y = 0; y < q; y++) for (let x = 0; x < q; x++) pts.push([x, y, 1]);
for (let m = 0; m < q; m++) pts.push([1, m, 0]);
pts.push([0, 1, 0]);
if (pts.length !== n) throw new Error('points');
const lines = []; const keys = new Set();
for (let a = 0; a < q; a++) for (let b = 0; b < q; b++) for (let c = 0; c < q; c++) {
  if (!a && !b && !c) continue;
  const fn = a ? 0 : (b ? 1 : 2);
  const lead = fn === 0 ? a : (fn === 1 ? b : c);
  let inv = -1; for (let t = 0; t < q; t++) if ((lead * t) % q === 1) { inv = t; break; }
  const na = (a * inv) % q, nb = (b * inv) % q, nc = (c * inv) % q;
  const key = na + ',' + nb + ',' + nc;
  if (keys.has(key)) continue; keys.add(key);
  let lo = 0, hi = 0;
  for (let i = 0; i < n; i++) {
    const d = (na * pts[i][0] + nb * pts[i][1] + nc * pts[i][2]) % q;
    if (d === 0) { if (i < 32) lo |= 1 << i; else hi |= 1 << (i - 32); }
  }
  lines.push([lo, hi]);
}
const nlines = lines.length; if (nlines !== q * q + q + 1) throw new Error("lines");
for (const [lo, hi] of lines) { let c = 0; for (let i = 0; i < n; i++) c += (i < 32 ? (lo >>> i) & 1 : (hi >>> (i - 32)) & 1); if (c !== q + 1) throw new Error("line size"); }
for (let i = 0; i < n; i++) { const cnt = lines.filter(([lo, hi]) => (i < 32 ? (lo >>> i) & 1 : (hi >>> (i - 32)) & 1)).length; if (cnt !== q + 1) throw new Error("lines/pt"); }
// flat typed arrays for hot loops
const lineLo = new Int32Array(nlines), lineHi = new Int32Array(nlines);
lines.forEach(([lo, hi], i) => { lineLo[i] = lo | 0; lineHi[i] = hi | 0; });
const PLINES = q + 1;
const ptLines = new Int32Array(n * PLINES);
{ const tmp = Array.from({ length: n }, () => []);
  lines.forEach(([lo, hi], li) => { for (let i = 0; i < n; i++) { const b = i < 32 ? (lo >>> i) & 1 : (hi >>> (i - 32)) & 1; if (b) tmp[i].push(li); } });
  for (let i = 0; i < n; i++) { if (tmp[i].length !== q + 1) throw new Error("ptlines"); for (let k = 0; k < PLINES; k++) ptLines[i * PLINES + k] = tmp[i][k]; } }
const pc16 = new Uint8Array(65536);
for (let i = 1; i < 65536; i++) pc16[i] = pc16[i >> 1] + (i & 1);
const pop = (x) => pc16[x & 65535] + pc16[(x >>> 16) & 65535];

function legalAdd(Slo, Shi, p) {
  const b = p * PLINES;
  for (let k = 0; k < PLINES; k++) {
    const li = ptLines[b + k];
    if (pop(Slo & lineLo[li]) + pop(Shi & lineHi[li]) >= s) return false;
  }
  return true;
}
function mkMask(idxs) { let lo = 0, hi = 0; for (const i of idxs) { if (i < 32) lo |= 1 << i; else hi |= 1 << (i - 32); } return [lo >>> 0, hi >>> 0]; }
const FncCands = [mkMask([0, 1, q]), mkMask([0, 2, q + 1]), mkMask([1, 3, q + 2])];
const FcCands = [];
for (const [lo, hi] of lines) {
  const on = []; for (let i = 0; i < n && on.length < 3; i++) { const b = i < 32 ? (lo >>> i) & 1 : (hi >>> (i - 32)) & 1; if (b) on.push(i); }
  FcCands.push(mkMask(on)); if (FcCands.length >= 3) break;
}
const F = cone === 'nc' ? FncCands[fset % 3] : FcCands[fset % 3];

if (mode === 'enum') {
  fs.mkdirSync(dir, { recursive: true });
  const CAP = 1 << 22; // entries per chunk buffer
  const emitBuf = {}; const emitPos = {}; const chunks = {}; const cnts = {};
  function emit(depth, lo, hi) {
    if (!emitBuf[depth]) { emitBuf[depth] = Buffer.allocUnsafe(CAP * 8); emitPos[depth] = 0; chunks[depth] = []; cnts[depth] = 0; }
    const p = emitPos[depth];
    emitBuf[depth].writeUInt32LE(lo >>> 0, p); emitBuf[depth].writeUInt32LE(hi >>> 0, p + 4);
    emitPos[depth] = p + 8; cnts[depth]++;
    if (emitPos[depth] >= CAP * 8) { chunks[depth].push(emitBuf[depth].subarray(0, emitPos[depth])); emitBuf[depth] = Buffer.allocUnsafe(CAP * 8); emitPos[depth] = 0; }
  }
  let nodes = 0; const t0 = Date.now();
  function rec(Slo, Shi, last, depth) {
    nodes++; emit(depth, Slo, Shi);
    for (let p = last + 1; p < n; p++) {
      const inS = p < 32 ? (Slo >>> p) & 1 : (Shi >>> (p - 32)) & 1;
      if (inS) continue;
      if (!legalAdd(Slo, Shi, p)) continue;
      rec(p < 32 ? (Slo | (1 << p)) >>> 0 : Slo >>> 0, p < 32 ? Shi >>> 0 : (Shi | (1 << (p - 32))) >>> 0, p, depth + 1);
    }
  }
  rec(F[0] >>> 0, F[1] >>> 0, -1, 3);
  for (const d of Object.keys(chunks)) { if (emitPos[d] > 0) chunks[d].push(emitBuf[d].subarray(0, emitPos[d])); if (chunks[d].length) fs.appendFileSync(path.join(dir, `layer_${d}.bin`), Buffer.concat(chunks[d])); }
  const sizes = {}; for (const d of Object.keys(cnts)) sizes[d] = cnts[d];
  const meta = { cone, fset, nodes, sizes, ms: Date.now() - t0 };
  fs.writeFileSync(path.join(dir, 'meta.json'), JSON.stringify(meta));
  console.log(JSON.stringify(meta));
  process.exit(0);
}

if (mode === 'dp') {
  const meta = JSON.parse(fs.readFileSync(path.join(dir, 'meta.json'), 'utf8'));
  const maxm = Math.max(...Object.keys(meta.sizes).map(Number));
  const counts = {}; const maximal = {}; let gF = -1;
  const CH = 1 << 22;
  for (let m = maxm; m >= 3; m--) {
    const size = meta.sizes[m];
    const t0 = Date.now();
    let loC = null, hiC = null, gC = null, sizeC = 0;
    if (m < maxm) {
      const sc = meta.sizes[m + 1];
      const rc = fs.readFileSync(path.join(dir, `sorted_${m + 1}.bin`));
      if (rc.length !== sc * 9) throw new Error('child size mismatch ' + (m + 1));
      sizeC = sc; loC = new Uint32Array(sc); hiC = new Uint32Array(sc); gC = new Uint8Array(sc);
      for (let i = 0; i < sc; i++) { loC[i] = rc.readUInt32LE(i * 9); hiC[i] = rc.readUInt32LE(i * 9 + 4); gC[i] = rc.readUInt8(i * 9 + 8); }
    }
    const fd = fs.openSync(path.join(dir, `layer_${m}.bin`), 'r');
    const gFd = fs.openSync(path.join(dir, `gM_${m}.bin`), 'w');
    const cntm = new Float64Array(64); let maxcnt = 0;
    const stampArr = new Int32Array(64);
    const cntLine = new Uint8Array(nlines);
    const rawChunk = Buffer.allocUnsafe(CH * 8);
    let done = 0; let idx = 0;
    while (done < size) {
      const take = Math.min(CH, size - done);
      const br = fs.readSync(fd, rawChunk, 0, take * 8, null);
      if (br !== take * 8) throw new Error('short read');
      const gOut = Buffer.allocUnsafe(take);
      for (let e = 0; e < take; e++) {
        const Slo = rawChunk.readUInt32LE(e * 8), Shi = rawChunk.readUInt32LE(e * 8 + 4);
        for (let li = 0; li < nlines; li++) cntLine[li] = pop(Slo & lineLo[li]) + pop(Shi & lineHi[li]);
        const stamp = idx + 1;
        let any = false;
        if (loC) {
          for (let p = 0; p < n; p++) {
            const inS = p < 32 ? (Slo >>> p) & 1 : (Shi >>> (p - 32)) & 1;
            if (inS) continue;
            const b = p * PLINES; let ok = true;
            for (let k = 0; k < PLINES; k++) { if (cntLine[ptLines[b + k]] >= s) { ok = false; break; } }
            if (!ok) continue;
            const clo = p < 32 ? (Slo | (1 << p)) >>> 0 : Slo >>> 0;
            const chi = p < 32 ? Shi >>> 0 : (Shi | (1 << (p - 32))) >>> 0;
            let l2 = 0, h2 = sizeC - 1, gv = -1;
            while (l2 <= h2) {
              const mid = (l2 + h2) >> 1;
              const cl = loC[mid];
              if (cl < clo) l2 = mid + 1;
              else if (cl > clo) h2 = mid - 1;
              else {
                const ch = hiC[mid];
                if (ch < chi) l2 = mid + 1;
                else if (ch > chi) h2 = mid - 1;
                else { gv = gC[mid]; break; }
              }
            }
            if (gv < 0) throw new Error('missing child m=' + m + ' p=' + p + ' i=' + idx);
            stampArr[gv] = stamp; any = true;
          }
        }
        let gval = 0; while (stampArr[gval] === stamp) gval++;
        gOut.writeUInt8(gval, e);
        cntm[gval]++;
        if (!any) maxcnt++;
        idx++;
      }
      fs.writeSync(gFd, gOut, 0, take, null);
      done += take;
    }
    fs.closeSync(fd); fs.closeSync(gFd);
    loC = null; hiC = null; gC = null;
    { let tot = 0; for (let g = 0; g < 64; g++) tot += cntm[g]; if (tot !== size) throw new Error('count sum m=' + m); }
    counts[m] = Array.from(cntm); maximal[m] = maxcnt;
    if (m === 3) { if (size !== 1) throw new Error('layer3'); const g3 = Buffer.allocUnsafe(1); const f3 = fs.openSync(path.join(dir, 'gM_3.bin'), 'r'); fs.readSync(f3, g3, 0, 1, 0); fs.closeSync(f3); gF = g3.readUInt8(0); }
    const t1 = Date.now();
    // --- step 2: ping-pong radix sort with index tracking, then gather grundy ---
    let sLo = new Uint32Array(size), sHi = new Uint32Array(size), sIdx = new Uint32Array(size);
    { const raw = fs.readFileSync(path.join(dir, `layer_${m}.bin`));
      for (let i = 0; i < size; i++) { sLo[i] = raw.readUInt32LE(i * 8); sHi[i] = raw.readUInt32LE(i * 8 + 4); sIdx[i] = i; } }
    let dLo = new Uint32Array(size), dHi = new Uint32Array(size), dIdx = new Uint32Array(size);
    for (let pass = 0; pass < 8; pass++) {
      const useHi = pass < 4; const byteIdx = pass % 4;
      const cnt = new Uint32Array(257);
      for (let i = 0; i < size; i++) { const v = useHi ? sHi[i] : sLo[i]; cnt[((v >>> (8 * byteIdx)) & 255) + 1]++; }
      for (let b = 0; b < 256; b++) cnt[b + 1] += cnt[b];
      for (let i = 0; i < size; i++) {
        const v = useHi ? sHi[i] : sLo[i];
        const t = cnt[(v >>> (8 * byteIdx)) & 255]++;
        dLo[t] = sLo[i]; dHi[t] = sHi[i]; dIdx[t] = sIdx[i];
      }
      const tl = sLo; sLo = dLo; dLo = tl;
      const th = sHi; sHi = dHi; dHi = th;
      const ti = sIdx; sIdx = dIdx; dIdx = ti;
    }
    // 8 passes (even) => sorted arrays are back in the original sLo/sHi buffers
    const gRaw = fs.readFileSync(path.join(dir, `gM_${m}.bin`));
    if (gRaw.length !== size) throw new Error('gM size');
    { const out = fs.openSync(path.join(dir, `sorted_${m}.bin`), 'w');
      const WB = 1 << 22; let w = 0;
      while (w < size) {
        const take = Math.min(WB, size - w);
        const buf = Buffer.allocUnsafe(take * 9);
        for (let e = 0; e < take; e++) {
          const i = w + e;
          buf.writeUInt32LE(sLo[i] >>> 0, e * 9); buf.writeUInt32LE(sHi[i] >>> 0, e * 9 + 4);
          buf.writeUInt8(gRaw.readUInt8(sIdx[i]), e * 9 + 8);
        }
        fs.writeSync(out, buf, 0, take * 9, null); w += take;
      }
      fs.closeSync(out); }
    sLo = null; sHi = null; sIdx = null; dLo = null; dHi = null; dIdx = null;
    fs.unlinkSync(path.join(dir, `layer_${m}.bin`));
    fs.unlinkSync(path.join(dir, `gM_${m}.bin`));
    if (m < maxm) fs.unlinkSync(path.join(dir, `sorted_${m + 1}.bin`));
    console.error(`m=${m} size=${size} maximal=${maxcnt} grundy_ms=${t1 - t0} sort_ms=${Date.now() - t1}`);
  }
  const out = { cone, fset, maxm, counts, maximal, gF, nodes: meta.nodes, sizes: meta.sizes };
  fs.writeFileSync(path.join(dir, 'dp_result.json'), JSON.stringify(out));
  console.log(JSON.stringify({ cone, fset, gF, maxm }));
  process.exit(0);
}
throw new Error('mode');
