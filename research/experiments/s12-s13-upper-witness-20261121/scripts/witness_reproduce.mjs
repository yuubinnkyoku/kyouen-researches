import { Board, State } from './hunt.mjs';
import { WITNESSES } from './witnesses.mjs';
let allok = true;
for (const w of WITNESSES) {
  const bd = new Board(w.n);
  const st = new State(bd);
  for (const [x,y] of w.coords) st.add(x + w.n*y);
  const okS = st.viol === 0, okM = st.uncovered === 0;
  console.log(`n=${w.n} (${w.src}): stones=${st.size()} safe=${okS} maximal=${okM}`);
  if (!okS || !okM) allok = false;
}
console.log(allok ? "ALL PUBLISHED WITNESSES REPRODUCE" : "FAIL");
