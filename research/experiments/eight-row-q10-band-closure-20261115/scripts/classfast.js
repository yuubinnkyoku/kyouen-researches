// classfast.js — sat3.js class-split driver with genfast3 chord-pair census installed
// (S.buildCensus patched at require time; byte-identical curve set+order for q>=w+2).
// Usage: node classfast.js w m q --class=D [--krow=y:k,...] [--minpos=P] [--lex=H] out.cnf
'use strict';
const path = require('path');
require('/home/user/krwork/eightq10/scripts/genfast3.js'); // installs fastCensus3 on shared sat.js
const sat3 = require(path.join(__dirname, 'sat3.js'));
const S2 = require(path.join(__dirname, 'sat2.js'));
const args = process.argv.slice(2);
const [w, m, q] = [Number(args[0]), Number(args[1]), Number(args[2])];
let i = 3, cls = null, out = null, lex = [], krow = [], minpos = null;
for (; i < args.length; i++) {
  const a = args[i];
  if (a.startsWith('--class=')) cls = a.slice(8).split(',').map(Number);
  else if (a.startsWith('--lex=')) lex = a.slice(6).split(',');
  else if (a.startsWith('--krow=')) krow = a.slice(7).split(',');
  else if (a.startsWith('--minpos=')) minpos = Number(a.slice(9));
  else if (!out) out = a;
}
const t0 = Date.now();
const { enc, meta } = sat3.dumpClass(w, m, q, cls, { lex, krow, minpos });
require('fs').writeFileSync(out, S2.toDimacs2(enc));
meta.file = out; meta.generator = 'sat3+genfast3-chord';
meta.gen_sec = ((Date.now() - t0) / 1000).toFixed(1);
console.log(JSON.stringify(meta));
