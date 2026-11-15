#!/usr/bin/env node
// census4_check.js — C4-style census-completeness control for surgery4.js:
// buildCensus4(w,m,q) must produce EXACTLY the same curve point-set family as
// sat.js all-triples buildCensus(w,m,q) (lines + circles, >= q window points).
// PASS at the listed (w,m,q) licenses surgery4.js surgery runs at those families.
"use strict";
const S = require("./sat.js");
const { buildCensus4 } = require("./surgery4.js");
const cases = process.argv.slice(2).map(a => a.split(",").map(Number));
let allPass = true;
for (const [w, m, q] of cases) {
  const sat = S.buildCensus(w, m, q);
  const satKeys = new Set();
  for (const cu of sat.curves) satKeys.add(cu.pts.join(","));
  const c4 = buildCensus4(w, m, q);
  const c4Keys = new Set();
  for (const cu of c4.curves) c4Keys.add(Array.from(cu).join(","));
  const onlySat = [...satKeys].filter(k => !c4Keys.has(k));
  const onlyC4 = [...c4Keys].filter(k => !satKeys.has(k));
  const pass = onlySat.length === 0 && onlyC4.length === 0 && satKeys.size === c4Keys.size;
  if (!pass) allPass = false;
  console.log(JSON.stringify({ w, m, q, satCurves: satKeys.size, c4Curves: c4Keys.size, c4Circles: c4.nCirc, onlySat: onlySat.length, onlyC4: onlyC4.length, pass }));
  if (!pass && onlySat.length) console.log("  sample onlySat:", onlySat[0]);
  if (!pass && onlyC4.length) console.log("  sample onlyC4:", onlyC4[0]);
}
console.log(JSON.stringify({ event: "summary", allPass, nCases: cases.length }));
process.exit(allPass ? 0 : 1);
