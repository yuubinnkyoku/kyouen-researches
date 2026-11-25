// append_records.js — extend the published K1177 records.jsonl with the four
// genfast3 band-extension records past the sat2.js memory wall (m=86..88
// q=7-witness-free UNSAT, plus the --lex=H cross-encoding of m=86).
// Field order and types byte-match the published schema (checked against the
// K1177 UNSAT records). Fail-closed: refuses to append if any of the four tags
// already exists.
'use strict';
const fs = require('fs');
const [, , inPath, outPath, liveDir] = process.argv;
const keep = [];

const TS = '2026-11-21T02:05:30Z';
const GEN = 'genfast3.js-md5-12c2bd9cb3b24887fc3896f7ea9bcadf-core-sat2.js-md5-282ae832efa0080127c6c153e65e1c3c';
// (m, tag-suffix, vars, clauses, curves, cnf_md5, gen_sec, gen_extra, conflicts, sec)
const rows = [
  [86, 'def',    7043, 24987, 133, 'dd97c9c9e159f7517ead5c8e92f27546', 0.13, '',       5930, 0.2],
  [87, 'def',    7180, 25477, 136, '73da5edfc282ed50014ca5e7ab685bc7', 0.13, '',       5191, 0.2],
  [88, 'def',    7317, 25967, 139, 'cb1fdbd9a75bcddeddeeda3c9d752028', 0.12, '',       6072, 0.2],
  [86, 'def_lexH', 7388, 27052, 133, 'e74ad6861321afa283b501ffb1150458', 0.12, '--lex=H', 3677, 0.2],
];

const existing = new Set();
const lines = fs.readFileSync(inPath, 'utf8').split('\n').filter(l => l.trim());
for (const l of lines) existing.add(JSON.parse(l).tag);
for (const [m, sfx] of rows.map(r => [r[0], r[1]])) {
  const tag = `s4x${m}q7_${sfx}`;
  if (existing.has(tag)) { console.error(`refuse: ${tag} already present`); process.exit(1); }
}
// sanity: every claimed cnf_md5/vars/clauses/curves must match the regenerated
// genfast3 meta JSON in output/live (byte-identical to the solved instances).
const metaOf = {};
for (const [m, sfx] of rows.map(r => [r[0], r[1]])) {
  const base = sfx === 'def_lexH' ? `gen_4x${m}q7_lexH.json` : `gen_4x${m}q7_${sfx}.json`;
  metaOf[`${m}_${sfx}`] = JSON.parse(fs.readFileSync(`${liveDir}/${base}`, 'utf8'));
}
for (const [m, sfx, vars, clauses, curves, md5] of rows) {
  const meta = metaOf[`${m}_${sfx}`];
  const expExtra = sfx === 'def_lexH' ? '--lex=H' : '';
  const lexArr = sfx === 'def_lexH' ? ['H'] : [];
  if (meta.vars !== vars || meta.clauses !== clauses || meta.curves !== curves)
    { console.error(`meta mismatch ${m} ${sfx}`); process.exit(1); }
  if (meta.mode !== 'deficient' || (meta.lex || []).join('') !== lexArr.join(''))
    { console.error(`mode/lex mismatch ${m} ${sfx}`); process.exit(1); }
}
// md5 of the on-disk CNF must equal the recorded one (CNFs are deleted from the
// repo — cnf_deleted:true — the md5 is the binding to the published solve log)
const cp = require('child_process');
for (const [m, sfx, , , , md5] of rows) {
  const f = sfx === 'def_lexH' ? `c_4x${m}q7_lexH.cnf` : `c_4x${m}q7_${sfx}.cnf`;
  const got = cp.execSync(`md5sum ${liveDir}/${f}`).toString().split(' ')[0];
  if (got !== md5) { console.error(`md5 mismatch ${f}: ${got}`); process.exit(1); }
}
const out = lines.slice();
for (const [m, sfx, vars, clauses, curves, md5, gen_sec, gen_extra, conflicts, sec] of rows) {
  const tag = `s4x${m}q7_${sfx}`;
  const rec = {
    w: 4, m, q: 7, mode: 'deficient', rowY: null, generator: GEN,
    vars, clauses, curves, cnf_md5: md5, gen_sec, gen_extra,
    kissat: { result: 'UNSATISFIABLE', rc: 20, conflicts, sec_cap: 200, sec },
    ts: TS, witness: null, tag, cnf_deleted: true,
  };
  out.push(JSON.stringify(rec));
}
fs.writeFileSync(outPath, out.join('\n') + '\n');
console.log(JSON.stringify({ input_records: lines.length, output_records: out.length, appended: rows.length }));
