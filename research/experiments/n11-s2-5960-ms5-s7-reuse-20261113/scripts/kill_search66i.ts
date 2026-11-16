// kill-table search for a single failing loser defense of a WIN7 root (2026-11-16)
// For (child, bit, move), tries each candidate winner reply (argv list) as the
// depth-1 kill-table pref and reports whether the subtree closes within budget.
// Search only: rows accumulate across attempts; the final certificate batch must
// be run in a fresh process with the discovered kill table.
import { extractBatch } from './class4_child1_cert_extractor_exact.ts';
const child = process.argv[2];
const bit = Number(process.argv[3]);
const move = Number(process.argv[4]);
const replies = process.argv[5].split(',').filter(s => s !== '').map(Number);
let fbtPrev = 0;
for (const r of replies) {
  const res = extractBatch(child, bit, { [move]: r }, [move]);
  const pm = res.perMove[String(move)] ?? res.perMove[move];
  const fbtDelta = res.fbt_drops - fbtPrev;
  fbtPrev = res.fbt_drops;
  const line = { reply: r, ok: pm.ok, capped: pm.capped, nodes: pm.nodes, fbt_delta: fbtDelta };
  process.stdout.write(JSON.stringify(line) + String.fromCharCode(10));
  if (pm.ok && !pm.capped) { process.stdout.write('KILL ' + move + ' -> ' + r + String.fromCharCode(10)); break; }
}
