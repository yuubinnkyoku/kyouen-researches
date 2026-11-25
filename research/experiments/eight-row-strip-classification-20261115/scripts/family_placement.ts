// family_placement.ts — in-board point counts n(u,m) for the nine census family
// geometries (the complete list of >=10-strip-point circle configs for m <= 984,
// per Theorem A — see ../output/stripsearch-w8-umax2100.json), and band-wide
// verification of the census counting formulas.
// Executed in full on 2026-11-15: all 976 widths m = 9..984 checked, 0 failures.
// Output: ../output/family-placement-m22-984.json.

const fams = [
  { name: "F1", R: 50, v0: 7, rows: [0, 1, 3, 4, 6, 7] },
  { name: "F2", R: 50, v0: 5, rows: [0, 2, 3, 5, 6] },
  { name: "F3", R: 50, v0: 9, rows: [1, 2, 4, 5, 7] },
  { name: "F4", R: 130, v0: 11, rows: [0, 1, 2, 4, 7] },
  { name: "F5", R: 130, v0: 3, rows: [0, 3, 5, 6, 7] },
  { name: "F6", R: 170, v0: 1, rows: [0, 1, 4, 6, 7] },
  { name: "F7", R: 170, v0: 13, rows: [0, 1, 3, 6, 7] },
  { name: "F8", R: 650, v0: 25, rows: [0, 1, 3, 4, 7] },
  { name: "F9", R: 650, v0: -11, rows: [0, 3, 4, 6, 7] }
];

// doubled chord c_y = sqrt(R - (2y - v0)^2), verified exact & odd for every row
for (const f of fams) {
  f.chords = f.rows.map((y: number) => {
    const n = f.R - (2 * y - f.v0) * (2 * y - f.v0);
    const r = Math.round(Math.sqrt(n));
    if (r * r !== n || r % 2 === 0) throw new Error("chord fail " + f.name);
    return r;
  });
  f.cmax = Math.max(...f.chords);
}

// in-board point count of the family member at position u (u odd):
//   n(u,m) = sum over rows y of ([c_y <= u <= 2m-2+c_y] + [-c_y <= u <= 2m-2-c_y])
// (x = (u +- c_y)/2 must be an integer in [0, m-1])
export function points(f: any, u: number, m: number): number {
  const M = 2 * m - 2;
  let n = 0;
  for (const c of f.chords) {
    if (c <= u && u <= M + c) n++;
    if (-c <= u && u <= M - c) n++;
  }
  return n;
}

// band-wide sweep: curves10(m) = 8 horizontal lines + #{(family,u): n >= 10};
// curves9(m) = curves10(m) + #{n == 9}. Expected (corollaries):
//   curves9 = 9m-97 and curves10 = 9m-105 for all m in [23, 984] / [23, 940];
//   exactly-9 = F8/F9 edge members u in {19, 21, 2m-23, 2m-21} (8 for m >= 23,
//   4 at m = 22, 0 for m <= 21); >= 11-point circles = F1 only (m-7 members).
export function sweep(mLo: number, mHi: number) {
  const censusSmall = [16, 19, 22, 27, 32, 39, 46, 53, 60, 67, 74, 81, 88]; // m=9..21
  const out: any[] = [];
  let fails = 0;
  for (let m = mLo; m <= mHi; m++) {
    let ge10 = 0, ex9 = 0, ge11 = 0;
    const ex9Set: string[] = [];
    for (const f of fams) {
      for (let u = -f.cmax; u <= 2 * m - 2 + f.cmax; u += 2) {
        const n = points(f, u, m);
        if (n >= 10) { ge10++; if (n >= 11) ge11++; }
        else if (n === 9) { ex9++; ex9Set.push(f.name + "@" + u); }
      }
    }
    const curves10 = 8 + ge10, curves9 = 8 + ge10 + ex9;
    if (m <= 21 && curves9 !== censusSmall[m - 9]) fails++;
    if (m === 22 && (curves9 !== 99 || curves10 !== 95 || ex9 !== 4)) fails++;
    if (m >= 23) {
      if (curves9 !== 9 * m - 97 || ex9 !== 8 || ge11 !== m - 7) fails++;
      if (m <= 940 && curves10 !== 9 * m - 105) fails++;
    }
    out.push({ m, ge10, exactly9: ex9, curves10, curves9, ex9Set: ex9Set.sort() });
  }
  return { widths: out, fails };
}

// full run: sweep(9, 984) => fails === 0 (verified 2026-11-15)