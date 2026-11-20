#!/usr/bin/env python3
"""Full cand9 draft (in_T9 measured + in_P9 fitted from probe) vs raw probe rows. Mismatch 0."""
import re

Y = 9

def q_odd(k):
    return k if k % 2 else k - 1

# ---------- T (value 2), verified mismatch=0 on 73811 probe points ----------
def in_T9(z, x, R):
    if R <= 0: return False
    if x <= z - Y - 1:
        return R % 2 == 1 and R <= q_odd(x + Y)
    d = x - z
    if z % 2 == 1:
        if d == -Y: return R % 2 == 1 and R <= z + Y - 1
        if d in (-7, -3, 1, 5, 9):
            pin = z + 2*Y + (d - Y) // 2
            return (R % 2 == 1 and R <= z) or R == pin
        if d == Y + 1:
            return (R % 2 == 1 and R <= z) or (R % 2 == 1 and z + 2*Y <= R <= x + z + Y)
        if d >= Y + 2:
            return (R % 2 == 1 and R <= z) or R == z + 2*Y
        return R % 2 == 1 and R <= z
    else:
        if d == -Y: return R % 2 == 1 and R <= z + Y
        if d in (-5, -1, 3, 7, 11):
            pin = z + (d + 3*Y) // 2
            return (R % 2 == 1 and R <= z - 1) or R == pin
        if d == Y + 1:
            return (R % 2 == 1 and R <= z - 1) or (R % 2 == 1 and z + 2*Y + 1 <= R <= x + z + Y)
        if d >= Y + 2:
            return (R % 2 == 1 and R <= z - 1) or R == z + 2*Y + 1
        return R % 2 == 1 and R <= z - 1

# ---------- P (value 1), fitted from probe ----------
def in_P9(z, x, R):
    if R <= 0: return False
    if x <= z - Y - 1:
        S = x + Y
        return S % 2 == 1 and R >= q_odd(S) + 1
    d = x - z
    b4 = 1 <= R - z <= 9 and (R - z) % 2 == 1
    b5 = b4 or (R - z == 11)
    b6 = b5 or (R - z == 13)
    b7 = b6 or (R - z == 15)
    base9 = b7 or (R - z == 17)
    if z % 2 == 1:
        if d == -9: return b4 or R >= z + 10
        if d == -8: return b4
        if d == -7: return b4 or R >= z + 11
        if d == -6: return b4
        if d == -5: return b5 or R >= z + 12
        if d == -4: return b5
        if d == -3: return b6 or R >= z + 14
        if d == -2: return b5
        if d == -1: return b6 or R >= z + 14
        if d == 0:  return b6
        if d == 1:  return b7 or R >= z + 16
        if d == 2:  return b6
        if d == 3:  return b7 or R >= z + 16
        if d == 4:  return b7
        if d == 5:  return base9 or R >= z + 18
        if d == 6:  return b7
        if d == 7:  return base9 or R >= z + 18
        if d == 8:  return base9
        if d == 9:  return base9 or R == z + 19 or R >= z + 20
        if d == 10: return base9
        band = (z + 18 <= R <= x + z + Y) and R % 2 == z % 2 and R != z + 2*Y
        tail = x % 2 == 0 and R >= x + z + Y + 1
        return base9 or band or tail
    else:
        if d == -9: return False
        if d == -8: return b4 or R >= z + 9
        if d == -7: return b4
        if d == -6: return b5 or R >= z + 12
        if d == -5: return b4
        if d == -4: return b5 or R >= z + 12
        if d == -3: return b5
        if d == -2: return b6 or R >= z + 14
        if d == -1: return b5
        if d == 0:  return b6 or R >= z + 14
        if d == 1:  return b6
        if d == 2:  return b7 or R >= z + 16
        if d == 3:  return b6
        if d == 4:  return b7 or R >= z + 16
        if d == 5:  return b7
        if d == 6:  return base9 or R >= z + 18
        if d == 7:  return b7
        if d == 8:  return base9 or R >= z + 18
        if d == 9:  return base9
        if d == 10:
            band = (z + 2*Y + 2 <= R <= x + z + Y) and R % 2 == z % 2
            tail = x % 2 == 0 and R >= x + z + Y + 1
            return base9 or band or tail
        band = (z + 2*Y + 2 <= R <= x + z + Y) and R % 2 == z % 2
        tail = x % 2 == 0 and R >= x + z + Y + 1
        return base9 or band or tail

def cand9(z, x, R):
    t = in_T9(z, x, R)
    p = in_P9(z, x, R)
    if t and p:
        return -99
    if t: return 2
    return 1 if p else 0

if __name__ == '__main__':
    pat = re.compile(r"z=(-?\d+) x=(-?\d+) d=(-?\d+) merge=(\d) :: (.+)")
    n = mt = ov = 0
    bad = []
    for line in open('probe_rows.txt'):
        m = pat.match(line.strip())
        if not m: continue
        z, x, d, mg = int(m[1]), int(m[2]), int(m[3]), int(m[4])
        vals = []
        for tok in m[5].split():
            v, c = tok.split('x')
            vals.extend([int(v)] * int(c))
        for R in range(1, len(vals) + 1):
            n += 1
            c = cand9(z, x, R)
            raw = vals[R - 1]
            if c == -99:
                ov += 1
                if len(bad) < 40: bad.append(('OV', z, x, d, R, raw))
            elif c != raw:
                mt += 1
                if len(bad) < 40: bad.append(('MM', z, x, d, R, raw, c))
    print(f"points={n} mismatch={mt} overlap_T_P={ov}")
    for b in bad[:40]:
        print(b)
