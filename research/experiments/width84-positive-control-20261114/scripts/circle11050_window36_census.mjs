// 11050円の幅w窓で36点（18行）に達する窓のcensus（34点窓censusの36点版・検証用）
const pts=[];
for(let x=-15;x<=120;x++)for(let y=-15;y<=120;y++) if((2*x-105)**2+(2*y-105)**2===11050) pts.push([x,y]);
const out={};
for(let w=83;w<=92;w++){
  const win34=[],win36=[];
  for(let a=-10;a<=40;a++){
    const inW=pts.filter(p=>p[0]>=a&&p[0]<=a+w-1);
    const rows=new Set(inW.map(p=>p[0]-a));
    if(inW.length>=34&&rows.size===17) win34.push({a,pts:inW.length});
    if(inW.length>=36&&rows.size===18) win36.push({a,pts:inW.length});
  }
  out[w]={win34:win34.length,win36:win36.map(x=>({a:x.a,pts:x.pts}))};
}
console.log(JSON.stringify(out));
