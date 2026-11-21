// Usage: node verify_witness.js <w> <m> <q> <json-stones>  -> prints verifyConfig result
const { verifyConfig } = require('./sat.js');
const [w, m, q] = process.argv.slice(2, 5).map(Number);
const stones = JSON.parse(process.argv[5]);
console.log(JSON.stringify(verifyConfig(w, m, q, stones)));
