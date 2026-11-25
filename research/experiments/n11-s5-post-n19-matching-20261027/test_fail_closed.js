#!/usr/bin/env node
'use strict';
// Standalone matching audit must terminal-replay every S9 proof in its dependency chain.
// A balanced metadata tamper passes structural census but must fail terminal replay.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const audit=require('./audit.js');
const modules=[
 ['degree2','../n11-s9-degree2-terminal-20261027/verify.js'],
 ['short13','../n11-s9-degree2-short-terminal-20261027/verify.js'],
 ['short46','../n11-s9-short46-terminal-20261027/verify.js'],
 ['short18','../n11-s9-short18-terminal-20261027/verify.js'],
 ['n19','../n11-s9-n19-terminal-20261027/verify.js'],
];
const seen=new Map(),restores=[];
for(const [name,file] of modules){
 const mod=require(file),original=mod.verify;
 assert.equal(typeof original,'function',name+' verifier missing');
 seen.set(name,0);
 mod.verify=function(rows,opts){
  assert.equal(opts?.terminal,true,name+' audit accepted a non-terminal certificate');
  seen.set(name,seen.get(name)+1);
  return original.apply(this,arguments);
 };
 restores.push(()=>{mod.verify=original;});
}
let result;
try{
 result=audit.audit(process.argv.includes('--negative'));
 for(const [name] of modules)assert.ok(seen.get(name)>0,name+' was not independently replayed');
}finally{
 for(const restore of restores.reverse())restore();
}
if(process.argv.includes('--negative')){
 const proof=require('../n11-s9-n19-terminal-20261027/verify.js');
 const cert=fs.readFileSync(path.join(__dirname,'../n11-s9-n19-terminal-20261027/certificate.tsv'),'utf8');
 const originalA='00008000400000821084000400000020 19 883';
 const originalB='00000000000000821080840040400020 19 1527';
 assert.ok(cert.includes(originalA)&&cert.includes(originalB),'witness metadata changed');
 const altered=cert.replace(originalA,originalA.replace('883','884'))
                   .replace(originalB,originalB.replace('1527','1526'));
 const rows=proof.parse(altered);
 assert.equal(proof.verify(rows,{terminal:false}).newS9Win,55,
  'balanced metadata corruption should pass the structure-only check');
 assert.throws(()=>proof.verify(rows,{terminal:true}),/terminal state count changed/,
  'balanced metadata corruption must fail independent terminal replay');
 console.error('PASS five fail-closed terminal gates and balanced-state metadata rejection');
}
console.log(JSON.stringify(result));
