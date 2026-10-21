#!/usr/bin/env python3
"""Reproduce a bounded cold-cache benchmark on the 826 saved n11 snapshots."""
import csv, hashlib, io, json, pathlib, subprocess, tempfile
ROOT=pathlib.Path(__file__).resolve().parents[3]
HERE=pathlib.Path(__file__).resolve().parent
SOURCE=ROOT/'research/experiments/n11-reduction-followup-20261005/output/n11-snapshots.json'

def main():
    source=json.loads(SOURCE.read_text())
    rows=[]
    for i,s in enumerate(source['snapshots']):
        labels={v:j for j,v in enumerate(s['legal'])}
        edges=[sum(1<<labels[v] for v in e) for e in s['minimal_residual_edges']]
        assert len(labels)<=18
        rows.append(' '.join(map(str,[i,len(labels),len(edges),*edges])))
    with tempfile.TemporaryDirectory() as tmp:
        exe=pathlib.Path(tmp)/'bench'
        subprocess.run(['g++','-std=c++20','-O2','-I'+str(ROOT/'cpp/solvers'),str(HERE/'bench.cpp'),'-o',str(exe)],check=True)
        raw=subprocess.check_output([str(exe),'7'],input='\n'.join(rows)+'\n',text=True)
    (HERE/'benchmark.csv').write_text(raw)
    result=list(csv.DictReader(io.StringIO(raw)))
    assert len(result)==len(source['snapshots'])==826
    totals={k:sum(float(r[k]) for r in result) for k in ['baseline_calls','fast_calls','baseline_memo','fast_memo','free_hits','two_hits','sunflower_hits','path_hits','baseline_us','fast_us']}
    summary={'source':str(SOURCE.relative_to(ROOT)),'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
             'snapshots':len(result),'repeats':7,'timing':'sum of per-root medians in microseconds; fresh memo; alternating run order',
             'totals':totals,'call_reduction':1-totals['fast_calls']/totals['baseline_calls'],
             'memo_reduction':1-totals['fast_memo']/totals['baseline_memo'],
             'time_ratio_fast_over_baseline':totals['fast_us']/totals['baseline_us'],
             'roots_with_fewer_calls':sum(int(r['fast_calls'])<int(r['baseline_calls']) for r in result),
             'n11_empty_root_outcome':'UNKNOWN'}
    (HERE/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
