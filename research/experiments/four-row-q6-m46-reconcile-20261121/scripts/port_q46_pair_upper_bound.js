#!/usr/bin/env node
// port_q46_pair_upper_bound.js — Node.js port of research/experiments/fixed-width/scripts/q46_pair_upper_bound.cpp
// (third-implementation replay of the three-occupied-rows circle-count upper bound 19 for the K0302 M_{4,6} proof).
// Vertex masks are BigInt (up to 63 coordinate vertices). Output matches the published q46_pair_upper_bound.json fields.
'use strict';

function idiv(a, b) { return Math.trunc(a / b); }   // C++ trunc division (used only on exact-divisible values or replicated checks)

function lexGreaterArr(A, B) {
  const n = Math.min(A.length, B.length);
  for (let i = 0; i < n; i++) { if (A[i] !== B[i]) return A[i] > B[i]; }
  return A.length > B.length;
}

function graphBound(rawEdges, stat) {
  const sortedEdges = rawEdges.map(e => [e[0], e[1]]).sort((a, b) => (a[0] - b[0]) || (a[1] - b[1]));
  const coordinates = [];
  for (const [u, v] of sortedEdges) { coordinates.push(u); coordinates.push(v); }
  coordinates.sort((a, b) => a - b);
  const coordIndex = new Map();
  const coordList = [];
  for (const c of coordinates) if (!coordIndex.has(c)) { coordIndex.set(c, coordList.length); coordList.push(c); }
  if (coordList.length > 63) throw new Error('coordinates exceed 63');
  const edges = [];
  const adjacency = new Array(coordList.length).fill(0n);
  for (const [a, b] of sortedEdges) {
    const u = coordIndex.get(a), v = coordIndex.get(b);
    if (edges.length && edges[edges.length - 1].u === u && edges[edges.length - 1].v === v) edges[edges.length - 1].w++;
    else edges.push({ u, v, w: 1 });
    adjacency[u] |= 1n << BigInt(v);
    adjacency[v] |= 1n << BigInt(u);
  }
  const maximum = new Array(6).fill(0);
  let frontier = [];
  for (let i = 0; i < coordList.length; i++) frontier.push(1n << BigInt(i));
  const one = 1n;
  for (let k = 2; k <= 5; k++) {
    let next = [];
    for (const vertices of frontier) {
      let neighbors = 0n;
      for (let remaining = vertices; remaining; ) {
        const low = remaining & -remaining;
        const idx = Number(low.toString(2).length - 1);
        neighbors |= adjacency[idx];
        remaining ^= low;
      }
      neighbors &= ~vertices;
      while (neighbors) {
        const low = neighbors & -neighbors;
        const i = Number(low.toString(2).length - 1);
        neighbors ^= low;
        next.push(vertices | (one << BigInt(i)));
      }
    }
    next.sort((a, b) => (a < b ? -1 : a > b ? 1 : 0));
    next = next.filter((x, i) => i === 0 || x !== next[i - 1]);
    stat.connected += next.length;
    for (const vertices of next) {
      let total = 0;
      for (const e of edges) if (((vertices >> BigInt(e.u)) & 1n) === 1n && ((vertices >> BigInt(e.v)) & 1n) === 1n) total += e.w;
      if (total > maximum[k]) maximum[k] = total;
    }
    frontier = next;
  }
  return Math.max(maximum[2], maximum[3], maximum[4], maximum[5], 2 * maximum[2], maximum[2] + maximum[3]);
}

function solve(span, t, v, w) {
  const result = { target_row: t, exterior_rows: [v, w], by_gap: Array.from({ length: 68 }, () => []), profile_count: 0, supports: 0, enumerated_graphs: 0, connected_subsets: 0, upper_bound: 0 };
  for (let db = 1; db <= span; db++) {
    for (let dc = 1; dc <= span; dc++) {
      if ((db - dc) % 2 !== 0) continue;
      const numerator = (w - t) * db * db + (t - v) * dc * dc - 4 * (t - v) * (t - w) * (w - v);
      if (numerator % (w - v) !== 0) continue;
      const square = numerator / (w - v);
      if (square <= 0) continue;
      let dt = 0;
      while ((dt + 1) * (dt + 1) <= square) ++dt;
      if (dt * dt !== square || dt > span || (dt - db) % 2 !== 0) continue;
      result.by_gap[db].push({ target: dt, b: db, c: dc });
      ++result.profile_count;
    }
  }
  const stat = { connected: 0 };
  for (let b4 = 4; b4 <= span; b4++) {
    for (let b1 = 1; b1 < b4; b1++) {
      for (let b2 = b1 + 1; b2 < b4; b2++) {
        for (let b3 = b2 + 1; b3 < b4; b3++) {
          const B = [0, b1, b2, b3, b4];
          const reflected = [0, b4 - b3, b4 - b2, b4 - b1, b4];
          if (lexGreaterArr(B, reflected)) continue;
          ++result.supports;
          const rawEdges = [];
          for (let i = 0; i < 5; i++) {
            for (let j = i + 1; j < 5; j++) {
              const sum = B[i] + B[j];
              const profs = result.by_gap[B[j] - B[i]];
              for (const p of profs) {
                const a0 = idiv(sum - p.target, 2);
                const a1 = idiv(sum + p.target, 2);
                const c0 = idiv(sum - p.c, 2);
                const c1 = idiv(sum + p.c, 2);
                if (Math.max(b4, a1, c1) - Math.min(0, a0, c0) > span) continue;
                rawEdges.push([c0, c1]);
              }
            }
          }
          if (rawEdges.length <= result.upper_bound) continue;
          ++result.enumerated_graphs;
          const gb = graphBound(rawEdges, stat);
          result.connected_subsets = stat.connected;
          if (gb > result.upper_bound) result.upper_bound = gb;
        }
      }
    }
  }
  return result;
}

function main() {
  const argv = process.argv.slice(2);
  const span = argv.length > 0 ? parseInt(argv[0], 10) : 67;
  const selectedShape = argv.length > 1 ? parseInt(argv[1], 10) : -1;
  if (span < 4 || span > 67 || selectedShape < -1 || selectedShape > 4) { process.stderr.write('Use span 4..67 and optional shape 0..4\n'); process.exit(2); }
  const shapes = [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 0, 2], [1, 0, 3]];
  const out = { maximum_horizontal_span: span, method: 'exhaustive normalized five-point supports and connected graph subsets', shapes: [] };
  for (let i = 0; i < 5; i++) {
    if (selectedShape >= 0 && selectedShape !== i) continue;
    const r = solve(span, shapes[i][0], shapes[i][1], shapes[i][2]);
    const shapeOut = {
      target_row: r.target_row, exterior_rows: r.exterior_rows, profile_count: r.profile_count,
      normalized_five_point_sets: r.supports, graphs_requiring_subset_enumeration: r.enumerated_graphs,
      connected_subsets_checked: r.connected_subsets, circle_count_upper_bound: r.upper_bound,
      chord_profiles: []
    };
    for (let gap = 1; gap <= span; gap++) for (const p of r.by_gap[gap]) shapeOut.chord_profiles.push([p.target, p.b, p.c]);
    out.shapes.push(shapeOut);
  }
  console.log(JSON.stringify(out, null, 1));
}
main();
