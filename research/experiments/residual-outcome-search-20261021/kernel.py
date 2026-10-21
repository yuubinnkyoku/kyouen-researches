#!/usr/bin/env python3
import csv,hashlib,io,json,pathlib,subprocess,tempfile
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SOURCE=ROOT/'research/experiments/n11-reduction-followup-20261005/output/n11-snapshots.json'

def main():
    snapshots=json.loads(SOURCE.read_text())['snapshots'];assert len(snapshots)==826
    rows=[]
    for i,s in enumerate(snapshots):
        labels={v:j for j,v in enumerate(s['legal'])}
        edges=[sum(1<<labels[v] for v in edge) for edge in s['minimal_residual_edges']]
        rows.append(' '.join(map(str,[i,len(labels),len(edges),*edges])))
    with tempfile.TemporaryDirectory() as tmp:
        exe=str(pathlib.Path(tmp)/'bench')
        subprocess.run(['g++','-std=c++20','-O2','-I'+str(ROOT/'cpp/solvers'),str(HERE/'bench.cpp'),'-o',exe],check=True)
        raw=subprocess.check_output([exe],input='\n'.join(rows)+'\n',text=True,timeout=120)
    (HERE/'kernel.csv').write_text(raw)
    result=list(csv.DictReader(io.StringIO(raw)));assert len(result)==826
    expected=json.loads((HERE.parent/'residual-gate-calibration-20261021/fixtures.json').read_text())
    for e in expected:
        r=result[e['source_index']];assert int(r['g'])==e['grundy'] and int(r['pn'])==(e['grundy']!=0)
    keys=('sg_calls','pn_calls','sg_memo','pn_memo','cutoffs','sg_us','pn_us')
    summary=dict(source=str(SOURCE.relative_to(ROOT)),sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        snapshots=826,repeats=7,quota=100000,totals={k:sum(float(r[k]) for r in result) for k in keys},
        timing='sum of per-root medians, alternating method order, fresh memo, single host',
        roots_faster=sum(float(r['pn_us'])<float(r['sg_us']) for r in result))
    (HERE/'kernel-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
