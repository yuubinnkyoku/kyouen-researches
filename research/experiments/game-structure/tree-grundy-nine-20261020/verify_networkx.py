#!/usr/bin/env python3
"""Independent nonisomorphic tree generator + surviving-vertices Grundy solver.
Requires networkx. Compare with verify.py's AHU generator results.
"""
import json
import subprocess
import tempfile
from collections import Counter
from pathlib import Path
import networkx as nx

HERE=Path(__file__).resolve().parent

def main():
    with tempfile.TemporaryDirectory() as tmp:
        binary=Path(tmp)/'remaining'
        subprocess.run(['g++','-O3','-std=c++17',str(HERE/'remaining_mex.cpp'),'-o',str(binary)],check=True)
        summary=json.loads((HERE/'output'/'leaf_ahu.json').read_text())
        results={}
        for n in range(1,18):
            trees=[nx.empty_graph(1)] if n==1 else list(nx.nonisomorphic_trees(n))
            data=''.join(str(n)+' '+' '.join(str(sum(1<<j for j in t.neighbors(i))) for i in range(n))+'\n' for t in trees)+'0\n'
            out=subprocess.run([str(binary)],input=data,text=True,capture_output=True,check=True)
            vals=list(map(int,out.stdout.split()))
            counts=dict(sorted(Counter(vals).items()))
            assert len(vals)==len(trees)
            assert summary[str(n)]['count']==len(trees)
            assert {int(k):v for k,v in summary[str(n)]['nimbers'].items()}==counts
            results[n]={'count':len(trees),'nimbers':counts}
            print(n,results[n],flush=True)
        (HERE/'output'/'networkx.json').write_text(json.dumps(results,indent=2)+'\n')
        print('INDEPENDENT TREE GENERATORS AND NIMBER DISTRIBUTIONS AGREE')

if __name__=='__main__':
    main()
