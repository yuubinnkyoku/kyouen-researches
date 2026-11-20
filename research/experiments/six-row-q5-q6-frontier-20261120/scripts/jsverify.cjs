const S = require('/home/user/kr65/scripts/sat.js');
const fs = require('fs');
const [w, m, q, file] = process.argv.slice(2);
const stones = JSON.parse(fs.readFileSync(file, 'utf8'));
const res = S.verifyConfig(Number(w), Number(m), Number(q), stones);
console.log(JSON.stringify(res));
if (!res.ok) process.exit(1);
