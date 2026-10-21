#!/usr/bin/env python3
"""Check all saved roots and children with the C++ labelled-edge comparator."""
import argparse,hashlib,json,pathlib,subprocess,tempfile
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SOURCE=ROOT/'research/experiments/n11-reduction-followup-20261005/output/n11-snapshots.json'
def main():
    p=argparse.ArgumentParser();p.add_argument('--test',required=True);args=p.parse_args()
    snapshots=json.loads(SOURCE.read_text())['snapshots'];assert len(snapshots)==826
    with tempfile.TemporaryDirectory() as tmp:
        path=pathlib.Path(tmp)/'roots.csv'
        path.write_text(''.join(f"{sum(1<<v for v in x['occupied'] if v<64)},{sum(1<<(v-64) for v in x['occupied'] if v>=64)}\n" for x in snapshots))
        result=subprocess.run([args.test,str(path)],check=True,text=True,capture_output=True,timeout=180)
    report=dict(source=str(SOURCE.relative_to(ROOT)),sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        scope='all safe n4 occupancies and legal children; n8 empty and singleton roots (64-bit boundary); all 826 saved n11 roots and legal children',output=result.stdout)
    (HERE/'builder-audit.json').write_text(json.dumps(report,indent=2)+'\n');print(result.stdout,end='')
if __name__=='__main__':main()
