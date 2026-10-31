'use strict';
// Fail closed on the exact withdrawn S5 evidence in the pinned historical corpus.
// A future rehabilitation must update this guard and its independent audit.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const assert=require('node:assert/strict');
const ROOT=path.resolve(__dirname,'../../..');
const REGISTRY='results/n11-s5-evidence-quarantine.json';
const REGISTRY_BLOB='6a320237545874ddd841c90be095cccccc46249d';
const EXPECTED=[
 '00000000000000809100000000000800',
 '00000000200000001000040200010000',
];
function excludeQuarantined(cache){
 const raw=fs.readFileSync(path.join(ROOT,REGISTRY));
 const sha=crypto.createHash('sha1').update('blob '+raw.length+'\0').update(raw).digest('hex');
 assert.equal(sha,REGISTRY_BLOB,'S5 quarantine policy changed: review before using the pinned corpus');
 const doc=JSON.parse(raw.toString('utf8'));
 assert.equal(doc.schema,'n11-s5-evidence-quarantine-v1');
 assert(Array.isArray(doc.entries));
 const active=doc.entries.filter(e=>e.active===true);
 assert.equal(active.length,2,'active S5 quarantine entries changed');
 const keys=active.map(e=>{
  assert(Array.isArray(e.key)&&e.key.length===2);
  const [lo,hi]=e.key.map(BigInt);
  assert(lo>=0n&&lo<1n<<64n&&hi>=0n&&hi<1n<<57n);
  assert.equal(e.unsupported_verdict,1);
  return (lo+(hi<<64n)).toString(16).padStart(32,'0');
 });
 assert.deepEqual(keys.slice().sort(),EXPECTED,'withdrawn S5 keys changed');
 for(const k of keys){
  assert(cache.has(k),'withdrawn S5 evidence missing from pinned corpus: '+k);
  assert.equal(cache.get(k),1,'withdrawn S5 polarity changed: '+k);
  cache.delete(k);
 }
 return cache;
}
module.exports={excludeQuarantined};
