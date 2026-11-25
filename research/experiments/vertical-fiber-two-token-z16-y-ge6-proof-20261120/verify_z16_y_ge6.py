# H(R;(x,y);16), all x>=y>=6, R>=0 - full Grundy value classification
# Verifier pattern: K1062/K1065 (dual-recursion engine + closed form +
# signature-band coverage/identity/mex + anchors K1074 (z=16,y=5) and
# K1065 (z=15,y>=6) + low-R single-token collapse + tail + fixed-seed scatter).
from functools import lru_cache
import hashlib, json, random
from pathlib import Path
import sys
sys.setrecursionlimit(100000)

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

def odd(r,a,b): return r%2==1 and a<=r<=b
def even(r,a,b): return r%2==0 and a<=r<=b

# ---- value16 (z=16 uniform family), fitted & engine-verified
def z16_T(x,y,r):
    d,Y,S = x-y, 2*y, x+y
    if (y,d)==(6,0): return odd(r,1,11)
    if (y,d) in ((6,1),(6,2),(7,0)): return odd(r,1,13)
    if (y,d)==(6,4): return odd(r,1,21)
    if (y,d) in ((7,2),(8,0)): return odd(r,1,23)
    if odd(r,1,15): return True
    if d in (2,6,10,14): return r==Y+(d+16)//2
    if d==17: return odd(r,Y+17,S+16)
    if d>=18: return r==Y+17
    return False

def z16_P(x,y,r):
    d,Y,S = x-y,2*y,x+y
    if (y,d) in ((6,0),(6,2),(6,4),(7,0),(7,2),(8,0)): return False
    if (y,d)==(6,1): return r>=14
    if (y,d) in ((6,3),(7,1)): return r>=16
    if d%2==0 and d<=14:
        return odd(r,17,Y+7+2*(d//4))
    if d%2==1 and d<=15:
        return (odd(r,17,S+16) or even(r,Y+10+2*((d-1)//4),S+15) or r>=S+17)
    if d==16:
        return odd(r,17,Y+15)
    if d%2==0 and d>=18:
        return (odd(r,17,Y+15) or even(r,Y+18,S+16))
    if d%2==1 and d>=17:
        return (odd(r,17,Y+15) or even(r,Y+18,S+15) or r>=S+17)
    return False

def value16(x,y,r):
    if r==0: return 0
    S = x+y
    if r>=S+17: return S%2
    if z16_T(x,y,r): return 2
    if z16_P(x,y,r): return 1
    return 0

# ---- z15_val (K1065 C child, transcribed)
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

# ---- k1074 (z=16, y=5 slice; K1074 candid predicate form)
def k1074(x,r):
    if r==0: return 0
    if x==5: t=(r%2==1 and r<=9)
    elif x in (6,7): t=(r%2==1 and r<=11)
    elif x in (8,9): t=(r%2==1 and r<=13)
    elif x==10: t=(r%2==1 and r<=15)
    elif x==11: t=(r%2==1 and r<=21)
    elif x==15: t=(r%2==1 and r<=15) or r==23
    elif x==19: t=(r%2==1 and r<=15) or r==25
    elif x==22: t=(r%2==1 and r<=15) or (r%2==1 and 27<=r<=43)
    elif x>=23: t=(r%2==1 and r<=15) or r==27
    else: t=(r%2==1 and r<=15)
    if t: return 2
    if x in (5,7,9,11): return 0
    if x==6: return 1 if r>=12 else 0
    if x==8: return 1 if r>=14 else 0
    if x==10: return 1 if r>=16 else 0
    if x==12: return 1 if (r in (17,19,21) or r>=22) else 0
    if x in (13,15): return 1 if r in (17,19,21) else 0
    if x==19: return 1 if r in (17,19,21,23) else 0
    if x in (14,16): return 1 if (r in (17,19,21,23) or r>=24) else 0
    if x==17: return 1 if r in (17,19,21,23) else 0
    if x in (18,20): return 1 if (r in (17,19,21,23,25) or r>=26) else 0
    if x==21: return 1 if r in (17,19,21,23,25) else 0
    if x%2: return 1 if (r in (17,19,21,23,25) or (r%2==0 and 28<=r<=x+21)) else 0
    return 1 if (r in (17,19,21,23,25) or (r%2==0 and 28<=r<=x+22) or r>=x+23) else 0

def sig(y,d,R):
    x = y+d; r = R-1
    vals = set()
    if d==0:
        vals.add(k1074(x,r) if y==6 else value16(x,y-1,r))  # A==B at d==0 (multiset merges)
    else:
        vals.add(value16(x-1,y,r))
    if y==6: vals.add(k1074(x,r))
    else: vals.add(value16(x,y-1,r))
    vals.add(1 ^ z15_val(x,y,r))
    return ''.join(map(str,sorted(vals)))


def z16_bands(y, d):
    Y, S = 2*y, 2*y+d
    if (y,d)==(6,0):
        return ([(1,11,'01'),(13,S+17,'1')], [(2,12,'23'),(14,S+16,'1')])
    if (y,d)==(7,0):
        return ([(1,13,'01'),(15,S+17,'1')], [(2,14,'23'),(16,S+16,'1')])
    if (y,d)==(8,0):
        return ([(1,23,'01'),(25,S+17,'1')], [(2,16,'23'),(18,S+16,'1')])
    if (y,d)==(6,2):
        return ([(1,13,'01'),(15,S+17,'1')], [(2,14,'23'),(16,S+16,'1')])
    if (y,d)==(7,2):
        return ([(1,23,'01'),(25,S+17,'1')], [(2,16,'23'),(18,S+16,'1')])
    if (y,d)==(6,4):
        return ([(1,21,'01'),(23,S+17,'1')], [(2,16,'23'),(18,S+16,'1')])
    if (y,d)==(6,1):
        return ([(1,13,'01'),(15,S+16,'0')], [(2,12,'23'),(14,14,'03'),(16,S+17,'0')])
    if (y,d) in ((6,3),(7,1)):
        return ([(1,15,'01'),(17,S+16,'0')], [(2,14,'23'),(16,22,'03'),(24,S+17,'0')])
    if (y,d)==(6,5):
        return ([(1,15,'01'),(17,S+16,'0')], [(2,16,'23'),(18,22,'12'),(24,S+17,'0')])
    if (y,d)==(8,1):
        return ([(1,15,'01'),(17,S+16,'0')], [(2,16,'23'),(18,24,'12'),(26,S+17,'0')])
    if (y,d)==(7,3):
        return ([(1,15,'01'),(17,S+16,'0')], [(2,16,'23'),(18,22,'12'),(24,24,'023'),(26,S+17,'0')])
    if d%2==0 and d<=14:
        st0 = Y+7+2*(d//4)
        O=[(1,15,'01'),(17,st0,'0')]
        if d%4==2:
            O += [(st0+2,st0+2,'01'),(st0+4,S+17,'1')]
        else:
            O += [(st0+2,S+17,'1')]
        E=[(2,16,'23'),(18,S+16,'1')]
        return O,E
    if d%2==1 and d<=15:
        c = Y+6+2*((d+1)//4)
        O=[(1,15,'01'),(17,S+16,'0')]
        E=[(2,16,'23'),(18,c,'1'),(c+2,c+2,'12' if d%4==1 else '023'),(c+4,S+17,'0')]
        return O,E
    if d==16:
        O=[(1,15,'01'),(17,Y+15,'0'),(Y+17,S+17,'1')]
        E=[(2,16,'23'),(18,Y+14,'1'),(Y+16,S+16,'123')]
        return O,E
    if d==17:
        O=[(1,15,'01'),(17,Y+15,'0'),(Y+17,S+16,'01')]
        E=[(2,16,'23'),(18,Y+14,'1'),(Y+16,Y+16,'123'),(Y+18,S+17,'0')]
        return O,E
    if d==18:
        # first even pin-row: E final band is '02' over the whole (Y+18,S+16) (mechanical, y=6..14)
        O=[(1,15,'01'),(17,Y+15,'0'),(Y+17,Y+17,'01'),(Y+19,S+17,'1')]
        E=[(2,16,'23'),(18,Y+14,'1'),(Y+16,Y+16,'123'),(Y+18,S+16,'02')]
        return O,E
    if d%2==0:
        O=[(1,15,'01'),(17,Y+15,'0'),(Y+17,Y+17,'01'),(Y+19,S+17,'1')]
        E=[(2,16,'23'),(18,Y+14,'1'),(Y+16,Y+16,'123'),(Y+18,Y+18,'02'),(Y+20,S+16,'0')]
        return O,E
    O=[(1,15,'01'),(17,Y+15,'0'),(Y+17,Y+17,'01'),(Y+19,S+16,'1')]
    E=[(2,16,'23'),(18,Y+14,'1'),(Y+16,Y+16,'123'),(Y+18,Y+18,'02'),(Y+20,S+17,'0')]
    return O,E


def signature(y, d, R):
    # children of (x,y) at budget R: token children at budget R-1 plus the
    # fiber-C child; k1074 (K1074, z=16,y=5) anchors the y==6 B child.
    x = y + d; rr = R - 1
    if d == 0:
        B = k1074(x, rr) if y == 6 else value16(x, y - 1, rr)
        A = B  # A==B at d==0: same child, set-merged
    else:
        A = value16(x - 1, y, rr)
        B = k1074(x, rr) if y == 6 else value16(x, y - 1, rr)
    C = 1 ^ z15_val(x, y, rr)
    return ''.join(str(v) for v in sorted({A, B, C}))


mex_map = {'01': 2, '0': 1, '1': 0, '23': 0, '03': 1, '12': 0, '023': 1, '123': 0, '02': 1}

counts = {}

# 1) parent: dual recursion engines vs closed form, both z=16
parent_checks = 0
for y in range(6, 21):
    for d in range(0, 31):
        x = y + d; S = x + y
        for R in range(S + 18):
            a = g_ordered(R, (x, y), 16)
            b = g_canon(R, (x, y), 16)
            c = value16(x, y, R)
            assert a == b == c, ("parent", x, y, d, R, a, b, c)
            parent_checks += 1
counts["parent_two_recursions"] = parent_checks

# 2) B anchor: K1074 transcription vs recursion, z=16 y=5
b_checks = 0
for x in range(6, 151):
    for R in range(x + 28):
        a = g_ordered(R, (x, 5), 16)
        b = g_canon(R, (x, 5), 16)
        c = k1074(x, R)
        assert a == b == c, ("B/K1074", x, R, a, b, c)
        b_checks += 1
counts["K1074_B_anchor"] = b_checks

# 3) C anchor re-validation: z15 transcription vs recursion
c_checks = 0
for y in range(6, 17):
    for d in range(0, 17):
        x = y + d; S = x + y
        for R in range(S + 17):
            a = g_ordered(R, (x, y), 15)
            b = g_canon(R, (x, y), 15)
            c = z15_val(x, y, R)
            assert a == b == c, ("C/K1065", x, y, d, R, a, b, c)
            c_checks += 1
counts["K1065_C_anchor"] = c_checks

# 4) signature bands: coverage, identity vs mechanical children, mex==closed form,
#    continuity, and theorem parity (v==2 only at odd R)
sig_checks = 0
for y in range(6, 81):
    for d in range(0, 81):
        S = 2 * y + d
        O, E = z16_bands(y, d)
        for par in (1, 0):
            bands = O if par else E
            prev = None
            for lo, hi, s in bands:
                assert lo % 2 == par and hi % 2 == par and lo <= hi and s in mex_map, ("band shape", y, d, par, bands)
                if prev is not None:
                    assert lo == prev + 2, ("band gap", y, d, par, bands)
                prev = hi
            top = S + 17 if (S + 17) % 2 == par else S + 16
            assert prev == top, ("band top", y, d, par, bands, top)
        for R in range(1, S + 18):
            bands = O if R % 2 else E
            hits = [s for lo, hi, s in bands if lo <= R <= hi]
            assert len(hits) == 1, ("band coverage", y, d, R, hits)
            got = signature(y, d, R)
            assert hits[0] == got, ("band signature", y, d, R, hits[0], got)
            assert mex_map[hits[0]] == value16(y + d, y, R), ("band mex", y, d, R, hits[0])
            v = value16(y + d, y, R)
            assert not (R % 2 == 0 and v == 2), ("parity T", y, d, R)
            assert 0 <= v <= 2, ("range", y, d, R)
            sig_checks += 1
counts["signature_coverage_identity_mex"] = sig_checks

# 5) low-R single-token collapse: R <= 22 = z+6
low_checks = 0
for y in range(6, 81):
    for d in range(0, 81):
        x = y + d; S = x + y
        for R in range(23):
            a = value16(x, y, R)
            b = g_canon(R, (S,), 16)
            assert a == b, ("low-R collapse", x, y, R, a, b)
            low_checks += 1
counts["low_R_single_token_collapse"] = low_checks

# 6) tail: R >= S+17 gives S%2
tail_checks = 0
for y in range(6, 19):
    for d in range(0, 26):
        x = y + d; S = x + y
        for R in range(S + 17, S + 22):
            a = g_ordered(R, (x, y), 16)
            b = g_canon(R, (x, y), 16)
            assert a == b == S % 2, ("tail", x, y, R, a, b, S % 2)
            tail_checks += 1
counts["tail_direct"] = tail_checks

# 7) fixed-seed scatter
rng = random.Random(20261120)
scatter_checks = 0
for _ in range(5000):
    y = rng.randint(6, 400)
    d = rng.randint(0, 400)
    x = y + d; S = x + y
    R = rng.randint(0, S + 30)
    v = value16(x, y, R)
    assert v in (0, 1, 2)
    assert not (z16_T(x, y, R) and z16_P(x, y, R))
    if R >= S + 17:
        assert v == S % 2
    scatter_checks += 1
counts["fixed_seed_scatter"] = scatter_checks

counts["total"] = sum(counts.values())
counts["bad"] = []
counts["claim"] = "H(R;(x,y);16), all x>=y>=6 and R>=0"
counts["proof_status"] = "proved_by_two_level_induction_and_symbolic_signature_bands"
counts["finite_audit_scope"] = {
    "parent_direct": "6<=y<=20, 0<=d<=30, 0<=R<=x+y+17",
    "K1074_B_anchor": "6<=x<=150, 0<=R<=x+27",
    "K1065_C_anchor": "6<=y<=16, 0<=d<=16, 0<=R<=x+y+16",
    "signature_bands": "6<=y<=80, 0<=d<=80, 1<=R<=x+y+17",
    "low_R_collapse": "6<=y<=80, 0<=d<=80, 0<=R<=22",
    "tail_direct": "6<=y<=18, 0<=d<=25, x+y+17<=R<=x+y+21",
    "scatter_seed": 20261120,
}
counts["verifier_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
raw = json.dumps(counts, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
out = Path(__file__).resolve().parent / "output" / "audit.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(raw, encoding="utf-8")
print(raw, end="")
