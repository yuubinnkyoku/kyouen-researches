#!/usr/bin/env python3
import argparse,json,pathlib,subprocess,tempfile
import oracle
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=pathlib.Path,default=HERE/'budget-audit.json');args=p.parse_args()
    snapshots=json.loads(oracle.SOURCE.read_text())['snapshots'];expected=json.loads((HERE/'oracle.json').read_text())
    rows=[]
    for i,(s,e) in enumerate(zip(snapshots,expected['rows'])):
        labels={v:j for j,v in enumerate(s['legal'])};edges=[sum(1<<labels[v] for v in edge) for edge in s['minimal_residual_edges']]
        rows.append(' '.join(map(str,[i,len(labels),len(edges),int(e['g']!=0),*edges])))
    with tempfile.TemporaryDirectory() as tmp:
        exe=str(pathlib.Path(tmp)/'audit')
        subprocess.run(['g++','-std=c++20','-O2','-I'+str(ROOT/'cpp/solvers'),str(HERE/'budget_audit.cpp'),'-o',exe],check=True)
        output=subprocess.check_output([exe],input='\n'.join(rows)+'\n',text=True,timeout=120)
    data=json.loads(output);data['source_sha256']=expected['sha256']
    args.output.write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data,indent=2))
if __name__=='__main__':main()
