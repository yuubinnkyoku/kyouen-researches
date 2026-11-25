// verify_bit7_win7_cert.ts (session 7, 2026-11-13) — independent certificate auditor,
// TypeScript port of research/experiments/n11-central-19-cover-20261031/verify_five_terminal_loss7.py
// adapted for the WIN7 orientation (original_first_WIN7 second_to_move_LOSS).
//
// INDEPENDENCE: no engine import, no verdict cache. All legal replies are recomputed with
// an exact 4x4 integer Bareiss determinant (number arithmetic: every intermediate is a
// kxk minor of a matrix whose row norms are <= sqrt(201); the Hadamard bound keeps all
// values far below 2^53, and Bareiss divisions are checked exact — identical results to
// the BigInt reference port used during session 7, which itself matches the Python
// verifier's exact-integer arithmetic).
//
// VERIFIED TARGET (see output/class4-batch1-bit7-certificate.json for the full record):
//   root 00000000020000003800000080080080 (S6 child 00000000020000003800000080080000 + 7th stone bit 7)
//   certificate: output/class4-batch1-certificates/n11_s7_00000000020000003800000080080080.cert
//   verdict: original_first_WIN7 second_to_move_LOSS — the 7th-stone player (winner_parity=1)
//   forces a win against every defense; terminals are loser-stuck positions (13..17 stones).
//
// METHOD. A full-tree single-root verification of a 30,947-row certificate does not fit the
// sandbox memory cap, so the traversal is decomposed exactly like the chunk proof: from the
// main root (loser to move, depth 0) every legal first move m is enumerated; the sub-root
// root|m (8 stones, winner to move, winner_parity=0 locally) is verified independently.
// Every winner state visited must have a strategy row whose move is legal; every loser
// state expands ALL legal replies; terminals must be loser-stuck. The union of consumed
// winner states over the 50 sub-roots must equal the certificate's row set exactly
// (unreachable or missing rows are rejected), and the per-sub-root statistics are recorded.
// Turn parity is a function of the stone count only, so the decomposition is sound.
//
// RESULT (session 7 runs V1..V7): all 50 sub-roots PASS; union of consumed winner states =
// 30,947 = the full row set (comm both directions empty); root checks PASS (7 stones, no 4
// cocircular points, loser mobility exactly 50). Control: the same verifier port accepted a
// fresh extraction on the published pilot root 00000000000000a03808100000000000
// (winner_parity=0, 2,510 rows, terminals [14,16]) and its number-arithmetic det4 matches
// the BigInt reference on all 84 triples of the diagnostic position root+8+21.
//
// CLI (zero dependencies, node --experimental-strip-types):
//   node --experimental-strip-types verify_bit7_win7_cert.ts --cert <cert file> --subroots 0,8,10
//   node --experimental-strip-types verify_bit7_win7_cert.ts --cert <cert file> --root-check
// With --subroots, prints per-sub-root stats and the consumed winner-state keys (hex) so the
// caller can accumulate the union across batches and compare against the certificate keys.

// NOTE (2026-11-14 repair): this module is ESM (top-level exports), so the CLI block's
// require('fs') was undefined under --experimental-strip-types; replaced with a
// top-level fs import.
import fs from 'fs';
const N = 121;
function require(cond: boolean, reason: string): void { if (!cond) throw new Error(reason); }
export function det4(points: number[]): number {
  const a: number[][] = points.map(p => { const x = p % 11, y = Math.floor(p / 11); return [x*x+y*y, x, y, 1]; });
  let sign = 1, divisor = 1;
  for (let k = 0; k < 3; k++) {
    if (a[k][k] === 0) { let sw = false;
      for (let j = k+1; j < 4; j++) if (a[j][k] !== 0) { const t = a[k]; a[k] = a[j]; a[j] = t; sign = -sign; sw = true; break; }
      if (!sw) return 0; }
    const pivot = a[k][k];
    for (let i = k+1; i < 4; i++) { for (let j = k+1; j < 4; j++) {
      const v = a[i][j]*pivot - a[i][k]*a[k][j];
      require(v % divisor === 0, 'non-integral Bareiss step');
      a[i][j] = v / divisor; } a[i][k] = 0; }
    divisor = pivot;
  }
  return sign * a[3][3];
}
const fbtCache = new Map<number, bigint>();
export function forbiddenByTriple(a: number, b: number, c: number): bigint {
  const key = a * 14641 + b * 121 + c;
  let m = fbtCache.get(key);
  if (m !== undefined) return m;
  if (fbtCache.size > 25000) fbtCache.clear();
  m = 0n;
  for (let d = 0; d < N; d++) if (d !== a && d !== b && d !== c && det4([a,b,c,d]) === 0) m |= 1n << BigInt(d);
  fbtCache.set(key, m);
  return m;
}
const FULL = (1n << 121n) - 1n;
export function pointsOf(mask: bigint): number[] {
  const pts: number[] = [];
  for (let i = 0; i < N; i++) if ((mask >> BigInt(i)) & 1n) pts.push(i);
  return pts;
}
export function legalOfPts(pts: number[]): bigint {
  let banned = 0n;
  for (const p of pts) banned |= 1n << BigInt(p);
  for (let i = 0; i < pts.length; i++)
    for (let j = i+1; j < pts.length; j++)
      for (let l = j+1; l < pts.length; l++)
        banned |= forbiddenByTriple(pts[i], pts[j], pts[l]);
  return FULL & ~banned;
}
export function verifySubRoot(strat: Map<string, number>, subRootHex: string) {
  const v = BigInt('0x' + subRootHex);
  const pts = pointsOf(v);
  require(pts.length === 8, 'sub-root must have 8 stones');
  const seen = new Set<string>();
  const consumed: string[] = [];
  const terminals: number[] = [];
  let opponentEdges = 0;
  const stack: [bigint, number][] = [[v, 0]];
  while (stack.length) {
    const [board, depth] = stack.pop()!;
    const hex = board.toString(16).padStart(32, '0');
    if (seen.has(hex)) continue;
    seen.add(hex);
    const bpts = pointsOf(board);
    const options = legalOfPts(bpts);
    if (options === 0n) {
      require(depth % 2 !== 0, 'winning player has no move');
      require(!strat.has(hex), 'terminal has strategy move');
      terminals.push(bpts.length);
      continue;
    }
    if (depth % 2 === 0) {
      const mv = strat.get(hex);
      require(mv !== undefined, 'missing winning-player move at ' + hex);
      require((options >> BigInt(mv)) & 1n, 'illegal strategy move at ' + hex);
      consumed.push(hex);
      stack.push([board | (1n << BigInt(mv)), depth + 1]);
    } else {
      require(!strat.has(hex), 'strategy provided on opponent turn');
      let opts = options;
      while (opts !== 0n) { const bit = opts & -opts; opts -= bit; opponentEdges++;
        stack.push([board | bit, depth + 1]); }
    }
  }
  return { seen: seen.size, consumed, terminals: terminals.length, opponentEdges,
    terminalMin: Math.min(...terminals), terminalMax: Math.max(...terminals) };
}
export function rootChecks(certRootHex: string) {
  const pts: number[] = [];
  const v = BigInt('0x' + certRootHex);
  for (let i = 0; i < N; i++) if ((v >> BigInt(i)) & 1n) pts.push(i);
  require(pts.length === 7, 'root must have 7 stones');
  for (let i = 0; i < 7; i++) for (let j = i+1; j < 7; j++) for (let l = j+1; l < 7; l++) for (let q = l+1; q < 7; q++)
    require(det4([pts[i], pts[j], pts[l], pts[q]]) !== 0, 'illegal root: 4 cocircular');
  const options = legalOfPts(pts);
  let cnt = 0; { let o = options; while (o !== 0n) { o &= o - 1n; cnt++; } }
  return { stones: 7, loserMobility: cnt };
}
export function parseCert(text: string, expectedRootHex: string) {
  const lines = text.split('\n').filter(s => s.trim() !== '');
  require(lines[0] === 'n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS', 'wrong certificate header');
  require(lines[1] === 'root ' + expectedRootHex, 'wrong certificate root');
  let prev = '';
  const strat = new Map<string, number>();
  for (const ln of lines.slice(2)) {
    const parts = ln.split(' ');
    require(parts.length === 2, 'bad strategy row');
    const [k, mv] = parts;
    require(k.length === 32 && /^[0-9a-f]+$/.test(k), 'bad board encoding');
    require(k > prev, 'unsorted or duplicate board');
    prev = k;
    require(/^\d+$/.test(mv) && Number(mv) < N, 'bad move');
    require(BigInt('0x' + k) <= FULL, 'out-of-board bit');
    strat.set(k, Number(mv));
  }
  return strat;
}

if (typeof process !== 'undefined' && process.argv && process.argv[1] && process.argv[1].endsWith('verify_bit7_win7_cert.ts')) {
  const arg = (name: string, dflt: string) => { const i = process.argv.indexOf('--'+name); return i >= 0 ? process.argv[i+1] : dflt; };
  const cert = fs.readFileSync(arg('cert', ''), 'utf8');
  const strat = parseCert(cert, arg('root', '00000000020000003800000080080080'));
  const rootV = BigInt('0x' + arg('root', '00000000020000003800000080080080'));
  if (process.argv.includes('--root-check')) {
    process.stdout.write(JSON.stringify(rootChecks(arg('root', '00000000020000003800000080080080'))) + '\n');
  }
  const subs = arg('subroots','').split(',').filter(s=>s!=='').map(Number);
  const consumed: string[] = [];
  const stats: Record<string, any> = {};
  for (const m of subs) {
    const subHex = (rootV | (1n << BigInt(m))).toString(16).padStart(32, '0');
    const st = verifySubRoot(strat, subHex);
    stats['m' + m] = { seen: st.seen, terminals: st.terminals, opponentEdges: st.opponentEdges, range: [st.terminalMin, st.terminalMax] };
    consumed.push(...st.consumed);
  }
  process.stdout.write(JSON.stringify({ rows: strat.size, stats }) + '\n');
  if (arg('consumed-out', '')) fs.appendFileSync(arg('consumed-out',''), consumed.join('\n') + '\n');
}
