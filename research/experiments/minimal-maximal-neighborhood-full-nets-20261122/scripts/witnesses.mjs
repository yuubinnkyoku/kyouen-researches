// Published witnesses (explicit coordinates [x,y]) for transplant diagnostics:
// K0031 (s_7=7), K0038 (n=10 ten-stone maximal), K0320 (n=11..15, n-1 stones).

export const WITNESSES = [
  { src: "K0031", n: 7, coords: [[1,0],[2,1],[1,3],[2,3],[6,3],[2,6],[3,6]] },
  { src: "K0038", n: 10, coords: [[1,2],[7,2],[1,3],[5,3],[6,3],[6,4],[5,6],[1,8],[9,2],[8,4]] },
  { src: "K0320", n: 11, coords: [[5,0],[8,0],[1,4],[6,4],[8,4],[0,5],[3,5],[8,5],[4,9],[5,10]] },
  { src: "K0320", n: 12, coords: [[6,0],[9,0],[2,4],[7,4],[9,4],[1,5],[4,5],[9,5],[5,9],[6,10],[5,11]] },
  { src: "K0320", n: 13, coords: [[7,0],[3,2],[2,3],[9,3],[10,3],[2,4],[6,4],[11,4],[6,6],[1,10],[2,10],[7,12]] },
  { src: "K0320", n: 14, coords: [[3,1],[7,1],[10,1],[9,2],[4,3],[11,4],[7,8],[2,9],[7,9],[9,9],[2,11],[3,12],[0,13]] },
  { src: "K0320", n: 15, coords: [[7,0],[6,1],[1,3],[0,4],[3,7],[5,7],[10,7],[6,8],[12,9],[7,11],[11,11],[14,11],[6,12],[14,12]] },
];

// D4 images of a coordinate set: (x,y) -> 8 transforms on the w-box.
export function d4Images(coords, w) {
  const t = (c) => [
    [c[0], c[1]],
    [w - 1 - c[0], c[1]],
    [c[0], w - 1 - c[1]],
    [w - 1 - c[0], w - 1 - c[1]],
    [c[1], c[0]],
    [w - 1 - c[1], c[0]],
    [c[1], w - 1 - c[0]],
    [w - 1 - c[1], w - 1 - c[0]],
  ];
  const sets = new Set();
  const out = [];
  for (let i = 0; i < 8; i++) {
    const cs = coords.map((c) => t(c)[i]);
    cs.sort((a, b) => a[1] - b[1] || a[0] - b[0]);
    const key = JSON.stringify(cs);
    if (!sets.has(key)) { sets.add(key); out.push(cs); }
  }
  return out;
}
