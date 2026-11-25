// explicit congruence check: does some (plane-D4 image + integer translation) of A equal B?
const A = [[6,0],[5,1],[6,2],[2,6],[7,6],[10,6],[2,7],[4,7],[9,7],[2,11],[5,11]]; // W_b
const K0320n12 = [[6,0],[9,0],[2,4],[7,4],[9,4],[1,5],[4,5],[9,5],[5,9],[6,10],[5,11]]; // K0320 n=12
const B = K0320n12;
const key = (s) => JSON.stringify([...s].sort((p,q)=>p[1]-q[1]||p[0]-q[0]));
let found = [];
for (const f of [
  (x,y)=>[x,y], (x,y)=>[-x,y], (x,y)=>[x,-y], (x,y)=>[-x,-y],
  (x,y)=>[y,x], (x,y)=>[-y,x], (x,y)=>[y,-x], (x,y)=>[-y,-x],
]) {
  const img = A.map(([x,y])=>f(x,y));
  // translate img onto B: try anchoring first stone of B to each stone of img
  for (const [bx,by] of B) {
    for (const [ax,ay] of img) {
      const dx = bx-ax, dy = by-ay;
      const t = img.map(([x,y])=>[x+dx,y+dy]);
      if (key(t) === key(B)) { found.push({f: f.toString().slice(0,20), dx, dy}); }
    }
  }
}
console.log(JSON.stringify({ congruent: found.length > 0, embeddings: found.slice(0,3) }));
// and W_c vs both:
const C = [[5,1],[4,2],[5,4],[9,5],[0,6],[10,6],[4,7],[0,9],[4,9],[5,9],[11,11]];
function congr(A, B) {
  for (const f of [(x,y)=>[x,y],(x,y)=>[-x,y],(x,y)=>[x,-y],(x,y)=>[-x,-y],(x,y)=>[y,x],(x,y)=>[-y,x],(x,y)=>[y,-x],(x,y)=>[-y,-x]]) {
    const img = A.map(([x,y])=>f(x,y));
    for (const [bx,by] of B) for (const [ax,ay] of img) {
      const t = img.map(([x,y])=>[x+bx-ax,y+by-ay]);
      if (key(t) === key(B)) return true;
    }
  }
  return false;
}
console.log(JSON.stringify({ Wc_vs_K0320n12: congr(C, B), Wc_vs_Wb: congr(C, A) }));
