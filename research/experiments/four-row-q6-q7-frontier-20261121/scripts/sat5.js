#!/usr/bin/env node
// sat5.js — capacity-attainment encoder on the K0810 sat2.js core (uses sat.js census +
// sat2.js counter core verbatim). Encodes: safety (every census curve <= q-1 stones) +
// "every row has >= q-1 stones" (unit clauses on the rowGe outputs). Any model is a safe
// set with all rows = q-1 (safety caps rows at q-1), i.e. (q-1)w stones = capacity —
// auto-maximal. Use only for m >= q (row curves present).
// Usage: node sat5.js w m q out.cnf   (prints meta JSON)
'use strict';
const { spawnSync } = require('child_process');
const fs = require('fs');
// Reuse sat2.js core through a child node process is clumsy; instead require sat2 internals.
// sat2.js exports dump/tonDimacs? (encodeCore, totalizerAtMost, lexLeader, S}).
const C2 = require('./sat2.js');
const [w, m, q] = [Number(process.argv[2]), Number(process.argv[3]), Number(process.argv[4])];
const out = process.argv[5];
if (m < q) { console.error('requires m >= q (row curves)'); process.exit(2); }
const { enc, cell, n, curves, rowGe } = C2.encodeCore(w, m, q);
for (const y of Object.keys(rowGe)) enc.add([[rowGe[y]]]);
const meta = { w, m, q, mode: 'capacity-allrows-ge-(q-1)', curves: curves.length, vars: enc.nv, clauses: enc.clauses.length, cnf_md5_hint: true };
fs.writeFileSync(out, C2.toDimacs2(enc));
console.log(JSON.stringify(meta));
