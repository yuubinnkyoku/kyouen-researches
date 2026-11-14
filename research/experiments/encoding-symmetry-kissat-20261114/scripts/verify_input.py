import json, math, sys
from fractions import Fraction
# verbatim port of research/experiments/witness-extension-kissat-20261114/scripts/verify_py.py safe_maximal
# (circle constant term without the corrected-initial-version bug), argv JSON input wrapper.
def safe_maximal(w,m,q,stones):
    S=[(int(x),int(y)) for x,y in stones]; ss=set(S)
    curves=[]
    n=len(S)
    for i in range(n):
        for j in range(i+1,n):
            (x1,y1),(x2,y2)=S[i],S[j]
            a=y1-y2; b=x2-x1; c=x1*y2-x2*y1
            g=0
            for v in (a,b,c): g=math.gcd(g,abs(v))
            if g: a//=g; b//=g; c//=g
            if (a,b,c)<(0,0,0): a,b,c=-a,-b,-c
            pts=[(x,y) for x in range(m) for y in range(w) if a*x+b*y+c==0]
            curves.append(pts)
    for i in range(n):
        for j in range(i+1,n):
            for k in range(j+1,n):
                (x1,y1),(x2,y2),(x3,y3)=S[i],S[j],S[k]
                a11=Fraction(x2-x1); a12=Fraction(y2-y1); b1=Fraction(-((x2*x2-x1*x1)+(y2*y2-y1*y1)))
                a21=Fraction(x3-x1); a22=Fraction(y3-y1); b2=Fraction(-((x3*x3-x1*x1)+(y3*y3-y1*y1)))
                det=a11*a22-a12*a21
                if det==0: continue
                B=(b1*a22-a12*b2)/det; C=(a11*b2-b1*a21)/det
                D=-Fraction(x1*x1+y1*y1)-B*x1-C*y1
                pts=[(x,y) for x in range(m) for y in range(w) if Fraction(x*x+y*y)+B*x+C*y+D==0]
                curves.append(pts)
    for pts in curves:
        cnt=sum(1 for p in pts if p in ss)
        if cnt>=q: return False,'unsafe',cnt
    for x in range(m):
        for y in range(w):
            if (x,y) in ss: continue
            blocked=False
            for pts in curves:
                if (x,y) in pts and sum(1 for p in pts if p in ss)>=q-1: blocked=True;break
            if not blocked: return False,'not maximal',(x,y)
    return True,'ok',len(S)
data=json.loads(sys.argv[1])
ok,reason,info=safe_maximal(data['w'],data['m'],data['q'],data['stones'])
print(json.dumps({'ok':ok,'reason':reason,'info':str(info)}))
