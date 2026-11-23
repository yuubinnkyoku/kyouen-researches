// wholesale TBL vs replica wob comparison
const mine = require('./third_impl.js');
const R = require('/home/user/knowledge/kyouen-research/_class1297036830122704896-lane-kit/inv/jsreplay.js');
const { wob, count } = R.buildCompletionTable();
console.log('replica quads', count, 'mine quads', mine.quadCount);
if (count !== mine.quadCount) { console.log('QUAD COUNT MISMATCH'); process.exit(1); }
// TBL access: need module-internal; rebuild via legalOf on single-position plumbing:
// trick: legalOf(pts,occ) with pts=[a,b,c] returns mask of ALL points except a,b,c minus danger:
// legal = ~(occ|danger) -> danger = ~legal & ~occ. Compare danger to wob.
const V = 121;
let bad = 0, checked = 0;
let seed = 99991;
function rnd() { seed = (Math.imul(seed, 1103515245) + 12345) >>> 0; return seed / 4294967296; }
const allOnes = [0xffffffff >>> 0, 0xffffffff >>> 0, 0xffffffff >>> 0, (1 << 25) - 1];
for (let t = 0; t < 200000; t++) {
  const a = Math.floor(rnd() * V), b = Math.floor(rnd() * V), c = Math.floor(rnd() * V);
  if (a === b || b === c || a === c) continue;
  const pts = [a, b, c].sort((x, y) => x - y);
  const occ = mine.occOf(pts);
  const legal = mine.legalOf(pts.slice(), occ);
  const danger = [0, 0, 0, 0];
  for (let w = 0; w < 4; w++) danger[w] = (~legal[w] & ~occ[w] & allOnes[w]) >>> 0;
  const base = 4 * ((pts[0] * V + pts[1]) * V + pts[2]);
  const rep = [wob[base], wob[base + 1], wob[base + 2], wob[base + 3]];
  let eq = rep[0] === danger[0] && rep[1] === danger[1] && rep[2] === danger[2] && rep[3] === danger[3];
  checked++;
  if (!eq) { bad++; if (bad <= 3) console.log('TBL mismatch at', pts, 'mine', danger.map(x=>x>>>0), 'rep', rep.map(x=>x>>>0)); }
}
console.log('triples checked', checked, 'mismatches', bad);
