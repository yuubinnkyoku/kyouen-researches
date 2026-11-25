from functools import lru_cache
import hashlib, json, random
from pathlib import Path

def mex(values):
    m = 0
    while m in values:
        m += 1
    return m

@lru_cache(None)
def g_ordered(R, xs, z):
    if R == 0:
        return 0
    opts = set()
    for i, a in enumerate(xs):
        if a > 1:
            child = xs[:i] + (a - 1,) + xs[i + 1:]
            zz = z
        else:
            child = xs[:i] + xs[i + 1:]
            zz = z + 1
        opts.add(g_ordered(R - 1, child, zz))
    if z:
        opts.add(1 ^ g_ordered(R - 1, xs, z - 1))
    return mex(opts)

@lru_cache(None)
def g_canon(R, xs, z):
    xs = tuple(sorted(xs, reverse=True))
    if R == 0:
        return 0
    opts = set()
    for i, a in enumerate(xs):
        if a > 1:
            child = xs[:i] + (a - 1,) + xs[i + 1:]
            zz = z
        else:
            child = xs[:i] + xs[i + 1:]
            zz = z + 1
        opts.add(g_canon(R - 1, child, zz))
    if z:
        opts.add(1 ^ g_canon(R - 1, xs, z - 1))
    return mex(opts)

def odd(r,a,b): return r % 2 == 1 and a <= r <= b
def even(r,a,b): return r % 2 == 0 and a <= r <= b

def z15_T(x,y,r):
    d=x-y; Y=2*y; S=x+y
    if (y,d)==(6,0): return odd(r,1,11)
    if (y,d) in ((6,1),(6,2),(7,0)): return odd(r,1,13)
    if (y,d) in ((6,3),(7,1)): return odd(r,1,21)
    if odd(r,1,15): return True
    if d in (3,7,11,15): return r==Y+(d+15)//2
    if d==16: return odd(r,Y+15,S+15)
    if d>=17: return r==Y+15
    return False

def z15_P(x,y,r):
    d=x-y; Y=2*y; S=x+y
    if (y,d) in ((6,0),(6,2),(7,0)): return False
    if (y,d)==(6,1): return r>=14
    if d%2==0 and d<=14:
        return even(r,16,Y+6+2*((d+3)//4))
    if d%2==1 and d<=15:
        return (even(r,16,S+15)
                or odd(r,Y+7+2*((d+5)//4),S+14)
                or r>=S+16)
    if d==16:
        return even(r,16,Y+14)
    if d>=17:
        hi=S+(15 if d%2==0 else 14)
        return (even(r,16,Y+14) or odd(r,Y+17,hi)
                or (d%2==1 and r>=S+16))
    return False

def z15_val(x,y,r):
    if r==0: return 0
    S=x+y
    if r>=S+16: return S%2
    if z15_T(x,y,r): return 2
    if z15_P(x,y,r): return 1
    return 0

def z14_T(x,y,r):
    d=x-y; Y=2*y; S=x+y
    if (y,d)==(6,0): return odd(r,1,11)
    if (y,d)==(7,0): return odd(r,1,21)
    if (y,d)==(6,2): return odd(r,1,19)
    if odd(r,1,13): return True
    if d in (0,4,8,12): return r==Y+7+d//2
    if d==15: return odd(r,Y+15,S+14)
    if d>=16: return r==Y+15
    return False

def z14_P(x,y,r):
    d=x-y; Y=2*y; S=x+y
    if (y,d) in ((6,0),(7,0),(6,2)): return False
    if (y,d)==(6,1): return r>=14
    if d%2==0 and d<=14:
        return odd(r,15,Y+5+2*((d+3)//4))
    if d%2==1 and d<=13:
        return (odd(r,15,S+14)
                or even(r,Y+8+2*((d+1)//4),S+13)
                or r>=S+15)
    if d%2==0 and d>=16:
        return odd(r,15,Y+13) or even(r,Y+16,S+14)
    if d%2==1 and d>=15:
        return odd(r,15,Y+13) or even(r,Y+16,S+13) or r>=S+15
    return False

def z14_val(x,y,r):
    if r==0: return 0
    S=x+y
    if r>=S+15: return S%2
    if z14_T(x,y,r): return 2
    if z14_P(x,y,r): return 1
    return 0

def k1049_T(x,r):
    if x==5: return odd(r,1,9)
    if x in (6,7): return odd(r,1,11)
    if x in (8,9): return odd(r,1,13)
    if x==10: return odd(r,1,19)
    if x==11: return odd(r,1,15)
    if x==12: return odd(r,1,15) or r==21
    if 13<=x<=15: return odd(r,1,15)
    if x==16: return odd(r,1,15) or r==23
    if 17<=x<=19: return odd(r,1,15)
    if x==20: return odd(r,1,15) or r==25
    if x==21: return odd(r,1,15) or odd(r,25,41)
    if x>=22: return odd(r,1,15) or r==25
    raise ValueError(x)

def k1049_P(x,r):
    finite={5:set(),6:None,7:set(),8:None,9:set(),10:{16,18,20},
            11:{16,18,20},12:{16,18,20},13:{16,18,20},
            14:{16,18,20,22},15:{16,18,20,22},
            16:{16,18,20,22},17:{16,18,20,22},
            18:{16,18,20,22,24},19:{16,18,20,22,24},
            20:{16,18,20,22,24,26},21:{16,18,20,22,24}}
    if x in finite:
        s=finite[x]
        if s is None: return r >= (12 if x==6 else 14)
        if r in s: return True
        if x in (10,12,14,16,18,20):
            start={10:21,12:22,14:23,16:24,18:25,20:27}[x]
            return r>=start
        return False
    if x>=22 and x%2==0:
        return (r in {16,18,20,22,24} or odd(r,27,x+21) or r>=x+22)
    if x>=23 and x%2==1:
        return r in {16,18,20,22,24} or odd(r,27,x+20)
    raise ValueError(x)

def k1049_val(x,r):
    if r==0: return 0
    return 2 if k1049_T(x,r) else 1 if k1049_P(x,r) else 0

def z15_bands(y,d):
    Y=2*y; S=2*y+d
    if (y,d)==(6,0):
        O=[(1,11,'01'),(13,27,'1')]; E=[(2,12,'23'),(14,26,'1')]
    elif (y,d)==(6,1):
        O=[(1,13,'01'),(15,27,'0')]; E=[(2,12,'23'),(14,14,'03'),(16,28,'0')]
    elif (y,d)==(6,2):
        O=[(1,13,'01'),(15,29,'1')]; E=[(2,14,'23'),(16,20,'13'),(22,28,'1')]
    elif (y,d)==(6,3):
        O=[(1,21,'01'),(23,29,'0')]; E=[(2,14,'23'),(16,30,'0')]
    elif (y,d)==(6,4):
        O=[(1,15,'01'),(17,31,'1')]; E=[(2,14,'23'),(16,20,'02'),(22,22,'123'),(24,30,'1')]
    elif (y,d)==(7,0):
        O=[(1,13,'01'),(15,29,'1')]; E=[(2,14,'23'),(16,22,'13'),(24,28,'1')]
    elif (y,d)==(7,1):
        O=[(1,21,'01'),(23,29,'0')]; E=[(2,14,'23'),(16,30,'0')]
    elif (y,d)==(7,2):
        O=[(1,15,'01'),(17,S+15,'1')]
        E=[(2,14,'23'),(16,Y+8,'02'),(Y+10,S+14,'1')]
    elif d==0 and y==8:
        O=[(1,15,'01'),(17,Y+15,'1')]
        E=[(2,14,'23'),(16,Y+6,'02'),(Y+8,Y+8,'13'),(Y+10,Y+14,'1')]
    elif d==0 and y>=9:
        O=[(1,15,'01'),(17,Y+15,'1')]
        E=[(2,14,'23'),(16,16,'02'),(18,Y+6,'0'),(Y+8,Y+8,'13'),(Y+10,Y+14,'1')]
    elif d%2==0 and 2<=d<=14:
        c=Y+8+2*(d//4)
        O=[(1,15,'01'),(17,S+15,'1')]
        E=[(2,14,'23'),(16,16,'02'),(18,c-2,'0'),
           (c,c,'123' if d%4==0 else '02'),(c+2,S+14,'1')]
    elif d%2==1 and 1<=d<=13:
        b=Y+5+2*((d+3)//4)
        O=[(1,15,'01'),(17,b,'1')]
        if d%4==3:
            c=Y+(d+15)//2
            O += [(c,c,'01'),(c+2,S+14,'0')]
        else:
            O += [(b+2,S+14,'0')]
        E=[(2,14,'23'),(16,16,'02'),(18,S+15,'0')]
    elif d==15:
        O=[(1,15,'01'),(17,Y+13,'1'),(Y+15,Y+15,'01'),(Y+17,S+14,'0')]
        E=[(2,14,'23'),(16,16,'02'),(18,Y+12,'0'),(Y+14,Y+14,'02'),(Y+16,S+15,'023')]
    elif d==16:
        O=[(1,15,'01'),(17,Y+13,'1'),(Y+15,S+15,'01')]
        E=[(2,14,'23'),(16,16,'02'),(18,Y+12,'0'),(Y+14,Y+14,'02'),
           (Y+16,Y+16,'123'),(Y+18,S+14,'1')]
    elif d==17:
        O=[(1,15,'01'),(17,Y+13,'1'),(Y+15,Y+15,'01'),(Y+17,S+14,'0')]
        E=[(2,14,'23'),(16,16,'02'),(18,Y+12,'0'),(Y+14,Y+14,'02'),
           (Y+16,Y+16,'123'),(Y+18,S+15,'12')]
    elif d>=18:
        ohi=S+(14 if d%2 else 15)
        ehi=S+(15 if d%2 else 14)
        O=[(1,15,'01'),(17,Y+13,'1'),(Y+15,Y+15,'01'),(Y+17,ohi,'0')]
        E=[(2,14,'23'),(16,16,'02'),(18,Y+12,'0'),(Y+14,Y+14,'02'),
           (Y+16,Y+16,'123'),(Y+18,ehi,'1')]
    else:
        raise ValueError((y,d))
    return O,E

def signature(y,d,r):
    x=y+d; rr=r-1
    if d==0:
        B=k1049_val(x,rr) if y==6 else z15_val(x,y-1,rr)
        A=B
    else:
        A=z15_val(x-1,y,rr)
        B=k1049_val(x,rr) if y==6 else z15_val(x,y-1,rr)
    C=1 ^ z14_val(x,y,rr)
    return ''.join(str(v) for v in sorted({A,B,C}))

counts = {}
parent_checks = 0
for y in range(6, 21):
    for d in range(0, 31):
        x = y + d; S = x + y
        for R in range(S + 17):
            a = g_ordered(R, (x, y), 15)
            b = g_canon(R, (x, y), 15)
            c = z15_val(x, y, R)
            assert a == b == c, ("parent", x, y, d, R, a, b, c)
            parent_checks += 1
counts["parent_two_recursions"] = parent_checks

b_checks = 0
for x in range(6, 151):
    for R in range(x + 22):
        a = g_ordered(R, (x, 5), 15)
        b = g_canon(R, (x, 5), 15)
        c = k1049_val(x, R)
        assert a == b == c, ("B/K1049", x, R, a, b, c)
        b_checks += 1
counts["K1049_B_anchor"] = b_checks

c_checks = 0
for y in range(6, 31):
    for d in range(0, 31):
        x = y + d; S = x + y
        for R in range(S + 15):
            a = g_ordered(R, (x, y), 14)
            b = g_canon(R, (x, y), 14)
            c = z14_val(x, y, R)
            assert a == b == c, ("C/K1062", x, y, d, R, a, b, c)
            c_checks += 1
counts["K1062_C_anchor"] = c_checks

sig_checks = 0
for y in range(6, 81):
    for d in range(0, 81):
        S = 2*y + d
        O, E = z15_bands(y, d)
        for R in range(1, S + 16):
            bands = O if R % 2 else E
            hits = [sig for lo, hi, sig in bands if lo <= R <= hi]
            assert len(hits) == 1, ("band coverage", y, d, R, hits)
            got = signature(y, d, R)
            assert hits[0] == got, ("band signature", y, d, R, hits[0], got)
            sig_checks += 1
counts["signature_coverage_and_identity"] = sig_checks

mex_map = {'01':2, '23':0, '03':1, '13':0, '02':1, '0':1, '1':0, '123':0, '023':1, '12':0}
mex_checks = 0
for y in range(6, 81):
    for d in range(0, 81):
        O, E = z15_bands(y, d)
        for R in range(1, 2*y+d+16):
            bands = O if R % 2 else E
            sig = next(s for lo, hi, s in bands if lo <= R <= hi)
            value = mex_map[sig]
            assert value == z15_val(y+d, y, R), ("mex", y, d, R, sig, value)
            mex_checks += 1
counts["signature_mex"] = mex_checks

low_checks = 0
for y in range(6, 81):
    for d in range(0, 81):
        x = y + d; S = x + y
        for R in range(22):
            a = z15_val(x, y, R)
            b = g_canon(R, (S,), 15)
            assert a == b, ("low-R collapse", x, y, R, a, b)
            low_checks += 1
counts["low_R_single_token_collapse"] = low_checks

tail_checks = 0
for y in range(6, 19):
    for d in range(0, 26):
        x = y + d; S = x + y
        for R in range(S + 16, S + 21):
            a = g_ordered(R, (x, y), 15)
            b = g_canon(R, (x, y), 15)
            assert a == b == S % 2, ("tail", x, y, R, a, b, S % 2)
            tail_checks += 1
counts["tail_direct"] = tail_checks

rng = random.Random(20261120)
scatter_checks = 0
for _ in range(5000):
    y = rng.randint(6, 400)
    d = rng.randint(0, 400)
    x = y + d; S = x + y
    R = rng.randint(0, S + 30)
    v = z15_val(x, y, R)
    assert v in (0, 1, 2)
    assert not (z15_T(x, y, R) and z15_P(x, y, R))
    if R >= S + 16:
        assert v == S % 2
    scatter_checks += 1
counts["fixed_seed_scatter"] = scatter_checks

theorem_t_checks = 0
for y in range(6, 21):
    for d in range(0, 31):
        x = y + d; S = x + y
        for R in range(S + 17):
            v = z15_val(x, y, R)
            assert not (R % 2 == 0 and v == 2)
            assert not (R % 2 == 1 and v > 2)
            theorem_t_checks += 1
counts["theorem_T_parity"] = theorem_t_checks

counts["total"] = sum(counts.values())
counts["bad"] = []
counts["claim"] = "H(R;(x,y);15), all x>=y>=6 and R>=0"
counts["proof_status"] = "proved_by_two_level_induction_and_symbolic_signature_bands"
counts["finite_audit_scope"] = {
    "parent_direct": "6<=y<=20, 0<=d<=30, 0<=R<=x+y+16",
    "K1049_B_anchor": "6<=x<=150, 0<=R<=x+21",
    "K1062_C_anchor": "6<=y<=30, 0<=d<=30, 0<=R<=x+y+14",
    "signature_bands": "6<=y<=80, 0<=d<=80, 1<=R<=x+y+15",
    "low_R": "6<=y<=80, 0<=d<=80, 0<=R<=21",
    "tail_direct": "6<=y<=18, 0<=d<=25, x+y+16<=R<=x+y+20",
    "scatter_seed": 20261120,
}
counts["verifier_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
raw = json.dumps(counts, ensure_ascii=False, indent=2, sort_keys=True) + "
"
out = Path(__file__).resolve().parent / "output" / "audit.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(raw, encoding="utf-8")
print(raw, end="")
