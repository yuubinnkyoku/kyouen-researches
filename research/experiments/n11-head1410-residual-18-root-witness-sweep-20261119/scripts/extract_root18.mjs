// Resumable single-root WIN7-D10 certificate extraction for the K1041 18-root witness.
import { extractBatch } from '../../n11-s2-5960-ms5-s7-reuse-20261113/scripts/class4_child1_cert_extractor_exact_v16.ts';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';

const BASE = path.dirname(fileURLToPath(import.meta.url));
const SOURCE_MAIN_BEFORE = '15d54369f6e348f7fc98581e099d7cd2e18518fd';
const ROOT = '00000000040080801202000000100000';
const COVERED_ROWS = ['0000000000000000380000000b000000'];
const INPUT = path.resolve(BASE, '../../n11-head1410-fifth-sixth-win7-receipt-fold-20261119/output/refuted-excluded-cover-refold-after-fifth-sixth-receipt-20261119.json');
const ENGINE = path.resolve(BASE, '../../n11-s2-5960-ms5-s7-reuse-20261113/scripts/class4_child1_cert_extractor_exact_v16.ts');
const INPUT_BLOB = 'dd2e8516c1b7424576a15bbbec6fcd38f4e0ba23';
const ENGINE_BLOB = '5518d375fc6b4a7a14c22a1a65586f0c1c5731c0';
const outDir = path.resolve(process.argv[2] || path.join(BASE, '../output/root-' + ROOT));
fs.mkdirSync(outDir, { recursive: true });

function gitBlobSha(bytes) {
  return createHash('sha1').update(Buffer.concat([Buffer.from('blob ' + bytes.length + '\0'), bytes])).digest('hex');
}
function rootCells(h) {
  const v = BigInt('0x' + h), out = [];
  for (let i = 0; i < 121; i++) if ((v >> BigInt(i)) & 1n) out.push(i);
  return out;
}
const X = i => i % 11, Y = i => Math.floor(i / 11);
function det4(a,b,c,d) {
  const pts = [a,b,c,d].map(i => [X(i),Y(i),X(i)*X(i)+Y(i)*Y(i),1]);
  const m = pts.map(r => r.slice());
  let sign=1, prev=1;
  for (let k=0;k<3;k++) {
    if (m[k][k]===0) {
      let s=-1;
      for (let i=k+1;i<4;i++) if (m[i][k]!==0) { s=i; break; }
      if (s<0) return 0;
      [m[k],m[s]]=[m[s],m[k]]; sign=-sign;
    }
    const pivot=m[k][k];
    for (let i=k+1;i<4;i++) {
      for (let j=k+1;j<4;j++) {
        const z=m[i][j]*pivot-m[i][k]*m[k][j];
        if (z%prev!==0) throw new Error('non-exact Bareiss division');
        m[i][j]=z/prev;
      }
      m[i][k]=0;
    }
    prev=pivot;
  }
  return sign*m[3][3];
}
function legalOf(h) {
  const cells=rootCells(h), blocked=new Set(cells);
  for(let i=0;i<cells.length;i++) for(let j=i+1;j<cells.length;j++) for(let k=j+1;k<cells.length;k++) {
    const a=cells[i],b=cells[j],c=cells[k];
    const qa=X(a)*X(a)+Y(a)*Y(a);
    const qb2=X(b)*X(b)+Y(b)*Y(b)-qa, qbx=X(b)-X(a), qby=Y(b)-Y(a);
    const qc2=X(c)*X(c)+Y(c)*Y(c)-qa, qcx=X(c)-X(a), qcy=Y(c)-Y(a);
    for(let d=0;d<121;d++) {
      if(d===a||d===b||d===c) continue;
      const qd2=X(d)*X(d)+Y(d)*Y(d)-qa, qdx=X(d)-X(a), qdy=Y(d)-Y(a);
      const det=qb2*(qcx*qdy-qcy*qdx)-qbx*(qc2*qdy-qcy*qd2)+qby*(qc2*qdx-qcx*qd2);
      if(det===0) blocked.add(d);
    }
  }
  return Array.from({length:121},(_,i)=>i).filter(i=>!blocked.has(i));
}
function transform(x,y,t) {
  if(t===0)return [x,y]; if(t===1)return [10-y,x]; if(t===2)return [10-x,10-y]; if(t===3)return [y,10-x];
  if(t===4)return [10-x,y]; if(t===5)return [x,10-y]; if(t===6)return [y,x]; return [10-y,10-x];
}
function d4Canonical(mask) {
  let best=null;
  for(let t=0;t<8;t++) {
    let v=0n;
    for(let i=0;i<121;i++) if((mask>>BigInt(i))&1n) {
      const xy=transform(i%11,Math.floor(i/11),t);
      v|=1n<<BigInt(xy[1]*11+xy[0]);
    }
    if(best===null||v<best)best=v;
  }
  return best===mask;
}
const inputBytes=fs.readFileSync(INPUT), engineBytes=fs.readFileSync(ENGINE);
const inputSha=gitBlobSha(inputBytes), engineSha=gitBlobSha(engineBytes);
if(inputSha!==INPUT_BLOB) throw new Error('K1041 input blob mismatch: '+inputSha);
if(engineSha!==ENGINE_BLOB) throw new Error('extractor engine blob mismatch: '+engineSha);
const input=JSON.parse(inputBytes.toString('utf8'));
const planned=input.witness_sweep_plan.untested_witness_roots;
if(!planned.includes(ROOT)) throw new Error('root is not in K1041 untested witness');
const plannedRows=input.witness.find(x=>x.root===ROOT)?.rows;
if(JSON.stringify(plannedRows)!==JSON.stringify(COVERED_ROWS)) throw new Error('K1041 covered-row mapping mismatch');
const root=BigInt('0x'+ROOT), cells=rootCells(ROOT);
if(cells.length!==7 || !d4Canonical(root)) throw new Error('root cardinality/D4 gate failed');
for(let i=0;i<7;i++)for(let j=i+1;j<7;j++)for(let k=j+1;k<7;k++)for(let l=k+1;l<7;l++)
  if(det4(cells[i],cells[j],cells[k],cells[l])===0) throw new Error('unsafe four-stone subset');
const legal=legalOf(ROOT);
const rootCheck={stones:cells.length,unsafe_quadruples:0,d4_canonical:true,legal_next_moves:legal.length};
const legalPath=path.join(outDir,'legal-moves.json');
fs.writeFileSync(legalPath,JSON.stringify({root:ROOT,legal,expected_count:legal.length,root_check:rootCheck,method:'exact integer lifted determinant over every root triple and board point'},null,2)+'\n');

const bit=Math.max(...cells);
const child=(root^(1n<<BigInt(bit))).toString(16).padStart(32,'0');
if(((root>>BigInt(bit))&1n)!==1n) throw new Error('added bit not present');
const rowsPath=path.join(outDir,'rows.txt');
const progressPath=path.join(outDir,'extraction-progress.jsonl');
const certPath=path.join(outDir,'win7-root-'+ROOT+'-20261119.n11');
const summaryPath=path.join(outDir,'extraction-summary.json');
const seen=new Set();
if(fs.existsSync(rowsPath)) for(const l of fs.readFileSync(rowsPath,'utf8').split(/\r?\n/)) if(l.trim())seen.add(l.trim());
const progress=[];
if(fs.existsSync(progressPath)) for(const l of fs.readFileSync(progressPath,'utf8').split(/\r?\n/)) if(l.trim()) {
  try { progress.push(JSON.parse(l)); } catch {}
}
const doneMoves=new Set(progress.filter(x=>x.status==='OK').map(x=>x.move));
let failure=null;
for(const move of legal) {
  if(doneMoves.has(move)) continue;
  const t0=Date.now();
  const r=extractBatch(child,bit,{},[move]);
  const p=r.perMove?.[String(move)];
  if(r.fatal||!r.rows||!p||!p.ok||p.capped||(r.fbt_drops??0)!==0) {
    failure={move,fatal:r.fatal??null,perMove:p??null,fbt_drops:r.fbt_drops??null};
    fs.appendFileSync(progressPath,JSON.stringify({move,status:'FAIL',...failure})+'\n');
    break;
  }
  const fresh=[];
  for(const line of r.rows) if(!seen.has(line)){seen.add(line);fresh.push(line);}
  if(fresh.length) fs.appendFileSync(rowsPath,fresh.join('\n')+'\n');
  const rec={move,status:'OK',nodes:p.nodes,new_rows:fresh.length,total_rows:seen.size,
             ms:Date.now()-t0,terminal_range:p.terminalRange,fbt_drops:r.fbt_drops??0};
  fs.appendFileSync(progressPath,JSON.stringify(rec)+'\n');
  progress.push(rec);
  console.log(JSON.stringify(rec));
}
const okMoves=[...new Set(progress.filter(x=>x.status==='OK').map(x=>x.move))].sort((a,b)=>a-b);
const nodeTotal=progress.filter(x=>x.status==='OK').reduce((s,x)=>s+x.nodes,0);
const ranges=progress.filter(x=>x.status==='OK'&&x.terminal_range).map(x=>x.terminal_range);
let status='INCOMPLETE', certSha=null;
if(!failure&&okMoves.length===legal.length) {
  const sorted=[...seen].sort((a,b)=>a<b?-1:a>b?1:0);
  const cert=['n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS','root '+ROOT,...sorted].join('\n')+'\n';
  fs.writeFileSync(certPath,cert);
  certSha=createHash('sha256').update(cert).digest('hex');
  status='EXTRACTED_UNVERIFIED';
}
const summary={
  schema:'n11-win7-d10-certificate-extraction-v1',
  source_main_before:SOURCE_MAIN_BEFORE,
  input_blob_sha1:INPUT_BLOB,
  engine_blob_sha1:ENGINE_BLOB,
  root:ROOT,child,added_bit:bit,covered_residual_rows:COVERED_ROWS,
  legal_next_moves:legal.length,completed_moves:okMoves.length,completed_move_list:okMoves,
  total_nodes:nodeTotal,unique_strategy_rows:seen.size,
  terminal_stone_range:ranges.length?[Math.min(...ranges.map(x=>x[0])),Math.max(...ranges.map(x=>x[1]))]:null,
  fbt_drops:progress.filter(x=>x.status==='OK').reduce((s,x)=>s+(x.fbt_drops??0),0),
  failure,status,certificate_sha256:certSha
};
fs.writeFileSync(summaryPath,JSON.stringify(summary,null,2)+'\n');
console.log(JSON.stringify(summary));
if(status!=='EXTRACTED_UNVERIFIED')process.exitCode=1;
