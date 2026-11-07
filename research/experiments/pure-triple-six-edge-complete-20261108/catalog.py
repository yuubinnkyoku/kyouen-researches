#!/usr/bin/env python3
"""The ten edge-minimal g6/g7 kernels and their free-point parity."""
from collections import Counter
import json
from pathlib import Path
from misere import cell_values


def main():
    directory=Path(__file__).resolve().parent
    all_rows=json.loads((directory/'output/audit.json').read_text())['records']
    rows=[]
    for row in all_rows:
        if row['grundy']!=6:continue
        a=cell_values(tuple(row['signature']),0);b=cell_values(tuple(row['signature']),1)
        assert a[0]==6 and b[0]==7
        rows.append(dict(n=row['n'],edges=row['edges'],misere_without_free=a[1],misere_one_free=b[1]))
    assert len(rows)==10
    sizes=dict(sorted(Counter(row['n'] for row in rows).items()));assert sizes=={8:3,9:6,10:1}
    output=dict(audit='PASS',maximum_normal_core=6,maximum_six_kernel_types=len(rows),by_points=sizes,records=rows,
                normal_six_condition='one of these kernels plus an even number of isolated legal points',
                normal_seven_condition='one of these kernels plus an odd number of isolated legal points')
    (directory/'output/maximal_six_kernels.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output,indent=2))


if __name__=='__main__':main()
