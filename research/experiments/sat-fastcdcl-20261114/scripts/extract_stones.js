const fs = require('fs');
const [w, m, q] = process.argv.slice(2, 5).map(Number);
const lits = fs.readFileSync(process.argv[5], 'utf8').trim().split(/\s+/).map(Number);
const pts = []; for (let y = 0; y < w; y++) for (let x = 0; x < m; x++) pts.push([x, y]);
const stones = [];
for (let i = 0; i < pts.length; i++) if (lits[i] > 0) stones.push(pts[i]);
console.log(JSON.stringify({ w, m, q, size: stones.length, stones }));
