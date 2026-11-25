#!/usr/bin/env python3
"""Independent exhaustive audit for rectangle V4 mod-4 cocircular/collinear counts."""
from collections import Counter, defaultdict
from itertools import combinations
from math import comb


def choose(n, k):
    return comb(n, k) if n >= k else 0


def cross(u, v):
    return u[0] * v[1] - u[1] * v[0]


def type_of_quad(quad):
    x0, y0 = quad[0]
    vec = [(x-x0, y-y0) for x,y in quad[1:]]
    if all(cross(vec[0], v) == 0 for v in vec[1:]):
        return 'line'
    a,b,c = vec
    aa,bb,cc = [u*u+v*v for u,v in vec]
    det = cross(a,b)*cc + cross(b,c)*aa + cross(c,a)*bb
    return 'circle' if det == 0 else 'other'


def fixed_count_formula(w,h):
    a,b=w//2,h//2
    # vertical axis x=(w-1)/2
    def axis_circle_term(max_distance, axis_length):
        # A symmetric chord at distance d and two points on the axis.
        # Write y0-y1=s, y2-y0=t.  Necessarily st=d^2.
        return sum(max(0, axis_length-s-d*d//s)
                   for d in range(1,max_distance+1)
                   for s in range(1,d*d+1) if d*d%s==0)

    vC=a*a*choose(h,2)+(w%2)*axis_circle_term(a,h)
    hC=b*b*choose(w,2)+(h%2)*axis_circle_term(b,w)
    vL=h*choose(a,2)+(w%2)*choose(h,4)
    hL=w*choose(b,2)+(h%2)*choose(w,4)
    # half-turn fixed circle: two pairs at equal squared radius
    # half-turn fixed line: two pairs along one center-through line
    radius=Counter(); direction=Counter()
    for x in range(w):
        for y in range(h):
            X,Y=w-1-x,h-1-y
            if (x,y)>=(X,Y): continue
            dx,dy=2*x-(w-1),2*y-(h-1)
            radius[dx*dx+dy*dy]+=1
            from math import gcd
            g=gcd(abs(dx),abs(dy))
            direction[(dx//g,dy//g) if dx>0 or dx==0 and dy>0 else (-dx//g,-dy//g)]+=1
    rC=sum(choose(k,2) for k in radius.values())
    rL=sum(choose(k,2) for k in direction.values())
    allC=a*b+(w%2)*(h%2)*min(a,b)
    allL=(h%2)*choose(a,2)+(w%2)*choose(b,2)
    return dict(circle=(vC+hC+rC-2*allC)%4,line=(vL+hL+rL-2*allL)%4,
                fixed={'vertical':(vC,vL),'horizontal':(hC,hL),'rotation':(rC,rL),'all':(allC,allL)})


def exhaustive(w,h):
    points=[(x,y) for x in range(w) for y in range(h)]
    v=lambda p:(w-1-p[0],p[1]); ho=lambda p:(p[0],h-1-p[1]); r=lambda p:(w-1-p[0],h-1-p[1])
    maps={'vertical':v,'horizontal':ho,'rotation':r}
    direct=Counter(); fixed={k:Counter() for k in ['vertical','horizontal','rotation','all']}
    for quad in combinations(points,4):
        typ=type_of_quad(quad)
        if typ=='other': continue
        direct[typ]+=1
        q=set(quad)
        isfixed={name: {f(p) for p in quad}==q for name,f in maps.items()}
        for name,yes in isfixed.items():
            if yes: fixed[name][typ]+=1
        if isfixed['vertical'] and isfixed['horizontal']:
            fixed['all'][typ]+=1
    formula=fixed_count_formula(w,h)
    for typ in ['circle','line']:
        assert direct[typ]%4==formula[typ],(w,h,typ,direct[typ],formula[typ])
    for name in fixed:
        for typ in ['circle','line']:
            assert fixed[name][typ]==formula['fixed'][name][0 if typ=='circle' else 1],(w,h,name,typ,fixed[name][typ],formula['fixed'][name])
    return direct,formula


def main():
    tests=[(w,h) for w in range(1,8) for h in range(1,8) if w*h<=42]
    count=0
    for w,h in tests:
        d,f=exhaustive(w,h)
        count+=choose(w*h,4)
        print(f'{w}x{h}: circle={d["circle"]}, line={d["line"]}, mod4={f["circle"]},{f["line"]}')
    print(f'PASS: {len(tests)} rectangles, {count} 4-subsets checked, all four fixed counts and both mod-4 identities match')

if __name__=='__main__': main()
