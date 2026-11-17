#!/usr/bin/env node
// Reduced-game engines U(m) and V(m) for the K0859 counting recursion.
//   U(m): m players (indices 0..m-1) each holding 2 stones, pot 2, pointer 0.
//   V(m): m players each holding 2 stones, pot 1, pointer 0.
// Stretch-1 reductions (proved in the report):
//   P(2m+2) = 3 + 2*U(m)   (even C >= 4)
//   P(2m+1) = 1 + 2*V(m)   (odd  C >= 3)
// The game: total stones T = 2m+pot is invariant. Each phase: deal `pot`
// stones one by one starting at the pointer; eliminate the next player;
// pot <- that player's holdings (post-deal); pointer <- player after them.
// Same dynamics as survivor_fast of the K0859 recursion restricted to the
// reduced state (independent implementation: no `ell = C - s` recomputation,
// works on a different state space).
"use strict";

function reducedSurvivor(m, pot0) {
  const active = new Int32Array(m);
  for (let i = 0; i < m; i++) active[i] = i;
  const counts = new Int32Array(m).fill(2);
  let k = m;
  let ptr = 0; // position in active
  let pot = pot0;
  while (k > 1) {
    // deal pot stones starting at position ptr
    let p = pot;
    let pos = ptr;
    while (p > 0) {
      counts[active[pos]] += 1;
      pos = pos + 1;
      if (pos === k) pos = 0;
      p--;
    }
    // eliminate player at position pos
    const loser = active[pos];
    pot = counts[loser];
    counts[loser] = 0;
    for (let i = pos; i < k - 1; i++) active[i] = active[i + 1];
    k -= 1;
    ptr = pos % k;
  }
  return active[0];
}

function main() {
  const M = parseInt(process.argv[2] || "4000", 10);
  const outPath = process.argv[3] || "pc_reduced.json";
  const t0 = Date.now();
  const U = new Array(M);
  const V = new Array(M);
  for (let m = 1; m <= M; m++) {
    U[m - 1] = reducedSurvivor(m, 2);
    V[m - 1] = reducedSurvivor(m, 1);
  }
  const fs = require("fs");
  fs.writeFileSync(outPath, JSON.stringify({
    M: M, ms: Date.now() - t0, U: U, V: V,
  }));
  console.log("M=" + M + " ms=" + (Date.now() - t0) + " -> " + outPath);
  console.log("U(1..10)=" + U.slice(0, 10).join(","));
  console.log("V(1..10)=" + V.slice(0, 10).join(","));
}
main();
