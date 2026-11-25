#!/usr/bin/env node
'use strict';
// This is a structural union audit, not an independent terminal verdict checker.
function audit(data) {
  const N=11, MASKS=Array.from({length:8},()=>[]);
  const assert=(ok,msg)=>{if(!ok)throw Error(msg)};
  for(let p=0;p<121;p++){
    const x=p%11,y=Math.floor(p/11);
    const a=[[x,y],[10-y,x],[10-x,10-y],[y,10-x],[10-x,y],[10-y,10-x],[x,10-y],[y,x]];
    for(let t=0;t<8;t++)MASKS[t][p]=1n<<BigInt(11*a[t][1]+a[t][0]);
  }
  function points(b){const a=[];for(let i=0;i<121;i++)if(b&(1n<<BigInt(i)))a.push(i);return a}
  function key(b){return b.toString(16).padStart(32,'0')}
  function canonical(b){
    const a=points(b);let best=null;
    for(const map of MASKS){let v=0n;for(const p of a)v|=map[p];if(best===null||v<best)best=v}
    return best;
  }
  function circle(a,b,c,d){
    const X=d%11,Y=Math.floor(d/11);
    const v=[a,b,c].map(p=>{const x=p%11,y=Math.floor(p/11);return [x-X,y-Y,x*x+y*y-X*X-Y*Y]});
    const [u,w,z]=v;
    return u[0]*(w[1]*z[2]-w[2]*z[1])
          -u[1]*(w[0]*z[2]-w[2]*z[0])
          +u[2]*(w[0]*z[1]-w[1]*z[0])===0;
  }
  function safe(b){
    const a=points(b);
    for(let i=0;i<a.length-3;i++)for(let j=i+1;j<a.length-2;j++)
      for(let k=j+1;k<a.length-1;k++)for(let l=k+1;l<a.length;l++)
        if(circle(a[i],a[j],a[k],a[l]))return false;
    return true;
  }
  function parse(text,label){
    const a=text.trim().split(/\s+/);
    assert(a.length>0&&a.every(s=>/^[0-9a-f]{32}$/.test(s)),'bad keys: '+label);
    assert(a.every((s,i)=>i===0||a[i-1]<s),'unsorted/duplicate: '+label);
    return a.map(s=>BigInt('0x'+s));
  }
  function reverse(boards){
    const out=new Map();
    for(const b of boards)for(const p of points(b)){
      const c=canonical(b^(1n<<BigInt(p)));out.set(key(c),c);
    }
    return out;
  }
  const old=JSON.parse(data.oldCert);
  const roots=data.winGroups.flatMap((text,i)=>parse(text,'WIN9 '+i))
                   .concat(old.new_s9_win.map(s=>BigInt('0x'+s)));
  assert(roots.length===120&&new Set(roots.map(key)).size===120,'S9 union changed');
  for(const b of roots)assert(points(b).length===9&&canonical(b)===b&&safe(b),'bad WIN9 '+key(b));
  const loss8=parse(data.loss35,'LOSS8 35').concat(old.s8_loss.map(s=>BigInt('0x'+s)));
  assert(loss8.length===38&&new Set(loss8.map(key)).size===38,'S8 LOSS union changed');
  for(const b of loss8)assert(points(b).length===8&&canonical(b)===b&&safe(b),'bad LOSS8 '+key(b));
  const win8=reverse(roots),s7=reverse(win8.values()),loss7=reverse(loss8);
  const loss8keys=new Set(loss8.map(key));
  assert(![...win8.keys()].some(k=>loss8keys.has(k)),'S8 WIN/LOSS conflict');
  let legalEdges=0,coveredEdges=0,distinctLegalEdges=0,distinctCoveredEdges=0,knownLoss=0,closed=0;
  const rows=[];
  for(const b of s7.values()){
    const a=points(b),tri=[];
    for(let i=0;i<5;i++)for(let j=i+1;j<6;j++)for(let k=j+1;k<7;k++)
      tri.push([a[i],a[j],a[k]]);
    let legal=0,covered=0;const childKeys=new Set(),coveredKeys=new Set();
    for(let p=0;p<121;p++){
      if(a.includes(p)||tri.some(q=>circle(q[0],q[1],q[2],p)))continue;
      const child=key(canonical(b|(1n<<BigInt(p))));
      legal++;childKeys.add(child);
      if(win8.has(child)){covered++;coveredKeys.add(child)}
    }
    const isLoss=loss7.has(key(b));
    if(isLoss)knownLoss++;
    if(covered===legal)closed++;
    legalEdges+=legal;coveredEdges+=covered;
    distinctLegalEdges+=childKeys.size;distinctCoveredEdges+=coveredKeys.size;
    rows.push({key:key(b),legal,covered,gap:legal-covered,
      distinctLegal:childKeys.size,distinctCovered:coveredKeys.size,
      distinctGap:childKeys.size-coveredKeys.size,knownLoss:isLoss});
  }
  const active=rows.filter(x=>!x.knownLoss).sort((a,b)=>
    a.distinctGap-b.distinctGap||b.distinctCovered-a.distinctCovered||(a.key<b.key?-1:a.key>b.key?1:0));
  const oldS7=rows.find(x=>x.key==='00000000100000021081000020000020');
  assert(oldS7&&oldS7.knownLoss&&oldS7.legal===36&&oldS7.covered===33,'known LOSS7 changed');
  assert(win8.size===961&&s7.size===3337&&loss7.size===268&&knownLoss===15&&
    legalEdges===209225&&coveredEdges===7690&&
    distinctLegalEdges===209205&&distinctCoveredEdges===7688&&closed===0,'union totals changed');
  assert(active[0].distinctGap===18&&
    active[0].key==='00000010001000009200001000100000',
    'minimum distinct-class gap changed');
  return {s9WinRoots:roots.length,s8WinUnion:win8.size,s8LossRoots:loss8.length,
    s7KnownLossAll:loss7.size,s7Candidates:s7.size,s7KnownLossWithinCandidates:knownLoss,
    s7UnclassifiedCandidates:active.length,s7LegalEdges:legalEdges,
    s7SecuredWinEdges:coveredEdges,s7DistinctLegalClassEdges:distinctLegalEdges,
    s7DistinctSecuredClassEdges:distinctCoveredEdges,s7NewClosedByAllWinChildren:closed,
    minGapExcludingKnownLoss:Math.min(...active.map(x=>x.gap)),
    minDistinctGapExcludingKnownLoss:active[0].distinctGap,topUnclassified:active.slice(0,12),
    emptyBoard:'UNKNOWN'};
}
if(typeof module!=='undefined'&&require.main===module){
  const fs=require('node:fs'),path=require('node:path');
  const exp=path.resolve(__dirname,'../');
  const groups=[
    'n11-s9-win29-lift-20261023/s9-win29.keys',
    'n11-s9-win27-expansion-20261024/s9-win27.keys',
    'n11-s9-win2-followup-20261024/s9-win2.keys',
    'n11-s9-win10-20261024/s9-win10.keys',
    'n11-s9-win7-expansion-20261024/s9-win7.keys',
    'n11-s9-win20-neighbor-20261024/s9-win20.keys',
    'n11-s8-frontier-13way-20261024/s9-win7.keys'];
  const read=p=>fs.readFileSync(path.join(exp,p),'utf8');
  const data={winGroups:groups.map(read),
    oldCert:read('n11-s7-terminal-loss12-20261024/certificate.json'),
    loss35:read('n11-s8-compact385-pruned1946-20261020/loss_roots35.txt')};
  console.log(JSON.stringify(audit(data),null,2));
}
