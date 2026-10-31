'use strict';
// Necessary dual-tight matching test for 31-class geometric covers.
// A deficient dual graph gives a directly checkable Tutte obstruction.
const fs=require('node:fs'),zlib=require('node:zlib'),assert=require('node:assert/strict');
const {witnesses,canonical,maps}=require('./audit_win4_exclusion');
const cert=JSON.parse(zlib.gunzipSync(Buffer.from(
  fs.readFileSync(__dirname+'/certificate.json.gz.b64','utf8').trim(),'base64')));
const REPS=[16,38,49,24,0,48,12,5,36];
function det(p){
  const a=p.map(i=>{const x=i%11,y=Math.floor(i/11);return[x*x+y*y,x,y]});
  const b=a.slice(1).map(row=>row.map((v,j)=>v-a[0][j]));
  return b[0][0]*(b[1][1]*b[2][2]-b[1][2]*b[2][1])
    -b[0][1]*(b[1][0]*b[2][2]-b[1][2]*b[2][0])
    +b[0][2]*(b[1][0]*b[2][1]-b[1][1]*b[2][0]);
}
function cover(p,a){
  let m=0n;
  for(const t of maps){
    const q=p.map(x=>t[x]);
    if(q.includes(a)&&q.includes(60))
      for(const x of q)if(x!==a&&x!==60)m|=1n<<BigInt(x);
  }
  return m;
}
function pop(n){let c=0;while(n){n&=n-1n;c++}return c}
function maximumMatching(g){
  const n=g.length,match=Array(n).fill(-1);
  function find(root){
    const used=Array(n).fill(false),p=Array(n).fill(-1);
    const base=Array.from({length:n},(_,i)=>i),q=[root];
    used[root]=true;
    function lca(a,b){
      const seen=Array(n).fill(false);
      while(true){a=base[a];seen[a]=true;if(match[a]===-1)break;a=p[match[a]]}
      while(true){b=base[b];if(seen[b])return b;b=p[match[b]]}
    }
    function mark(v,b,child,blossom){
      while(base[v]!==b){
        blossom[base[v]]=true;blossom[base[match[v]]]=true;
        p[v]=child;child=match[v];v=p[match[v]];
      }
    }
    for(let qi=0;qi<q.length;qi++){
      const v=q[qi];
      for(const u of g[v]){
        if(base[v]===base[u]||match[v]===u)continue;
        if(u===root||(match[u]!==-1&&p[match[u]]!==-1)){
          const b=lca(v,u),blossom=Array(n).fill(false);
          mark(v,b,u,blossom);mark(u,b,v,blossom);
          for(let i=0;i<n;i++)if(blossom[base[i]]){
            base[i]=b;if(!used[i]){used[i]=true;q.push(i)}
          }
        }else if(p[u]===-1){
          p[u]=v;
          if(match[u]===-1){
            let x=u;
            while(x!==-1){
              const pv=p[x],nv=pv===-1?-1:match[pv];
              match[x]=pv;if(pv!==-1)match[pv]=x;x=nv;
            }
            return true;
          }
          used[match[u]]=true;q.push(match[u]);
        }
      }
    }
    return false;
  }
  for(let i=0;i<n;i++)if(match[i]===-1)find(i);
  for(let i=0;i<n;i++)if(match[i]!==-1)assert.equal(match[match[i]],i);
  return {size:match.filter(x=>x!==-1).length/2,match};
}
function oddComponents(g,deleted){
  const n=g.length,used=new Set(deleted),sizes=[];
  for(let i=0;i<n;i++)if(!used.has(i)){
    const q=[i];used.add(i);
    for(let k=0;k<q.length;k++)for(const j of g[q[k]])
      if(!used.has(j)){used.add(j);q.push(j)}
    sizes.push(q.length);
  }
  return sizes.filter(x=>x%2).length;
}
function barrier(g,matchingSize){
  const n=g.length,D=new Set();
  for(let v=0;v<n;v++){
    const rest=Array.from({length:n},(_,i)=>i).filter(i=>i!==v);
    const idx=new Map(rest.map((x,i)=>[x,i]));
    const sub=rest.map(x=>g[x].filter(y=>y!==v).map(y=>idx.get(y)));
    if(maximumMatching(sub).size===matchingSize)D.add(v);
  }
  const A=new Set();
  for(const v of D)for(const u of g[v])if(!D.has(u))A.add(u);
  const odd=oddComponents(g,A);
  if(odd> A.size)return {vertices:[...A].sort((a,b)=>a-b),oddComponents:odd,barrierSize:A.size};
  return null;
}
// Compare blossom against brute-force perfect matching on all graphs of n=5.
function brute(g){
  const n=g.length, memo=new Map();
  function f(mask){
    if(!mask)return 0;
    if(memo.has(mask))return memo.get(mask);
    const v=Array.from({length:n},(_,i)=>i).find(i=>mask&(1<<i));
    let best=f(mask&~(1<<v));
    for(const u of g[v])if(mask&(1<<u))best=Math.max(best,1+f(mask&~(1<<v)&~(1<<u)));
    memo.set(mask,best);return best;
  }
  return f((1<<n)-1);
}
for(let mask=0;mask<1<<10;mask++){
  const g=Array.from({length:5},()=>[]);
  let k=0;
  for(let i=0;i<5;i++)for(let j=i+1;j<5;j++,k++)if(mask&(1<<k)){
    g[i].push(j);g[j].push(i);
  }
  assert.equal(maximumMatching(g).size,brute(g));
}
const results=[];
for(const a of REPS){
  const row=cert.roots.find(x=>x.first===a);
  assert(row&&row.minimum_classes===31);
  const dual=Object.keys(row.dual_numerators).map(Number).sort((x,y)=>x-y);
  assert.equal(dual.length,62);
  const idx=new Map(dual.map((x,i)=>[x,i]));
  const dualMask=dual.reduce((m,x)=>m|1n<<BigInt(x),0n);
  const seen=new Set(),edges=new Set();
  for(let c=0;c<121;c++)if(c!==a&&c!==60)
    for(let d=c+1;d<121;d++)if(d!==a&&d!==60){
      const p=[a,60,c,d];if(det(p)===0)continue;
      const key=canonical(p);if(seen.has(key))continue;seen.add(key);
      if(witnesses.has(key))continue;
      const m=cover(p,a)&dualMask;if(pop(m)!==2)continue;
      const v=dual.filter(x=>m&(1n<<BigInt(x))).map(x=>idx.get(x));
      edges.add(v[0]+','+v[1]);
    }
  const g=Array.from({length:62},()=>[]);
  for(const edge of edges){
    const [u,v]=edge.split(',').map(Number);g[u].push(v);g[v].push(u);
  }
  const matching=maximumMatching(g);
  const obstruction=matching.size<31?barrier(g,matching.size):null;
  if(matching.size<31)assert(obstruction,'missing Tutte barrier');
  if(obstruction){
    const del=new Set(obstruction.vertices);
    assert(oddComponents(g,del)>del.size);
  }
  results.push({first:a,dualVertices:62,dualEdges:edges.size,
    maxMatching:matching.size,hasPerfectMatching:matching.size===31,
    obstruction:obstruction?{dualThirds:obstruction.vertices.map(i=>dual[i]),
      oddComponents:obstruction.oddComponents,barrierSize:obstruction.barrierSize}:null});
}
console.log(JSON.stringify({schema:'n11-central-dual-tight-matching-v1',
  roots:results,emptyBoard:'UNKNOWN',
  note:'Matching is necessary, not sufficient, for a WIN4-safe 31-cover.'},null,2));
