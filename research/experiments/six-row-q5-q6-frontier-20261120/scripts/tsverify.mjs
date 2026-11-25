import { verify } from '/home/user/kr65/scripts/verify_independent.ts';
import fs from 'fs';
const [w, m, q, file] = process.argv.slice(2);
const stones = JSON.parse(fs.readFileSync(file, 'utf8'));
const res = verify(stones, Number(w), Number(m), Number(q));
console.log(JSON.stringify(res));
if (!res.pass) process.exit(1);
