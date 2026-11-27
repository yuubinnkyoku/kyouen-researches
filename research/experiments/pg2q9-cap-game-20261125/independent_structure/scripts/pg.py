"""Small PG(2,9) toolkit for the independent verification.

Coordinate convention (verified against output/board_pg2q9.txt):
  GF(9) = GF(3)[i]/(i^2+1), element a+bi is encoded as label 3*a+b (0..8).
  A point is a canonical nonzero vector (first nonzero coordinate = 1).
  Board index = rank among sorted canonical vectors by (x-label, y-label, z-label):
    index 0            -> (0,0,1)
    index 1+z (0..8)   -> (0,1,z)
    index 10+9y+z      -> (1,y,z)
  (The conjugate labelling 3*a+2*b also reproduces the same line family; it is
   the field automorphism i -> -i.  Conic/cap families are invariant sets, so
   the choice does not affect them.)
"""
import itertools

# ---- field operations on labels 0..8, element = a + b i, label = 3a + b ----
def pair(l):
    return (l // 3, l % 3)


def label(a, b):
    return 3 * a + b


def _add(x, y):
    a, b = pair(x)
    c, d = pair(y)
    return label((a + c) % 3, (b + d) % 3)


def _neg(x):
    a, b = pair(x)
    return label((-a) % 3, (-b) % 3)


def _mul(x, y):
    a, b = pair(x)
    c, d = pair(y)
    # (a+bi)(c+di) = ac + bd i^2 + (ad+bc)i, i^2 = -1 = 2
    return label((a * c + 2 * b * d) % 3, (a * d + b * c) % 3)


ADD = [[_add(x, y) for y in range(9)] for x in range(9)]
MUL = [[_mul(x, y) for y in range(9)] for x in range(9)]
NEG = [_neg(x) for x in range(9)]
ONE = 3  # field 1 = label 3
TWO = 6  # field 2 = label 6 = -1
I = 1    # field i = label 1

# ---- points ----
def make_coords():
    coords = []
    coords.append((0, 0, ONE))
    for z in range(9):
        coords.append((0, ONE, z))
    for y in range(9):
        for z in range(9):
            coords.append((ONE, y, z))
    return coords


COORDS = make_coords()
NPOINTS = 91
FULL = (1 << 91) - 1


def dot(a, b):
    s = 0
    for x, y in zip(a, b):
        s = ADD[s][MUL[x][y]]
    return s


def zero_mask(coords, normal):
    m = 0
    for i, p in enumerate(coords):
        if dot(normal, p) == 0:
            m |= 1 << i
    return m


def make_lines(coords):
    normals = [(0, 0, ONE)]
    for z in range(9):
        normals.append((0, ONE, z))
    for y in range(9):
        for z in range(9):
            normals.append((ONE, y, z))
    masks = []
    seen = set()
    for nv in normals:
        m = zero_mask(coords, nv)
        assert m.bit_count() == 10, (nv, m.bit_count())
        if m not in seen:
            seen.add(m)
            masks.append(m)
    assert len(masks) == 91
    return masks


LINES = make_lines(COORDS)
# pair -> line id
PAIR_LINE = {}
for li, m in enumerate(LINES):
    pts = [p for p in range(NPOINTS) if (m >> p) & 1]
    for a, b in itertools.combinations(pts, 2):
        PAIR_LINE[(a, b)] = li


def line_mask(a, b):
    return LINES[PAIR_LINE[(a, b) if a < b else (b, a)]]


def secant_union(points):
    m = 0
    for a, b in itertools.combinations(points, 2):
        m |= line_mask(a, b)
    return m


def addable_mask(points):
    """Points not on any line through two of the given points."""
    return FULL & ~secant_union(points)


def is_cap(points):
    return all(PAIR_LINE[(a, b)] != PAIR_LINE[(a, c)]
               for a, b, c in itertools.combinations(sorted(points), 3))


FULL = (1 << 91) - 1
