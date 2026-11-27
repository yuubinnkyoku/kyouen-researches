"""Build the AG(2,9) board (81 points, 90 lines of 9) over GF(9)=GF(3)[i]/(i^2+1)."""
from pathlib import Path
def gmul(a,b): return ((a[0]*b[0]-a[1]*b[1])%3, (a[0]*b[1]+a[1]*b[0])%3)
def gadd(a,b): return ((a[0]+b[0])%3,(a[1]+b[1])%3)
E=[(a,b) for a in range(3) for b in range(3)]
pts=[(x,y) for x in E for y in E]; idx={p:i for i,p in enumerate(pts)}
lines=[]
for x in E: lines.append(tuple(idx[(x,y)] for y in E))
for m in E:
    for b in E:
        lines.append(tuple(idx[(x,gadd(gmul(m,x),b))] for x in E))
out=Path(__file__).resolve().parents[1]/'output'/'board_ag2q9.txt'
out.parent.mkdir(parents=True,exist_ok=True)
with open(out,'w') as f:
    f.write(f'{len(pts)} {len(lines)}\n')
    for L in lines: f.write(str(len(L))+' '+' '.join(map(str,L))+'\n')
print('wrote',out,len(pts),len(lines))
