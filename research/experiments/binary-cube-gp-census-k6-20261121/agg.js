const lines = require('fs').readFileSync('/home/user/work/cen2/r6.jsonl', 'utf8').trim().split('\n');
const tot = new Array(11).fill(0);
const perV = [];
for (const ln of lines) {
  const o = JSON.parse(ln);
  perV[o.v2] = o.counts;
  for (let s = 0; s <= 10; s++) tot[s] += (o.counts[s] || 0);
}
const missing = [];
for (let v = 1; v <= 63; v++) if (!perV[v]) missing.push(v);
console.log('pairs present:', perV.filter(Boolean).length, 'missing:', JSON.stringify(missing));
console.log('counts[2]=' + tot[2], '(expect 63)');
console.log('counts[3]=' + tot[3], '(expect 1953 = C(63,2), all triples affinely independent)');
console.log('counts[4]=' + tot[4], '(audit-derived expect 39,410 = (C(64,4)-4816)*4/64)');
console.log('counts[5]=' + tot[5], '(audit-derived expect 571,340 = 7,313,152*5/64)');
console.log('counts[6]=' + tot[6], '(audit-derived expect 6,029,142 = 64,310,848*6/64)');
console.log('counts[7]=' + tot[7], '(audit-derived expect 40,050,850 = 366,179,200*7/64)');
console.log('counts[8]=' + tot[8], '(no prior expectation)');
console.log('counts[9]=' + tot[9], '(no prior expectation)');
console.log('counts[10]=' + tot[10], '******** 0 => no GP-10 => K_6 = 9 ********');
