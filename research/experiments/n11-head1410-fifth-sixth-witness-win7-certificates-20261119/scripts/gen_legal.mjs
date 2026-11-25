// Legal first-mover move list generator for the three witness WIN roots (2026-11-19 recovery).
// Survival-move convention: a cell is legal for the next (winner-side) stone iff it is empty
// and is not cocircular/collinear with any triple of existing root stones (det==0 test over
// all triples x all cells, exactly the independent recheck embedded in the extraction driver).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const BASE = path.dirname(fileURLToPath(import.meta.url));
const X = i => i % 11, Y = i => (i / 11) | 0;
const rootCells = h => { const v = BigInt('0x' + h); const out = []; for (let i = 0; i < 121; i++) if ((v >> BigInt(i)) & 1n) out.push(i); return out; };
function legalOf(h) {
  const cells = rootCells(h);
  const blocked = new Set(cells);
  for (let i = 0; i < cells.length; i++) for (let j = i + 1; j < cells.length; j++) for (let k = j + 1; k < cells.length; k++) {
    const a = cells[i], b = cells[j], c = cells[k];
    const qa = X(a)*X(a)+Y(a)*Y(a), qb2 = X(b)*X(b)+Y(b)*Y(b)-qa, qbx = X(b)-X(a), qby = Y(b)-Y(a);
    const qc2 = X(c)*X(c)+Y(c)*Y(c)-qa, qcx = X(c)-X(a), qcy = Y(c)-Y(a);
    for (let d = 0; d < 121; d++) {
      if (d === a || d === b || d === c) continue;
      const qd2 = X(d)*X(d)+Y(d)*Y(d)-qa, qdx = X(d)-X(a), qdy = Y(d)-Y(a);
      const det = qb2*(qcx*qdy-qcy*qdx) - qbx*(qc2*qdy-qcy*qd2) + qby*(qc2*qdx-qcx*qd2);
      if (det === 0) blocked.add(d);
    }
  }
  const lm = []; for (let d = 0; d < 121; d++) if (!blocked.has(d)) lm.push(d);
  return lm;
}
const EXPECT = { '00000000000000801202060001000000': 53, '00000000000000805202080001000000': 54, '00000000040000801202000080100000': 55 };
const out = {};
for (const [h, n] of Object.entries(EXPECT)) {
  const lm = legalOf(h);
  if (lm.length !== n) { console.error('LEGAL COUNT MISMATCH ' + h + ': ' + lm.length + ' != ' + n); process.exit(1); }
  out[h] = { legal: lm, expected_count: n };
}
fs.writeFileSync(path.join(BASE, 'win_legal_gen.json'), JSON.stringify(out, null, 1) + '\n');
console.log(JSON.stringify(Object.fromEntries(Object.entries(out).map(([k, v]) => [k, v.legal.length]))));
