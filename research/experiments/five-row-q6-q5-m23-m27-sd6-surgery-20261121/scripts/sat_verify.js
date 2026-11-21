// Standalone seed witness verifier: wraps S.verifyConfig(w, m, q, stones) from sat.js
// Usage: node sat_verify.js <w> <m> <q> <seed.json>
const S = require("./sat.js");
const fs = require("fs");
const w = parseInt(process.argv[2], 10);
const m = parseInt(process.argv[3], 10);
const q = parseInt(process.argv[4], 10);
const parsed = JSON.parse(fs.readFileSync(process.argv[5], "utf8"));
const stones = Array.isArray(parsed) ? parsed : parsed.stones;
const res = S.verifyConfig(w, m, q, stones);
const ok = res && res.ok;
console.log(ok ? "PASS" : "FAIL " + JSON.stringify(res));
process.exit(ok ? 0 : 1);
