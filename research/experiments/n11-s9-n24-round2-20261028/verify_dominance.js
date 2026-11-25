#!/usr/bin/env node
'use strict';
// Independent finite regression for the dominance reduction in plan_next.js.
// This proves only that the small-instance lexicographic selection objective
// is preserved; it does NOT classify any 11x11 game position.
const {pruneDominated,popcount}=require('./plan_next.js');
const need=(v,m)=>{if(!v)throw Error(m);};
function optimum(rows,limit){
  let bestCoverage=-1,bestCost=Infinity;
  for(let subset=0;subset<(1<<rows.length);subset++){
    if(popcount(BigInt(subset))>limit)continue;
    let covered=0n,cost=0;
    for(let i=0;i<rows.length;i++)if(subset&(1<<i)){
      covered|=rows[i].mask;cost+=rows[i].children;
    }
    const n=popcount(covered);
    if(n>bestCoverage||(n===bestCoverage&&cost<bestCost)){
      bestCoverage=n;bestCost=cost;
    }
  }
  return [bestCoverage,bestCost];
}
function check(rows){
  const reduced=pruneDominated(rows);
  for(const limit of [1,2,3]){
    const before=optimum(rows,limit),after=optimum(reduced,limit);
    need(before[0]===after[0]&&before[1]===after[1],
      'dominated pruning changed exact optimum '+JSON.stringify({
        rows:rows.map(x=>({...x,mask:String(x.mask)})),limit,before,after
      }));
  }
}
let checked=0;
for(let a=1;a<=7;a++)for(let b=1;b<=7;b++)for(let c=1;c<=7;c++)
  for(let x=1;x<=3;x++)for(let y=1;y<=3;y++)for(let z=1;z<=3;z++){
    check([{h:'a',mask:BigInt(a),children:x},
      {h:'b',mask:BigInt(b),children:y},
      {h:'c',mask:BigInt(c),children:z}]);
    checked++;
  }
// Additional deterministic four-candidate cases exercise longer chains.
let seed=10091;
function rand(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed;}
for(let t=0;t<5000;t++){
  const rows=Array.from({length:4},(_,i)=>({
    h:String(i),mask:BigInt(1+rand()%31),children:1+rand()%6
  }));
  check(rows);checked++;
}
console.log(JSON.stringify({verified:true,smallInstanceFamilies:checked,
  objective:'max potential coverage, then min S10 child cost',
  board11Winner:'UNKNOWN'}));
