#!/usr/bin/env node
// runner.js — four-row q=6/q=7 deficient-maximal witness frontier sweep (w=4 fixed)
// Mirrors six-row-q5-q6-frontier-20261120 ops conventions: records.jsonl append-only,
// CNF md5, conflicts field, per-instance time cap, 3-system witness verification
// (sat.js verifyConfig / verify_witness.py / verify3.py subset-based independent).
// pins: sat.js 0cc6021a4e523a0d7f4d5ea0f5f5d40c, sat2.js 282ae832efa0080127c6c153e65e1c3c,
//       verify_witness.py 0530d166572987988a01ec40dee12d4c, kissat 4.0.4 linux-amd64 3a5eba830aa6008a604fcc9bbe99a325
'use strict';
const { spawnSync } = require('child_process');
const fs = require('fs'), path = require('path'), crypto = require('crypto');

const DIR = __dirname;                 // <exp>/scripts
const EXP = path.dirname(DIR);         // <exp>
const OUT = path.join(EXP, 'output');
const RECS = path.join(OUT, 'records.jsonl');
const KISSAT = process.env.KISSAT_BIN || path.join(EXP, '..', '..', 'bin', 'kissat-4.0.4-linux-amd64');
const W = 4;
const md5file = f => crypto.createHash('md5').update(fs.readFileSync(f)).digest('hex');
const md5str = s => crypto.createHash('md5').update(s).digest('hex');
const now = () => new Date().toISOString().replace(/\.\d{3}Z$/, 'Z');

function genCnf(m, q, mode, rowY, lex, cnfPath) {
  const cli = ['sat2.js', String(W), String(m), String(q)];
  if (mode === 'deficient') cli.push('--deficient');
  else if (mode === 'rowfixed') cli.push('--rowY=' + rowY);
  else throw new Error('mode ' + mode);
  if (lex && lex.length) cli.push('--lex=' + lex.join(','));
  cli.push(cnfPath);
  const t0 = Date.now();
  const res = spawnSync('node', cli, { cwd: DIR, encoding: 'utf8' });
  if (res.status !== 0) throw new Error('sat2.js failed: ' + res.stdout + res.stderr);
  const meta = JSON.parse(res.stdout);
  meta.gen_sec = Math.round((Date.now() - t0)) / 1000;
  meta.cnf_md5 = md5file(cnfPath);
  meta.gen_extra = (lex && lex.length) ? '--lex=' + lex.join(',') : '';
  return meta;
}

function solve(cnfPath, capSec) {
  const t0 = Date.now();
  const res = spawnSync(KISSAT, ['--time=' + capSec, cnfPath], { encoding: 'utf8', maxBuffer: 128 * 1024 * 1024 });
  const sec = (Date.now() - t0) / 1000;
  const out = res.stdout || '';
  let result = 'UNKNOWN';
  if (/^s SATISFIABLE/m.test(out)) result = 'SATISFIABLE';
  else if (/^s UNSATISFIABLE/m.test(out)) result = 'UNSATISFIABLE';
  const conf = out.match(/^c\s+conflicts:\s+(\d+)/m);
  const conflicts = conf ? Number(conf[1]) : null;
  let lits = null;
  if (result === 'SATISFIABLE') {
    lits = [];
    for (const line of out.split('\n')) if (line.startsWith('v ')) lits.push(...line.slice(2).trim().split(/\s+/).map(Number));
  }
  return { result, rc: res.status, conflicts, sec, lits };
}

const idxToXY = (i, m) => [i % m, Math.floor(i / m)];

function runInstance(m, q, mode, rowY, lex, capSec) {
  const tag = `s${W}x${m}q${q}${mode === 'rowfixed' ? '_rowY' + rowY : '_def'}${lex && lex.length ? '_lexH' : ''}`;
  if (fs.existsSync(RECS) && fs.readFileSync(RECS, 'utf8').includes('"tag":"' + tag + '"')) return { skip: true, tag };
  const tmp = path.join(OUT, '.tmp.cnf');
  const meta = genCnf(m, q, mode, rowY, lex, tmp);
  const ks = solve(tmp, capSec);
  const rec = {
    w: W, m, q, mode, rowY: mode === 'rowfixed' ? rowY : null,
    generator: 'sat2.js-md5-' + md5file(path.join(DIR, 'sat2.js')),
    vars: meta.vars, clauses: meta.clauses, curves: meta.curves,
    cnf_md5: meta.cnf_md5, gen_sec: meta.gen_sec, gen_extra: meta.gen_extra || '',
    kissat: { result: ks.result, rc: ks.rc, conflicts: ks.conflicts, sec_cap: capSec, sec: Math.round(ks.sec * 100) / 100 },
    ts: now(), witness: null, tag
  };
  if (ks.result === 'SATISFIABLE') {
    const stonesXY = ks.lits.filter(l => l > 0 && l - 1 < W * m).map(l => idxToXY(l - 1, m));
    stonesXY.sort((a, b) => a[1] - b[1] || a[0] - b[0]);
    const S2 = require(path.join(DIR, 'sat.js'));
    const v1 = S2.verifyConfig(W, m, q, stonesXY);
    const p2 = spawnSync('python3', [path.join(DIR, 'verify_witness.py'), String(W), String(m), String(q)], { input: JSON.stringify(stonesXY), encoding: 'utf8' });
    let v2 = null; try { v2 = JSON.parse(p2.stdout); } catch (e) { v2 = { ok: false, parse_error: String(e), raw: String(p2.stdout).slice(0, 300) }; }
    const p3 = spawnSync('python3', [path.join(DIR, 'verify3.py'), String(W), String(m), String(q)], { input: JSON.stringify(stonesXY), encoding: 'utf8' });
    let v3 = null; try { v3 = JSON.parse(p3.stdout); } catch (e) { v3 = { pass: false, parse_error: String(e), raw: String(p3.stdout).slice(0, 300) }; }
    const rows = Array(W).fill(0); for (const p of stonesXY) rows[p[1]]++;
    rec.witness = {
      nStones: stonesXY.length, rows,
      js_ok: v1.ok === true, py_ok: p2.status === 0 && v2.ok === true, three_ok: p3.status === 0 && v3.pass === true,
      js_rc: v1.ok, py_rc: p2.status, three_rc: p3.status,
      verify_outputs: {
        js: JSON.stringify({ ok: v1.ok, size: v1.size, rows: v1.rows, minRow: v1.minRow, why: v1.why || null }),
        py: p2.stdout.trim(), three: p3.stdout.trim()
      },
      stones: stonesXY
    };
    const allOk = rec.witness.js_ok && rec.witness.py_ok && rec.witness.three_ok;
    rec.witness_verify = allOk ? 'js+py+three PASS' : 'FAIL-DO-NOT-USE';
    if (allOk) {
      const wdir = path.join(OUT, 'witnesses'); fs.mkdirSync(wdir, { recursive: true });
      fs.writeFileSync(path.join(wdir, tag + '.witness.json'), JSON.stringify({ w: W, m, q, mode, rows, stones: stonesXY }, null, 1) + '\n');
    }
  } else {
    rec.cnf_deleted = true;
  }
  fs.unlinkSync(tmp);
  fs.appendFileSync(RECS, JSON.stringify(rec) + '\n');
  return rec;
}

function main() {
  fs.mkdirSync(OUT, { recursive: true });
  const cmd = process.argv[2];
  if (cmd === 'cal') {
    // Positive control (6,16,6) driven through this pipeline but with w=6 one-off:
    // expected (published six-row record): cnf_md5 22dd41bae3f338713c8ed866b9a28f8e,
    // SAT 46 conflicts, 29-stone witness rows [5,4,5,5,5,5].
    const tmp = path.join(OUT, '.cal_6x16q6.cnf');
    const t0 = Date.now();
    const res = spawnSync('node', ['sat2.js', '6', '16', '6', '--deficient', tmp], { cwd: DIR, encoding: 'utf8' });
    if (res.status !== 0) throw new Error(res.stderr);
    const meta = JSON.parse(res.stdout); meta.gen_sec = (Date.now() - t0) / 1000;
    const h = md5file(tmp);
    const ks = solve(tmp, 60);
    const nStones = ks.lits ? ks.lits.filter(l => l > 0 && l - 1 < 6 * 16).length : null;
    console.log(JSON.stringify({ cal: '(6,16,6)', cnf_md5: h, cnf_md5_expected: '22dd41bae3f338713c8ed866b9a28f8e', match: h === '22dd41bae3f338713c8ed866b9a28f8e', meta: { vars: meta.vars, clauses: meta.clauses, curves: meta.curves }, kissat: { result: ks.result, conflicts: ks.conflicts, conflicts_expected: 46, sec: Math.round(ks.sec * 100) / 100 }, nStones, nStones_expected: 29 }, null, 1));
    fs.unlinkSync(tmp);
    return;
  }
  if (cmd === 'sweep') {
    const q = Number(process.argv[3]), mStart = Number(process.argv[4]), mMax = Number(process.argv[5]);
    const capSec = Number(process.argv[6]), budgetSec = Number(process.argv[7]);
    const t0 = Date.now();
    for (let m = mStart; m <= mMax; m++) {
      if (m < q) { console.log(JSON.stringify({ skip_m_lt_q: m })); continue; }
      if ((Date.now() - t0) / 1000 > budgetSec) { console.log('BUDGET'); break; }
      const rec = runInstance(m, q, 'deficient', null, null, capSec);
      console.log(rec.skip ? JSON.stringify({ skip: rec.tag }) : JSON.stringify({ m, q, res: rec.kissat.result, conflicts: rec.kissat.conflicts, sec: rec.kissat.sec, witness: rec.witness ? { n: rec.witness.nStones, rows: rec.witness.rows, verify: rec.witness_verify } : null }));
    }
    return;
  }
  if (cmd === 'rowfixed' || cmd === 'lexdef') {
    const q = Number(process.argv[3]), m = Number(process.argv[4]), rowY = Number(process.argv[5]) || 0, capSec = Number(process.argv[6]);
    const rec = cmd === 'rowfixed'
      ? runInstance(m, q, 'rowfixed', rowY, null, capSec)
      : runInstance(m, q, 'deficient', null, ['H'], capSec);
    console.log(JSON.stringify(rec));
    return;
  }
  if (cmd === 'cap') {
    // capacity attainment at width m: sat5.js (safety + all rows >= q-1 units) + 3-system verify.
    const q = Number(process.argv[3]), m = Number(process.argv[4]), capSec = Number(process.argv[5]) || 90;
    const tag = `s${W}x${m}q${q}_capacity`;
    if (fs.existsSync(RECS) && fs.readFileSync(RECS, 'utf8').includes('"tag":"' + tag + '"')) { console.log(JSON.stringify({ skip: tag })); return; }
    const tmp = path.join(OUT, '.tmp_cap.cnf');
    const t0 = Date.now();
    let res = spawnSync('node', ['sat5.js', String(W), String(m), String(q), tmp], { cwd: DIR, encoding: 'utf8' });
    if (res.status !== 0) throw new Error(res.stdout + res.stderr);
    const meta = JSON.parse(res.stdout);
    meta.gen_sec = (Date.now() - t0) / 1000;
    const cnfMd5 = md5file(tmp);
    const ks = solve(tmp, capSec);
    const rec = {
      w: W, m, q, mode: 'capacity', rowY: null,
      generator: 'sat5.js-md5-' + md5file(path.join(DIR, 'sat5.js')) + '-core-sat2.js-md5-' + md5file(path.join(DIR, 'sat2.js')),
      vars: meta.vars, clauses: meta.clauses, curves: meta.curves,
      cnf_md5: cnfMd5, gen_sec: meta.gen_sec, gen_extra: '',
      kissat: { result: ks.result, rc: ks.rc, conflicts: ks.conflicts, sec_cap: capSec, sec: Math.round(ks.sec * 100) / 100 },
      ts: now(), witness: null, tag
    };
    let rowSummary = null, allOk = false;
    if (ks.result === 'SATISFIABLE') {
      const stonesXY = ks.lits.filter(l => l > 0 && l - 1 < W * m).map(l => idxToXY(l - 1, m));
      stonesXY.sort((a, b) => a[1] - b[1] || a[0] - b[0]);
      // capacity-set semantics: safety + maximality + every row exactly q-1 (auto-maximal
      // once safe & full). Row-deficiency is FALSE by definition, so the deficient-mode
      // verifiers must NOT be required to return their deficiency flag.
      const S2 = require(path.join(DIR, 'sat.js'));
      const v1 = S2.verifyConfig(W, m, q, stonesXY);            // system 1: safety+maximality
      const p3 = spawnSync('python3', [path.join(DIR, 'verify3.py'), String(W), String(m), String(q), '--capacity'],  { input: JSON.stringify(stonesXY), encoding: 'utf8' });
      const p3j = JSON.parse(p3.stdout);                       // system 3: safety+maximality+capacity
      const p2 = spawnSync('python3', [path.join(DIR, 'verify_witness.py'), String(W), String(m), String(q), '--capacity'], { input: JSON.stringify(stonesXY), encoding: 'utf8' });
      let v2 = {}; try { v2 = JSON.parse(p2.stdout); } catch (e) { v2 = { parse_error: String(e) }; }
      const rows = Array(W).fill(0); for (const p of stonesXY) rows[p[1]]++;
      rowSummary = { nStones: stonesXY.length, rows };
      allOk = v1.ok === true
        && p3.status === 0 && p3j.pass === true && p3j.mode === 'capacity' && p3j.safe === true && p3j.maximal === true && p3j.capacity === true
        && p2.status === 0 && v2.ok === true && v2.mode === 'capacity' && v2.n === (q - 1) * W && Array.isArray(v2.rows) && v2.rows.every(r => r === q - 1)
        && stonesXY.length === (q - 1) * W && rows.every(r => r === q - 1);
      rec.witness = {
        nStones: stonesXY.length, rows, stones: stonesXY,
        js_ok: v1.ok === true, three_ok: p3.status === 0 && p3j.pass === true, py_ok: p2.status === 0 && v2.ok === true,
        verify_outputs: { js: JSON.stringify({ ok: v1.ok, size: v1.size, rows: v1.rows, minRow: v1.minRow, why: v1.why || null }), py: p2.stdout.trim(), three: p3.stdout.trim() }
      };
      rec.witness_verify = allOk ? 'js+py(capacity)+three PASS; all rows q-1 (capacity)' : 'FAIL-DO-NOT-USE';
      if (allOk) {
        const wdir = path.join(OUT, 'witnesses'); fs.mkdirSync(wdir, { recursive: true });
        fs.writeFileSync(path.join(wdir, tag + '.witness.json'), JSON.stringify({ w: W, m, q, mode: 'capacity', rows, stones: stonesXY }, null, 1) + '\n');
      }
    } else {
      rec.cnf_deleted = true;
    }
    fs.unlinkSync(tmp);
    fs.appendFileSync(RECS, JSON.stringify(rec) + '\n');
    console.log(JSON.stringify({ m, q, res: ks.result, conflicts: ks.conflicts, sec: ks.sec, capacity: rowSummary, verify: rec.witness_verify }));
    return;
  }
  console.log('cmds: cal | sweep q mStart mMax capSec budgetSec | rowfixed q m rowY capSec | lexdef q m 0 capSec | cap q m capSec');
}
main();
