#!/usr/bin/env node
// Fast P(C) = S(C,C) computation for the K0859 counting recursion (uniform board).
// Two independent implementations:
//   - survivorFast: closed-form phase distribution (same dynamics as the
//     published K0926 verifier's survivor_fast)
//   - survivorVerbatim: per-stone distribution loop (K0859 verbatim twin)
// Writes JSON: {"P": [P(1),...,P(N)], "meta": {...}}
// Usage: node pc_fast.js N out.json [mode]

"use strict";

function survivorFast(C, r) {
  const active = new Int32Array(r);
  for (let i = 0; i < r; i++) active[i] = i;
  const counts = new Int32Array(r); // player index -> stones (0 for removed)
  let k = r;
  let turn = 0;
  let s = 0; // total stones held by active
  while (k > 1) {
    const ell = C - s;
    const q = Math.floor(ell / k);
    let t = ell - q * k;
    // distribute q to everyone (cyclically from turn), +1 to first t
    for (let i = 0; i < k; i++) {
      let pos = turn + i;
      if (pos >= k) pos -= k;
      counts[active[pos]] += q;
    }
    // +1 for first t positions (i in 0..t-1)
    if (t > 0) {
      if (t > k) t = k; // only happens if ell<0 would be invalid anyway
    }
    for (let i = 0; i < t; i++) {
      let pos = turn + i;
      if (pos >= k) pos -= k;
      counts[active[pos]] += 1;
    }
    s += ell;
    let li = turn + ell;
    li = li % k;
    const loser = active[li];
    s -= counts[loser];
    counts[loser] = 0;
    // remove li from active (shift left)
    for (let i = li; i < k - 1; i++) active[i] = active[i + 1];
    k -= 1;
    if (k > 0) turn = li % k;
  }
  return active[0];
}

function survivorVerbatim(C, r) {
  const active = new Int32Array(r);
  for (let i = 0; i < r; i++) active[i] = i;
  const counts = new Int32Array(r);
  let k = r;
  let turn = 0;
  let s = 0;
  while (k > 1) {
    const ell = C - s;
    for (let m = 0; m < ell; m++) {
      let pos = turn + m;
      pos %= k;
      counts[active[pos]] += 1;
    }
    s += ell;
    let li = (turn + ell) % k;
    const loser = active[li];
    s -= counts[loser];
    counts[loser] = 0;
    for (let i = li; i < k - 1; i++) active[i] = active[i + 1];
    k -= 1;
    if (k > 0) turn = li % k;
  }
  return active[0];
}

function main() {
  const N = parseInt(process.argv[2] || "300", 10);
  const outPath = process.argv[3] || "pc.json";
  const mode = process.argv[4] || "fast";
  const t0 = Date.now();
  const P = new Array(N);
  if (mode === "fast") {
    for (let C = 1; C <= N; C++) P[C - 1] = survivorFast(C, C);
  } else {
    for (let C = 1; C <= N; C++) P[C - 1] = survivorVerbatim(C, C);
  }
  const dt = Date.now() - t0;
  const fs = require("fs");
  const payload = {
    N: N,
    mode: mode,
    ms: dt,
    P: P,
  };
  fs.writeFileSync(outPath, JSON.stringify(payload));
  console.log("N=" + N + " mode=" + mode + " ms=" + dt + " -> " + outPath);
  console.log("P(1..12)=" + P.slice(0, 12).join(","));
}

main();
