from pathlib import Path
import re
p=Path(__file__).parent
for n in range(5,10):
    def parse(file):
        d={}
        for line in (p/file).read_text().splitlines():
            fields={k:int(v) for k,v in re.findall(r'([\w-]+)=(\d+)',line)}
            if line.startswith('n='):
                d.update(fields)
            elif line.startswith('linear-max='):
                d['linear-max']=int(line.split('=')[1])
            elif line.startswith('linear-g='):
                d['linear-'+str(fields['linear-g'])]=fields['count']
            elif line.startswith('g='):
                g=fields['g']
                if 'count' in fields:
                    d['g'+str(g)]=fields['count']
                else:
                    d['g'+str(g)]=fields['cover']
                    d['linear-'+str(g)]=fields['linear']
        return d
    a=parse(f'main_{n}.txt')
    b=parse(f'independent_{n}.txt')
    for g in range(16):
        a.setdefault('g'+str(g),0); b.setdefault('g'+str(g),0)
        a.setdefault('linear-'+str(g),0); b.setdefault('linear-'+str(g),0)
    a.setdefault('linear-max',-1); b.setdefault('linear-max',-1)
    assert a==b,(n,a,b)
    print(n,'OK',a['cover'],'max',a['max'],'linear max',a['linear-max'])
