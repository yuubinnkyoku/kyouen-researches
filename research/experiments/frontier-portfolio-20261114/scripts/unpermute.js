// unpermute.js model.txt map.json out.txt  -- model lines "v ..." in permuted numbering -> original numbering
const fs = require('fs');
const [modelf, mapf, outf] = process.argv.slice(2);
const { perm } = JSON.parse(fs.readFileSync(mapf, 'utf8'));
const inv = new Array(perm.length); for (let i = 1; i < perm.length; i++) inv[perm[i]] = i;
const out = [];
for (const line of fs.readFileSync(modelf, 'utf8').split('\n')) {
  if (!line.startsWith('v ')) continue;
  const lits = line.slice(2).trim().split(/\s+/).map(Number).filter(x => x !== 0);
  const orig = lits.map(l => (l > 0 ? inv[l] : -inv[-l]));
  for (let i = 0; i < orig.length; i += 25) out.push('v ' + orig.slice(i, i + 25).join(' '));
}
fs.writeFileSync(outf, out.join('\n') + '\n0\n');
console.log('unpermuted ' + out.length + ' lines');
