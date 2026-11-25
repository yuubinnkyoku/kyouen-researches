#!/usr/bin/env python3
"""Rebuild the S7 certificate from the independent C++ terminal solver TSVs."""
import argparse,json
from pathlib import Path
from terminal_geometry import children
p=argparse.ArgumentParser();p.add_argument('--prefix',default='min_s7');p.add_argument('--output',default='s7_win_four_min_certificate.json');p.add_argument('--roots',default='missing_s7.txt');args=p.parse_args()
rows=lambda f:{a[0]:a[1:] for line in Path(f).read_text().splitlines() if (a:=line.split('\t'))}
s8=rows(args.prefix+'.s8.tsv');s9=rows(args.prefix+'.s9.tsv');s10=rows(args.prefix+'.s10.tsv')
roots=Path(args.roots).read_text().split()
cert={'rule':'11x11 standard q4, complete call, normal play, fixed original-first-player WIN/LOSS','s6_target':'00000000041000001000401000100000','roots':{},'s8_witness':{},'s9_children':{},'s10_verdict':{}}
for r in roots:
    cs=[f'{x:032x}' for x in children(int(r,16))]
    cert['roots'][r]=cs
    for a in cs:
        assert s8[a][0]=='WIN' and len(s8[a])==2,(a,s8[a])
        w=s8[a][1]
        if a in cert['s8_witness']:assert cert['s8_witness'][a]==w
        cert['s8_witness'][a]=w
        assert s9[w][0]=='WIN'
        leaves=s9[w][1:]
        assert leaves
        cert['s9_children'][w]=leaves
        for leaf in leaves:
            assert s10[leaf][0]=='WIN'
            cert['s10_verdict'][leaf]=[int(s10[leaf][1]),int(s10[leaf][2])]
Path(args.output).write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n')
print('roots',len(cert['roots']),'s8',len(cert['s8_witness']),'s9',len(cert['s9_children']),'s10',len(cert['s10_verdict']),'states',sum(x[0] for x in cert['s10_verdict'].values()))
