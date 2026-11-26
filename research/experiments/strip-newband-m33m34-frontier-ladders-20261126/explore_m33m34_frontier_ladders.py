#!/usr/bin/env python3
"""explore_m33m34_frontier_ladders: FROZEN PRE-DECLARATION census for:

1. the THIRTY-FOUR binding candidate rows of the kit-8 frozen output
   section future_slice_registration_constants (commit 7af915fb, the
   publish-priority kit-8 census of 2026-11-26; the concurrent
   second-census kit 680421eb/e9847712 registered the same 32 core rows
   confirmatorily and its log S5 named THESE the operative ones): the
   ladder continuation / birth / death rows of m=19..m=28 (items 1-20),
   the m=29/m=30 rows (items 21-26), the CONTINGENT m=31/m=32
   mini-ladder rows (items 27-32, contingent on the kit-8 frontier
   first contacts which DID measure the 19th/20th parity datums), and
   the frontier first contacts m=33@z=65 / m=34@z=66 (items 33-34, the
   registered 21st / 22nd K1268 parity datum candidates, FIRST-EVER
   rows for those m). Every candidate literal is machine-regenerated
   engine-free from the K0832 closed form + the seat-lifecycle scaffold
   by derive_kit9.py (579 structural asserts, 0 failures; the
   regenerated prediction TEXT of all 34 rows byte-matches the kit-8
   frozen constants, proving the generator AND the transcription).
2. the STACK-SHADOW candidate enumeration (kit-8 log S5 item-9 rule,
   BINDING): at every kit-9 birth slice, every admissible co-token
   split stack {m,x,y} with x+y=co(d), x,y>=m seats at the NEW seat's
   S is registered as an explicit candidate (expected by the
   observation record: exact numeric mimic of the NEW seat). The
   enumeration is EMPTY at every kit-9 birth depth below mid-ladder
   (engine-free co(d)<2m diagnostic, derive-checked); the nonempty
   rows are m=19 z=59 (co=42: splits (19,23),(20,22),(21,21) -> the
   L8 S-family-size tracker expectation 4 at S=61) and m=20 z=60
   (co=42: splits (20,22),(21,21) -> family-size expectation 3 at
   S=62), both registered with the kit-8-second-census S5 wording.
3. the TRIO-TRACKER rows (kit-8 future item 37 + the second-census S5
   trio death-expectation row, NON-BINDING; any outcome is the datum):
   at m=19 z=58 and z=59 the stacked trio {19,19,19}@S=57 is tracked
   beside the binding seat candidates: the S=57 family GLIDE-DEAD
   slice z=58=S+1 expects CONFORM (the kit-8 published dead-shape
   collapse v(57,58,78)=1) by the L8 same-family observation; any
   other value is L8-external and is the datum.
4. the m=13/15/17 PROBE LIFECYCLE rows (kit-8 future item 36,
   contingent => the kit-8 probes DID measure their trios UP 2v0, so
   the lifecycle rows z=3m-1, 3m, 3m+1 are registered; NON-BINDING
   scaffold observation rows with K0832-scaffold seat candidates and
   trio expectations birth->one-past->stick->glide after the m=19
   precedent; the mid+1 birth rows carry the S5 item-9 stack
   candidates {m,m,m+2},{m,m+1,m+1} @S=3m+2, derive-derived).
5. the EVEN-m MID-SLICE PROBES m=14@z=40, m=16@z=46, m=18@z=52
   (kit-8 second-census S5 proposals; counter-probed 0-hit at this
   build BEFORE registering - see the counter-probe paragraph below):
   full x0 row records at the even mid-ladder birth slices d=m/2,
   z=3m-2, S_birth=3m; BINDING birth template seats EXACT (stick +
   NEW, even form DOWN 0v2 / UP 2v1) plus the NON-BINDING equistack
   trio {m,m,m}@S=3m UP 2v1 exact-mimic candidate (the even analogue
   of the kit-8 m=20 d=10 precedent (20,20,20)@60 UP 2v1).
6. the WINDOW SWEEPS m=31 z in {53..60} and m=32 z in {54..61} (kit-8
   frozen items 35-36 window proposals; register-before-measure
   satisfied by THIS FREEZE; candidates 0 separations each per the
   in-band-clean precedent; FIRST-EVER below-frontier rows for
   m=31/m=32, no strip-derivation claim made - m=31/m=32 are NOT
   strip-covered).
7. THE ANCHOR CHAIN: the 180 kit-8-era published anchors VERBATIM
   (inherited anchor_spec block, byte-copied from the kit-8 explorer at
   pin 7af915fb and re-measured here) PLUS the 54 kit-8 separation
   spots (48 rows of the publish-priority kit-8 census), machine-
   extracted from the published kit-8 frozen .out (fetched
   byte-identical, sha 5723304c...) and machine-verified 54/54 BEFORE
   the first run of this file by verify_new_anchors_kit9.py (canonical
   engine, published values only).
8. the K0832 battery: the UNION of the kit-8 1,004 battery literal
   triples (no prior datum lost; no prior literal dropped; sorted-
   unique triple set, the checked property unchanged: closed==
   canonical==ordered per triple) PLUS the kit-9 literals: stair rows
   of every measured row, the registered candidate collapse literals,
   the new anchor collapse literals, and the kit-10 future constants.

SWEEP-DOMAIN RULE (frozen here, disclosed): every depth row sweeps
S in {m..max(m+38, z+2)} with the published x0 convention (parts>=m,
arity<=3 TOTAL, X[0]=m, co-token m allowed). The z+2 extension covers
the NEW birth seats S(d)=z+2 where they exceed m+38: kit-9 needs it at
m=19 z=58/59 (S<=60/61) and m=20 z=59/60 (S<=61/62). Any separation
found inside the extended domain beyond the registered seats is a
deviation = the datum.

Counter-probe at this build (2026-11-26, head 332ce273): 12 kit-specific
content queries (kit-9, "m=33 z=65", frontier_m33, explore_m33m34,
"m=14 z=40", "m=16 z=46", "m=18 z=52", "even mid-slice",
inband_m31_z53, inband_m32, "m=13 z=38", "m=13 z=39") returned only
kit-8 registration/proposal records (the frozen constants of commit
7af915fb and the second-census S5 proposals), no measurement records,
and no experiment directory or log for any of this kit's rows exists
on main. Re-run at push time against then-current main and disclosed
in the push commit body.

DOUBLE-REGISTRATION CHECK (the kit-7 S6 item-3 lesson, machine-made
at this build): every one of the 34 binding rows was checked against
every measured row of the published kit-4..kit-8 chain (row, hole,
probe and window slices) - each registered slice is a genuinely new
(m,z) measurement (the m=31 z=62 / m=32 z=63 one-past rows are the
first post-frontier slices of the kit-8 first-contact lines).

NO K slot is claimed by this file; the 34 binding candidate rows, the
3 even-probe rows and the 16 window rows in this docstring were frozen
BEFORE the first run of this file (the trio-tracker and lifecycle
statuses are NON-BINDING and their outcome is the datum). The only edit
performed after any run must be disclosed here in dated form
(verifier-table or docstring fixes only; no candidate, engine, or
measurement code was edited at any time).
"""

import hashlib, json, sys
from functools import lru_cache

ENGINE_BLOCK = '''def mex(values):
    values = set(values)
    m = 0
    while m in values:
        m += 1
    return m

# ------------------------------------------------------------------
# Raw engines (verbatim from the published K1138 verifier block; the same
# transcription is embedded in the published y22 machine K1257).
# ------------------------------------------------------------------
@lru_cache(maxsize=6_000_000)
def H_ordered(R, X, z):
    if R == 0:
        return 0
    opts = set()
    for i, v in enumerate(X):
        if v > 1:
            opts.add(H_ordered(R - 1, X[:i] + (v - 1,) + X[i + 1:], z))
        else:
            opts.add(H_ordered(R - 1, X[:i] + X[i + 1:], z + 1))
    if z >= 1:
        opts.add(1 ^ H_ordered(R - 1, X, z - 1))
    return mex(opts)

@lru_cache(maxsize=6_000_000)
def H_canonical(R, X, z):
    X = tuple(sorted(X, reverse=True))
    if R == 0:
        return 0
    opts = set()
    i = 0
    while i < len(X):
        v = X[i]
        if v > 1:
            child = tuple(sorted(X[:i] + (v - 1,) + X[i + 1:], reverse=True))
            opts.add(H_canonical(R - 1, child, z))
        else:
            child = tuple(sorted(X[:i] + X[i + 1:], reverse=True))
            opts.add(H_canonical(R - 1, child, z + 1))
        while i + 1 < len(X) and X[i + 1] == v:
            i += 1
        i += 1
    if z >= 1:
        opts.add(1 ^ H_canonical(R - 1, X, z - 1))
    return mex(opts)

def vC(x, z, R):  # canonical-engine single token
    return H_canonical(R, (x,), z)
def vO(x, z, R):  # ordered-engine single token
    return H_ordered(R, (x,), z)

# ------------------------------------------------------------------
# Published K0832 single-token closed form (transcription of the published
# single_token block in the y22 machine K1257; see report provenance).
# ------------------------------------------------------------------
def q_odd(k):
    return k if k % 2 else k - 1

def single_token(x, z, R):
    if R == 0 or x <= 0:
        return 0
    if z == 0:
        return min(R, x) % 2
    if z == x:
        if R % 2 and R <= 2 * x - 1:
            return 2
        if R % 2 == 0 and R <= x - 1:
            return 0
        return x % 2
    if 1 <= z <= x - 1:
        m = q_odd(z)
        if R <= m:
            return 2 if R % 2 else 0
        if m < R < x + z:
            return (R + z) % 2
        return x % 2
    if z >= x + 1:
        m = q_odd(x)
        if R <= m:
            return 2 if R % 2 else 0
        return x % 2
    raise ValueError((x, z, R))
'''

PIN = 'bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92'
sha = hashlib.sha256(ENGINE_BLOCK.encode('utf-8')).hexdigest()
assert sha == PIN, sha
ns = {'lru_cache': lru_cache}
exec(ENGINE_BLOCK, ns)
H = ns['H_canonical']
v = ns['single_token']


def parts(s, lo, arity):
    """all multisets (nondecreasing tuples) of tokens >= lo, sum s, 1..arity tokens"""
    out = []

    def rec(rem, k, cur):
        if rem == 0:
            if 1 <= len(cur) <= arity:
                out.append(tuple(cur))
            return
        if k == arity:
            return
        for t in range(lo, rem + 1):
            if cur and t < cur[-1]:
                continue
            cur.append(t)
            rec(rem - t, k + 1, cur)
            cur.pop()

    rec(s, 0, [])
    return out


def row_record_x0(sec, rlabel, extra, R, z, m, smin, smax):
    """published residual-band record style: X = parts(S, m, 3) with
    X[0] == m, i.e. all parts >= m with co-token m allowed, arity <= 3
    TOTAL. Shape-for-shape comparable with the published entries."""
    H.cache_clear()
    sep = []
    scnt = 0
    for S in range(smin, smax + 1):
        for X in parts(S, m, 3):
            if not X or X[0] != m:
                continue
            hv = H(R, X, z)
            ev = v(S, z, R)
            scnt += 1
            if hv != ev:
                sep.append({'X': list(X), 'S': S, 'value': hv,
                            'collapse': ev,
                            'direction': 'UP' if hv > ev else 'DOWN'})
    return {'section': sec, 'label': rlabel, 'R': R, 'z': z, 'min': m,
            **extra, 'shapes': scnt, 'separations': sep}


K9_BINDING_JSON = "[\n {\n  \"cand\": \"EXACTLY ONE: {19,40}@S=59 UP 1v0 (collapse v(59,58,78)=0); {19,38} conform-DEAD at z=58=S+1 (collapse v(57,58,78)=1); death-of-d=9\",\n  \"dead_seat\": [\n   19,\n   38,\n   58\n  ],\n  \"item\": 1,\n  \"kind\": \"one-past\",\n  \"kind_label\": \"one-past\",\n  \"m\": 19,\n  \"seat_ud\": null,\n  \"seats\": [\n   [\n    19,\n    40,\n    59,\n    \"one-past seat\"\n   ]\n  ],\n  \"tracker\": [\n   {\n    \"S\": 57,\n    \"X\": [\n     19,\n     19,\n     19\n    ],\n    \"cand\": \"kit-8 second-census S5 trio death-expectation row: by L8 the trio tracks down with its S=57 family into the GLIDE-DEAD slice z=58=S+1: expected CONFORM (value = collapse v(57,58,78)=1, the kit-8 published z=58 dead-shape collapse); any other value is the datum (L8-external); NON-BINDING\",\n    \"m\": 19,\n    \"z\": 58\n   }\n  ],\n  \"z\": 58\n },\n {\n  \"cand\": \"EXACTLY TWO: stick {19,40} DOWN 1v2 (collapse v(59,59,79)=2) + NEW {19,42}@S=61 UP 2v0 (collapse v(61,59,79)=0), d=11 seat gap 23; STACK-SHADOW candidates (kit-8 log S5 item-9 rule, binding): every admissible co-token split of co=42 seats at the NEW seat S=61: {19,19,23} {19,20,22} {19,21,21} ; expected by the observation record: exact numeric mimic of the NEW seat (UP 2v0, same collapse); any deviation is the datum\",\n  \"dead_seat\": null,\n  \"item\": 2,\n  \"kind\": \"birth\",\n  \"kind_label\": \"birth\",\n  \"m\": 19,\n  \"seat_ud\": \"UP 2v0\",\n  \"seats\": [\n   [\n    19,\n    40,\n    59,\n    \"stick seat DOWN\"\n   ],\n   [\n    19,\n    42,\n    61,\n    \"NEW birth seat UP\"\n   ]\n  ],\n  \"stack_candidates\": [\n   {\n    \"S\": 61,\n    \"X\": [\n     19,\n     19,\n     23\n    ],\n    \"expect\": \"exact mimic of the NEW seat UP 2v0\"\n   },\n   {\n    \"S\": 61,\n    \"X\": [\n     19,\n     20,\n     22\n    ],\n    \"expect\": \"exact mimic of the NEW seat UP 2v0\"\n   },\n   {\n    \"S\": 61,\n    \"X\": [\n     19,\n     21,\n     21\n    ],\n    \"expect\": \"exact mimic of the NEW seat UP 2v0\"\n   }\n  ],\n  \"tracker\": [\n   {\n    \"S\": 57,\n    \"X\": [\n     19,\n     19,\n     19\n    ],\n    \"cand\": \"trio-tracker continuation: expected CONFORM (the S=57 family stays dead; collapse v(57,59,79)); any deviation is the datum; NON-BINDING\",\n    \"m\": 19,\n    \"z\": 59\n   }\n  ],\n  \"z\": 59\n },\n {\n  \"cand\": \"EXACTLY ONE: (20,40)@S=60 DOWN 0v1 (collapse v(60,59,80)=1); (20,38) conform-DEAD at z=59=S+1 (collapse v(58,59,80)=0); death-of-d=9\",\n  \"dead_seat\": [\n   20,\n   38,\n   59\n  ],\n  \"item\": 3,\n  \"kind\": \"one-past\",\n  \"kind_label\": \"one-past\",\n  \"m\": 20,\n  \"seat_ud\": null,\n  \"seats\": [\n   [\n    20,\n    40,\n    60,\n    \"one-past seat\"\n   ]\n  ],\n  \"z\": 59\n },\n {\n  \"cand\": \"EXACTLY TWO: stick (20,40) DOWN 0v2 (collapse v(60,60,81)=2) + NEW (20,42)@S=62 UP 2v1 (collapse v(62,60,81)=1), d=11 seat gap 22; STACK-SHADOW candidates (kit-8 log S5 item-9 rule, binding): every admissible co-token split of co=42 seats at the NEW seat S=62: {20,20,22} {20,21,21} ; expected by the observation record: exact numeric mimic of the NEW seat (UP 2v1, same collapse); any deviation is the datum\",\n  \"dead_seat\": null,\n  \"item\": 4,\n  \"kind\": \"birth\",\n  \"kind_label\": \"birth\",\n  \"m\": 20,\n  \"seat_ud\": \"UP 2v1\",\n  \"seats\": [\n   [\n    20,\n    40,\n    60,\n    \"stick seat DOWN\"\n   ],\n   [\n    20,\n    42,\n    62,\n    \"NEW birth seat UP\"\n   ]\n  ],\n  \"stack_candidates\": [\n   {\n    \"S\": 62,\n    \"X\": [\n     20,\n     20,\n     22\n    ],\n    \"expect\": \"exact mimic of the NEW seat UP 2v1\"\n   },\n   {\n    \"S\": 62,\n    \"X\": [\n     20,\n     21,\n     21\n    ],\n    \"expect\": \"exact mimic of the NEW seat UP 2v1\"\n   }\n  ],\n  \"z\": 60\n },\n {\n  \"cand\": \"EXACTLY ONE: {21,34}@S=55 UP 1v0 (collapse v(55,54,76)=0); {21,32} conform-DEAD at z=54=S+1 (collapse v(53,54,76)=1); death-of-d=5\",\n  \"dead_seat\": [\n   21,\n   32,\n   54\n  ],\n  \"item\": 5,\n  \"kind\": \"one-past\",\n  \"kind_label\": \"one-past\",\n  \"m\": 21,\n  \"seat_ud\": null,\n  \"seats\": [\n   [\n    21,\n    34,\n    55,\n    \"one-past seat\"\n   ]\n  ],\n  \"z\": 54\n },\n {\n  \"cand\": \"EXACTLY TWO: stick {21,34} DOWN 1v2 (collapse v(55,55,77)=2) + NEW {21,36}@S=57 UP 2v0 (collapse v(57,55,77)=0), d=7 seat gap 15\",\n  \"dead_seat\": null,\n  \"item\": 6,\n  \"kind\": \"birth\",\n  \"kind_label\": \"birth\",\n  \"m\": 21,\n  \"seat_ud\": \"UP 2v0\",\n  \"seats\": [\n   [\n    21,\n    34,\n    55,\n    \"stick seat DOWN\"\n   ],\n   [\n    21,\n    36,\n    57,\n    \"NEW birth seat UP\"\n   ]\n  ],\n  \"z\": 55\n },\n {\n  \"cand\": \"EXACTLY ONE: (22,34)@S=56 DOWN 0v1 (collapse v(56,55,78)=1); (22,32) conform-DEAD at z=55=S+1 (collapse v(54,55,78)=0); death-of-d=5\",\n  \"dead_seat\": [\n   22,\n   32,\n   55\n  ],\n  \"item\": 7,\n  \"kind\": \"one-past\",\n  \"kind_label\": \"one-past\",\n  \"m\": 22,\n  \"seat_ud\": null,\n  \"seats\": [\n   [\n    22,\n    34,\n    56,\n    \"one-past seat\"\n   ]\n  ],\n  \"z\": 55\n },\n {\n  \"cand\": \"EXACTLY TWO: stick (22,34) DOWN 0v2 (collapse v(56,56,79)=2) + NEW (22,36)@S=58 UP 2v1 (collapse v(58,56,79)=1), d=7 seat gap 14\",\n  \"dead_seat\": null,\n  \"item\": 8,\n  \"kind\": \"birth\",\n  \"kind_label\": \"birth\",\n  \"m\": 22,\n  \"seat_ud\": \"UP 2v1\",\n  \"seats\": [\n   [\n    22,\n    34,\n    56,\n    \"stick seat DOWN\"\n   ],\n   [\n    22,\n    36,\n    58,\n    \"NEW birth seat UP\"\n   ]\n  ],\n  \"z\": 56\n },\n {\n  \"cand\": \"EXACTLY ONE: {23,34}@S=57 UP 1v0 (collapse v(57,56,80)=0); {23,32} conform-DEAD at z=56=S+1 (collapse v(55,56,80)=1); death-of-d=4\",\n  \"dead_seat\": [\n   23,\n   32,\n   56\n  ],\n  \"item\": 9,\n  \"kind\": \"one-past\",\n  \"kind_label\": \"one-past\",\n  \"m\": 23,\n  \"seat_ud\": null,\n  \"seats\": [\n   [\n    23,\n    34,\n    57,\n    \"one-past seat\"\n   ]\n  ],\n  \"z\": 56\n },\n {\n  \"cand\": \"EXACTLY TWO: stick {23,34} DOWN 1v2 (collapse v(57,57,81)=2) + NEW {23,36}@S=59 UP 2v0 (collapse v(59,57,81)=0), d=6 seat gap 13\",\n  \"dead_seat\": null,\n  \"item\": 10,\n  \"kind\": \"birth\",\n  \"kind_label\": \"birth\",\n  \"m\": 23,\n  \"seat_ud\": \"UP 2v0\",\n  \"seats\": [\n   [\n    23,\n    34,\n    57,\n    \"stick seat DOWN\"\n   ],\n   [\n    23,\n    36,\n    59,\n    \"NEW birth seat UP\"\n   ]\n  ],\n  \"z\": 57\n },\n {\n  \"cand\": \"EXACTLY ONE: (24,34)@S=58 DOWN 0v1 (collapse v(58,57,82)=1); (24,32) conform-DEAD at z=57=S+1 (collapse v(56,57,82)=0); death-of-d=4\",\n  \"dead_seat\": [\n   24,\n   32,\n   57\n  ],\n  \"item\": 11,\n  \"kind\": \"one-past\",\n  \"kind_label\": \"one-past\",\n  \"m\": 24,\n  \"seat_ud\": null,\n  \"seats\": [\n   [\n    24,\n    34,\n    58,\n    \"one-past seat\"\n   ]\n  ],\n  \"z\": 57\n },\n {\n  \"cand\": \"EXACTLY TWO: stick (24,34) DOWN 0v2 (collapse v(58,58,83)=2) + NEW (24,36)@S=60 UP 2v1 (collapse v(60,58,83)=1), d=6 seat gap 12\",\n  \"dead_seat\": null,\n  \"item\": 12,\n  \"kind\": \"birth\",\n  \"kind_label\": \"birth\",\n  \"m\": 24,\n  \"seat_ud\": \"UP 2v1\",\n  \"seats\": [\n   [\n    24,\n    34,\n    58,\n    \"stick seat DOWN\"\n   ],\n   [\n    24,\n    36,\n    60,\n    \"NEW birth seat UP\"\n   ]\n  ],\n  \"z\": 58\n },\n {\n  \"cand\": \"EXACTLY ONE: {25,34}@S=59 UP 1v0 (collapse v(59,58,84)=0); {25,32} conform-DEAD at z=58=S+1 (collapse v(57,58,84)=1); death-of-d=3\",\n  \"dead_seat\": [\n   25,\n   32,\n   58\n  ],\n  \"item\": 13,\n  \"kind\": \"one-past\",\n  \"kind_label\": \"one-past\",\n  \"m\": 25,\n  \"seat_ud\": null,\n  \"seats\": [\n   [\n    25,\n    34,\n    59,\n    \"one-past seat\"\n   ]\n  ],\n  \"z\": 58\n },\n {\n  \"cand\": \"EXACTLY TWO: stick {25,34} DOWN 1v2 (collapse v(59,59,85)=2) + NEW {25,36}@S=61 UP 2v0 (collapse v(61,59,85)=0), d=5 seat gap 11\",\n  \"dead_seat\": null,\n  \"item\": 14,\n  \"kind\": \"birth\",\n  \"kind_label\": \"birth\",\n  \"m\": 25,\n  \"seat_ud\": \"UP 2v0\",\n  \"seats\": [\n   [\n    25,\n    34,\n    59,\n    \"stick seat DOWN\"\n   ],\n   [\n    25,\n    36,\n    61,\n    \"NEW birth seat UP\"\n   ]\n  ],\n  \"z\": 59\n },\n {\n  \"cand\": \"EXACTLY ONE: (26,34)@S=60 DOWN 0v1 (collapse v(60,59,86)=1); (26,32) conform-DEAD at z=59=S+1 (collapse v(58,59,86)=0); death-of-d=3\",\n  \"dead_seat\": [\n   26,\n   32,\n   59\n  ],\n  \"item\": 15,\n  \"kind\": \"one-past\",\n  \"kind_label\": \"one-past\",\n  \"m\": 26,\n  \"seat_ud\": null,\n  \"seats\": [\n   [\n    26,\n    34,\n    60,\n    \"one-past seat\"\n   ]\n  ],\n  \"z\": 59\n },\n {\n  \"cand\": \"EXACTLY TWO: stick (26,34) DOWN 0v2 (collapse v(60,60,87)=2) + NEW (26,36)@S=62 UP 2v1 (collapse v(62,60,87)=1), d=5 seat gap 10\",\n  \"dead_seat\": null,\n  \"item\": 16,\n  \"kind\": \"birth\",\n  \"kind_label\": \"birth\",\n  \"m\": 26,\n  \"seat_ud\": \"UP 2v1\",\n  \"seats\": [\n   [\n    26,\n    34,\n    60,\n    \"stick seat DOWN\"\n   ],\n   [\n    26,\n    36,\n    62,\n    \"NEW birth seat UP\"\n   ]\n  ],\n  \"z\": 60\n },\n {\n  \"cand\": \"EXACTLY ONE: {27,32}@S=59 UP 1v0 (collapse v(59,58,86)=0); {27,30} conform-DEAD at z=58=S+1 (collapse v(57,58,86)=1); death-of-d=1\",\n  \"dead_seat\": [\n   27,\n   30,\n   58\n  ],\n  \"item\": 17,\n  \"kind\": \"one-past\",\n  \"kind_label\": \"one-past\",\n  \"m\": 27,\n  \"seat_ud\": null,\n  \"seats\": [\n   [\n    27,\n    32,\n    59,\n    \"one-past seat\"\n   ]\n  ],\n  \"z\": 58\n },\n {\n  \"cand\": \"EXACTLY TWO: stick {27,32} DOWN 1v2 (collapse v(59,59,87)=2) + NEW {27,34}@S=61 UP 2v0 (collapse v(61,59,87)=0), d=3 seat gap 7\",\n  \"dead_seat\": null,\n  \"item\": 18,\n  \"kind\": \"birth\",\n  \"kind_label\": \"birth\",\n  \"m\": 27,\n  \"seat_ud\": \"UP 2v0\",\n  \"seats\": [\n   [\n    27,\n    32,\n    59,\n    \"stick seat DOWN\"\n   ],\n   [\n    27,\n    34,\n    61,\n    \"NEW birth seat UP\"\n   ]\n  ],\n  \"z\": 59\n },\n {\n  \"cand\": \"EXACTLY ONE: (28,32)@S=60 DOWN 0v1 (collapse v(60,59,88)=1); (28,30) conform-DEAD at z=59=S+1 (collapse v(58,59,88)=0); death-of-d=1\",\n  \"dead_seat\": [\n   28,\n   30,\n   59\n  ],\n  \"item\": 19,\n  \"kind\": \"one-past\",\n  \"kind_label\": \"one-past\",\n  \"m\": 28,\n  \"seat_ud\": null,\n  \"seats\": [\n   [\n    28,\n    32,\n    60,\n    \"one-past seat\"\n   ]\n  ],\n  \"z\": 59\n },\n {\n  \"cand\": \"EXACTLY TWO: stick (28,32) DOWN 0v2 (collapse v(60,60,89)=2) + NEW (28,34)@S=62 UP 2v1 (collapse v(62,60,89)=1), d=3 seat gap 6\",\n  \"dead_seat\": null,\n  \"item\": 20,\n  \"kind\": \"birth\",\n  \"kind_label\": \"birth\",\n  \"m\": 28,\n  \"seat_ud\": \"UP 2v1\",\n  \"seats\": [\n   [\n    28,\n    32,\n    60,\n    \"stick seat DOWN\"\n   ],\n   [\n    28,\n    34,\n    62,\n    \"NEW birth seat UP\"\n   ]\n  ],\n  \"z\": 60\n },\n {\n  \"cand\": \"EXACTLY TWO: stick {29,32} DOWN 1v2 (collapse v(61,61,91)=2) + NEW {29,34}@S=63 UP 2v0 (collapse v(63,61,91)=0), d=2 seat gap 5\",\n  \"dead_seat\": null,\n  \"item\": 21,\n  \"kind\": \"birth\",\n  \"kind_label\": \"birth\",\n  \"m\": 29,\n  \"seat_ud\": \"UP 2v0\",\n  \"seats\": [\n   [\n    29,\n    32,\n    61,\n    \"stick seat DOWN\"\n   ],\n   [\n    29,\n    34,\n    63,\n    \"NEW birth seat UP\"\n   ]\n  ],\n  \"z\": 61\n },\n {\n  \"cand\": \"EXACTLY ONE: {29,34}@S=63 UP 1v0 (collapse v(63,62,92)=0); {29,32} conform-DEAD at z=62=S+1 (collapse v(61,62,92)=1); death-of-d=1\",\n  \"dead_seat\": [\n   29,\n   32,\n   62\n  ],\n  \"item\": 22,\n  \"kind\": \"one-past\",\n  \"kind_label\": \"one-past\",\n  \"m\": 29,\n  \"seat_ud\": null,\n  \"seats\": [\n   [\n    29,\n    34,\n    63,\n    \"one-past seat\"\n   ]\n  ],\n  \"z\": 62\n },\n {\n  \"cand\": \"EXACTLY TWO: stick {29,34} DOWN 1v2 (collapse v(63,63,93)=2) + NEW {29,36}@S=65 UP 2v0 (collapse v(65,63,93)=0), d=3 seat gap 7\",\n  \"dead_seat\": null,\n  \"item\": 23,\n  \"kind\": \"birth\",\n  \"kind_label\": \"birth\",\n  \"m\": 29,\n  \"seat_ud\": \"UP 2v0\",\n  \"seats\": [\n   [\n    29,\n    34,\n    63,\n    \"stick seat DOWN\"\n   ],\n   [\n    29,\n    36,\n    65,\n    \"NEW birth seat UP\"\n   ]\n  ],\n  \"z\": 63\n },\n {\n  \"cand\": \"EXACTLY TWO: stick (30,32) DOWN 0v2 (collapse v(62,62,93)=2) + NEW (30,34)@S=64 UP 2v1 (collapse v(64,62,93)=1), d=2 seat gap 4\",\n  \"dead_seat\": null,\n  \"item\": 24,\n  \"kind\": \"birth\",\n  \"kind_label\": \"birth\",\n  \"m\": 30,\n  \"seat_ud\": \"UP 2v1\",\n  \"seats\": [\n   [\n    30,\n    32,\n    62,\n    \"stick seat DOWN\"\n   ],\n   [\n    30,\n    34,\n    64,\n    \"NEW birth seat UP\"\n   ]\n  ],\n  \"z\": 62\n },\n {\n  \"cand\": \"EXACTLY ONE: (30,34)@S=64 DOWN 0v1 (collapse v(64,63,94)=1); (30,32) conform-DEAD at z=63=S+1 (collapse v(62,63,94)=0); death-of-d=1\",\n  \"dead_seat\": [\n   30,\n   32,\n   63\n  ],\n  \"item\": 25,\n  \"kind\": \"one-past\",\n  \"kind_label\": \"one-past\",\n  \"m\": 30,\n  \"seat_ud\": null,\n  \"seats\": [\n   [\n    30,\n    34,\n    64,\n    \"one-past seat\"\n   ]\n  ],\n  \"z\": 63\n },\n {\n  \"cand\": \"EXACTLY TWO: stick (30,34) DOWN 0v2 (collapse v(64,64,95)=2) + NEW (30,36)@S=66 UP 2v1 (collapse v(66,64,95)=1), d=3 seat gap 6\",\n  \"dead_seat\": null,\n  \"item\": 26,\n  \"kind\": \"birth\",\n  \"kind_label\": \"birth\",\n  \"m\": 30,\n  \"seat_ud\": \"UP 2v1\",\n  \"seats\": [\n   [\n    30,\n    34,\n    64,\n    \"stick seat DOWN\"\n   ],\n   [\n    30,\n    36,\n    66,\n    \"NEW birth seat UP\"\n   ]\n  ],\n  \"z\": 64\n },\n {\n  \"cand\": \"EXACTLY ONE: {31,32}@S=63 UP 1v0 (collapse v(63,62,94)=0); one-past of the d=0 seat (frontier decay 2->1); CONTINGENT: registered under the assumption the kit-8 frontier first contact m=31@z=61 measures the 19th parity datum; any deviation is the datum\",\n  \"dead_seat\": null,\n  \"item\": 27,\n  \"kind\": \"one-past\",\n  \"kind_label\": \"one-past\",\n  \"m\": 31,\n  \"seat_ud\": null,\n  \"seats\": [\n   [\n    31,\n    32,\n    63,\n    \"one-past seat\"\n   ]\n  ],\n  \"z\": 62\n },\n {\n  \"cand\": \"EXACTLY TWO: stick {31,32} DOWN 1v2 (collapse v(63,63,95)=2) + NEW {31,34}@S=65 UP 2v0 (collapse v(65,63,95)=0), d=1 seat gap 3\",\n  \"dead_seat\": null,\n  \"item\": 28,\n  \"kind\": \"birth\",\n  \"kind_label\": \"birth\",\n  \"m\": 31,\n  \"seat_ud\": \"UP 2v0\",\n  \"seats\": [\n   [\n    31,\n    32,\n    63,\n    \"stick seat DOWN\"\n   ],\n   [\n    31,\n    34,\n    65,\n    \"NEW birth seat UP\"\n   ]\n  ],\n  \"z\": 63\n },\n {\n  \"cand\": \"EXACTLY ONE: {31,34}@S=65 UP 1v0 (collapse v(65,64,96)=0); {31,32} conform-DEAD at z=64=S+1 (collapse v(63,64,96)=1); death-of-d=0\",\n  \"dead_seat\": [\n   31,\n   32,\n   64\n  ],\n  \"item\": 29,\n  \"kind\": \"one-past\",\n  \"kind_label\": \"one-past\",\n  \"m\": 31,\n  \"seat_ud\": null,\n  \"seats\": [\n   [\n    31,\n    34,\n    65,\n    \"one-past seat\"\n   ]\n  ],\n  \"z\": 64\n },\n {\n  \"cand\": \"EXACTLY ONE: (32,32)@S=64 DOWN 0v1 (collapse v(64,63,96)=1); one-past of the d=0 seat (frontier decay 2->0); CONTINGENT: registered under the assumption the kit-8 frontier first contact m=31@z=61 measures the 19th parity datum; any deviation is the datum\",\n  \"dead_seat\": null,\n  \"item\": 30,\n  \"kind\": \"one-past\",\n  \"kind_label\": \"one-past\",\n  \"m\": 32,\n  \"seat_ud\": null,\n  \"seats\": [\n   [\n    32,\n    32,\n    64,\n    \"one-past seat\"\n   ]\n  ],\n  \"z\": 63\n },\n {\n  \"cand\": \"EXACTLY TWO: stick (32,32) DOWN 0v2 (collapse v(64,64,97)=2) + NEW (32,34)@S=66 UP 2v1 (collapse v(66,64,97)=1), d=1 seat gap 2\",\n  \"dead_seat\": null,\n  \"item\": 31,\n  \"kind\": \"birth\",\n  \"kind_label\": \"birth\",\n  \"m\": 32,\n  \"seat_ud\": \"UP 2v1\",\n  \"seats\": [\n   [\n    32,\n    32,\n    64,\n    \"stick seat DOWN\"\n   ],\n   [\n    32,\n    34,\n    66,\n    \"NEW birth seat UP\"\n   ]\n  ],\n  \"z\": 64\n },\n {\n  \"cand\": \"EXACTLY ONE: (32,34)@S=66 DOWN 0v1 (collapse v(66,65,98)=1); (32,32) conform-DEAD at z=65=S+1 (collapse v(64,65,98)=0); death-of-d=0\",\n  \"dead_seat\": [\n   32,\n   32,\n   65\n  ],\n  \"item\": 32,\n  \"kind\": \"one-past\",\n  \"kind_label\": \"one-past\",\n  \"m\": 32,\n  \"seat_ud\": null,\n  \"seats\": [\n   [\n    32,\n    34,\n    66,\n    \"one-past seat\"\n   ]\n  ],\n  \"z\": 65\n },\n {\n  \"cand\": \"EXACTLY ONE: {33,34}@S=67 UP 2v0 (collapse v(67,65,99)=0); z*(33)=2*33-2+1=65 per K1268 (derive_check double-checked); R=99\",\n  \"dead_seat\": null,\n  \"frontier\": true,\n  \"item\": 33,\n  \"kind\": \"frontier first contact proposal (FIRST-EVER m=33 row)\",\n  \"kind_label\": \"frontier first contact proposal (FIRST-EVER m=33 row)\",\n  \"m\": 33,\n  \"nth\": \"21st\",\n  \"seat_ud\": \"UP 2v0\",\n  \"seats\": [\n   [\n    33,\n    34,\n    67,\n    \"NEW frontier seat UP 2v0\"\n   ]\n  ],\n  \"z\": 65\n },\n {\n  \"cand\": \"EXACTLY ONE: (34,34)@S=68 UP 2v1 (collapse v(68,66,101)=1); z*(34)=2*34-2+0=66 per K1268 (derive_check double-checked); R=101\",\n  \"dead_seat\": null,\n  \"frontier\": true,\n  \"item\": 34,\n  \"kind\": \"frontier first contact proposal (FIRST-EVER m=34 row)\",\n  \"kind_label\": \"frontier first contact proposal (FIRST-EVER m=34 row)\",\n  \"m\": 34,\n  \"nth\": \"22nd\",\n  \"seat_ud\": \"UP 2v1\",\n  \"seats\": [\n   [\n    34,\n    34,\n    68,\n    \"NEW frontier seat UP 2v1\"\n   ]\n  ],\n  \"z\": 66\n }\n]"
K9_LIFECYCLE_JSON = "[\n {\n  \"cand\": \"EXACTLY ONE: {13,26}@S=39 UP 1v0 (collapse v(39,38,52)=0); {13,24} conform-DEAD at z=38=S+1 (collapse v(37,38,52)=1); death-of-d=5; any deviation is the datum (NON-BINDING scaffold row)\",\n  \"dead_seat\": [\n   13,\n   24,\n   38\n  ],\n  \"m\": 13,\n  \"seats\": [\n   [\n    13,\n    26,\n    39,\n    \"one-past seat\"\n   ]\n  ],\n  \"trio\": \"mimic: UP 1v0 (value 1, collapse v(39,38,52)) like the one-past of the family seat, or conform (value 0), or other; the m=19 z=56 precedent; NON-BINDING\",\n  \"z\": 38\n },\n {\n  \"cand\": \"EXACTLY TWO: stick {13,26} DOWN 1v2 (collapse v(39,39,53)=2) + NEW {13,28}@S=41 UP 2v0 (collapse v(41,39,53)=0), d=7 seat gap 15; any deviation is the datum (NON-BINDING scaffold row); STACK-SHADOW candidates (S5 item-9 rule): co=28 splits seat at S=41: {13,13,15} {13,14,14}; expected exact mimics; any deviation is the datum\",\n  \"dead_seat\": null,\n  \"m\": 13,\n  \"seats\": [\n   [\n    13,\n    26,\n    39,\n    \"stick seat DOWN\"\n   ],\n   [\n    13,\n    28,\n    41,\n    \"NEW birth seat UP\"\n   ]\n  ],\n  \"stack_candidates\": [\n   {\n    \"S\": 41,\n    \"X\": [\n     13,\n     13,\n     15\n    ],\n    \"expect\": \"exact mimic of the NEW seat UP 2v0\"\n   },\n   {\n    \"S\": 41,\n    \"X\": [\n     13,\n     14,\n     14\n    ],\n    \"expect\": \"exact mimic of the NEW seat UP 2v0\"\n   }\n  ],\n  \"trio\": \"mimic: DOWN 1v2 (value 1, collapse v(39,39,53)=2) like the stick of the family seat, or conform (value 2), or other; the m=19 z=57 precedent; NON-BINDING\",\n  \"z\": 39\n },\n {\n  \"cand\": \"EXACTLY ONE: {13,28}@S=41 UP 1v0 (collapse v(41,40,54)=0); {13,26} conform-DEAD at z=40=S+1 (collapse v(39,40,54)=1); death-of-d=6; any deviation is the datum (NON-BINDING scaffold row)\",\n  \"dead_seat\": [\n   13,\n   26,\n   40\n  ],\n  \"m\": 13,\n  \"seats\": [\n   [\n    13,\n    28,\n    41,\n    \"one-past seat\"\n   ]\n  ],\n  \"trio\": \"expected CONFORM (the S=39 family GLIDE-DEAD slice z=40=S+1, the death slice of the mid-ladder family; by L8 the trio tracks down with its family into death; the m=19 z=58 expectation registered same-source); any other value is the datum (L8-external); NON-BINDING\",\n  \"z\": 40\n },\n {\n  \"cand\": \"EXACTLY ONE: {15,30}@S=45 UP 1v0 (collapse v(45,44,60)=0); {15,28} conform-DEAD at z=44=S+1 (collapse v(43,44,60)=1); death-of-d=6; any deviation is the datum (NON-BINDING scaffold row)\",\n  \"dead_seat\": [\n   15,\n   28,\n   44\n  ],\n  \"m\": 15,\n  \"seats\": [\n   [\n    15,\n    30,\n    45,\n    \"one-past seat\"\n   ]\n  ],\n  \"trio\": \"mimic: UP 1v0 (value 1, collapse v(45,44,60)) like the one-past of the family seat, or conform (value 0), or other; the m=19 z=56 precedent; NON-BINDING\",\n  \"z\": 44\n },\n {\n  \"cand\": \"EXACTLY TWO: stick {15,30} DOWN 1v2 (collapse v(45,45,61)=2) + NEW {15,32}@S=47 UP 2v0 (collapse v(47,45,61)=0), d=8 seat gap 17; any deviation is the datum (NON-BINDING scaffold row); STACK-SHADOW candidates (S5 item-9 rule): co=32 splits seat at S=47: {15,15,17} {15,16,16}; expected exact mimics; any deviation is the datum\",\n  \"dead_seat\": null,\n  \"m\": 15,\n  \"seats\": [\n   [\n    15,\n    30,\n    45,\n    \"stick seat DOWN\"\n   ],\n   [\n    15,\n    32,\n    47,\n    \"NEW birth seat UP\"\n   ]\n  ],\n  \"stack_candidates\": [\n   {\n    \"S\": 47,\n    \"X\": [\n     15,\n     15,\n     17\n    ],\n    \"expect\": \"exact mimic of the NEW seat UP 2v0\"\n   },\n   {\n    \"S\": 47,\n    \"X\": [\n     15,\n     16,\n     16\n    ],\n    \"expect\": \"exact mimic of the NEW seat UP 2v0\"\n   }\n  ],\n  \"trio\": \"mimic: DOWN 1v2 (value 1, collapse v(45,45,61)=2) like the stick of the family seat, or conform (value 2), or other; the m=19 z=57 precedent; NON-BINDING\",\n  \"z\": 45\n },\n {\n  \"cand\": \"EXACTLY ONE: {15,32}@S=47 UP 1v0 (collapse v(47,46,62)=0); {15,30} conform-DEAD at z=46=S+1 (collapse v(45,46,62)=1); death-of-d=7; any deviation is the datum (NON-BINDING scaffold row)\",\n  \"dead_seat\": [\n   15,\n   30,\n   46\n  ],\n  \"m\": 15,\n  \"seats\": [\n   [\n    15,\n    32,\n    47,\n    \"one-past seat\"\n   ]\n  ],\n  \"trio\": \"expected CONFORM (the S=45 family GLIDE-DEAD slice z=46=S+1, the death slice of the mid-ladder family; by L8 the trio tracks down with its family into death; the m=19 z=58 expectation registered same-source); any other value is the datum (L8-external); NON-BINDING\",\n  \"z\": 46\n },\n {\n  \"cand\": \"EXACTLY ONE: {17,34}@S=51 UP 1v0 (collapse v(51,50,68)=0); {17,32} conform-DEAD at z=50=S+1 (collapse v(49,50,68)=1); death-of-d=7; any deviation is the datum (NON-BINDING scaffold row)\",\n  \"dead_seat\": [\n   17,\n   32,\n   50\n  ],\n  \"m\": 17,\n  \"seats\": [\n   [\n    17,\n    34,\n    51,\n    \"one-past seat\"\n   ]\n  ],\n  \"trio\": \"mimic: UP 1v0 (value 1, collapse v(51,50,68)) like the one-past of the family seat, or conform (value 0), or other; the m=19 z=56 precedent; NON-BINDING\",\n  \"z\": 50\n },\n {\n  \"cand\": \"EXACTLY TWO: stick {17,34} DOWN 1v2 (collapse v(51,51,69)=2) + NEW {17,36}@S=53 UP 2v0 (collapse v(53,51,69)=0), d=9 seat gap 19; any deviation is the datum (NON-BINDING scaffold row); STACK-SHADOW candidates (S5 item-9 rule): co=36 splits seat at S=53: {17,17,19} {17,18,18}; expected exact mimics; any deviation is the datum\",\n  \"dead_seat\": null,\n  \"m\": 17,\n  \"seats\": [\n   [\n    17,\n    34,\n    51,\n    \"stick seat DOWN\"\n   ],\n   [\n    17,\n    36,\n    53,\n    \"NEW birth seat UP\"\n   ]\n  ],\n  \"stack_candidates\": [\n   {\n    \"S\": 53,\n    \"X\": [\n     17,\n     17,\n     19\n    ],\n    \"expect\": \"exact mimic of the NEW seat UP 2v0\"\n   },\n   {\n    \"S\": 53,\n    \"X\": [\n     17,\n     18,\n     18\n    ],\n    \"expect\": \"exact mimic of the NEW seat UP 2v0\"\n   }\n  ],\n  \"trio\": \"mimic: DOWN 1v2 (value 1, collapse v(51,51,69)=2) like the stick of the family seat, or conform (value 2), or other; the m=19 z=57 precedent; NON-BINDING\",\n  \"z\": 51\n },\n {\n  \"cand\": \"EXACTLY ONE: {17,36}@S=53 UP 1v0 (collapse v(53,52,70)=0); {17,34} conform-DEAD at z=52=S+1 (collapse v(51,52,70)=1); death-of-d=8; any deviation is the datum (NON-BINDING scaffold row)\",\n  \"dead_seat\": [\n   17,\n   34,\n   52\n  ],\n  \"m\": 17,\n  \"seats\": [\n   [\n    17,\n    36,\n    53,\n    \"one-past seat\"\n   ]\n  ],\n  \"trio\": \"expected CONFORM (the S=51 family GLIDE-DEAD slice z=52=S+1, the death slice of the mid-ladder family; by L8 the trio tracks down with its family into death; the m=19 z=58 expectation registered same-source); any other value is the datum (L8-external); NON-BINDING\",\n  \"z\": 52\n }\n]"
K9_PROBES_JSON = "[\n {\n  \"cand\": \"EXACTLY TWO: stick (14,26) DOWN 0v2 (collapse v(40,40,55)=2) + NEW (14,28)@S=42 UP 2v1 (collapse v(42,40,55)=1), d=7 seat gap 14\",\n  \"dead_seat\": null,\n  \"m\": 14,\n  \"seats\": [\n   [\n    14,\n    26,\n    40,\n    \"stick seat DOWN\"\n   ],\n   [\n    14,\n    28,\n    42,\n    \"NEW birth seat UP\"\n   ]\n  ],\n  \"stack_candidates\": [\n   {\n    \"S\": 42,\n    \"X\": [\n     14,\n     14,\n     14\n    ],\n    \"expect\": \"exact mimic of the NEW seat UP 2v1\"\n   }\n  ],\n  \"trio\": \"trio {14,14,14}@S=42 exact-mimic candidate of the NEW seat UP 2v1 (value 2, collapse v(42,40,55)=1), or conform (value 1), or other; the even analogue of the kit-8 m=20 d=10 precedent (20,20,20)@60 UP 2v1; NON-BINDING probe, any outcome is the datum\",\n  \"z\": 40\n },\n {\n  \"cand\": \"EXACTLY TWO: stick (16,30) DOWN 0v2 (collapse v(46,46,63)=2) + NEW (16,32)@S=48 UP 2v1 (collapse v(48,46,63)=1), d=8 seat gap 16\",\n  \"dead_seat\": null,\n  \"m\": 16,\n  \"seats\": [\n   [\n    16,\n    30,\n    46,\n    \"stick seat DOWN\"\n   ],\n   [\n    16,\n    32,\n    48,\n    \"NEW birth seat UP\"\n   ]\n  ],\n  \"stack_candidates\": [\n   {\n    \"S\": 48,\n    \"X\": [\n     16,\n     16,\n     16\n    ],\n    \"expect\": \"exact mimic of the NEW seat UP 2v1\"\n   }\n  ],\n  \"trio\": \"trio {16,16,16}@S=48 exact-mimic candidate of the NEW seat UP 2v1 (value 2, collapse v(48,46,63)=1), or conform (value 1), or other; the even analogue of the kit-8 m=20 d=10 precedent (20,20,20)@60 UP 2v1; NON-BINDING probe, any outcome is the datum\",\n  \"z\": 46\n },\n {\n  \"cand\": \"EXACTLY TWO: stick (18,34) DOWN 0v2 (collapse v(52,52,71)=2) + NEW (18,36)@S=54 UP 2v1 (collapse v(54,52,71)=1), d=9 seat gap 18\",\n  \"dead_seat\": null,\n  \"m\": 18,\n  \"seats\": [\n   [\n    18,\n    34,\n    52,\n    \"stick seat DOWN\"\n   ],\n   [\n    18,\n    36,\n    54,\n    \"NEW birth seat UP\"\n   ]\n  ],\n  \"stack_candidates\": [\n   {\n    \"S\": 54,\n    \"X\": [\n     18,\n     18,\n     18\n    ],\n    \"expect\": \"exact mimic of the NEW seat UP 2v1\"\n   }\n  ],\n  \"trio\": \"trio {18,18,18}@S=54 exact-mimic candidate of the NEW seat UP 2v1 (value 2, collapse v(54,52,71)=1), or conform (value 1), or other; the even analogue of the kit-8 m=20 d=10 precedent (20,20,20)@60 UP 2v1; NON-BINDING probe, any outcome is the datum\",\n  \"z\": 52\n }\n]"
K10_FUTURE_JSON = "[\n {\n  \"kind\": \"one-past\",\n  \"m\": 19,\n  \"prediction\": \"EXACTLY ONE: {19,42}@S=61 UP 1v0 (collapse v(61,60,80)=0); {19,40} conform-DEAD at z=60=S+1 (collapse v(59,60,80)=1); death-of-d=10\",\n  \"z\": 60\n },\n {\n  \"kind\": \"birth\",\n  \"m\": 19,\n  \"prediction\": \"EXACTLY TWO: stick {19,42} DOWN 1v2 (collapse v(61,61,81)=2) + NEW {19,44}@S=63 UP 2v0 (collapse v(63,61,81)=0), d=12 seat gap 25\",\n  \"z\": 61\n },\n {\n  \"kind\": \"one-past\",\n  \"m\": 20,\n  \"prediction\": \"EXACTLY ONE: (20,42)@S=62 DOWN 0v1 (collapse v(62,61,82)=1); (20,40) conform-DEAD at z=61=S+1 (collapse v(60,61,82)=0); death-of-d=10\",\n  \"z\": 61\n },\n {\n  \"kind\": \"birth\",\n  \"m\": 20,\n  \"prediction\": \"EXACTLY TWO: stick (20,42) DOWN 0v2 (collapse v(62,62,83)=2) + NEW (20,44)@S=64 UP 2v1 (collapse v(64,62,83)=1), d=12 seat gap 24\",\n  \"z\": 62\n },\n {\n  \"kind\": \"one-past\",\n  \"m\": 21,\n  \"prediction\": \"EXACTLY ONE: {21,36}@S=57 UP 1v0 (collapse v(57,56,78)=0); {21,34} conform-DEAD at z=56=S+1 (collapse v(55,56,78)=1); death-of-d=6\",\n  \"z\": 56\n },\n {\n  \"kind\": \"birth\",\n  \"m\": 21,\n  \"prediction\": \"EXACTLY TWO: stick {21,36} DOWN 1v2 (collapse v(57,57,79)=2) + NEW {21,38}@S=59 UP 2v0 (collapse v(59,57,79)=0), d=8 seat gap 17\",\n  \"z\": 57\n },\n {\n  \"kind\": \"one-past\",\n  \"m\": 22,\n  \"prediction\": \"EXACTLY ONE: (22,36)@S=58 DOWN 0v1 (collapse v(58,57,80)=1); (22,34) conform-DEAD at z=57=S+1 (collapse v(56,57,80)=0); death-of-d=6\",\n  \"z\": 57\n },\n {\n  \"kind\": \"birth\",\n  \"m\": 22,\n  \"prediction\": \"EXACTLY TWO: stick (22,36) DOWN 0v2 (collapse v(58,58,81)=2) + NEW (22,38)@S=60 UP 2v1 (collapse v(60,58,81)=1), d=8 seat gap 16\",\n  \"z\": 58\n },\n {\n  \"kind\": \"one-past\",\n  \"m\": 23,\n  \"prediction\": \"EXACTLY ONE: {23,36}@S=59 UP 1v0 (collapse v(59,58,82)=0); {23,34} conform-DEAD at z=58=S+1 (collapse v(57,58,82)=1); death-of-d=5\",\n  \"z\": 58\n },\n {\n  \"kind\": \"birth\",\n  \"m\": 23,\n  \"prediction\": \"EXACTLY TWO: stick {23,36} DOWN 1v2 (collapse v(59,59,83)=2) + NEW {23,38}@S=61 UP 2v0 (collapse v(61,59,83)=0), d=7 seat gap 15\",\n  \"z\": 59\n },\n {\n  \"kind\": \"one-past\",\n  \"m\": 24,\n  \"prediction\": \"EXACTLY ONE: (24,36)@S=60 DOWN 0v1 (collapse v(60,59,84)=1); (24,34) conform-DEAD at z=59=S+1 (collapse v(58,59,84)=0); death-of-d=5\",\n  \"z\": 59\n },\n {\n  \"kind\": \"birth\",\n  \"m\": 24,\n  \"prediction\": \"EXACTLY TWO: stick (24,36) DOWN 0v2 (collapse v(60,60,85)=2) + NEW (24,38)@S=62 UP 2v1 (collapse v(62,60,85)=1), d=7 seat gap 14\",\n  \"z\": 60\n },\n {\n  \"kind\": \"one-past\",\n  \"m\": 25,\n  \"prediction\": \"EXACTLY ONE: {25,36}@S=61 UP 1v0 (collapse v(61,60,86)=0); {25,34} conform-DEAD at z=60=S+1 (collapse v(59,60,86)=1); death-of-d=4\",\n  \"z\": 60\n },\n {\n  \"kind\": \"birth\",\n  \"m\": 25,\n  \"prediction\": \"EXACTLY TWO: stick {25,36} DOWN 1v2 (collapse v(61,61,87)=2) + NEW {25,38}@S=63 UP 2v0 (collapse v(63,61,87)=0), d=6 seat gap 13\",\n  \"z\": 61\n },\n {\n  \"kind\": \"one-past\",\n  \"m\": 26,\n  \"prediction\": \"EXACTLY ONE: (26,36)@S=62 DOWN 0v1 (collapse v(62,61,88)=1); (26,34) conform-DEAD at z=61=S+1 (collapse v(60,61,88)=0); death-of-d=4\",\n  \"z\": 61\n },\n {\n  \"kind\": \"birth\",\n  \"m\": 26,\n  \"prediction\": \"EXACTLY TWO: stick (26,36) DOWN 0v2 (collapse v(62,62,89)=2) + NEW (26,38)@S=64 UP 2v1 (collapse v(64,62,89)=1), d=6 seat gap 12\",\n  \"z\": 62\n },\n {\n  \"kind\": \"one-past\",\n  \"m\": 27,\n  \"prediction\": \"EXACTLY ONE: {27,34}@S=61 UP 1v0 (collapse v(61,60,88)=0); {27,32} conform-DEAD at z=60=S+1 (collapse v(59,60,88)=1); death-of-d=2\",\n  \"z\": 60\n },\n {\n  \"kind\": \"birth\",\n  \"m\": 27,\n  \"prediction\": \"EXACTLY TWO: stick {27,34} DOWN 1v2 (collapse v(61,61,89)=2) + NEW {27,36}@S=63 UP 2v0 (collapse v(63,61,89)=0), d=4 seat gap 9\",\n  \"z\": 61\n },\n {\n  \"kind\": \"one-past\",\n  \"m\": 28,\n  \"prediction\": \"EXACTLY ONE: (28,34)@S=62 DOWN 0v1 (collapse v(62,61,90)=1); (28,32) conform-DEAD at z=61=S+1 (collapse v(60,61,90)=0); death-of-d=2\",\n  \"z\": 61\n },\n {\n  \"kind\": \"birth\",\n  \"m\": 28,\n  \"prediction\": \"EXACTLY TWO: stick (28,34) DOWN 0v2 (collapse v(62,62,91)=2) + NEW (28,36)@S=64 UP 2v1 (collapse v(64,62,91)=1), d=4 seat gap 8\",\n  \"z\": 62\n },\n {\n  \"kind\": \"birth\",\n  \"m\": 29,\n  \"prediction\": \"EXACTLY TWO: stick {29,36} DOWN 1v2 (collapse v(65,65,95)=2) + NEW {29,38}@S=67 UP 2v0 (collapse v(67,65,95)=0), d=4 seat gap 9\",\n  \"z\": 65\n },\n {\n  \"kind\": \"one-past\",\n  \"m\": 29,\n  \"prediction\": \"EXACTLY ONE: {29,38}@S=67 UP 1v0 (collapse v(67,66,96)=0); {29,36} conform-DEAD at z=66=S+1 (collapse v(65,66,96)=1); death-of-d=3\",\n  \"z\": 66\n },\n {\n  \"kind\": \"birth\",\n  \"m\": 29,\n  \"prediction\": \"EXACTLY TWO: stick {29,38} DOWN 1v2 (collapse v(67,67,97)=2) + NEW {29,40}@S=69 UP 2v0 (collapse v(69,67,97)=0), d=5 seat gap 11\",\n  \"z\": 67\n },\n {\n  \"kind\": \"birth\",\n  \"m\": 30,\n  \"prediction\": \"EXACTLY TWO: stick (30,36) DOWN 0v2 (collapse v(66,66,97)=2) + NEW (30,38)@S=68 UP 2v1 (collapse v(68,66,97)=1), d=4 seat gap 8\",\n  \"z\": 66\n },\n {\n  \"kind\": \"one-past\",\n  \"m\": 30,\n  \"prediction\": \"EXACTLY ONE: (30,38)@S=68 DOWN 0v1 (collapse v(68,67,98)=1); (30,36) conform-DEAD at z=67=S+1 (collapse v(66,67,98)=0); death-of-d=3\",\n  \"z\": 67\n },\n {\n  \"kind\": \"birth\",\n  \"m\": 30,\n  \"prediction\": \"EXACTLY TWO: stick (30,38) DOWN 0v2 (collapse v(68,68,99)=2) + NEW (30,40)@S=70 UP 2v1 (collapse v(70,68,99)=1), d=5 seat gap 10\",\n  \"z\": 68\n },\n {\n  \"kind\": \"one-past\",\n  \"m\": 31,\n  \"prediction\": \"EXACTLY ONE: {31,34}@S=65 UP 1v0 (collapse v(65,64,96)=0); {31,32} conform-DEAD at z=64=S+1 (collapse v(63,64,96)=1); death-of-d=0\",\n  \"z\": 64\n },\n {\n  \"kind\": \"birth\",\n  \"m\": 31,\n  \"prediction\": \"EXACTLY TWO: stick {31,34} DOWN 1v2 (collapse v(65,65,97)=2) + NEW {31,36}@S=67 UP 2v0 (collapse v(67,65,97)=0), d=2 seat gap 5\",\n  \"z\": 65\n },\n {\n  \"kind\": \"one-past\",\n  \"m\": 31,\n  \"prediction\": \"EXACTLY ONE: {31,36}@S=67 UP 1v0 (collapse v(67,66,98)=0); {31,34} conform-DEAD at z=66=S+1 (collapse v(65,66,98)=1); death-of-d=1\",\n  \"z\": 66\n },\n {\n  \"kind\": \"one-past\",\n  \"m\": 32,\n  \"prediction\": \"EXACTLY ONE: (32,34)@S=66 DOWN 0v1 (collapse v(66,65,98)=1); (32,32) conform-DEAD at z=65=S+1 (collapse v(64,65,98)=0); death-of-d=0\",\n  \"z\": 65\n },\n {\n  \"kind\": \"birth\",\n  \"m\": 32,\n  \"prediction\": \"EXACTLY TWO: stick (32,34) DOWN 0v2 (collapse v(66,66,99)=2) + NEW (32,36)@S=68 UP 2v1 (collapse v(68,66,99)=1), d=2 seat gap 4\",\n  \"z\": 66\n },\n {\n  \"kind\": \"one-past\",\n  \"m\": 32,\n  \"prediction\": \"EXACTLY ONE: (32,36)@S=68 DOWN 0v1 (collapse v(68,67,100)=1); (32,34) conform-DEAD at z=67=S+1 (collapse v(66,67,100)=0); death-of-d=1\",\n  \"z\": 67\n },\n {\n  \"kind\": \"frontier first contact proposal (FIRST-EVER m=35 row)\",\n  \"m\": 35,\n  \"prediction\": \"EXACTLY ONE: {35,36}@S=71 UP 2v0 (collapse v(71,69,105)=0); z*(35)=2*35-2+1=69 per K1268 (derive_check double-checked); R=105\",\n  \"z\": 69\n },\n {\n  \"kind\": \"frontier first contact proposal (FIRST-EVER m=36 row)\",\n  \"m\": 36,\n  \"prediction\": \"EXACTLY ONE: (36,36)@S=72 UP 2v1 (collapse v(72,70,107)=1); z*(36)=2*36-2+0=70 per K1268 (derive_check double-checked); R=107\",\n  \"z\": 70\n },\n {\n  \"d\": 12,\n  \"kind\": \"stack-shadow candidates for the kit-10 birth rows (kit-8 log S5 item-9 rule, engine-free)\",\n  \"m\": 19,\n  \"prediction\": \"co(19,12)=44 => 4 admissible splits (19,25),(20,24),(21,23),(22,22) seating stacks {19,19,25},{19,20,24},{19,21,23},{19,22,22} @S=63 as exact numeric mimics of the NEW seat {19,44}@S=63 UP 2v0; any deviation is the datum\"\n },\n {\n  \"d\": 12,\n  \"kind\": \"stack-shadow candidates for the kit-10 birth rows (kit-8 log S5 item-9 rule, engine-free)\",\n  \"m\": 20,\n  \"prediction\": \"co(20,12)=44 => 3 admissible splits (20,24),(21,23),(22,22) seating stacks {20,20,24},{20,21,23},{20,22,22} @S=64 as exact numeric mimics of the NEW seat (20,44)@S=64 UP 2v1; any deviation is the datum\"\n },\n {\n  \"kind\": \"in-band window sweep proposal\",\n  \"m\": 33,\n  \"prediction\": \"0 separations each (candidate); z*(33)-8..-1 = 57..64; m=33 is NOT strip-covered; register before measuring\",\n  \"z\": \"57..64\"\n },\n {\n  \"kind\": \"in-band window sweep proposal\",\n  \"m\": 34,\n  \"prediction\": \"0 separations each (candidate); z*(34)-8..-1 = 58..65; m=34 is NOT strip-covered; register before measuring\",\n  \"z\": \"58..65\"\n },\n {\n  \"kind\": \"trio-tracker continuation proposal (contingent on kit-9 outcomes, NON-BINDING, log-level)\",\n  \"m\": 19,\n  \"prediction\": \"if the kit-9 trio-tracker rows measure the S=57 family GLIDE-DEAD/CONFORM as registered, the m=19 trio lifecycle is COMPLETE birth->one-past->stick->death and the m=13/15/17 lifecycle termini z=3m+1 become the shadow-death template; if any trio row deviates, the deviation is the datum and the trio ledger reopens\"\n },\n {\n  \"kind\": \"even-m probe continuation proposal (contingent on kit-9 probe outcomes, NON-BINDING)\",\n  \"prediction\": \"if the m=14/16/18 mid-slice probes measure their equistacks as exact mimics of the NEW seats (UP 2v1), register the even-m lifecycle rows (one-past z=3m+1, stick z=3m+2) and the m=13/15/17-style next-depth stack splits for those m; any other outcome is the datum either way\"\n }\n]"
BATTERY_TRIPLES_JSON = "[\n [\n  13,\n  37,\n  51\n ],\n [\n  13,\n  38,\n  52\n ],\n [\n  13,\n  39,\n  53\n ],\n [\n  13,\n  40,\n  54\n ],\n [\n  14,\n  40,\n  55\n ],\n [\n  15,\n  37,\n  51\n ],\n [\n  15,\n  38,\n  52\n ],\n [\n  15,\n  39,\n  53\n ],\n [\n  15,\n  40,\n  54\n ],\n [\n  15,\n  43,\n  59\n ],\n [\n  15,\n  44,\n  60\n ],\n [\n  15,\n  45,\n  61\n ],\n [\n  15,\n  46,\n  62\n ],\n [\n  16,\n  40,\n  55\n ],\n [\n  16,\n  46,\n  63\n ],\n [\n  17,\n  43,\n  59\n ],\n [\n  17,\n  44,\n  60\n ],\n [\n  17,\n  45,\n  61\n ],\n [\n  17,\n  46,\n  62\n ],\n [\n  17,\n  49,\n  67\n ],\n [\n  17,\n  50,\n  68\n ],\n [\n  17,\n  51,\n  69\n ],\n [\n  17,\n  52,\n  70\n ],\n [\n  18,\n  46,\n  63\n ],\n [\n  18,\n  52,\n  71\n ],\n [\n  19,\n  49,\n  67\n ],\n [\n  19,\n  50,\n  68\n ],\n [\n  19,\n  51,\n  69\n ],\n [\n  19,\n  52,\n  70\n ],\n [\n  19,\n  54,\n  74\n ],\n [\n  19,\n  55,\n  75\n ],\n [\n  19,\n  56,\n  76\n ],\n [\n  19,\n  57,\n  77\n ],\n [\n  19,\n  58,\n  78\n ],\n [\n  19,\n  59,\n  79\n ],\n [\n  20,\n  52,\n  71\n ],\n [\n  20,\n  55,\n  76\n ],\n [\n  20,\n  56,\n  77\n ],\n [\n  20,\n  57,\n  78\n ],\n [\n  20,\n  58,\n  79\n ],\n [\n  20,\n  59,\n  80\n ],\n [\n  20,\n  60,\n  81\n ],\n [\n  21,\n  50,\n  72\n ],\n [\n  21,\n  51,\n  73\n ],\n [\n  21,\n  52,\n  74\n ],\n [\n  21,\n  53,\n  75\n ],\n [\n  21,\n  54,\n  74\n ],\n [\n  21,\n  54,\n  76\n ],\n [\n  21,\n  55,\n  75\n ],\n [\n  21,\n  55,\n  77\n ],\n [\n  21,\n  56,\n  76\n ],\n [\n  21,\n  57,\n  77\n ],\n [\n  21,\n  58,\n  78\n ],\n [\n  21,\n  59,\n  79\n ],\n [\n  22,\n  51,\n  74\n ],\n [\n  22,\n  52,\n  75\n ],\n [\n  22,\n  53,\n  76\n ],\n [\n  22,\n  54,\n  77\n ],\n [\n  22,\n  55,\n  76\n ],\n [\n  22,\n  55,\n  78\n ],\n [\n  22,\n  56,\n  77\n ],\n [\n  22,\n  56,\n  79\n ],\n [\n  22,\n  57,\n  78\n ],\n [\n  22,\n  58,\n  79\n ],\n [\n  22,\n  59,\n  80\n ],\n [\n  22,\n  60,\n  81\n ],\n [\n  23,\n  50,\n  72\n ],\n [\n  23,\n  51,\n  73\n ],\n [\n  23,\n  52,\n  74\n ],\n [\n  23,\n  52,\n  76\n ],\n [\n  23,\n  53,\n  75\n ],\n [\n  23,\n  53,\n  77\n ],\n [\n  23,\n  54,\n  76\n ],\n [\n  23,\n  54,\n  78\n ],\n [\n  23,\n  55,\n  77\n ],\n [\n  23,\n  55,\n  79\n ],\n [\n  23,\n  56,\n  80\n ],\n [\n  23,\n  57,\n  81\n ],\n [\n  24,\n  51,\n  74\n ],\n [\n  24,\n  52,\n  75\n ],\n [\n  24,\n  53,\n  76\n ],\n [\n  24,\n  53,\n  78\n ],\n [\n  24,\n  54,\n  77\n ],\n [\n  24,\n  54,\n  79\n ],\n [\n  24,\n  55,\n  78\n ],\n [\n  24,\n  55,\n  80\n ],\n [\n  24,\n  56,\n  79\n ],\n [\n  24,\n  56,\n  81\n ],\n [\n  24,\n  57,\n  82\n ],\n [\n  24,\n  58,\n  83\n ],\n [\n  25,\n  27,\n  53\n ],\n [\n  25,\n  28,\n  54\n ],\n [\n  25,\n  29,\n  55\n ],\n [\n  25,\n  30,\n  56\n ],\n [\n  25,\n  31,\n  57\n ],\n [\n  25,\n  32,\n  58\n ],\n [\n  25,\n  33,\n  59\n ],\n [\n  25,\n  34,\n  60\n ],\n [\n  25,\n  35,\n  61\n ],\n [\n  25,\n  36,\n  62\n ],\n [\n  25,\n  37,\n  63\n ],\n [\n  25,\n  38,\n  64\n ],\n [\n  25,\n  39,\n  65\n ],\n [\n  25,\n  40,\n  66\n ],\n [\n  25,\n  52,\n  76\n ],\n [\n  25,\n  53,\n  77\n ],\n [\n  25,\n  53,\n  79\n ],\n [\n  25,\n  54,\n  78\n ],\n [\n  25,\n  54,\n  80\n ],\n [\n  25,\n  55,\n  79\n ],\n [\n  25,\n  55,\n  81\n ],\n [\n  25,\n  56,\n  80\n ],\n [\n  25,\n  56,\n  82\n ],\n [\n  25,\n  57,\n  81\n ],\n [\n  25,\n  57,\n  83\n ],\n [\n  25,\n  58,\n  84\n ],\n [\n  25,\n  59,\n  85\n ],\n [\n  26,\n  25,\n  52\n ],\n [\n  26,\n  27,\n  54\n ],\n [\n  26,\n  28,\n  55\n ],\n [\n  26,\n  29,\n  56\n ],\n [\n  26,\n  30,\n  57\n ],\n [\n  26,\n  31,\n  58\n ],\n [\n  26,\n  32,\n  59\n ],\n [\n  26,\n  33,\n  60\n ],\n [\n  26,\n  34,\n  61\n ],\n [\n  26,\n  35,\n  62\n ],\n [\n  26,\n  36,\n  63\n ],\n [\n  26,\n  37,\n  51\n ],\n [\n  26,\n  37,\n  64\n ],\n [\n  26,\n  38,\n  52\n ],\n [\n  26,\n  38,\n  65\n ],\n [\n  26,\n  39,\n  53\n ],\n [\n  26,\n  39,\n  66\n ],\n [\n  26,\n  40,\n  54\n ],\n [\n  26,\n  40,\n  67\n ],\n [\n  26,\n  41,\n  68\n ],\n [\n  26,\n  42,\n  69\n ],\n [\n  26,\n  53,\n  78\n ],\n [\n  26,\n  54,\n  79\n ],\n [\n  26,\n  54,\n  81\n ],\n [\n  26,\n  55,\n  80\n ],\n [\n  26,\n  55,\n  82\n ],\n [\n  26,\n  56,\n  81\n ],\n [\n  26,\n  56,\n  83\n ],\n [\n  26,\n  57,\n  82\n ],\n [\n  26,\n  57,\n  84\n ],\n [\n  26,\n  58,\n  83\n ],\n [\n  26,\n  58,\n  85\n ],\n [\n  26,\n  59,\n  86\n ],\n [\n  26,\n  60,\n  87\n ],\n [\n  27,\n  27,\n  41\n ],\n [\n  27,\n  27,\n  53\n ],\n [\n  27,\n  28,\n  54\n ],\n [\n  27,\n  29,\n  55\n ],\n [\n  27,\n  30,\n  56\n ],\n [\n  27,\n  31,\n  57\n ],\n [\n  27,\n  32,\n  58\n ],\n [\n  27,\n  33,\n  59\n ],\n [\n  27,\n  34,\n  60\n ],\n [\n  27,\n  35,\n  61\n ],\n [\n  27,\n  36,\n  62\n ],\n [\n  27,\n  37,\n  51\n ],\n [\n  27,\n  37,\n  63\n ],\n [\n  27,\n  38,\n  52\n ],\n [\n  27,\n  38,\n  64\n ],\n [\n  27,\n  39,\n  53\n ],\n [\n  27,\n  39,\n  65\n ],\n [\n  27,\n  40,\n  54\n ],\n [\n  27,\n  40,\n  66\n ],\n [\n  27,\n  45,\n  73\n ],\n [\n  27,\n  46,\n  74\n ],\n [\n  27,\n  47,\n  75\n ],\n [\n  27,\n  48,\n  76\n ],\n [\n  27,\n  49,\n  77\n ],\n [\n  27,\n  50,\n  78\n ],\n [\n  27,\n  51,\n  79\n ],\n [\n  27,\n  52,\n  80\n ],\n [\n  27,\n  53,\n  79\n ],\n [\n  27,\n  54,\n  80\n ],\n [\n  27,\n  54,\n  82\n ],\n [\n  27,\n  55,\n  81\n ],\n [\n  27,\n  55,\n  83\n ],\n [\n  27,\n  56,\n  82\n ],\n [\n  27,\n  56,\n  84\n ],\n [\n  27,\n  57,\n  83\n ],\n [\n  27,\n  57,\n  85\n ],\n [\n  27,\n  58,\n  84\n ],\n [\n  27,\n  58,\n  86\n ],\n [\n  27,\n  59,\n  85\n ],\n [\n  27,\n  59,\n  87\n ],\n [\n  28,\n  25,\n  52\n ],\n [\n  28,\n  27,\n  54\n ],\n [\n  28,\n  28,\n  55\n ],\n [\n  28,\n  29,\n  56\n ],\n [\n  28,\n  30,\n  57\n ],\n [\n  28,\n  31,\n  58\n ],\n [\n  28,\n  32,\n  59\n ],\n [\n  28,\n  33,\n  60\n ],\n [\n  28,\n  34,\n  61\n ],\n [\n  28,\n  35,\n  62\n ],\n [\n  28,\n  36,\n  63\n ],\n [\n  28,\n  37,\n  64\n ],\n [\n  28,\n  38,\n  65\n ],\n [\n  28,\n  39,\n  66\n ],\n [\n  28,\n  40,\n  55\n ],\n [\n  28,\n  40,\n  67\n ],\n [\n  28,\n  41,\n  68\n ],\n [\n  28,\n  42,\n  69\n ],\n [\n  28,\n  46,\n  75\n ],\n [\n  28,\n  47,\n  76\n ],\n [\n  28,\n  48,\n  77\n ],\n [\n  28,\n  49,\n  78\n ],\n [\n  28,\n  50,\n  79\n ],\n [\n  28,\n  51,\n  80\n ],\n [\n  28,\n  52,\n  81\n ],\n [\n  28,\n  53,\n  82\n ],\n [\n  28,\n  54,\n  81\n ],\n [\n  28,\n  55,\n  82\n ],\n [\n  28,\n  55,\n  84\n ],\n [\n  28,\n  56,\n  83\n ],\n [\n  28,\n  56,\n  85\n ],\n [\n  28,\n  57,\n  84\n ],\n [\n  28,\n  57,\n  86\n ],\n [\n  28,\n  58,\n  85\n ],\n [\n  28,\n  58,\n  87\n ],\n [\n  28,\n  59,\n  86\n ],\n [\n  28,\n  59,\n  88\n ],\n [\n  28,\n  60,\n  87\n ],\n [\n  28,\n  60,\n  89\n ],\n [\n  29,\n  27,\n  41\n ],\n [\n  29,\n  40,\n  55\n ],\n [\n  29,\n  45,\n  73\n ],\n [\n  29,\n  46,\n  74\n ],\n [\n  29,\n  47,\n  75\n ],\n [\n  29,\n  48,\n  76\n ],\n [\n  29,\n  49,\n  77\n ],\n [\n  29,\n  49,\n  79\n ],\n [\n  29,\n  50,\n  78\n ],\n [\n  29,\n  50,\n  80\n ],\n [\n  29,\n  51,\n  79\n ],\n [\n  29,\n  51,\n  81\n ],\n [\n  29,\n  52,\n  80\n ],\n [\n  29,\n  52,\n  82\n ],\n [\n  29,\n  53,\n  83\n ],\n [\n  29,\n  54,\n  82\n ],\n [\n  29,\n  54,\n  84\n ],\n [\n  29,\n  55,\n  83\n ],\n [\n  29,\n  55,\n  85\n ],\n [\n  29,\n  56,\n  84\n ],\n [\n  29,\n  56,\n  86\n ],\n [\n  29,\n  57,\n  85\n ],\n [\n  29,\n  57,\n  87\n ],\n [\n  29,\n  58,\n  86\n ],\n [\n  29,\n  58,\n  88\n ],\n [\n  29,\n  59,\n  87\n ],\n [\n  29,\n  59,\n  89\n ],\n [\n  29,\n  60,\n  90\n ],\n [\n  29,\n  61,\n  91\n ],\n [\n  29,\n  62,\n  92\n ],\n [\n  29,\n  63,\n  93\n ],\n [\n  30,\n  43,\n  59\n ],\n [\n  30,\n  44,\n  60\n ],\n [\n  30,\n  45,\n  61\n ],\n [\n  30,\n  46,\n  62\n ],\n [\n  30,\n  46,\n  75\n ],\n [\n  30,\n  47,\n  76\n ],\n [\n  30,\n  48,\n  77\n ],\n [\n  30,\n  49,\n  78\n ],\n [\n  30,\n  50,\n  79\n ],\n [\n  30,\n  50,\n  81\n ],\n [\n  30,\n  51,\n  80\n ],\n [\n  30,\n  51,\n  82\n ],\n [\n  30,\n  52,\n  81\n ],\n [\n  30,\n  52,\n  83\n ],\n [\n  30,\n  53,\n  82\n ],\n [\n  30,\n  53,\n  84\n ],\n [\n  30,\n  54,\n  85\n ],\n [\n  30,\n  55,\n  84\n ],\n [\n  30,\n  55,\n  86\n ],\n [\n  30,\n  56,\n  85\n ],\n [\n  30,\n  56,\n  87\n ],\n [\n  30,\n  57,\n  86\n ],\n [\n  30,\n  57,\n  88\n ],\n [\n  30,\n  58,\n  87\n ],\n [\n  30,\n  58,\n  89\n ],\n [\n  30,\n  59,\n  88\n ],\n [\n  30,\n  59,\n  90\n ],\n [\n  30,\n  60,\n  89\n ],\n [\n  30,\n  60,\n  91\n ],\n [\n  30,\n  61,\n  92\n ],\n [\n  30,\n  62,\n  93\n ],\n [\n  30,\n  63,\n  94\n ],\n [\n  30,\n  64,\n  95\n ],\n [\n  31,\n  29,\n  45\n ],\n [\n  31,\n  30,\n  46\n ],\n [\n  31,\n  43,\n  59\n ],\n [\n  31,\n  44,\n  60\n ],\n [\n  31,\n  45,\n  61\n ],\n [\n  31,\n  46,\n  62\n ],\n [\n  31,\n  49,\n  79\n ],\n [\n  31,\n  50,\n  80\n ],\n [\n  31,\n  51,\n  81\n ],\n [\n  31,\n  52,\n  82\n ],\n [\n  31,\n  53,\n  83\n ],\n [\n  31,\n  53,\n  85\n ],\n [\n  31,\n  54,\n  84\n ],\n [\n  31,\n  54,\n  86\n ],\n [\n  31,\n  55,\n  85\n ],\n [\n  31,\n  55,\n  87\n ],\n [\n  31,\n  56,\n  86\n ],\n [\n  31,\n  56,\n  88\n ],\n [\n  31,\n  57,\n  87\n ],\n [\n  31,\n  57,\n  89\n ],\n [\n  31,\n  58,\n  88\n ],\n [\n  31,\n  58,\n  90\n ],\n [\n  31,\n  59,\n  89\n ],\n [\n  31,\n  59,\n  91\n ],\n [\n  31,\n  60,\n  90\n ],\n [\n  31,\n  60,\n  92\n ],\n [\n  31,\n  61,\n  91\n ],\n [\n  31,\n  61,\n  93\n ],\n [\n  31,\n  62,\n  92\n ],\n [\n  31,\n  62,\n  94\n ],\n [\n  31,\n  63,\n  93\n ],\n [\n  31,\n  63,\n  95\n ],\n [\n  31,\n  64,\n  96\n ],\n [\n  32,\n  30,\n  47\n ],\n [\n  32,\n  31,\n  48\n ],\n [\n  32,\n  46,\n  63\n ],\n [\n  32,\n  50,\n  81\n ],\n [\n  32,\n  51,\n  82\n ],\n [\n  32,\n  52,\n  83\n ],\n [\n  32,\n  53,\n  84\n ],\n [\n  32,\n  54,\n  85\n ],\n [\n  32,\n  54,\n  87\n ],\n [\n  32,\n  55,\n  86\n ],\n [\n  32,\n  55,\n  88\n ],\n [\n  32,\n  56,\n  87\n ],\n [\n  32,\n  56,\n  89\n ],\n [\n  32,\n  57,\n  88\n ],\n [\n  32,\n  57,\n  90\n ],\n [\n  32,\n  58,\n  89\n ],\n [\n  32,\n  58,\n  91\n ],\n [\n  32,\n  59,\n  90\n ],\n [\n  32,\n  59,\n  92\n ],\n [\n  32,\n  60,\n  91\n ],\n [\n  32,\n  60,\n  93\n ],\n [\n  32,\n  61,\n  92\n ],\n [\n  32,\n  61,\n  94\n ],\n [\n  32,\n  62,\n  93\n ],\n [\n  32,\n  62,\n  95\n ],\n [\n  32,\n  63,\n  94\n ],\n [\n  32,\n  63,\n  96\n ],\n [\n  32,\n  64,\n  95\n ],\n [\n  32,\n  64,\n  97\n ],\n [\n  32,\n  65,\n  98\n ],\n [\n  33,\n  28,\n  45\n ],\n [\n  33,\n  29,\n  46\n ],\n [\n  33,\n  30,\n  47\n ],\n [\n  33,\n  31,\n  48\n ],\n [\n  33,\n  32,\n  49\n ],\n [\n  33,\n  33,\n  47\n ],\n [\n  33,\n  46,\n  63\n ],\n [\n  33,\n  53,\n  85\n ],\n [\n  33,\n  54,\n  86\n ],\n [\n  33,\n  55,\n  87\n ],\n [\n  33,\n  56,\n  88\n ],\n [\n  33,\n  57,\n  89\n ],\n [\n  33,\n  58,\n  90\n ],\n [\n  33,\n  59,\n  91\n ],\n [\n  33,\n  60,\n  92\n ],\n [\n  33,\n  61,\n  93\n ],\n [\n  33,\n  62,\n  94\n ],\n [\n  33,\n  63,\n  95\n ],\n [\n  33,\n  64,\n  96\n ],\n [\n  33,\n  65,\n  99\n ],\n [\n  34,\n  28,\n  46\n ],\n [\n  34,\n  29,\n  47\n ],\n [\n  34,\n  30,\n  48\n ],\n [\n  34,\n  31,\n  49\n ],\n [\n  34,\n  32,\n  50\n ],\n [\n  34,\n  49,\n  67\n ],\n [\n  34,\n  50,\n  68\n ],\n [\n  34,\n  51,\n  69\n ],\n [\n  34,\n  52,\n  70\n ],\n [\n  34,\n  54,\n  87\n ],\n [\n  34,\n  55,\n  88\n ],\n [\n  34,\n  56,\n  89\n ],\n [\n  34,\n  57,\n  90\n ],\n [\n  34,\n  58,\n  91\n ],\n [\n  34,\n  59,\n  92\n ],\n [\n  34,\n  60,\n  93\n ],\n [\n  34,\n  61,\n  94\n ],\n [\n  34,\n  62,\n  95\n ],\n [\n  34,\n  63,\n  96\n ],\n [\n  34,\n  64,\n  97\n ],\n [\n  34,\n  65,\n  98\n ],\n [\n  34,\n  66,\n  101\n ],\n [\n  35,\n  28,\n  46\n ],\n [\n  35,\n  29,\n  47\n ],\n [\n  35,\n  30,\n  48\n ],\n [\n  35,\n  31,\n  49\n ],\n [\n  35,\n  32,\n  50\n ],\n [\n  35,\n  33,\n  47\n ],\n [\n  35,\n  35,\n  53\n ],\n [\n  35,\n  49,\n  67\n ],\n [\n  35,\n  50,\n  68\n ],\n [\n  35,\n  51,\n  69\n ],\n [\n  35,\n  52,\n  70\n ],\n [\n  35,\n  65,\n  99\n ],\n [\n  36,\n  28,\n  47\n ],\n [\n  36,\n  29,\n  48\n ],\n [\n  36,\n  30,\n  49\n ],\n [\n  36,\n  31,\n  50\n ],\n [\n  36,\n  32,\n  51\n ],\n [\n  36,\n  52,\n  71\n ],\n [\n  36,\n  66,\n  101\n ],\n [\n  37,\n  35,\n  53\n ],\n [\n  37,\n  37,\n  51\n ],\n [\n  37,\n  38,\n  52\n ],\n [\n  37,\n  52,\n  71\n ],\n [\n  38,\n  25,\n  45\n ],\n [\n  38,\n  26,\n  46\n ],\n [\n  38,\n  54,\n  74\n ],\n [\n  38,\n  55,\n  75\n ],\n [\n  38,\n  56,\n  76\n ],\n [\n  38,\n  57,\n  77\n ],\n [\n  38,\n  58,\n  78\n ],\n [\n  38,\n  59,\n  79\n ],\n [\n  39,\n  37,\n  51\n ],\n [\n  39,\n  37,\n  57\n ],\n [\n  39,\n  38,\n  52\n ],\n [\n  39,\n  38,\n  58\n ],\n [\n  39,\n  39,\n  53\n ],\n [\n  39,\n  39,\n  59\n ],\n [\n  39,\n  40,\n  54\n ],\n [\n  39,\n  54,\n  74\n ],\n [\n  39,\n  55,\n  75\n ],\n [\n  39,\n  56,\n  76\n ],\n [\n  39,\n  57,\n  77\n ],\n [\n  39,\n  58,\n  78\n ],\n [\n  39,\n  59,\n  79\n ],\n [\n  40,\n  38,\n  59\n ],\n [\n  40,\n  39,\n  60\n ],\n [\n  40,\n  40,\n  55\n ],\n [\n  40,\n  40,\n  61\n ],\n [\n  40,\n  55,\n  76\n ],\n [\n  40,\n  56,\n  77\n ],\n [\n  40,\n  57,\n  78\n ],\n [\n  40,\n  58,\n  79\n ],\n [\n  40,\n  59,\n  80\n ],\n [\n  40,\n  60,\n  81\n ],\n [\n  41,\n  39,\n  53\n ],\n [\n  41,\n  39,\n  59\n ],\n [\n  41,\n  40,\n  54\n ],\n [\n  41,\n  40,\n  60\n ],\n [\n  41,\n  41,\n  61\n ],\n [\n  41,\n  55,\n  76\n ],\n [\n  41,\n  56,\n  77\n ],\n [\n  41,\n  57,\n  78\n ],\n [\n  41,\n  58,\n  79\n ],\n [\n  41,\n  59,\n  80\n ],\n [\n  41,\n  60,\n  81\n ],\n [\n  42,\n  40,\n  55\n ],\n [\n  42,\n  40,\n  61\n ],\n [\n  42,\n  41,\n  62\n ],\n [\n  42,\n  42,\n  63\n ],\n [\n  42,\n  50,\n  72\n ],\n [\n  42,\n  51,\n  73\n ],\n [\n  42,\n  52,\n  74\n ],\n [\n  42,\n  53,\n  75\n ],\n [\n  42,\n  54,\n  76\n ],\n [\n  42,\n  55,\n  77\n ],\n [\n  43,\n  41,\n  61\n ],\n [\n  43,\n  41,\n  63\n ],\n [\n  43,\n  42,\n  62\n ],\n [\n  43,\n  42,\n  64\n ],\n [\n  43,\n  43,\n  59\n ],\n [\n  43,\n  43,\n  63\n ],\n [\n  43,\n  43,\n  65\n ],\n [\n  43,\n  44,\n  60\n ],\n [\n  43,\n  50,\n  72\n ],\n [\n  43,\n  51,\n  73\n ],\n [\n  43,\n  52,\n  74\n ],\n [\n  43,\n  53,\n  75\n ],\n [\n  43,\n  54,\n  76\n ],\n [\n  43,\n  55,\n  77\n ],\n [\n  44,\n  42,\n  63\n ],\n [\n  44,\n  42,\n  65\n ],\n [\n  44,\n  43,\n  64\n ],\n [\n  44,\n  43,\n  66\n ],\n [\n  44,\n  44,\n  65\n ],\n [\n  44,\n  44,\n  67\n ],\n [\n  44,\n  51,\n  74\n ],\n [\n  44,\n  52,\n  75\n ],\n [\n  44,\n  53,\n  76\n ],\n [\n  44,\n  54,\n  77\n ],\n [\n  44,\n  55,\n  78\n ],\n [\n  44,\n  56,\n  79\n ],\n [\n  45,\n  43,\n  59\n ],\n [\n  45,\n  43,\n  63\n ],\n [\n  45,\n  43,\n  65\n ],\n [\n  45,\n  44,\n  60\n ],\n [\n  45,\n  44,\n  64\n ],\n [\n  45,\n  44,\n  66\n ],\n [\n  45,\n  45,\n  61\n ],\n [\n  45,\n  45,\n  65\n ],\n [\n  45,\n  45,\n  67\n ],\n [\n  45,\n  46,\n  62\n ],\n [\n  45,\n  46,\n  68\n ],\n [\n  45,\n  51,\n  74\n ],\n [\n  45,\n  52,\n  75\n ],\n [\n  45,\n  53,\n  76\n ],\n [\n  45,\n  54,\n  77\n ],\n [\n  45,\n  55,\n  78\n ],\n [\n  45,\n  56,\n  79\n ],\n [\n  46,\n  44,\n  65\n ],\n [\n  46,\n  44,\n  67\n ],\n [\n  46,\n  45,\n  66\n ],\n [\n  46,\n  45,\n  68\n ],\n [\n  46,\n  46,\n  63\n ],\n [\n  46,\n  46,\n  67\n ],\n [\n  46,\n  46,\n  69\n ],\n [\n  46,\n  47,\n  68\n ],\n [\n  46,\n  47,\n  70\n ],\n [\n  46,\n  52,\n  76\n ],\n [\n  46,\n  53,\n  77\n ],\n [\n  46,\n  54,\n  78\n ],\n [\n  46,\n  55,\n  79\n ],\n [\n  46,\n  56,\n  80\n ],\n [\n  46,\n  57,\n  81\n ],\n [\n  47,\n  45,\n  61\n ],\n [\n  47,\n  45,\n  65\n ],\n [\n  47,\n  45,\n  67\n ],\n [\n  47,\n  45,\n  69\n ],\n [\n  47,\n  46,\n  62\n ],\n [\n  47,\n  46,\n  66\n ],\n [\n  47,\n  46,\n  68\n ],\n [\n  47,\n  46,\n  70\n ],\n [\n  47,\n  47,\n  67\n ],\n [\n  47,\n  47,\n  69\n ],\n [\n  47,\n  47,\n  71\n ],\n [\n  47,\n  48,\n  70\n ],\n [\n  47,\n  48,\n  72\n ],\n [\n  47,\n  52,\n  76\n ],\n [\n  47,\n  53,\n  77\n ],\n [\n  47,\n  54,\n  78\n ],\n [\n  47,\n  55,\n  79\n ],\n [\n  47,\n  56,\n  80\n ],\n [\n  47,\n  57,\n  81\n ],\n [\n  48,\n  46,\n  63\n ],\n [\n  48,\n  46,\n  67\n ],\n [\n  48,\n  46,\n  69\n ],\n [\n  48,\n  46,\n  71\n ],\n [\n  48,\n  47,\n  68\n ],\n [\n  48,\n  47,\n  70\n ],\n [\n  48,\n  47,\n  72\n ],\n [\n  48,\n  48,\n  69\n ],\n [\n  48,\n  48,\n  71\n ],\n [\n  48,\n  48,\n  73\n ],\n [\n  48,\n  49,\n  72\n ],\n [\n  48,\n  53,\n  78\n ],\n [\n  48,\n  54,\n  79\n ],\n [\n  48,\n  55,\n  80\n ],\n [\n  48,\n  56,\n  81\n ],\n [\n  48,\n  57,\n  82\n ],\n [\n  48,\n  58,\n  83\n ],\n [\n  49,\n  47,\n  67\n ],\n [\n  49,\n  47,\n  69\n ],\n [\n  49,\n  47,\n  71\n ],\n [\n  49,\n  48,\n  68\n ],\n [\n  49,\n  48,\n  70\n ],\n [\n  49,\n  48,\n  72\n ],\n [\n  49,\n  49,\n  67\n ],\n [\n  49,\n  49,\n  69\n ],\n [\n  49,\n  49,\n  71\n ],\n [\n  49,\n  49,\n  73\n ],\n [\n  49,\n  50,\n  68\n ],\n [\n  49,\n  50,\n  70\n ],\n [\n  49,\n  50,\n  74\n ],\n [\n  49,\n  53,\n  78\n ],\n [\n  49,\n  54,\n  79\n ],\n [\n  49,\n  55,\n  80\n ],\n [\n  49,\n  56,\n  81\n ],\n [\n  49,\n  57,\n  82\n ],\n [\n  49,\n  58,\n  83\n ],\n [\n  50,\n  27,\n  53\n ],\n [\n  50,\n  28,\n  54\n ],\n [\n  50,\n  29,\n  55\n ],\n [\n  50,\n  30,\n  56\n ],\n [\n  50,\n  31,\n  57\n ],\n [\n  50,\n  32,\n  58\n ],\n [\n  50,\n  33,\n  59\n ],\n [\n  50,\n  34,\n  60\n ],\n [\n  50,\n  35,\n  61\n ],\n [\n  50,\n  36,\n  62\n ],\n [\n  50,\n  37,\n  51\n ],\n [\n  50,\n  37,\n  63\n ],\n [\n  50,\n  38,\n  52\n ],\n [\n  50,\n  38,\n  64\n ],\n [\n  50,\n  39,\n  53\n ],\n [\n  50,\n  39,\n  65\n ],\n [\n  50,\n  40,\n  54\n ],\n [\n  50,\n  40,\n  66\n ],\n [\n  50,\n  48,\n  69\n ],\n [\n  50,\n  48,\n  71\n ],\n [\n  50,\n  48,\n  73\n ],\n [\n  50,\n  49,\n  70\n ],\n [\n  50,\n  49,\n  72\n ],\n [\n  50,\n  49,\n  74\n ],\n [\n  50,\n  50,\n  71\n ],\n [\n  50,\n  50,\n  73\n ],\n [\n  50,\n  50,\n  75\n ],\n [\n  50,\n  51,\n  72\n ],\n [\n  50,\n  51,\n  76\n ],\n [\n  50,\n  53,\n  79\n ],\n [\n  50,\n  54,\n  80\n ],\n [\n  50,\n  55,\n  81\n ],\n [\n  50,\n  56,\n  82\n ],\n [\n  50,\n  57,\n  83\n ],\n [\n  50,\n  58,\n  84\n ],\n [\n  50,\n  59,\n  85\n ],\n [\n  51,\n  27,\n  53\n ],\n [\n  51,\n  28,\n  54\n ],\n [\n  51,\n  29,\n  55\n ],\n [\n  51,\n  30,\n  56\n ],\n [\n  51,\n  31,\n  57\n ],\n [\n  51,\n  32,\n  58\n ],\n [\n  51,\n  33,\n  59\n ],\n [\n  51,\n  34,\n  60\n ],\n [\n  51,\n  35,\n  61\n ],\n [\n  51,\n  36,\n  62\n ],\n [\n  51,\n  37,\n  51\n ],\n [\n  51,\n  37,\n  63\n ],\n [\n  51,\n  38,\n  52\n ],\n [\n  51,\n  38,\n  64\n ],\n [\n  51,\n  39,\n  53\n ],\n [\n  51,\n  39,\n  65\n ],\n [\n  51,\n  40,\n  54\n ],\n [\n  51,\n  40,\n  55\n ],\n [\n  51,\n  40,\n  66\n ],\n [\n  51,\n  49,\n  67\n ],\n [\n  51,\n  49,\n  69\n ],\n [\n  51,\n  49,\n  71\n ],\n [\n  51,\n  49,\n  73\n ],\n [\n  51,\n  49,\n  75\n ],\n [\n  51,\n  50,\n  68\n ],\n [\n  51,\n  50,\n  70\n ],\n [\n  51,\n  50,\n  72\n ],\n [\n  51,\n  50,\n  74\n ],\n [\n  51,\n  50,\n  76\n ],\n [\n  51,\n  51,\n  69\n ],\n [\n  51,\n  51,\n  71\n ],\n [\n  51,\n  51,\n  73\n ],\n [\n  51,\n  51,\n  75\n ],\n [\n  51,\n  51,\n  77\n ],\n [\n  51,\n  52,\n  70\n ],\n [\n  51,\n  52,\n  72\n ],\n [\n  51,\n  52,\n  74\n ],\n [\n  51,\n  52,\n  76\n ],\n [\n  51,\n  52,\n  78\n ],\n [\n  51,\n  53,\n  79\n ],\n [\n  51,\n  54,\n  80\n ],\n [\n  51,\n  55,\n  81\n ],\n [\n  51,\n  56,\n  82\n ],\n [\n  51,\n  57,\n  83\n ],\n [\n  51,\n  58,\n  84\n ],\n [\n  51,\n  59,\n  85\n ],\n [\n  52,\n  25,\n  52\n ],\n [\n  52,\n  27,\n  54\n ],\n [\n  52,\n  28,\n  55\n ],\n [\n  52,\n  29,\n  56\n ],\n [\n  52,\n  30,\n  57\n ],\n [\n  52,\n  31,\n  58\n ],\n [\n  52,\n  32,\n  59\n ],\n [\n  52,\n  33,\n  60\n ],\n [\n  52,\n  34,\n  61\n ],\n [\n  52,\n  35,\n  62\n ],\n [\n  52,\n  36,\n  63\n ],\n [\n  52,\n  37,\n  64\n ],\n [\n  52,\n  38,\n  65\n ],\n [\n  52,\n  39,\n  66\n ],\n [\n  52,\n  40,\n  55\n ],\n [\n  52,\n  40,\n  67\n ],\n [\n  52,\n  41,\n  68\n ],\n [\n  52,\n  42,\n  69\n ],\n [\n  52,\n  43,\n  59\n ],\n [\n  52,\n  44,\n  60\n ],\n [\n  52,\n  45,\n  61\n ],\n [\n  52,\n  46,\n  62\n ],\n [\n  52,\n  50,\n  71\n ],\n [\n  52,\n  50,\n  73\n ],\n [\n  52,\n  50,\n  75\n ],\n [\n  52,\n  50,\n  77\n ],\n [\n  52,\n  51,\n  72\n ],\n [\n  52,\n  51,\n  74\n ],\n [\n  52,\n  51,\n  76\n ],\n [\n  52,\n  51,\n  78\n ],\n [\n  52,\n  52,\n  71\n ],\n [\n  52,\n  52,\n  73\n ],\n [\n  52,\n  52,\n  75\n ],\n [\n  52,\n  52,\n  77\n ],\n [\n  52,\n  52,\n  79\n ],\n [\n  52,\n  53,\n  74\n ],\n [\n  52,\n  53,\n  76\n ],\n [\n  52,\n  53,\n  78\n ],\n [\n  52,\n  53,\n  80\n ],\n [\n  52,\n  54,\n  81\n ],\n [\n  52,\n  55,\n  82\n ],\n [\n  52,\n  56,\n  83\n ],\n [\n  52,\n  57,\n  84\n ],\n [\n  52,\n  58,\n  85\n ],\n [\n  52,\n  59,\n  86\n ],\n [\n  52,\n  60,\n  87\n ],\n [\n  53,\n  25,\n  52\n ],\n [\n  53,\n  27,\n  54\n ],\n [\n  53,\n  28,\n  55\n ],\n [\n  53,\n  29,\n  56\n ],\n [\n  53,\n  30,\n  57\n ],\n [\n  53,\n  31,\n  58\n ],\n [\n  53,\n  32,\n  59\n ],\n [\n  53,\n  33,\n  60\n ],\n [\n  53,\n  34,\n  61\n ],\n [\n  53,\n  35,\n  62\n ],\n [\n  53,\n  36,\n  63\n ],\n [\n  53,\n  37,\n  64\n ],\n [\n  53,\n  38,\n  65\n ],\n [\n  53,\n  39,\n  66\n ],\n [\n  53,\n  40,\n  67\n ],\n [\n  53,\n  41,\n  68\n ],\n [\n  53,\n  42,\n  69\n ],\n [\n  53,\n  43,\n  59\n ],\n [\n  53,\n  44,\n  60\n ],\n [\n  53,\n  45,\n  61\n ],\n [\n  53,\n  46,\n  62\n ],\n [\n  53,\n  46,\n  63\n ],\n [\n  53,\n  51,\n  69\n ],\n [\n  53,\n  51,\n  71\n ],\n [\n  53,\n  51,\n  73\n ],\n [\n  53,\n  51,\n  75\n ],\n [\n  53,\n  51,\n  77\n ],\n [\n  53,\n  52,\n  70\n ],\n [\n  53,\n  52,\n  72\n ],\n [\n  53,\n  52,\n  74\n ],\n [\n  53,\n  52,\n  76\n ],\n [\n  53,\n  52,\n  78\n ],\n [\n  53,\n  53,\n  73\n ],\n [\n  53,\n  53,\n  75\n ],\n [\n  53,\n  53,\n  77\n ],\n [\n  53,\n  53,\n  79\n ],\n [\n  53,\n  54,\n  74\n ],\n [\n  53,\n  54,\n  76\n ],\n [\n  53,\n  54,\n  78\n ],\n [\n  53,\n  54,\n  80\n ],\n [\n  53,\n  54,\n  81\n ],\n [\n  53,\n  55,\n  82\n ],\n [\n  53,\n  56,\n  83\n ],\n [\n  53,\n  57,\n  84\n ],\n [\n  53,\n  58,\n  85\n ],\n [\n  53,\n  59,\n  86\n ],\n [\n  53,\n  60,\n  87\n ],\n [\n  54,\n  45,\n  73\n ],\n [\n  54,\n  46,\n  63\n ],\n [\n  54,\n  46,\n  74\n ],\n [\n  54,\n  47,\n  75\n ],\n [\n  54,\n  48,\n  76\n ],\n [\n  54,\n  49,\n  67\n ],\n [\n  54,\n  49,\n  77\n ],\n [\n  54,\n  50,\n  68\n ],\n [\n  54,\n  50,\n  78\n ],\n [\n  54,\n  51,\n  69\n ],\n [\n  54,\n  51,\n  79\n ],\n [\n  54,\n  52,\n  70\n ],\n [\n  54,\n  52,\n  71\n ],\n [\n  54,\n  52,\n  73\n ],\n [\n  54,\n  52,\n  75\n ],\n [\n  54,\n  52,\n  77\n ],\n [\n  54,\n  52,\n  79\n ],\n [\n  54,\n  52,\n  80\n ],\n [\n  54,\n  53,\n  74\n ],\n [\n  54,\n  53,\n  76\n ],\n [\n  54,\n  53,\n  78\n ],\n [\n  54,\n  53,\n  80\n ],\n [\n  54,\n  54,\n  75\n ],\n [\n  54,\n  54,\n  77\n ],\n [\n  54,\n  54,\n  79\n ],\n [\n  54,\n  54,\n  81\n ],\n [\n  54,\n  54,\n  82\n ],\n [\n  54,\n  55,\n  76\n ],\n [\n  54,\n  55,\n  78\n ],\n [\n  54,\n  55,\n  80\n ],\n [\n  54,\n  55,\n  82\n ],\n [\n  54,\n  55,\n  83\n ],\n [\n  54,\n  56,\n  84\n ],\n [\n  54,\n  57,\n  85\n ],\n [\n  54,\n  58,\n  86\n ],\n [\n  54,\n  59,\n  87\n ],\n [\n  55,\n  45,\n  73\n ],\n [\n  55,\n  46,\n  74\n ],\n [\n  55,\n  47,\n  75\n ],\n [\n  55,\n  48,\n  76\n ],\n [\n  55,\n  49,\n  67\n ],\n [\n  55,\n  49,\n  77\n ],\n [\n  55,\n  50,\n  68\n ],\n [\n  55,\n  50,\n  78\n ],\n [\n  55,\n  51,\n  69\n ],\n [\n  55,\n  51,\n  79\n ],\n [\n  55,\n  52,\n  70\n ],\n [\n  55,\n  52,\n  71\n ],\n [\n  55,\n  52,\n  80\n ],\n [\n  55,\n  53,\n  73\n ],\n [\n  55,\n  53,\n  75\n ],\n [\n  55,\n  53,\n  77\n ],\n [\n  55,\n  53,\n  79\n ],\n [\n  55,\n  53,\n  81\n ],\n [\n  55,\n  54,\n  74\n ],\n [\n  55,\n  54,\n  76\n ],\n [\n  55,\n  54,\n  78\n ],\n [\n  55,\n  54,\n  80\n ],\n [\n  55,\n  54,\n  82\n ],\n [\n  55,\n  55,\n  75\n ],\n [\n  55,\n  55,\n  77\n ],\n [\n  55,\n  55,\n  79\n ],\n [\n  55,\n  55,\n  81\n ],\n [\n  55,\n  55,\n  83\n ],\n [\n  55,\n  56,\n  76\n ],\n [\n  55,\n  56,\n  78\n ],\n [\n  55,\n  56,\n  80\n ],\n [\n  55,\n  56,\n  82\n ],\n [\n  55,\n  56,\n  84\n ],\n [\n  55,\n  57,\n  85\n ],\n [\n  55,\n  58,\n  86\n ],\n [\n  55,\n  59,\n  87\n ],\n [\n  56,\n  46,\n  75\n ],\n [\n  56,\n  47,\n  76\n ],\n [\n  56,\n  48,\n  77\n ],\n [\n  56,\n  49,\n  78\n ],\n [\n  56,\n  50,\n  79\n ],\n [\n  56,\n  51,\n  80\n ],\n [\n  56,\n  52,\n  71\n ],\n [\n  56,\n  52,\n  81\n ],\n [\n  56,\n  53,\n  82\n ],\n [\n  56,\n  54,\n  74\n ],\n [\n  56,\n  54,\n  75\n ],\n [\n  56,\n  54,\n  77\n ],\n [\n  56,\n  54,\n  79\n ],\n [\n  56,\n  54,\n  81\n ],\n [\n  56,\n  54,\n  83\n ],\n [\n  56,\n  55,\n  75\n ],\n [\n  56,\n  55,\n  76\n ],\n [\n  56,\n  55,\n  78\n ],\n [\n  56,\n  55,\n  80\n ],\n [\n  56,\n  55,\n  82\n ],\n [\n  56,\n  55,\n  84\n ],\n [\n  56,\n  56,\n  76\n ],\n [\n  56,\n  56,\n  77\n ],\n [\n  56,\n  56,\n  79\n ],\n [\n  56,\n  56,\n  81\n ],\n [\n  56,\n  56,\n  83\n ],\n [\n  56,\n  56,\n  85\n ],\n [\n  56,\n  57,\n  77\n ],\n [\n  56,\n  57,\n  78\n ],\n [\n  56,\n  57,\n  80\n ],\n [\n  56,\n  57,\n  82\n ],\n [\n  56,\n  57,\n  84\n ],\n [\n  56,\n  57,\n  86\n ],\n [\n  56,\n  58,\n  78\n ],\n [\n  56,\n  58,\n  87\n ],\n [\n  56,\n  59,\n  79\n ],\n [\n  56,\n  59,\n  88\n ],\n [\n  56,\n  60,\n  89\n ],\n [\n  57,\n  46,\n  75\n ],\n [\n  57,\n  47,\n  76\n ],\n [\n  57,\n  48,\n  77\n ],\n [\n  57,\n  49,\n  78\n ],\n [\n  57,\n  50,\n  79\n ],\n [\n  57,\n  51,\n  80\n ],\n [\n  57,\n  52,\n  81\n ],\n [\n  57,\n  53,\n  82\n ],\n [\n  57,\n  54,\n  74\n ],\n [\n  57,\n  55,\n  75\n ],\n [\n  57,\n  55,\n  76\n ],\n [\n  57,\n  55,\n  77\n ],\n [\n  57,\n  55,\n  79\n ],\n [\n  57,\n  55,\n  81\n ],\n [\n  57,\n  55,\n  83\n ],\n [\n  57,\n  55,\n  84\n ],\n [\n  57,\n  56,\n  76\n ],\n [\n  57,\n  56,\n  77\n ],\n [\n  57,\n  56,\n  78\n ],\n [\n  57,\n  56,\n  80\n ],\n [\n  57,\n  56,\n  82\n ],\n [\n  57,\n  56,\n  84\n ],\n [\n  57,\n  56,\n  85\n ],\n [\n  57,\n  57,\n  77\n ],\n [\n  57,\n  57,\n  78\n ],\n [\n  57,\n  57,\n  79\n ],\n [\n  57,\n  57,\n  81\n ],\n [\n  57,\n  57,\n  83\n ],\n [\n  57,\n  57,\n  85\n ],\n [\n  57,\n  57,\n  86\n ],\n [\n  57,\n  58,\n  78\n ],\n [\n  57,\n  58,\n  79\n ],\n [\n  57,\n  58,\n  82\n ],\n [\n  57,\n  58,\n  84\n ],\n [\n  57,\n  58,\n  86\n ],\n [\n  57,\n  58,\n  87\n ],\n [\n  57,\n  59,\n  79\n ],\n [\n  57,\n  59,\n  80\n ],\n [\n  57,\n  59,\n  88\n ],\n [\n  57,\n  60,\n  81\n ],\n [\n  57,\n  60,\n  89\n ],\n [\n  58,\n  49,\n  79\n ],\n [\n  58,\n  50,\n  72\n ],\n [\n  58,\n  50,\n  80\n ],\n [\n  58,\n  51,\n  73\n ],\n [\n  58,\n  51,\n  81\n ],\n [\n  58,\n  52,\n  74\n ],\n [\n  58,\n  52,\n  82\n ],\n [\n  58,\n  53,\n  75\n ],\n [\n  58,\n  53,\n  83\n ],\n [\n  58,\n  54,\n  76\n ],\n [\n  58,\n  54,\n  84\n ],\n [\n  58,\n  55,\n  76\n ],\n [\n  58,\n  55,\n  77\n ],\n [\n  58,\n  55,\n  85\n ],\n [\n  58,\n  56,\n  77\n ],\n [\n  58,\n  56,\n  79\n ],\n [\n  58,\n  56,\n  81\n ],\n [\n  58,\n  56,\n  83\n ],\n [\n  58,\n  56,\n  85\n ],\n [\n  58,\n  56,\n  86\n ],\n [\n  58,\n  57,\n  78\n ],\n [\n  58,\n  57,\n  80\n ],\n [\n  58,\n  57,\n  82\n ],\n [\n  58,\n  57,\n  84\n ],\n [\n  58,\n  57,\n  86\n ],\n [\n  58,\n  57,\n  87\n ],\n [\n  58,\n  58,\n  79\n ],\n [\n  58,\n  58,\n  81\n ],\n [\n  58,\n  58,\n  83\n ],\n [\n  58,\n  58,\n  85\n ],\n [\n  58,\n  58,\n  87\n ],\n [\n  58,\n  58,\n  88\n ],\n [\n  58,\n  59,\n  80\n ],\n [\n  58,\n  59,\n  84\n ],\n [\n  58,\n  59,\n  86\n ],\n [\n  58,\n  59,\n  88\n ],\n [\n  58,\n  59,\n  89\n ],\n [\n  58,\n  60,\n  81\n ],\n [\n  58,\n  60,\n  90\n ],\n [\n  58,\n  61,\n  91\n ],\n [\n  58,\n  62,\n  92\n ],\n [\n  58,\n  63,\n  93\n ],\n [\n  59,\n  49,\n  79\n ],\n [\n  59,\n  50,\n  72\n ],\n [\n  59,\n  50,\n  80\n ],\n [\n  59,\n  51,\n  73\n ],\n [\n  59,\n  51,\n  74\n ],\n [\n  59,\n  51,\n  81\n ],\n [\n  59,\n  52,\n  74\n ],\n [\n  59,\n  52,\n  75\n ],\n [\n  59,\n  52,\n  82\n ],\n [\n  59,\n  53,\n  75\n ],\n [\n  59,\n  53,\n  76\n ],\n [\n  59,\n  53,\n  83\n ],\n [\n  59,\n  54,\n  76\n ],\n [\n  59,\n  54,\n  77\n ],\n [\n  59,\n  54,\n  84\n ],\n [\n  59,\n  55,\n  77\n ],\n [\n  59,\n  55,\n  78\n ],\n [\n  59,\n  55,\n  85\n ],\n [\n  59,\n  56,\n  79\n ],\n [\n  59,\n  56,\n  86\n ],\n [\n  59,\n  57,\n  77\n ],\n [\n  59,\n  57,\n  79\n ],\n [\n  59,\n  57,\n  81\n ],\n [\n  59,\n  57,\n  83\n ],\n [\n  59,\n  57,\n  85\n ],\n [\n  59,\n  57,\n  87\n ],\n [\n  59,\n  58,\n  78\n ],\n [\n  59,\n  58,\n  82\n ],\n [\n  59,\n  58,\n  84\n ],\n [\n  59,\n  58,\n  86\n ],\n [\n  59,\n  58,\n  88\n ],\n [\n  59,\n  59,\n  79\n ],\n [\n  59,\n  59,\n  83\n ],\n [\n  59,\n  59,\n  85\n ],\n [\n  59,\n  59,\n  87\n ],\n [\n  59,\n  59,\n  89\n ],\n [\n  59,\n  60,\n  80\n ],\n [\n  59,\n  60,\n  86\n ],\n [\n  59,\n  60,\n  88\n ],\n [\n  59,\n  60,\n  90\n ],\n [\n  59,\n  61,\n  91\n ],\n [\n  59,\n  62,\n  92\n ],\n [\n  59,\n  63,\n  93\n ],\n [\n  60,\n  50,\n  81\n ],\n [\n  60,\n  51,\n  74\n ],\n [\n  60,\n  51,\n  82\n ],\n [\n  60,\n  52,\n  75\n ],\n [\n  60,\n  52,\n  76\n ],\n [\n  60,\n  52,\n  83\n ],\n [\n  60,\n  53,\n  76\n ],\n [\n  60,\n  53,\n  77\n ],\n [\n  60,\n  53,\n  84\n ],\n [\n  60,\n  54,\n  77\n ],\n [\n  60,\n  54,\n  78\n ],\n [\n  60,\n  54,\n  85\n ],\n [\n  60,\n  55,\n  78\n ],\n [\n  60,\n  55,\n  79\n ],\n [\n  60,\n  55,\n  86\n ],\n [\n  60,\n  56,\n  79\n ],\n [\n  60,\n  56,\n  80\n ],\n [\n  60,\n  56,\n  87\n ],\n [\n  60,\n  57,\n  81\n ],\n [\n  60,\n  57,\n  88\n ],\n [\n  60,\n  58,\n  78\n ],\n [\n  60,\n  58,\n  79\n ],\n [\n  60,\n  58,\n  81\n ],\n [\n  60,\n  58,\n  83\n ],\n [\n  60,\n  58,\n  85\n ],\n [\n  60,\n  58,\n  87\n ],\n [\n  60,\n  58,\n  89\n ],\n [\n  60,\n  59,\n  80\n ],\n [\n  60,\n  59,\n  84\n ],\n [\n  60,\n  59,\n  86\n ],\n [\n  60,\n  59,\n  88\n ],\n [\n  60,\n  59,\n  90\n ],\n [\n  60,\n  60,\n  81\n ],\n [\n  60,\n  60,\n  85\n ],\n [\n  60,\n  60,\n  87\n ],\n [\n  60,\n  60,\n  89\n ],\n [\n  60,\n  60,\n  91\n ],\n [\n  60,\n  61,\n  82\n ],\n [\n  60,\n  61,\n  88\n ],\n [\n  60,\n  61,\n  90\n ],\n [\n  60,\n  61,\n  92\n ],\n [\n  60,\n  62,\n  93\n ],\n [\n  60,\n  63,\n  94\n ],\n [\n  60,\n  64,\n  95\n ],\n [\n  61,\n  50,\n  81\n ],\n [\n  61,\n  51,\n  82\n ],\n [\n  61,\n  52,\n  76\n ],\n [\n  61,\n  52,\n  83\n ],\n [\n  61,\n  53,\n  77\n ],\n [\n  61,\n  53,\n  78\n ],\n [\n  61,\n  53,\n  84\n ],\n [\n  61,\n  54,\n  78\n ],\n [\n  61,\n  54,\n  79\n ],\n [\n  61,\n  54,\n  85\n ],\n [\n  61,\n  55,\n  79\n ],\n [\n  61,\n  55,\n  80\n ],\n [\n  61,\n  55,\n  86\n ],\n [\n  61,\n  56,\n  80\n ],\n [\n  61,\n  56,\n  81\n ],\n [\n  61,\n  56,\n  87\n ],\n [\n  61,\n  57,\n  81\n ],\n [\n  61,\n  57,\n  82\n ],\n [\n  61,\n  57,\n  88\n ],\n [\n  61,\n  58,\n  83\n ],\n [\n  61,\n  58,\n  89\n ],\n [\n  61,\n  59,\n  79\n ],\n [\n  61,\n  59,\n  80\n ],\n [\n  61,\n  59,\n  83\n ],\n [\n  61,\n  59,\n  85\n ],\n [\n  61,\n  59,\n  87\n ],\n [\n  61,\n  59,\n  89\n ],\n [\n  61,\n  59,\n  90\n ],\n [\n  61,\n  60,\n  80\n ],\n [\n  61,\n  60,\n  86\n ],\n [\n  61,\n  60,\n  88\n ],\n [\n  61,\n  60,\n  90\n ],\n [\n  61,\n  60,\n  91\n ],\n [\n  61,\n  61,\n  81\n ],\n [\n  61,\n  61,\n  87\n ],\n [\n  61,\n  61,\n  89\n ],\n [\n  61,\n  61,\n  91\n ],\n [\n  61,\n  61,\n  92\n ],\n [\n  61,\n  62,\n  92\n ],\n [\n  61,\n  62,\n  93\n ],\n [\n  61,\n  63,\n  94\n ],\n [\n  61,\n  64,\n  95\n ],\n [\n  62,\n  27,\n  53\n ],\n [\n  62,\n  28,\n  54\n ],\n [\n  62,\n  29,\n  55\n ],\n [\n  62,\n  30,\n  56\n ],\n [\n  62,\n  31,\n  57\n ],\n [\n  62,\n  32,\n  58\n ],\n [\n  62,\n  33,\n  59\n ],\n [\n  62,\n  34,\n  60\n ],\n [\n  62,\n  35,\n  61\n ],\n [\n  62,\n  36,\n  62\n ],\n [\n  62,\n  37,\n  63\n ],\n [\n  62,\n  38,\n  64\n ],\n [\n  62,\n  39,\n  65\n ],\n [\n  62,\n  40,\n  66\n ],\n [\n  62,\n  53,\n  78\n ],\n [\n  62,\n  53,\n  79\n ],\n [\n  62,\n  53,\n  85\n ],\n [\n  62,\n  54,\n  79\n ],\n [\n  62,\n  54,\n  80\n ],\n [\n  62,\n  54,\n  86\n ],\n [\n  62,\n  55,\n  80\n ],\n [\n  62,\n  55,\n  81\n ],\n [\n  62,\n  55,\n  87\n ],\n [\n  62,\n  56,\n  81\n ],\n [\n  62,\n  56,\n  82\n ],\n [\n  62,\n  56,\n  88\n ],\n [\n  62,\n  57,\n  82\n ],\n [\n  62,\n  57,\n  83\n ],\n [\n  62,\n  57,\n  89\n ],\n [\n  62,\n  58,\n  83\n ],\n [\n  62,\n  58,\n  84\n ],\n [\n  62,\n  58,\n  90\n ],\n [\n  62,\n  59,\n  85\n ],\n [\n  62,\n  59,\n  91\n ],\n [\n  62,\n  60,\n  81\n ],\n [\n  62,\n  60,\n  85\n ],\n [\n  62,\n  60,\n  87\n ],\n [\n  62,\n  60,\n  89\n ],\n [\n  62,\n  60,\n  91\n ],\n [\n  62,\n  60,\n  92\n ],\n [\n  62,\n  61,\n  82\n ],\n [\n  62,\n  61,\n  88\n ],\n [\n  62,\n  61,\n  90\n ],\n [\n  62,\n  61,\n  92\n ],\n [\n  62,\n  61,\n  93\n ],\n [\n  62,\n  62,\n  83\n ],\n [\n  62,\n  62,\n  89\n ],\n [\n  62,\n  62,\n  91\n ],\n [\n  62,\n  62,\n  93\n ],\n [\n  62,\n  62,\n  94\n ],\n [\n  62,\n  63,\n  94\n ],\n [\n  62,\n  63,\n  95\n ],\n [\n  62,\n  64,\n  96\n ],\n [\n  63,\n  25,\n  52\n ],\n [\n  63,\n  27,\n  53\n ],\n [\n  63,\n  27,\n  54\n ],\n [\n  63,\n  28,\n  54\n ],\n [\n  63,\n  28,\n  55\n ],\n [\n  63,\n  29,\n  55\n ],\n [\n  63,\n  29,\n  56\n ],\n [\n  63,\n  30,\n  56\n ],\n [\n  63,\n  30,\n  57\n ],\n [\n  63,\n  31,\n  57\n ],\n [\n  63,\n  31,\n  58\n ],\n [\n  63,\n  32,\n  58\n ],\n [\n  63,\n  32,\n  59\n ],\n [\n  63,\n  33,\n  59\n ],\n [\n  63,\n  33,\n  60\n ],\n [\n  63,\n  34,\n  60\n ],\n [\n  63,\n  34,\n  61\n ],\n [\n  63,\n  35,\n  61\n ],\n [\n  63,\n  35,\n  62\n ],\n [\n  63,\n  36,\n  62\n ],\n [\n  63,\n  36,\n  63\n ],\n [\n  63,\n  37,\n  63\n ],\n [\n  63,\n  37,\n  64\n ],\n [\n  63,\n  38,\n  64\n ],\n [\n  63,\n  38,\n  65\n ],\n [\n  63,\n  39,\n  65\n ],\n [\n  63,\n  39,\n  66\n ],\n [\n  63,\n  40,\n  66\n ],\n [\n  63,\n  40,\n  67\n ],\n [\n  63,\n  41,\n  68\n ],\n [\n  63,\n  42,\n  69\n ],\n [\n  63,\n  53,\n  79\n ],\n [\n  63,\n  53,\n  85\n ],\n [\n  63,\n  54,\n  80\n ],\n [\n  63,\n  54,\n  81\n ],\n [\n  63,\n  54,\n  86\n ],\n [\n  63,\n  55,\n  81\n ],\n [\n  63,\n  55,\n  82\n ],\n [\n  63,\n  55,\n  87\n ],\n [\n  63,\n  56,\n  82\n ],\n [\n  63,\n  56,\n  83\n ],\n [\n  63,\n  56,\n  88\n ],\n [\n  63,\n  57,\n  83\n ],\n [\n  63,\n  57,\n  84\n ],\n [\n  63,\n  57,\n  89\n ],\n [\n  63,\n  58,\n  84\n ],\n [\n  63,\n  58,\n  85\n ],\n [\n  63,\n  58,\n  90\n ],\n [\n  63,\n  59,\n  85\n ],\n [\n  63,\n  59,\n  86\n ],\n [\n  63,\n  59,\n  91\n ],\n [\n  63,\n  60,\n  87\n ],\n [\n  63,\n  60,\n  92\n ],\n [\n  63,\n  61,\n  81\n ],\n [\n  63,\n  61,\n  87\n ],\n [\n  63,\n  61,\n  89\n ],\n [\n  63,\n  61,\n  91\n ],\n [\n  63,\n  61,\n  93\n ],\n [\n  63,\n  62,\n  92\n ],\n [\n  63,\n  62,\n  94\n ],\n [\n  63,\n  63,\n  93\n ],\n [\n  63,\n  63,\n  95\n ],\n [\n  63,\n  64,\n  96\n ],\n [\n  64,\n  25,\n  52\n ],\n [\n  64,\n  27,\n  54\n ],\n [\n  64,\n  28,\n  55\n ],\n [\n  64,\n  29,\n  56\n ],\n [\n  64,\n  30,\n  57\n ],\n [\n  64,\n  31,\n  58\n ],\n [\n  64,\n  32,\n  59\n ],\n [\n  64,\n  33,\n  60\n ],\n [\n  64,\n  34,\n  61\n ],\n [\n  64,\n  35,\n  62\n ],\n [\n  64,\n  36,\n  63\n ],\n [\n  64,\n  37,\n  64\n ],\n [\n  64,\n  38,\n  65\n ],\n [\n  64,\n  39,\n  66\n ],\n [\n  64,\n  40,\n  67\n ],\n [\n  64,\n  41,\n  68\n ],\n [\n  64,\n  42,\n  69\n ],\n [\n  64,\n  45,\n  73\n ],\n [\n  64,\n  46,\n  74\n ],\n [\n  64,\n  47,\n  75\n ],\n [\n  64,\n  48,\n  76\n ],\n [\n  64,\n  49,\n  77\n ],\n [\n  64,\n  50,\n  78\n ],\n [\n  64,\n  51,\n  79\n ],\n [\n  64,\n  52,\n  80\n ],\n [\n  64,\n  54,\n  81\n ],\n [\n  64,\n  54,\n  82\n ],\n [\n  64,\n  54,\n  87\n ],\n [\n  64,\n  55,\n  82\n ],\n [\n  64,\n  55,\n  83\n ],\n [\n  64,\n  55,\n  88\n ],\n [\n  64,\n  56,\n  83\n ],\n [\n  64,\n  56,\n  84\n ],\n [\n  64,\n  56,\n  89\n ],\n [\n  64,\n  57,\n  84\n ],\n [\n  64,\n  57,\n  85\n ],\n [\n  64,\n  57,\n  90\n ],\n [\n  64,\n  58,\n  85\n ],\n [\n  64,\n  58,\n  86\n ],\n [\n  64,\n  58,\n  91\n ],\n [\n  64,\n  59,\n  86\n ],\n [\n  64,\n  59,\n  87\n ],\n [\n  64,\n  59,\n  92\n ],\n [\n  64,\n  60,\n  87\n ],\n [\n  64,\n  60,\n  93\n ],\n [\n  64,\n  61,\n  94\n ],\n [\n  64,\n  62,\n  83\n ],\n [\n  64,\n  62,\n  89\n ],\n [\n  64,\n  62,\n  91\n ],\n [\n  64,\n  62,\n  93\n ],\n [\n  64,\n  62,\n  95\n ],\n [\n  64,\n  63,\n  94\n ],\n [\n  64,\n  63,\n  96\n ],\n [\n  64,\n  64,\n  95\n ],\n [\n  64,\n  64,\n  97\n ],\n [\n  64,\n  65,\n  98\n ],\n [\n  65,\n  45,\n  73\n ],\n [\n  65,\n  46,\n  74\n ],\n [\n  65,\n  46,\n  75\n ],\n [\n  65,\n  47,\n  75\n ],\n [\n  65,\n  47,\n  76\n ],\n [\n  65,\n  48,\n  76\n ],\n [\n  65,\n  48,\n  77\n ],\n [\n  65,\n  49,\n  77\n ],\n [\n  65,\n  49,\n  78\n ],\n [\n  65,\n  50,\n  78\n ],\n [\n  65,\n  50,\n  79\n ],\n [\n  65,\n  51,\n  79\n ],\n [\n  65,\n  51,\n  80\n ],\n [\n  65,\n  52,\n  80\n ],\n [\n  65,\n  52,\n  81\n ],\n [\n  65,\n  53,\n  82\n ],\n [\n  65,\n  54,\n  82\n ],\n [\n  65,\n  54,\n  87\n ],\n [\n  65,\n  55,\n  83\n ],\n [\n  65,\n  55,\n  84\n ],\n [\n  65,\n  55,\n  88\n ],\n [\n  65,\n  56,\n  84\n ],\n [\n  65,\n  56,\n  85\n ],\n [\n  65,\n  56,\n  89\n ],\n [\n  65,\n  57,\n  85\n ],\n [\n  65,\n  57,\n  86\n ],\n [\n  65,\n  57,\n  90\n ],\n [\n  65,\n  58,\n  86\n ],\n [\n  65,\n  58,\n  87\n ],\n [\n  65,\n  58,\n  91\n ],\n [\n  65,\n  59,\n  87\n ],\n [\n  65,\n  59,\n  88\n ],\n [\n  65,\n  59,\n  92\n ],\n [\n  65,\n  60,\n  89\n ],\n [\n  65,\n  60,\n  93\n ],\n [\n  65,\n  61,\n  94\n ],\n [\n  65,\n  62,\n  95\n ],\n [\n  65,\n  63,\n  93\n ],\n [\n  65,\n  63,\n  95\n ],\n [\n  65,\n  63,\n  96\n ],\n [\n  65,\n  64,\n  96\n ],\n [\n  65,\n  64,\n  97\n ],\n [\n  65,\n  65,\n  95\n ],\n [\n  65,\n  65,\n  97\n ],\n [\n  65,\n  65,\n  98\n ],\n [\n  65,\n  66,\n  96\n ],\n [\n  65,\n  66,\n  98\n ],\n [\n  66,\n  46,\n  75\n ],\n [\n  66,\n  47,\n  76\n ],\n [\n  66,\n  48,\n  77\n ],\n [\n  66,\n  49,\n  78\n ],\n [\n  66,\n  49,\n  79\n ],\n [\n  66,\n  50,\n  79\n ],\n [\n  66,\n  50,\n  80\n ],\n [\n  66,\n  51,\n  80\n ],\n [\n  66,\n  51,\n  81\n ],\n [\n  66,\n  52,\n  81\n ],\n [\n  66,\n  52,\n  82\n ],\n [\n  66,\n  53,\n  82\n ],\n [\n  66,\n  53,\n  83\n ],\n [\n  66,\n  54,\n  84\n ],\n [\n  66,\n  55,\n  84\n ],\n [\n  66,\n  55,\n  85\n ],\n [\n  66,\n  56,\n  85\n ],\n [\n  66,\n  56,\n  86\n ],\n [\n  66,\n  57,\n  86\n ],\n [\n  66,\n  57,\n  87\n ],\n [\n  66,\n  58,\n  87\n ],\n [\n  66,\n  58,\n  88\n ],\n [\n  66,\n  59,\n  88\n ],\n [\n  66,\n  59,\n  89\n ],\n [\n  66,\n  60,\n  89\n ],\n [\n  66,\n  60,\n  90\n ],\n [\n  66,\n  61,\n  91\n ],\n [\n  66,\n  62,\n  92\n ],\n [\n  66,\n  63,\n  93\n ],\n [\n  66,\n  64,\n  95\n ],\n [\n  66,\n  64,\n  97\n ],\n [\n  66,\n  65,\n  98\n ],\n [\n  66,\n  65,\n  99\n ],\n [\n  66,\n  66,\n  97\n ],\n [\n  66,\n  66,\n  99\n ],\n [\n  66,\n  67,\n  98\n ],\n [\n  66,\n  67,\n  100\n ],\n [\n  67,\n  49,\n  79\n ],\n [\n  67,\n  50,\n  80\n ],\n [\n  67,\n  50,\n  81\n ],\n [\n  67,\n  51,\n  81\n ],\n [\n  67,\n  51,\n  82\n ],\n [\n  67,\n  52,\n  82\n ],\n [\n  67,\n  52,\n  83\n ],\n [\n  67,\n  53,\n  83\n ],\n [\n  67,\n  53,\n  84\n ],\n [\n  67,\n  54,\n  84\n ],\n [\n  67,\n  54,\n  85\n ],\n [\n  67,\n  55,\n  85\n ],\n [\n  67,\n  55,\n  86\n ],\n [\n  67,\n  56,\n  86\n ],\n [\n  67,\n  56,\n  87\n ],\n [\n  67,\n  57,\n  87\n ],\n [\n  67,\n  57,\n  88\n ],\n [\n  67,\n  58,\n  88\n ],\n [\n  67,\n  58,\n  89\n ],\n [\n  67,\n  59,\n  89\n ],\n [\n  67,\n  59,\n  90\n ],\n [\n  67,\n  60,\n  90\n ],\n [\n  67,\n  60,\n  91\n ],\n [\n  67,\n  61,\n  91\n ],\n [\n  67,\n  61,\n  92\n ],\n [\n  67,\n  62,\n  92\n ],\n [\n  67,\n  62,\n  93\n ],\n [\n  67,\n  63,\n  93\n ],\n [\n  67,\n  63,\n  94\n ],\n [\n  67,\n  64,\n  95\n ],\n [\n  67,\n  65,\n  95\n ],\n [\n  67,\n  65,\n  97\n ],\n [\n  67,\n  65,\n  99\n ],\n [\n  67,\n  66,\n  96\n ],\n [\n  67,\n  66,\n  98\n ],\n [\n  67,\n  67,\n  97\n ],\n [\n  68,\n  50,\n  81\n ],\n [\n  68,\n  51,\n  82\n ],\n [\n  68,\n  52,\n  83\n ],\n [\n  68,\n  53,\n  84\n ],\n [\n  68,\n  53,\n  85\n ],\n [\n  68,\n  54,\n  85\n ],\n [\n  68,\n  54,\n  86\n ],\n [\n  68,\n  55,\n  86\n ],\n [\n  68,\n  55,\n  87\n ],\n [\n  68,\n  56,\n  87\n ],\n [\n  68,\n  56,\n  88\n ],\n [\n  68,\n  57,\n  88\n ],\n [\n  68,\n  57,\n  89\n ],\n [\n  68,\n  58,\n  89\n ],\n [\n  68,\n  58,\n  90\n ],\n [\n  68,\n  59,\n  90\n ],\n [\n  68,\n  59,\n  91\n ],\n [\n  68,\n  60,\n  91\n ],\n [\n  68,\n  60,\n  92\n ],\n [\n  68,\n  61,\n  92\n ],\n [\n  68,\n  61,\n  93\n ],\n [\n  68,\n  62,\n  93\n ],\n [\n  68,\n  62,\n  94\n ],\n [\n  68,\n  63,\n  94\n ],\n [\n  68,\n  63,\n  95\n ],\n [\n  68,\n  64,\n  95\n ],\n [\n  68,\n  64,\n  96\n ],\n [\n  68,\n  66,\n  97\n ],\n [\n  68,\n  66,\n  99\n ],\n [\n  68,\n  66,\n  101\n ],\n [\n  68,\n  67,\n  98\n ],\n [\n  68,\n  67,\n  100\n ],\n [\n  68,\n  68,\n  99\n ],\n [\n  69,\n  53,\n  85\n ],\n [\n  69,\n  54,\n  86\n ],\n [\n  69,\n  54,\n  87\n ],\n [\n  69,\n  55,\n  87\n ],\n [\n  69,\n  55,\n  88\n ],\n [\n  69,\n  56,\n  88\n ],\n [\n  69,\n  56,\n  89\n ],\n [\n  69,\n  57,\n  89\n ],\n [\n  69,\n  57,\n  90\n ],\n [\n  69,\n  58,\n  90\n ],\n [\n  69,\n  58,\n  91\n ],\n [\n  69,\n  59,\n  91\n ],\n [\n  69,\n  59,\n  92\n ],\n [\n  69,\n  60,\n  92\n ],\n [\n  69,\n  60,\n  93\n ],\n [\n  69,\n  61,\n  93\n ],\n [\n  69,\n  61,\n  94\n ],\n [\n  69,\n  62,\n  94\n ],\n [\n  69,\n  62,\n  95\n ],\n [\n  69,\n  63,\n  95\n ],\n [\n  69,\n  63,\n  96\n ],\n [\n  69,\n  64,\n  96\n ],\n [\n  69,\n  64,\n  97\n ],\n [\n  69,\n  65,\n  98\n ],\n [\n  69,\n  66,\n  101\n ],\n [\n  69,\n  67,\n  97\n ],\n [\n  70,\n  54,\n  87\n ],\n [\n  70,\n  55,\n  88\n ],\n [\n  70,\n  56,\n  89\n ],\n [\n  70,\n  57,\n  90\n ],\n [\n  70,\n  58,\n  91\n ],\n [\n  70,\n  59,\n  92\n ],\n [\n  70,\n  60,\n  93\n ],\n [\n  70,\n  61,\n  94\n ],\n [\n  70,\n  62,\n  95\n ],\n [\n  70,\n  63,\n  96\n ],\n [\n  70,\n  64,\n  97\n ],\n [\n  70,\n  65,\n  98\n ],\n [\n  70,\n  65,\n  99\n ],\n [\n  70,\n  68,\n  99\n ],\n [\n  71,\n  65,\n  99\n ],\n [\n  71,\n  66,\n  101\n ],\n [\n  71,\n  69,\n  105\n ],\n [\n  72,\n  66,\n  101\n ],\n [\n  72,\n  70,\n  107\n ]\n]"


def main():
    out = []
    out.append({'section': 'engine_gate', 'engine_sha': sha, 'pin': PIN,
                'gate': 'PASS'})
    vC = ns['vC']
    vO = ns['vO']

    anchor_spec = [
        (72, (19, 34), 52, 1, 'kit-6 (76c461da) kit5 S5 item1 one past of d7 death of d6 -- one-past-of-d=7 separation (death-of-d=6: {19,32} conform-DEAD)'),
        (73, (19, 34), 53, 1, 'kit-6 (76c461da) kit5 S5 item2 birth slice d8 -- d=8 birth slice'),
        (73, (19, 36), 53, 2, 'kit-6 (76c461da) kit5 S5 item2 birth slice d8 -- d=8 birth slice'),
        (74, (20, 34), 53, 0, 'kit-6 (76c461da) kit5 S5 item3 one past of d7 death of d6 -- one-past-of-d=7 separation (death-of-d=6)'),
        (75, (20, 34), 54, 0, 'kit-6 (76c461da) kit5 S5 item4 birth slice d8 -- d=8 birth slice'),
        (75, (20, 36), 54, 2, 'kit-6 (76c461da) kit5 S5 item4 birth slice d8 -- d=8 birth slice'),
        (70, (21, 28), 48, 1, 'kit-6 (76c461da) kit5 S5 item5 one past of d3 death of d2 -- one-past-of-d=3 separation (first m=21 d=2 death row)'),
        (71, (21, 28), 49, 1, 'kit-6 (76c461da) kit5 S5 item6 birth slice d4 -- d=4 birth slice'),
        (71, (21, 30), 49, 2, 'kit-6 (76c461da) kit5 S5 item6 birth slice d4 -- d=4 birth slice'),
        (72, (22, 28), 49, 0, 'kit-6 (76c461da) kit5 S5 item7 one past of d3 death of d2 -- one-past-of-d=3 separation (first m=22 d=2 death row)'),
        (73, (22, 28), 50, 0, 'kit-6 (76c461da) kit5 S5 item8 birth slice d4 -- d=4 birth slice'),
        (73, (22, 30), 50, 2, 'kit-6 (76c461da) kit5 S5 item8 birth slice d4 -- d=4 birth slice'),
        (74, (23, 28), 50, 1, 'kit-6 (76c461da) kit5 S5 item9 one past of d2 death of d1 -- one-past-of-d=2 separation (first m=23 d=1 death row)'),
        (75, (23, 28), 51, 1, 'kit-6 (76c461da) kit5 S5 item10 birth slice d3 -- d=2 birth slice'),
        (75, (23, 30), 51, 2, 'kit-6 (76c461da) kit5 S5 item10 birth slice d3 -- d=2 birth slice'),
        (76, (24, 28), 51, 0, 'kit-6 (76c461da) kit5 S5 item11 one past of d2 death of d1 -- one-past-of-d=2 separation (first m=24 d=1 death row)'),
        (77, (24, 28), 52, 0, 'kit-6 (76c461da) kit5 S5 item12 birth slice d3 -- d=3 birth slice'),
        (77, (24, 30), 52, 2, 'kit-6 (76c461da) kit5 S5 item12 birth slice d3 -- d=3 birth slice'),
        (81, (27, 28), 53, 2, 'kit-6 (76c461da) frontier record m27 z53 K1268 15th datum candidate -- FRONTIER separation (the 15th parity datum, FIRST-EVER m=27 row)'),
        (83, (28, 28), 54, 2, 'kit-6 (76c461da) frontier record m28 z54 K1268 16th datum candidate -- FRONTIER separation (the 16th parity datum, FIRST-EVER m=28 row)'),
        (76, (25, 26), 50, 1, 'kit-6 (76c461da) kit5 S5 item13 one past of the d0 seat -- one-past-of-d=0 decay separation (2->1)'),
        (77, (25, 26), 51, 1, 'kit-6 (76c461da) kit5 S5 item14 birth slice d1 stick coincides -- d=1 birth slice (stick seat coincides z=S(d0))'),
        (77, (25, 28), 51, 2, 'kit-6 (76c461da) kit5 S5 item14 birth slice d1 stick coincides -- d=1 birth slice (stick seat coincides z=S(d0))'),
        (78, (25, 28), 52, 1, 'kit-6 (76c461da) kit5 S5 item15 one past of d1 death of d0 first m25 death -- one-past-of-d=1 separation (THE FIRST m=25 death datum, d=0)'),
        (78, (26, 26), 51, 0, 'kit-6 (76c461da) kit5 S5 item16 one past of the d0 seat -- one-past-of-d=0 decay separation (2->0)'),
        (79, (26, 26), 52, 0, 'kit-6 (76c461da) kit5 S5 item17 birth slice d1 stick coincides -- d=1 birth slice (stick seat coincides z=S(d0))'),
        (79, (26, 28), 52, 2, 'kit-6 (76c461da) kit5 S5 item17 birth slice d1 stick coincides -- d=1 birth slice (stick seat coincides z=S(d0))'),
        (80, (26, 28), 53, 0, 'kit-6 (76c461da) kit5 S5 item18 one past of d1 death of d0 first m26 death -- one-past-of-d=1 separation (THE FIRST m=26 death datum, d=0)'),
        (77, (26, 26), 50, 2, 'kit-6 (76c461da) frontier recheck m26 z50 published 14th datum blind reverification -- blind re-verification of the kit-5 published 14th frontier datum'),
        (46, (17, 18), 28, 0, 'lifecycle kit z=28 handoff h1'),
        (45, (16, 17), 28, 1, 'lifecycle kit z=28 handoff h2'),
        (47, (18, 18), 28, 1, 'lifecycle kit z=28 handoff h3'),
        (46, (17, 17), 28, 0, 'lifecycle kit z=28 handoff h4'),
        (47, (17, 18), 29, 0, 'decay kit z=29 touch u1'),
        (46, (16, 17), 29, 1, 'decay kit z=29 touch u2'),
        (48, (18, 18), 29, 1, 'decay kit z=29 touch u3'),
        (47, (17, 17), 29, 0, 'decay kit z=29 touch u4'),
        (48, (17, 18), 30, 0, 'wavetrain kit z=30 touch w1'),
        (47, (16, 17), 30, 1, 'wavetrain kit z=30 touch w2'),
        (49, (18, 18), 30, 1, 'wavetrain kit z=30 touch w3'),
        (48, (17, 17), 30, 0, 'wavetrain kit z=30 touch w4'),
        (49, (17, 18), 31, 0, 'fifthwave kit z=31 touch x1'),
        (48, (16, 17), 31, 1, 'fifthwave kit z=31 touch y1'),
        (50, (18, 18), 31, 1, 'fifthwave kit z=31 touch x3'),
        (49, (17, 17), 31, 0, 'fifthwave kit z=31 touch x4'),
        (50, (17, 18), 32, 0, 'sixthwave kit z=32 touch x1'),
        (49, (16, 17), 32, 1, 'sixthwave kit z=32 touch y1'),
        (51, (18, 18), 32, 1, 'sixthwave kit z=32 touch x3'),
        (50, (17, 17), 32, 0, 'sixthwave kit z=32 touch x4'),
        (45, (15, 16), 29, 2, 'frontier m=15@z=29 separation (lifecycle kit + d49b480a blind replication)'),
        (47, (16, 16), 30, 2, 'frontier m=16@z=30 separation (lifecycle kit + d49b480a)'),
        (46, (15, 16), 30, 1, 'one-past m=15@z=30 separation (lifecycle kit + d49b480a)'),
        (48, (16, 16), 31, 0, 'one-past m=16@z=31 separation (lifecycle kit + d49b480a)'),
        (41, (13, 14), 27, 1, 'two-past m=13@z=27 stick separation (d49b480a)'),
        (41, (13, 16), 27, 2, 'two-past m=13@z=27 d=1 birth separation (d49b480a)'),
        (53, (17, 18), 35, 1, 'two-past m=17@z=35 stick separation (fifthwave kit)'),
        (53, (17, 20), 35, 2, 'two-past m=17@z=35 d=1 birth separation (fifthwave kit)'),
        (47, (13, 20), 33, 1, 'm=13@z=33 stick separation (fifthwave kit)'),
        (47, (13, 22), 33, 2, 'm=13@z=33 d=4 birth separation (fifthwave kit)'),
        (57, (19, 20), 37, 2, 'kit-1 (6057ed51) frontier m=19@z=37 d=0 birth separation UP 2v0'),
        (58, (19, 20), 38, 1, 'kit-1 (6057ed51) one-past m=19@z=38 separation UP 1v0 (odd decay 2->1)'),
        (59, (19, 20), 39, 1, 'kit-1 (6057ed51) two-past m=19@z=39 stick separation DOWN 1v2'),
        (59, (19, 22), 39, 2, 'kit-1 (6057ed51) two-past m=19@z=39 d=1 birth separation UP 2v0'),
        (59, (20, 20), 38, 2, 'kit-1 (6057ed51) frontier m=20@z=38 d=0 birth separation UP 2v1'),
        (60, (20, 20), 39, 0, 'kit-1 (6057ed51) one-past m=20@z=39 separation DOWN 0v1 (even decay 2->0)'),
        (61, (20, 20), 40, 0, 'kit-1 (6057ed51) two-past m=20@z=40 stick separation DOWN 0v2'),
        (61, (20, 22), 40, 2, 'kit-1 (6057ed51) two-past m=20@z=40 d=1 birth separation UP 2v1'),
        (45, (19, 19), 25, 0, 'z25-min20 kit base spot H(45;(19,19);25)=0 published CONFORM'),
        (46, (19, 19), 26, 0, 'z26-floor20 kit base spot H(46;(19,19);26)=0 published CONFORM'),
        (60, (19, 22), 40, 1, 'kit-2 (637d15e1) ladder m=19@z=40 one-past-of-d=1 separation UP 1v0'),
        (61, (19, 22), 41, 1, 'kit-2 (637d15e1) ladder m=19@z=41 stick separation DOWN 1v2'),
        (61, (19, 24), 41, 2, 'kit-2 (637d15e1) ladder m=19@z=41 d=2 birth separation UP 2v0'),
        (62, (19, 24), 42, 1, 'kit-2 (637d15e1) ladder m=19@z=42 one-past-of-d=2 separation UP 1v0'),
        (63, (19, 24), 43, 1, 'kit-2 (637d15e1) ladder m=19@z=43 stick separation DOWN 1v2'),
        (63, (19, 26), 43, 2, 'kit-2 (637d15e1) ladder m=19@z=43 d=3 birth separation UP 2v0'),
        (62, (20, 22), 41, 0, 'kit-2 (637d15e1) ladder m=20@z=41 one-past-of-d=1 separation DOWN 0v1'),
        (63, (20, 22), 42, 0, 'kit-2 (637d15e1) ladder m=20@z=42 stick separation DOWN 0v2'),
        (63, (20, 24), 42, 2, 'kit-2 (637d15e1) ladder m=20@z=42 d=2 birth separation UP 2v1'),
        (64, (20, 24), 43, 0, 'kit-2 (637d15e1) ladder m=20@z=43 one-past-of-d=2 separation DOWN 0v1'),
        (65, (20, 24), 44, 0, 'kit-2 (637d15e1) ladder m=20@z=44 stick separation DOWN 0v2'),
        (65, (20, 26), 44, 2, 'kit-2 (637d15e1) ladder m=20@z=44 d=3 birth separation UP 2v1'),
        (64, (19, 26), 44, 1, 'kit-3 (6554de44) ladder m=19@z=44 one-past-of-d=3 separation UP 1v0'),
        (65, (19, 26), 45, 1, 'kit-3 (6554de44) ladder m=19@z=45 stick separation DOWN 1v2'),
        (65, (19, 28), 45, 2, 'kit-3 (6554de44) ladder m=19@z=45 d=4 birth separation UP 2v0 seat gap 9'),
        (66, (19, 28), 46, 1, 'kit-3 (6554de44) ladder m=19@z=46 one-past-of-d=4 separation UP 1v0'),
        (67, (19, 28), 47, 1, 'kit-3 (6554de44) ladder m=19@z=47 stick separation DOWN 1v2'),
        (67, (19, 30), 47, 2, 'kit-3 (6554de44) ladder m=19@z=47 d=5 birth separation UP 2v0 seat gap 11'),
        (66, (20, 26), 45, 0, 'kit-3 (6554de44) ladder m=20@z=45 one-past-of-d=3 separation DOWN 0v1'),
        (67, (20, 26), 46, 0, 'kit-3 (6554de44) ladder m=20@z=46 stick separation DOWN 0v2'),
        (67, (20, 28), 46, 2, 'kit-3 (6554de44) ladder m=20@z=46 d=4 birth separation UP 2v1 seat gap 8'),
        (68, (20, 28), 47, 0, 'kit-3 (6554de44) ladder m=20@z=47 one-past-of-d=4 separation DOWN 0v1'),
        (69, (20, 28), 48, 0, 'kit-3 (6554de44) ladder m=20@z=48 stick separation DOWN 0v2'),
        (69, (20, 30), 48, 2, 'kit-3 (6554de44) ladder m=20@z=48 d=5 birth separation UP 2v1 seat gap 10'),
        (63, (21, 22), 41, 2, 'kit-3 (6554de44) frontier m=21@z=41 d=0 birth separation UP 2v0'),
        (64, (21, 22), 42, 1, 'kit-3 (6554de44) one-past m=21@z=42 separation UP 1v0 (odd decay 2->1)'),
        (65, (21, 22), 43, 1, 'kit-3 (6554de44) two-past m=21@z=43 stick separation DOWN 1v2'),
        (65, (21, 24), 43, 2, 'kit-3 (6554de44) two-past m=21@z=43 d=1 birth separation UP 2v0 seat gap 3'),
        (65, (22, 22), 42, 2, 'kit-3 (6554de44) frontier m=22@z=42 d=0 birth separation UP 2v1'),
        (66, (22, 22), 43, 0, 'kit-3 (6554de44) one-past m=22@z=43 separation DOWN 0v1 (even decay 2->0)'),
        (67, (22, 22), 44, 0, 'kit-3 (6554de44) two-past m=22@z=44 stick separation DOWN 0v2'),
        (67, (22, 24), 44, 2, 'kit-3 (6554de44) two-past m=22@z=44 d=1 birth separation UP 2v1 seat gap 2'),
        (68, (19, 30), 48, 1, 'kit-4 (fe0a2d01) ladder m=19@z=48 one-past-of-d=5 separation UP 1v0'),
        (69, (19, 30), 49, 1, 'kit-4 (fe0a2d01) stick m=19@z=49 separation DOWN 1v2'),
        (69, (19, 32), 49, 2, 'kit-4 (fe0a2d01) birth m=19@z=49 d=6 separation UP 2v0 seat gap 13'),
        (70, (20, 30), 49, 0, 'kit-4 (fe0a2d01) one-past m=20@z=49 separation DOWN 0v1'),
        (71, (20, 30), 50, 0, 'kit-4 (fe0a2d01) stick m=20@z=50 separation DOWN 0v2'),
        (71, (20, 32), 50, 2, 'kit-4 (fe0a2d01) birth m=20@z=50 d=6 separation UP 2v1 seat gap 12'),
        (66, (21, 24), 44, 1, 'kit-4 (fe0a2d01) one-past m=21@z=44 separation UP 1v0 (first m=21 death row: {21,22} conform-DEAD)'),
        (67, (21, 24), 45, 1, 'kit-4 (fe0a2d01) stick m=21@z=45 separation DOWN 1v2'),
        (67, (21, 26), 45, 2, 'kit-4 (fe0a2d01) birth m=21@z=45 d=2 separation UP 2v0 seat gap 5'),
        (68, (22, 24), 45, 0, 'kit-4 (fe0a2d01) one-past m=22@z=45 separation DOWN 0v1 (first m=22 death row: (22,22) conform-DEAD at z=45=S+1)'),
        (69, (22, 24), 46, 0, 'kit-4 (fe0a2d01) stick m=22@z=46 separation DOWN 0v2'),
        (69, (22, 26), 46, 2, 'kit-4 (fe0a2d01) birth m=22@z=46 d=2 separation UP 2v1 seat gap 4'),
        (69, (23, 24), 45, 2, 'kit-4 (fe0a2d01) frontier m=23@z=45 separation UP 2v0 (the 11th datum, corrected registration)'),
        (70, (23, 24), 46, 1, 'kit-4 (fe0a2d01) one-past m=23@z=46 separation UP 1v0'),
        (71, (23, 24), 47, 1, 'kit-4 (fe0a2d01) stick m=23@z=47 separation DOWN 1v2'),
        (71, (23, 26), 47, 2, 'kit-4 (fe0a2d01) birth m=23@z=47 d=1 separation UP 2v0 seat gap 3'),
        (71, (24, 24), 46, 2, 'kit-4 (fe0a2d01) frontier m=24@z=46 separation UP 2v1 (the 12th datum)'),
        (72, (24, 24), 47, 0, 'kit-4 (fe0a2d01) one-past m=24@z=47 separation DOWN 0v1'),
        (73, (24, 24), 48, 0, 'kit-4 (fe0a2d01) stick m=24@z=48 separation DOWN 0v2'),
        (73, (24, 26), 48, 2, 'kit-4 (fe0a2d01) birth m=24@z=48 d=1 separation UP 2v1 seat gap 2'),
        (74, (24, 26), 49, 0, 'kit-4 (fe0a2d01) one-past-of-d=1 m=24@z=49 separation DOWN 0v1 (first m=24 death row: (24,24) conform-DEAD at z=49=S+1)'),
        (70, (19, 32), 50, 1, 'kit-5 (d52f2be7) ladder m=19@z=50 one-past-of-d=6 separation UP 1v0 (first m=19 d=5 death row: {19,30} conform-DEAD)'),
        (71, (19, 32), 51, 1, 'kit-5 (d52f2be7) stick m=19@z=51 separation DOWN 1v2'),
        (71, (19, 34), 51, 2, 'kit-5 (d52f2be7) birth m=19@z=51 d=7 separation UP 2v0 seat gap 15 (m=19 ladder COMPLETE d=7)'),
        (72, (20, 32), 51, 0, 'kit-5 (d52f2be7) ladder m=20@z=51 one-past-of-d=6 separation DOWN 0v1 ((20,30) conform-DEAD, first m=20 d=5 death row)'),
        (73, (20, 32), 52, 0, 'kit-5 (d52f2be7) stick m=20@z=52 separation DOWN 0v2'),
        (73, (20, 34), 52, 2, 'kit-5 (d52f2be7) birth m=20@z=52 d=7 separation UP 2v1 seat gap 14 (m=20 ladder COMPLETE d=7)'),
        (68, (21, 26), 46, 1, 'kit-5 (d52f2be7) ladder m=21@z=46 one-past-of-d=2 separation UP 1v0 ({21,24} conform-DEAD, first m=21 d=1 death row)'),
        (69, (21, 26), 47, 1, 'kit-5 (d52f2be7) stick m=21@z=47 separation DOWN 1v2'),
        (69, (21, 28), 47, 2, 'kit-5 (d52f2be7) birth m=21@z=47 d=3 separation UP 2v0 seat gap 7'),
        (70, (22, 26), 47, 0, 'kit-5 (d52f2be7) ladder m=22@z=47 one-past-of-d=2 separation DOWN 0v1 ((22,24) conform-DEAD, first m=22 d=1 death row)'),
        (71, (22, 26), 48, 0, 'kit-5 (d52f2be7) stick m=22@z=48 separation DOWN 0v2'),
        (71, (22, 28), 48, 2, 'kit-5 (d52f2be7) birth m=22@z=48 d=3 separation UP 2v1 seat gap 6'),
        (72, (23, 26), 48, 1, 'kit-5 (d52f2be7) ladder m=23@z=48 one-past-of-d=1 separation UP 1v0 (THE FIRST m=23 death datum: {23,24} conform-DEAD)'),
        (73, (23, 26), 49, 1, 'kit-5 (d52f2be7) stick m=23@z=49 separation DOWN 1v2'),
        (73, (23, 28), 49, 2, 'kit-5 (d52f2be7) birth m=23@z=49 d=2 separation UP 2v0 seat gap 5'),
        (75, (24, 26), 50, 0, 'kit-5 (d52f2be7) stick m=24@z=50 separation DOWN 0v2 (stick seat coincides S(d1)=50=z)'),
        (75, (24, 28), 50, 2, 'kit-5 (d52f2be7) birth m=24@z=50 d=2 separation UP 2v1 seat gap 4'),
        (75, (25, 26), 49, 2, 'kit-5 (d52f2be7) frontier m=25@z=49 separation UP 2v0 (the 13th datum, first-ever m=25 row)'),
        (77, (26, 26), 50, 2, 'kit-5 (d52f2be7) frontier m=26@z=50 separation UP 2v1 (the 14th datum, first-ever m=26 row)'),
        (74, (36, 19), 54, 1, 'kit-7 (a62c5d2e) frozen section (d) item 1 m=19 z=54  -- seat separation [19, 36] 1 v 0 (S=55) UP'),
        (75, (36, 19), 55, 1, 'kit-7 (a62c5d2e) frozen section (d) item 2 m=19 z=55  -- seat separation [19, 36] 1 v 2 (S=55) DOWN'),
        (75, (19, 19, 19), 55, 2, 'kit-7 (a62c5d2e) STACKED-TRIO SHADOW SEAT datum {19,19,19}@S=57 UP 2v0 (the kit series FIRST registered-candidate deviation, unregistered third separation at the m=19 z=55 d=9 birth slice)'),
        (75, (38, 19), 55, 2, 'kit-7 (a62c5d2e) frozen section (d) item 2 m=19 z=55  -- seat separation [19, 38] 2 v 0 (S=57) UP'),
        (76, (36, 20), 55, 0, 'kit-7 (a62c5d2e) frozen section (d) item 3 m=20 z=55  -- seat separation [20, 36] 0 v 1 (S=56) DOWN'),
        (77, (36, 20), 56, 0, 'kit-7 (a62c5d2e) frozen section (d) item 4 m=20 z=56  -- seat separation [20, 36] 0 v 2 (S=56) DOWN'),
        (77, (38, 20), 56, 2, 'kit-7 (a62c5d2e) frozen section (d) item 4 m=20 z=56  -- seat separation [20, 38] 2 v 1 (S=58) UP'),
        (72, (30, 21), 50, 1, 'kit-7 (a62c5d2e) frozen section (d) item 5 m=21 z=50  -- seat separation [21, 30] 1 v 0 (S=51) UP'),
        (73, (30, 21), 51, 1, 'kit-7 (a62c5d2e) frozen section (d) item 6 m=21 z=51  -- seat separation [21, 30] 1 v 2 (S=51) DOWN'),
        (73, (32, 21), 51, 2, 'kit-7 (a62c5d2e) frozen section (d) item 6 m=21 z=51  -- seat separation [21, 32] 2 v 0 (S=53) UP'),
        (74, (30, 22), 51, 0, 'kit-7 (a62c5d2e) frozen section (d) item 7 m=22 z=51  -- seat separation [22, 30] 0 v 1 (S=52) DOWN'),
        (75, (30, 22), 52, 0, 'kit-7 (a62c5d2e) frozen section (d) item 8 m=22 z=52  -- seat separation [22, 30] 0 v 2 (S=52) DOWN'),
        (75, (32, 22), 52, 2, 'kit-7 (a62c5d2e) frozen section (d) item 8 m=22 z=52  -- seat separation [22, 32] 2 v 1 (S=54) UP'),
        (76, (30, 23), 52, 1, 'kit-7 (a62c5d2e) frozen section (d) item 9 m=23 z=52  -- seat separation [23, 30] 1 v 0 (S=53) UP'),
        (77, (30, 23), 53, 1, 'kit-7 (a62c5d2e) frozen section (d) item 10 m=23 z=53  -- seat separation [23, 30] 1 v 2 (S=53) DOWN'),
        (77, (32, 23), 53, 2, 'kit-7 (a62c5d2e) frozen section (d) item 10 m=23 z=53  -- seat separation [23, 32] 2 v 0 (S=55) UP'),
        (78, (30, 24), 53, 0, 'kit-7 (a62c5d2e) frozen section (d) item 11 m=24 z=53  -- seat separation [24, 30] 0 v 1 (S=54) DOWN'),
        (79, (30, 24), 54, 0, 'kit-7 (a62c5d2e) frozen section (d) item 12 m=24 z=54  -- seat separation [24, 30] 0 v 2 (S=54) DOWN'),
        (79, (32, 24), 54, 2, 'kit-7 (a62c5d2e) frozen section (d) item 12 m=24 z=54  -- seat separation [24, 32] 2 v 1 (S=56) UP'),
        (79, (28, 25), 53, 1, 'kit-7 (a62c5d2e) frozen section (d) item 13 m=25 z=53  -- seat separation [25, 28] 1 v 2 (S=53) DOWN'),
        (79, (30, 25), 53, 2, 'kit-7 (a62c5d2e) frozen section (d) item 13 m=25 z=53  -- seat separation [25, 30] 2 v 0 (S=55) UP'),
        (80, (30, 25), 54, 1, 'kit-7 (a62c5d2e) frozen section (d) item 14 m=25 z=54  -- seat separation [25, 30] 1 v 0 (S=55) UP'),
        (81, (30, 25), 55, 1, 'kit-7 (a62c5d2e) frozen section (d) item 15 m=25 z=55  -- seat separation [25, 30] 1 v 2 (S=55) DOWN'),
        (81, (32, 25), 55, 2, 'kit-7 (a62c5d2e) frozen section (d) item 15 m=25 z=55  -- seat separation [25, 32] 2 v 0 (S=57) UP'),
        (81, (28, 26), 54, 0, 'kit-7 (a62c5d2e) frozen section (d) item 16 m=26 z=54  -- seat separation [26, 28] 0 v 2 (S=54) DOWN'),
        (81, (30, 26), 54, 2, 'kit-7 (a62c5d2e) frozen section (d) item 16 m=26 z=54  -- seat separation [26, 30] 2 v 1 (S=56) UP'),
        (82, (30, 26), 55, 0, 'kit-7 (a62c5d2e) frozen section (d) item 17 m=26 z=55  -- seat separation [26, 30] 0 v 1 (S=56) DOWN'),
        (83, (30, 26), 56, 0, 'kit-7 (a62c5d2e) frozen section (d) item 18 m=26 z=56  -- seat separation [26, 30] 0 v 2 (S=56) DOWN'),
        (83, (32, 26), 56, 2, 'kit-7 (a62c5d2e) frozen section (d) item 18 m=26 z=56  -- seat separation [26, 32] 2 v 1 (S=58) UP'),
        (82, (28, 27), 54, 1, 'kit-7 (a62c5d2e) frozen section (d) item 19 m=27 z=54  -- seat separation [27, 28] 1 v 0 (S=55) UP'),
        (83, (28, 27), 55, 1, 'kit-7 (a62c5d2e) frozen section (d) item 20 m=27 z=55  -- seat separation [27, 28] 1 v 2 (S=55) DOWN'),
        (83, (30, 27), 55, 2, 'kit-7 (a62c5d2e) frozen section (d) item 20 m=27 z=55  -- seat separation [27, 30] 2 v 0 (S=57) UP'),
        (84, (30, 27), 56, 1, 'kit-7 (a62c5d2e) frozen section (d) item 21 m=27 z=56 one-past-of-d=1 / death-of-d=0 -- seat separation [27, 30] 1 v 0 (S=57) UP'),
        (84, (28, 28), 55, 0, 'kit-7 (a62c5d2e) frozen section (d) item 22 m=28 z=55  -- seat separation [28, 28] 0 v 1 (S=56) DOWN'),
        (85, (28, 28), 56, 0, 'kit-7 (a62c5d2e) frozen section (d) item 23 m=28 z=56  -- seat separation [28, 28] 0 v 2 (S=56) DOWN'),
        (85, (30, 28), 56, 2, 'kit-7 (a62c5d2e) frozen section (d) item 23 m=28 z=56  -- seat separation [28, 30] 2 v 1 (S=58) UP'),
        (86, (30, 28), 57, 0, 'kit-7 (a62c5d2e) frozen section (d) item 24 m=28 z=57 one-past-of-d=1 / death-of-d=0 -- seat separation [28, 30] 0 v 1 (S=58) DOWN'),
        (87, (30, 29), 57, 2, 'kit-7 (a62c5d2e) frontier m=29@z=57 separation (the 17th parity datum, FIRST-EVER m=29 row)'),
        (89, (30, 30), 58, 2, 'kit-7 (a62c5d2e) frontier m=30@z=58 separation (the 18th parity datum, FIRST-EVER m=30 row)'),
        (76, (19, 19, 19), 56, 1, 'kit-8 (7af915fb) published kit-8 census row ladder_m19_z56 -- kit-8 measured seat separation (19, 19, 19) @S=57 1v0 UP'),
        (76, (38, 19), 56, 1, 'kit-8 (7af915fb) published kit-8 census row ladder_m19_z56 -- kit-8 measured seat separation (38, 19) @S=57 1v0 UP'),
        (77, (19, 19, 19), 57, 1, 'kit-8 (7af915fb) published kit-8 census row ladder_m19_z57 -- kit-8 measured seat separation (19, 19, 19) @S=57 1v2 DOWN'),
        (77, (38, 19), 57, 1, 'kit-8 (7af915fb) published kit-8 census row ladder_m19_z57 -- kit-8 measured seat separation (38, 19) @S=57 1v2 DOWN'),
        (77, (21, 19, 19), 57, 2, 'kit-8 (7af915fb) published kit-8 census row ladder_m19_z57 -- kit-8 measured seat separation (21, 19, 19) @S=59 2v0 UP'),
        (77, (20, 20, 19), 57, 2, 'kit-8 (7af915fb) published kit-8 census row ladder_m19_z57 -- kit-8 measured seat separation (20, 20, 19) @S=59 2v0 UP'),
        (77, (40, 19), 57, 2, 'kit-8 (7af915fb) published kit-8 census row ladder_m19_z57 -- kit-8 measured seat separation (40, 19) @S=59 2v0 UP'),
        (78, (38, 20), 57, 0, 'kit-8 (7af915fb) published kit-8 census row ladder_m20_z57 -- kit-8 measured seat separation (38, 20) @S=58 0v1 DOWN'),
        (79, (38, 20), 58, 0, 'kit-8 (7af915fb) published kit-8 census row ladder_m20_z58 -- kit-8 measured seat separation (38, 20) @S=58 0v2 DOWN'),
        (79, (20, 20, 20), 58, 2, 'kit-8 (7af915fb) published kit-8 census row ladder_m20_z58 -- kit-8 measured seat separation (20, 20, 20) @S=60 2v1 UP'),
        (79, (40, 20), 58, 2, 'kit-8 (7af915fb) published kit-8 census row ladder_m20_z58 -- kit-8 measured seat separation (40, 20) @S=60 2v1 UP'),
        (74, (32, 21), 52, 1, 'kit-8 (7af915fb) published kit-8 census row ladder_m21_z52 -- kit-8 measured seat separation (32, 21) @S=53 1v0 UP'),
        (75, (32, 21), 53, 1, 'kit-8 (7af915fb) published kit-8 census row ladder_m21_z53 -- kit-8 measured seat separation (32, 21) @S=53 1v2 DOWN'),
        (75, (34, 21), 53, 2, 'kit-8 (7af915fb) published kit-8 census row ladder_m21_z53 -- kit-8 measured seat separation (34, 21) @S=55 2v0 UP'),
        (76, (32, 22), 53, 0, 'kit-8 (7af915fb) published kit-8 census row ladder_m22_z53 -- kit-8 measured seat separation (32, 22) @S=54 0v1 DOWN'),
        (77, (32, 22), 54, 0, 'kit-8 (7af915fb) published kit-8 census row ladder_m22_z54 -- kit-8 measured seat separation (32, 22) @S=54 0v2 DOWN'),
        (77, (34, 22), 54, 2, 'kit-8 (7af915fb) published kit-8 census row ladder_m22_z54 -- kit-8 measured seat separation (34, 22) @S=56 2v1 UP'),
        (78, (32, 23), 54, 1, 'kit-8 (7af915fb) published kit-8 census row ladder_m23_z54 -- kit-8 measured seat separation (32, 23) @S=55 1v0 UP'),
        (79, (32, 23), 55, 1, 'kit-8 (7af915fb) published kit-8 census row ladder_m23_z55 -- kit-8 measured seat separation (32, 23) @S=55 1v2 DOWN'),
        (79, (34, 23), 55, 2, 'kit-8 (7af915fb) published kit-8 census row ladder_m23_z55 -- kit-8 measured seat separation (34, 23) @S=57 2v0 UP'),
        (80, (32, 24), 55, 0, 'kit-8 (7af915fb) published kit-8 census row ladder_m24_z55 -- kit-8 measured seat separation (32, 24) @S=56 0v1 DOWN'),
        (81, (32, 24), 56, 0, 'kit-8 (7af915fb) published kit-8 census row ladder_m24_z56 -- kit-8 measured seat separation (32, 24) @S=56 0v2 DOWN'),
        (81, (34, 24), 56, 2, 'kit-8 (7af915fb) published kit-8 census row ladder_m24_z56 -- kit-8 measured seat separation (34, 24) @S=58 2v1 UP'),
        (82, (32, 25), 56, 1, 'kit-8 (7af915fb) published kit-8 census row ladder_m25_z56 -- kit-8 measured seat separation (32, 25) @S=57 1v0 UP'),
        (83, (32, 25), 57, 1, 'kit-8 (7af915fb) published kit-8 census row ladder_m25_z57 -- kit-8 measured seat separation (32, 25) @S=57 1v2 DOWN'),
        (83, (34, 25), 57, 2, 'kit-8 (7af915fb) published kit-8 census row ladder_m25_z57 -- kit-8 measured seat separation (34, 25) @S=59 2v0 UP'),
        (84, (32, 26), 57, 0, 'kit-8 (7af915fb) published kit-8 census row ladder_m26_z57 -- kit-8 measured seat separation (32, 26) @S=58 0v1 DOWN'),
        (85, (32, 26), 58, 0, 'kit-8 (7af915fb) published kit-8 census row ladder_m26_z58 -- kit-8 measured seat separation (32, 26) @S=58 0v2 DOWN'),
        (85, (34, 26), 58, 2, 'kit-8 (7af915fb) published kit-8 census row ladder_m26_z58 -- kit-8 measured seat separation (34, 26) @S=60 2v1 UP'),
        (84, (30, 27), 56, 1, 'kit-8 (7af915fb) published kit-8 census row ladder_m27_z56 -- kit-8 measured seat separation (30, 27) @S=57 1v0 UP'),
        (85, (30, 27), 57, 1, 'kit-8 (7af915fb) published kit-8 census row ladder_m27_z57 -- kit-8 measured seat separation (30, 27) @S=57 1v2 DOWN'),
        (85, (32, 27), 57, 2, 'kit-8 (7af915fb) published kit-8 census row ladder_m27_z57 -- kit-8 measured seat separation (32, 27) @S=59 2v0 UP'),
        (86, (30, 28), 57, 0, 'kit-8 (7af915fb) published kit-8 census row ladder_m28_z57 -- kit-8 measured seat separation (30, 28) @S=58 0v1 DOWN'),
        (87, (30, 28), 58, 0, 'kit-8 (7af915fb) published kit-8 census row ladder_m28_z58 -- kit-8 measured seat separation (30, 28) @S=58 0v2 DOWN'),
        (87, (32, 28), 58, 2, 'kit-8 (7af915fb) published kit-8 census row ladder_m28_z58 -- kit-8 measured seat separation (32, 28) @S=60 2v1 UP'),
        (88, (30, 29), 58, 1, 'kit-8 (7af915fb) published kit-8 census row ladder_m29_z58 -- kit-8 measured seat separation (30, 29) @S=59 1v0 UP'),
        (89, (30, 29), 59, 1, 'kit-8 (7af915fb) published kit-8 census row ladder_m29_z59 -- kit-8 measured seat separation (30, 29) @S=59 1v2 DOWN'),
        (89, (32, 29), 59, 2, 'kit-8 (7af915fb) published kit-8 census row ladder_m29_z59 -- kit-8 measured seat separation (32, 29) @S=61 2v0 UP'),
        (90, (32, 29), 60, 1, 'kit-8 (7af915fb) published kit-8 census row ladder_m29_z60 -- kit-8 measured seat separation (32, 29) @S=61 1v0 UP'),
        (90, (30, 30), 59, 0, 'kit-8 (7af915fb) published kit-8 census row ladder_m30_z59 -- kit-8 measured seat separation (30, 30) @S=60 0v1 DOWN'),
        (91, (30, 30), 60, 0, 'kit-8 (7af915fb) published kit-8 census row ladder_m30_z60 -- kit-8 measured seat separation (30, 30) @S=60 0v2 DOWN'),
        (91, (32, 30), 60, 2, 'kit-8 (7af915fb) published kit-8 census row ladder_m30_z60 -- kit-8 measured seat separation (32, 30) @S=62 2v1 UP'),
        (92, (32, 30), 61, 0, 'kit-8 (7af915fb) published kit-8 census row ladder_m30_z61 -- kit-8 measured seat separation (32, 30) @S=62 0v1 DOWN'),
        (93, (32, 31), 61, 2, 'kit-8 (7af915fb) published kit-8 census row frontier_m31_z61 -- kit-8 measured seat separation (32, 31) @S=63 2v0 UP'),
        (95, (32, 32), 62, 2, 'kit-8 (7af915fb) published kit-8 census row frontier_m32_z62 -- kit-8 measured seat separation (32, 32) @S=64 2v1 UP'),
        (51, (24, 13), 37, 1, 'kit-8 (7af915fb) published kit-8 census row trio_mid_slice_m13_z37 -- kit-8 measured seat separation (24, 13) @S=37 1v2 DOWN'),
        (51, (13, 13, 13), 37, 2, 'kit-8 (7af915fb) published kit-8 census row trio_mid_slice_m13_z37 -- kit-8 measured seat separation (13, 13, 13) @S=39 2v0 UP'),
        (51, (26, 13), 37, 2, 'kit-8 (7af915fb) published kit-8 census row trio_mid_slice_m13_z37 -- kit-8 measured seat separation (26, 13) @S=39 2v0 UP'),
        (59, (28, 15), 43, 1, 'kit-8 (7af915fb) published kit-8 census row trio_mid_slice_m15_z43 -- kit-8 measured seat separation (28, 15) @S=43 1v2 DOWN'),
        (59, (15, 15, 15), 43, 2, 'kit-8 (7af915fb) published kit-8 census row trio_mid_slice_m15_z43 -- kit-8 measured seat separation (15, 15, 15) @S=45 2v0 UP'),
        (59, (30, 15), 43, 2, 'kit-8 (7af915fb) published kit-8 census row trio_mid_slice_m15_z43 -- kit-8 measured seat separation (30, 15) @S=45 2v0 UP'),
        (67, (32, 17), 49, 1, 'kit-8 (7af915fb) published kit-8 census row trio_mid_slice_m17_z49 -- kit-8 measured seat separation (32, 17) @S=49 1v2 DOWN'),
        (67, (17, 17, 17), 49, 2, 'kit-8 (7af915fb) published kit-8 census row trio_mid_slice_m17_z49 -- kit-8 measured seat separation (17, 17, 17) @S=51 2v0 UP'),
        (67, (34, 17), 49, 2, 'kit-8 (7af915fb) published kit-8 census row trio_mid_slice_m17_z49 -- kit-8 measured seat separation (34, 17) @S=51 2v0 UP'),
    ]

    # (a) K0832 battery: the UNION of the kit-8 1,004 literal triples
    #     (sorted-unique layout; property checked unchanged) plus the
    #     kit-9 literals below (stair rows, candidate literals, new
    #     anchor collapses, kit-10 future constants).
    battery_lits = json.loads(BATTERY_TRIPLES_JSON)
    battery = []
    bad_bat = 0
    for (x, z2, R2) in battery_lits:
        cf = v(x, z2, R2)
        cn = vC(x, z2, R2)
        od = vO(x, z2, R2)
        ok = (cf == cn == od)
        if not ok:
            bad_bat += 1
        battery.append({'x': x, 'z': z2, 'R': R2, 'closed': cf,
                        'vC': cn, 'vO': od, 'match': ok})
    out.append({'section': 'k0832_battery', 'literals': len(battery),
                'all_match': bad_bat == 0, 'bad': bad_bat,
                'rows': battery})

    # (b) the 34 binding candidate rows (kit-8 frozen future constants,
    #     verbatim; machine-regenerated byte-identical at this build).
    K9_BINDING = json.loads(K9_BINDING_JSON)

    def emit_k9_row(r):
        m = r['m']
        z = r['z']
        R = m + z + 1
        smax = max(m + 38, z + 2)
        extra = {'co_token_%d_allowed' % m: True,
                 's_domain': '{%d..%d}' % (m, smax), 'arity_max': 3,
                 'style': 'x0 published residual-band style',
                 'registered_by': r['registered_by'],
                 'candidate': r['cand'],
                 'seat_kind': r['kind'],
                 'expect_seats': r['seats'],
                 'expect_dead_seat': r['dead_seat'],
                 'binding': True}
        for tr in r.get('tracker', []):
            extra['trio_tracker_%s' % tr['z']] = tr['cand']
        if r.get('stack_candidates'):
            extra['stack_candidates'] = r['stack_candidates']
        secname = r['secname']
        return row_record_x0(secname, r['label'], extra, R, z, m, m, smax)

    for r in K9_BINDING:
        m = r['m']
        z = r['z']
        if r.get('frontier'):
            r['secname'] = 'frontier_m%d_z%d_row_record' % (m, z)
            r['label'] = ('registered_frontier_record_m%d_z%d_K1268_%s_datum_candidate'
                          % (m, z, r['nth']))
            r['registered_by'] = ('kit-8 frozen output section future_slice_registration_constants '
                                  'item %d (commit 7af915fb), the registered %s parity datum candidate; '
                                  'the frozen prediction text is byte-verbatim and was machine-regenerated '
                                  'by derive_kit9.py before this freeze' % (r['item'], r['nth']))
        else:
            r['secname'] = 'ladder_m%d_z%d_row_record' % (m, z)
            r['label'] = 'registered_kit8future_item%d_%s' % (r['item'], r['kind_label'])
            r['registered_by'] = ('kit-8 frozen output section future_slice_registration_constants '
                                  'item %d (commit 7af915fb); the frozen prediction text is byte-verbatim '
                                  'and was machine-regenerated by derive_kit9.py before this freeze'
                                  % r['item'])
        out.append(emit_k9_row(r))

    # (b2) the m=13/15/17 probe lifecycle rows (kit-8 future item 36,
    #      contingent on the kit-8 probe outcomes which measured the trios
    #      UP 2v0; NON-BINDING scaffold observation rows).
    K9_LIFECYCLE = json.loads(K9_LIFECYCLE_JSON)
    for r in K9_LIFECYCLE:
        m = r['m']; z = r['z']
        R = m + z + 1
        smax = max(m + 38, z + 2)
        extra = {'co_token_%d_allowed' % m: True,
                 's_domain': '{%d..%d}' % (m, smax), 'arity_max': 3,
                 'style': 'x0 published residual-band style',
                 'registered_by': ('kit-8 frozen future_slice_registration_constants item 36 '
                                   '(commit 7af915fb) probe continuation, contingent on the kit-8 probe '
                                   'outcomes (trios measured UP 2v0): the lifecycle rows z=3m-1, 3m, 3m+1; '
                                   'NON-BINDING scaffold observation row'),
                 'candidate': r['cand'],
                 'trio_tracker_z': r['trio'],
                 'seat_kind': 'probe lifecycle',
                 'expect_seats': r['seats'],
                 'expect_dead_seat': r['dead_seat'],
                 'binding': False}
        if r.get('stack_candidates'):
            extra['stack_candidates'] = r['stack_candidates']
        out.append(row_record_x0('lifecycle_m%d_z%d_row_record' % (m, z),
                                 'probe_lifecycle_m%d_z%d' % (m, z),
                                 extra, R, z, m, m, smax))

    # (b3) the EVEN-m mid-slice probes m=14@z=40 / m=16@z=46 / m=18@z=52
    #      (kit-8 second-census S5 proposals, counter-probed 0-hit at
    #      this build BEFORE registering; z DERIVED z=z*(m)+2d=3m-2;
    #      BINDING birth template + NON-BINDING equistack trio).
    K9_PROBES = json.loads(K9_PROBES_JSON)
    for r in K9_PROBES:
        m = r['m']; z = r['z']
        R = m + z + 1
        smax = max(m + 38, z + 2)
        extra = {'co_token_%d_allowed' % m: True,
                 's_domain': '{%d..%d}' % (m, smax), 'arity_max': 3,
                 'style': 'x0 published residual-band style',
                 'registered_by': ('kit-8 second-census S5 even-m mid-slice probe proposal '
                                   '(commit 680421eb/e9847712), counter-probed 0-hit at this build '
                                   'BEFORE registering; z derived z=z*(m)+2d=3m-2=%d' % z),
                 'candidate': r['cand'] + '; the birth template seats are BINDING EXACT candidates '
                              'and any deviation is the datum; the equistack trio is NON-BINDING',
                 'trio_probe_%d' % m: r['trio'],
                 'seat_kind': 'even-m mid-slice probe',
                 'expect_seats': r['seats'],
                 'expect_dead_seat': r['dead_seat'],
                 'binding': True,
                 'stack_candidates': r['stack_candidates']}
        out.append(row_record_x0('evenmid_m%d_z%d_row_record' % (m, z),
                                 'even_mid_slice_probe_m%d_z%d' % (m, z),
                                 extra, R, z, m, m, smax))

    # (b4) the WINDOW SWEEPS m=31 z in {53..60}, m=32 z in {54..61}
    #      (kit-8 frozen items 35-36; registered at this build:
    #      register-before-measure satisfied by this freeze).
    for z in range(53, 61):
        R = 31 + z + 1
        out.append(row_record_x0(
            'inband_m31_z%d_row_record' % z,
            'inband_window_m31_z%d' % z,
            {'co_token_31_allowed': True,
             's_domain': '{31..%d}' % max(31 + 38, z + 2), 'arity_max': 3,
             'style': 'x0 published residual-band style',
             'registered_by': 'kit-8 frozen output section future_slice_registration_constants window proposal (commit 7af915fb), rows z in {53..60} = z*(31)-8..-1; register-before-measure satisfied by this freeze; m=31 is NOT strip-covered',
             'candidate': '0 separations each (in-band-clean precedent); FIRST-EVER below-frontier m=31 rows, no strip-derivation claim made',
             'band': 'm=31 window pinning: z in {53..60} here + frontier {61} + mini-ladder {62,63,64} (kit-8/kit-9); z in {25..52} remains unmeasured, unregistered'},
            R, z, 31, 31, max(31 + 38, z + 2)))

    for z in range(54, 62):
        R = 32 + z + 1
        out.append(row_record_x0(
            'inband_m32_z%d_row_record' % z,
            'inband_window_m32_z%d' % z,
            {'co_token_32_allowed': True,
             's_domain': '{32..%d}' % max(32 + 38, z + 2), 'arity_max': 3,
             'style': 'x0 published residual-band style',
             'registered_by': 'kit-8 frozen output section future_slice_registration_constants window proposal (commit 7af915fb), rows z in {54..61} = z*(32)-8..-1; register-before-measure satisfied by this freeze; m=32 is NOT strip-covered',
             'candidate': '0 separations each (in-band-clean precedent); FIRST-EVER below-frontier m=32 rows, no strip-derivation claim made',
             'band': 'm=32 window pinning: z in {54..61} here + frontier {62} + mini-ladder {63,64,65} (kit-8/kit-9); z in {25..53} remains unmeasured, unregistered'},
            R, z, 32, 32, max(32 + 38, z + 2)))

    # (c) future-slice registration constants for kit-10 (engine-free,
    #     NOT measured here); includes the S5 item-9 stack enumerations
    #     for the m=19/m=20 d=12 birth rows (4 and 3 admissible splits).
    out.append({'section': 'future_slice_registration_constants',
                'label': 'engine_free_paper_only_K0832_closed_form_next_slice_predictions_NOT_measured_here',
                'registered_for_next_execution_kit_log_S5': [[
                    json.loads(K10_FUTURE_JSON)
                ]]})

    # (h) published anchor rechecks (234 spots, verbatim published values)
    rechecks = []
    H.cache_clear()
    for (R, X, z2, expected, role) in anchor_spec:
        XX = tuple(sorted(X, reverse=True))
        hv = H(R, XX, z2)
        S = sum(X)
        ev = v(S, z2, R)
        rechecks.append({'R': R, 'X': list(XX), 'z': z2, 'value': hv,
                         'collapse': ev, 'published_value': expected,
                         'match': hv == expected,
                         'conform': hv == ev,
                         'role': role})
    out.append({'section': 'published_anchor_rechecks',
                'label': 'two_hundred_thirty_four_published_spots_reproduce_exactly_match_field_is_value_equality_with_published',
                'rows': rechecks,
                'note': 'the separation spots are separations by construction (value != collapse BY DESIGN); the match criterion is equality with the PUBLISHED value'})

    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
