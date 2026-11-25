// census_dump.js — dump the sat.js forbidden-curve census as canonical text for
// cross-system comparison (w-generic, lane parameters only). Read-only use of the
// published four-row lane's sat.js (md5 0cc6021a...), unmodified.
'use strict';
const S = require('./sat.js');

function dump(w, m, q) {
  const { P, curves } = S.buildCensus(w, m, q);
  const out = curves.map(cu => {
    const pts = cu.pts.map(i => P[i][0] + ',' + P[i][1]).sort();
    return cu.type + '|' + (cu.type === 'line' ? cu.co.join('/') : cu.co.join('/')) + '|' + pts.join(';');
  }).sort();
  return out;
}

const [w, m, q] = [Number(process.argv[2]), Number(process.argv[3]), Number(process.argv[4])];
const lines = dump(w, m, q);
require('fs').writeFileSync(process.argv[5], lines.join('\n') + '\n');
console.log(JSON.stringify({ w, m, q, curves: lines.length }));
