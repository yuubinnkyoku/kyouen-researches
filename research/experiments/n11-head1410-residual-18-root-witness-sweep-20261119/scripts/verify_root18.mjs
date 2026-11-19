// Dual-independent verifier for the K1041 18-root witness WIN7-D10 certificate.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const BASE=path.dirname(fileURLToPath(import.meta.url));
const EXP=path.resolve(BASE,'..');
const SHARED=path.resolve(BASE,'../../n11-s2-5960-ms5-s7-reuse-20261113/scripts');
const ROOT='00000000040080801202000000100000';
const outDir=path.resolve(process.argv[2]||path.join(EXP,'output/root-'+ROOT));
const summary=JSON.parse(fs.readFileSync(path.join(outDir,'extraction-summary.json'),'utf8'));
const legal=JSON.parse(fs.readFileSync(path.join(outDir,'legal-moves.json'),'utf8'));
const certPath=path.join(outDir,'win7-root-'+ROOT+'-20261119.n11');
const cert=fs.readFileSync(certPath);
const certSha=crypto.createHash('sha256').update(cert).digest('hex');
if(summary.status!=='EXTRACTED_UNVERIFIED'||summary.root!==ROOT||summary.certificate_sha256!==certSha)throw new Error('extraction summary/certificate gate');
if(legal.root!==ROOT||legal.expected_count!==legal.legal.length||legal.legal.length!==summary.legal_next_moves)throw new Error('legal list gate');
const BIGINT=path.join(SHARED,'verify_win7_certificate_bigint_independent.mjs');
const BAREISS=path.join(SHARED,'verify_bit7_win7_cert.ts');
const big=spawnSync(process.execPath,[BIGINT,certPath,String(legal.legal.length)],{encoding:'utf8',maxBuffer:32*1024*1024});
if(big.status!==0)throw new Error('BigInt verifier failed: '+big.stderr);
const verification=JSON.parse(big.stdout.trim());
if(verification.verdict!=='WIN7 certificate independently verified'||verification.root_hex!==ROOT||
   verification.subroots_passed!==legal.legal.length||verification.union_missing!==0||verification.union_extra!==0||
   verification.strategy_rows!==summary.unique_strategy_rows||verification.root_safe!==true||
   verification.root_mobility!==legal.legal.length||verification.terminal_range[0]!==13||verification.terminal_range[1]!==17)
  throw new Error('BigInt verification gates failed');
const consumedPath=path.join(outDir,'bareiss-consumed.txt');
const bareiss=spawnSync(process.execPath,['--experimental-strip-types',BAREISS,'--cert',certPath,
  '--root',ROOT,'--root-check','--subroots',legal.legal.join(','),'--consumed-out',consumedPath],
  {encoding:'utf8',maxBuffer:64*1024*1024});
if(bareiss.status!==0)throw new Error('Bareiss verifier failed: '+bareiss.stderr);
const lines=bareiss.stdout.trim().split(/\r?\n/);
if(lines.length!==2)throw new Error('Bareiss output line count '+lines.length);
const rootCheck=JSON.parse(lines[0]),stats=JSON.parse(lines[1]);
const per=Object.values(stats.stats);
if(rootCheck.stones!==7||rootCheck.loserMobility!==legal.legal.length||
   stats.rows!==summary.unique_strategy_rows||per.length!==legal.legal.length)throw new Error('Bareiss root/subroot gates');
const totals={
  seen:per.reduce((s,x)=>s+x.seen,0),
  terminals:per.reduce((s,x)=>s+x.terminals,0),
  opponent_edges:per.reduce((s,x)=>s+x.opponentEdges,0),
  terminal_min:Math.min(...per.map(x=>x.range[0])),
  terminal_max:Math.max(...per.map(x=>x.range[1]))
};
if(totals.seen!==verification.visited_states_across_subroots||
   totals.terminals!==verification.terminal_count||
   totals.opponent_edges!==verification.loser_reply_edges||
   totals.terminal_min!==verification.terminal_range[0]||
   totals.terminal_max!==verification.terminal_range[1])throw new Error('BigInt/Bareiss state-flow disagreement');
const certRows=new Set(cert.toString('utf8').trimEnd().split(/\r?\n/).slice(2).map(x=>x.split(' ')[0]));
const consumed=fs.readFileSync(consumedPath,'utf8').trim().split(/\r?\n/).filter(Boolean);
const consumedUnique=new Set(consumed);
const missing=[...certRows].filter(x=>!consumedUnique.has(x)).length;
const extra=[...consumedUnique].filter(x=>!certRows.has(x)).length;
if(certRows.size!==summary.unique_strategy_rows||consumedUnique.size!==summary.unique_strategy_rows||missing||extra)throw new Error('Bareiss consumed union mismatch');
const unionAudit={certificate_rows:certRows.size,consumed_records:consumed.length,
  consumed_unique:consumedUnique.size,missing,extra,exact_union:true};
const result={
  schema:'n11-win7-d10-dual-independent-verification-v1',
  root:ROOT,covered_residual_rows:summary.covered_residual_rows,
  certificate_bytes:cert.length,certificate_sha256:certSha,
  legal_next_moves:legal.legal.length,strategy_rows:summary.unique_strategy_rows,
  bigint:verification,
  bareiss:{root_check:rootCheck,subroots:per.length,...totals},
  union_audit:unionAudit,
  cross_method_state_flow_agreement:true,
  all_pass:true
};
fs.writeFileSync(path.join(outDir,'independent-verification.json'),JSON.stringify(result,null,2)+'\n');
fs.writeFileSync(path.join(outDir,'bareiss-subroots.jsonl'),lines.join('\n')+'\n');
fs.writeFileSync(path.join(outDir,'bareiss-union-audit.json'),JSON.stringify(unionAudit,null,2)+'\n');
console.log(JSON.stringify({root:ROOT,status:'dual-independent-verification-pass',
  legal:legal.legal.length,rows:summary.unique_strategy_rows,sha256:certSha,
  bigint:{states:verification.visited_states_across_subroots,terminals:verification.terminal_count,edges:verification.loser_reply_edges},
  bareiss:totals,unionAudit}));
