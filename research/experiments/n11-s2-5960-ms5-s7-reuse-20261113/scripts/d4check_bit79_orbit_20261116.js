// Independent D4 canonicalization, 11x11, bit = y*11+x, exact BigInt.
const N = 11;
function hexToBitset(h) { return BigInt('0x' + h); }
function bitsetToHex(b) { return b.toString(16).padStart(32, '0'); }
function bits(b) { const r = []; for (let i = 0n; i < 128n; i++) if ((b >> i) & 1n) r.push(Number(i)); return r; }
function bitset(list) { let b = 0n; for (const i of list) b |= 1n << BigInt(i); return b; }
// D4 transforms on (x,y): identity, rot90, rot180, rot270, flipX, flipY, flipDiag, flipAntiDiag
const T = [
  (x,y)=>[x,y], (x,y)=>[N-1-y,x], (x,y)=>[N-1-x,N-1-y], (x,y)=>[y,N-1-x],
  (x,y)=>[N-1-x,y], (x,y)=>[x,N-1-y], (x,y)=>[y,x], (x,y)=>[N-1-y,N-1-x]
];
function d4Images(h) {
  const b = hexToBitset(h); const pts = bits(b).map(i => [i % N, Math.floor(i / N)]);
  return T.map(t => bitset(pts.map(([x,y]) => { const [nx,ny] = t(x,y); return ny*N + nx; })));
}
function canon(h) { return d4Images(h).reduce((m, b) => (bitsetToHex(b) < m ? bitsetToHex(b) : m), 'ffffffffffffffffffffffffffffffff'); }
const a = '00000000000080809102000080000000'; // 65f bit-79 root (published cert, win13 manifest)
const b = '00000002000000809102000800000000'; // 63a bit-97 root (cost-63a sweep, claimed same orbit)
// sanity: popcounts
const pa = bits(hexToBitset(a)).length, pb = bits(hexToBitset(b)).length;
const ca = canon(a), cb = canon(b);
console.log(JSON.stringify({ popcount_a: pa, popcount_b: pb, canon_a: ca, canon_b: cb, same_orbit: ca === cb }, null, 1));
