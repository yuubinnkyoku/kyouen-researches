#!/usr/bin/env python3
"""Independent whole-chain audit of the published fold-chain root inventory
and head bookkeeping (2026-11-15).

Pure-stdlib, published-files-only audit: re-fetches nothing, runs no runpy
chain, re-derives no solved sets. It re-reads the 26 blob-verified base
certificate files, the 52 blob-verified pre-70e chain head JSONs and the 22
post-70e chain head JSONs, and checks:

1. 100 published git blob pins byte-exact (26 base + 52 chain heads + 22
   pinned post-70e heads through the 83d endpoint); the 4 unpinned post-70e
   heads (71c/70f/73g/70g) get their computed git blob shas recorded for
   future pinning;
2. the root inventory: 194 distinct WIN7 base roots (with the single
   intra-base duplicate root enumerated), 402 distinct receipt roots
   recorded in the 52 chain head addition records, and the cumulative
   published-root inventory at every post-70e checkpoint
   (497@1233 ... 569@75d, 577@77d lane-local, 580@merged-75d-77d, 583@79a,
   587@80d, 592@82c, 596@83a, 601@83b, 603@83c, 606@83d) reconciled against each
   fold's own published folded-root count;
3. D4 orbit structure of the full 606-root inventory: twin pairs
   (same D4 orbit, different raw hex), their per-pair classification and
   provenance (a fold whose roots are all D4-duplicates of already-folded
   inventory is legal set bookkeeping, never a new orbit);
4. per-record geometry of every published receipt record (popcount 7,
   covers 7, d4 canonical hex agreement, marginal hexes subset of covers,
   count consistency) and every nested group-additions record;
5. child-orbit closure bookkeeping at every head that declares one;
6. convention-external receipts: receipt records that live outside the
   published root-count convention keys (*_addition / merged_receipts /
   group_additions) - each must be a D4 twin of an already-inventoried
   orbit, keeping the orbit inventory complete as a SET;
7. head arithmetic: for every head with a baseline_main quote and a
   frontier record, the baseline quote is classified (consistent /
   erratum-pointer / fork-merge / multi-branch / own-label-recompute /
   unverifiable-quote) and the delta arithmetic is re-derived from the
   published marginal records; anomalies must be zero;
8. the 75d / 80d / 82c / 83a / 83b / 83c / 83d endpoint heads and their
   completed-claim fold records.

Second, independently extended implementation of the published-fold-chain
audit: written from the v1 baseline (endpoint 77a) WITHOUT seeing the
parallel lane's v3 extension of the v1 script, extending the same corpus to
the 75d endpoint (v2), the 80d endpoint (v4), the 82c endpoint (v5), the
83a endpoint (v6), the 83b / 83c endpoints (v7) and now the 83d endpoint
(v8): the lane-local 77d
head (1290 -> 1299), the merged 75d+77d head (1302), the 79a head (1304)
and the 80d head (1305) are pinned, inventoried, arithmetically reconciled,
appended to the canonical-line hex-level exactly-once check (81 manifest
hexes claimed exactly once between the 1233 baseline and the 1314 endpoint)
and the bit-78 duplicate root (== the 75d bit-92 receipt root) gets an
explicit exactly-once bookkeeping control (root identity, identical 1290-
baseline marginal records, single canonical-line claim via 75d bit-92,
single inventory entry, merged receipts == 77d receipts minus bit-78). The three canonical heads folded after 77a (77b @1286,
77c @1290, 75d @1296) are pinned, inventoried, arithmetically reconciled
and appended to the canonical-line hex-level exactly-once check (63
manifest hexes claimed exactly once between the 1233 baseline and the 1296
endpoint). Every substantive control of this v2 output agrees with the
published v3 audit JSON (the canonical audit file, written by the v1
script extended in place); this implementation pins 100 blobs (leaving the
four v2 pin proposals 71c/70f/73g/70g unpinned with computed shas - which
match the shas the v3 audit pinned), re-crosschecks the 75d claim
byte-exact including its parents_lost_rows record of the bit-92 cross-cover
of the parallel cost-77d child row, re-crosschecks the 79a, 80d, 82c,
83a, 83b, 83c and 83d completed claims byte-exact, and is published as the second
independent verification record of the extended chain.

The audit asserts; on success it writes the audit JSON. Running it twice
must produce byte-identical output (deterministic ordering throughout).
Bookkeeping audit only - no sweep, no solved-set reconstruction, and no
game-theoretic claim: 11x11 empty board / two-stone root {49,60} /
S2 {59,60} / class 1 / class 2 / class 4 all remain UNKNOWN.
"""
import hashlib, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

def git_blob_sha(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest(), len(data)

# ---------- geometry (verbatim from the 71c fold script) ----------
def images(mask):
    result = [0] * 8
    for p in range(121):
        if mask >> p & 1:
            x, y = p % 11, p // 11
            coords = ((x, y), (y, 10 - x), (10 - x, 10 - y), (10 - y, x),
                      (10 - x, y), (x, 10 - y), (y, x), (10 - y, 10 - x))
            for i, (a, b) in enumerate(coords):
                result[i] |= 1 << (11 * b + a)
    return result

IMG = [images(1 << p) for p in range(121)]

def canon(mask):
    best = None
    for r in range(8):
        v = 0
        for p in range(121):
            if mask >> p & 1:
                v |= IMG[p][r]
        if best is None or v < best:
            best = v
    return best

def covers(root):
    return {canon(root ^ (1 << i)) for i in range(121) if root >> i & 1}

def popcount(x):
    return bin(x).count('1')

HEX32 = re.compile(r'^[0-9a-f]{32}$')

# ---------- 1. published pins byte-exact ----------
BASE_PINS = {
    'priority-certificates-verified.json': '30970ad6f0aef8ceccdc2199090b29930eaecb6f',
    'class2-certificates-verified.json': '9f58be71f986b55632e4be658c4343bba7bd4518',
    'class2-next-certificates-verified.json': '05952496cd040bb614d45ab146598016bc9bffc7',
    'class2-next2-certificates-verified.json': '62171158ea54b0acd9238f6864b2dc7f0a935edc',
    'class2-next3-certificates-verified.json': '6654bfeefe0314d5e6e94578aa36e09de849aaaa',
    'class2-next4-certificates-verified.json': 'f0570f152fe5886f0589e5b00de3038fbf783094',
    'class2-batch5-certificates-verified.json': '02bb76b2b0c135356271978cab0fbd03612a704e',
    'class2-batch3-certificates-verified.json': '1fab35b3d598d629406a09d8f431cb5df2eb045b',
    'class2-batch2-certificates-verified.json': '82098bfb0160758127af5c0c0769d89d19582bdd',
    'class2-batch2b-certificates-verified.json': '5d5e339b5bc9dd4dbe294c878412eb0295de8468',
    'class2-batch1-certificates-verified.json': '24ddd94bf60b2f315801cbd48f08962de81485c6',
    'class2-batch1b-certificates-verified.json': 'b25598a3d11d031bd7a4df0d3d3d4e3d41cda741',
    'class4-batch1-certificates-verified.json': '6ff00942c9fb20e429194dd6a4ed2e0a2dfd50da',
    'class4-batch2-certificates-verified.json': 'd96dc6dbadfdc1284c6cf3c66558afab6f0bf1be',
    'class4-batch3-bit37-certificate.json': 'e804eb7d1304a0ecc1ef19fad80cd9d67d39d2c2',
    'class4-batch3-win7-certificates-20261114.json': 'a00d963e535ba9717777930deb3c8f443c4a9b07',
    'class4-batch3-win7-certificates-child5-20261114.json': '548294d42deb2ee7fbc4807a41cda09479a3f8ec',
    'class4-batch3-win7-certificates-child7-20261114.json': 'f86f4607b23b3e9ba09c0dbd6b047ea01b57b32a',
    'class2-lane-cost58-win7-certificates-20261114.json': 'ba89609330174024b72aaf8eb9ad02d7e3674d1a',
    'class2-lane-cost60-win7-certificates-20261114.json': 'cc17b20dfefa118ad0b07e01735299435f790feb',
    'class2-lane-cost61-win7-certificates-20261114.json': '498ea98124c3dd3e345470719f32b74c20111cbc',
    'class2-lane-cost61b-win7-certificates-20261114.json': '6eb8689b8b2eba722429348e22294ce9e9513739',
    'class2-lane-cost64-win7-certificates-20261114.json': 'b53bcddd5989f3ef807f7d813d422074d49be035',
    'class2-lane-cost65-win7-certificates-20261114.json': 'a666843dd9c2033e6fbacee9aea0bf5edb0e878f',
    'class2-lane-cost68-win7-certificates-20261114.json': 'a9ab77063746f78d4409debe170f55825064399b',
    'class2-lane-cost75-win7-certificates-20261114.json': 'c82ed068a1405d4ac2b898757506e98faa4b605a',
}
CHAIN_PINS = {
    'class-frontier-after-cost70c-warm3-recompute-20261115.json': '50735896bfbfdcf99291200ba77e9551559502a4',
    'class-frontier-cost56a-recompute-20261114.json': '7d07267cb0f69d8ac7882c716683bcf36450d247',
    'class-frontier-cost58b-recompute-20261114.json': 'cf0fd1e484b11c766ad1dc89eef7c2f883afe57d',
    'class-frontier-cost60b-recompute-20261114.json': '27f69b8e2424366f844fe1b20603ec5f9323a8cd',
    'class-frontier-cost61d-recompute-20261114.json': 'be4eda7f34bff42b344f8ffd747114930c95f993',
    'class-frontier-cost61e-recompute-20261114.json': 'caa81d99a619a4436eeba883e8cdf7ce5e788419',
    'class-frontier-cost61f-recompute-20261114.json': '73604c726243bf469d54ea171af018ae94129745',
    'class-frontier-cost62a-recompute-20261114.json': 'b3f3654f29bf75767018f03fbe757edb1596d5c6',
    'class-frontier-cost63e-recompute-20261114.json': 'fd61b3cc71e532866ff848c1e0466f39f2e1e124',
    'class-frontier-cost63e-warm-recompute-20261114.json': '09c7bf14205031d0027a519962e73f226178a737',
    'class-frontier-cost63f-receipts-recompute-20261115.json': 'e1e72b12ca39769f2c4a298d91833b612c97afeb',
    'class-frontier-cost63g-receipts-recompute-20261115.json': 'e311e24346adad570e42f145f9190fe8427ae921',
    'class-frontier-cost64b-recompute-20261114.json': '89893377d6c319cd3ebaacfe569a5350af93d00b',
    'class-frontier-cost65g-recompute-20261114.json': '1d3e29598ff691c5c5c782c1e04c57908a16eb23',
    'class-frontier-cost65g-warm-recompute-20261114.json': '285d8f48f91e3b70e788282b967a4419aafa1cdc',
    'class-frontier-cost65h-65i-recompute-20261114.json': 'a733aa6130320101be2acd0c5bd101c3dbfd0fd7',
    'class-frontier-cost67-recompute-20261114.json': '81807223a4f04cdf3efe75d6fbf2158cd9b83419',
    'class-frontier-cost67b-recompute-20261114.json': '868d3a179757e7a195a6a42e1fdcfe07c2072a22',
    'class-frontier-cost67c-receipts-recompute-20261115.json': '6d187f48420a9b66d527c3c0fb2764ad5f63235a',
    'class-frontier-cost68b-recompute-20261114.json': '24a96c2f8e7636f816893867b7c21fdfa153e57a',
    'class-frontier-cost68c-recompute-20261114.json': '67ac08bf8da9d45909325fd35bee077f77ba834d',
    'class-frontier-cost68d-recompute-20261115.json': '452a1b52238f0d12e9915adccc58ed9f010bb5d2',
    'class-frontier-cost69a-recompute-20261114.json': 'fdd4edf5b39d347a8a07024f343b7da14add8865',
    'class-frontier-cost69c-recompute-20261114.json': 'a4684a59f5aeb77238c5fddc2df027bbab78ee59',
    'class-frontier-cost69e-recompute-20261115.json': 'a06e7aec29fe9830755325eb29bf17dcc2eead22',
    'class-frontier-cost69f-receipts-recompute-20261115.json': '683cbb8671e12ce0f91cd3c4bd0bbb519878a965',
    'class-frontier-cost69h-receipts-recompute-20261115.json': 'd25eb3a00f73cf9ca34fc2816d28045c1e23f3ae',
    'class-frontier-cost70b-recompute-20261114.json': '357cd3413d65bf205034c2f1b23f3eb7afa60763',
    'class-frontier-cost71-recompute-20261114.json': 'eede9095366880e5a3f6cd7c719030b5aa50fe8a',
    'class-frontier-cost72b-receipts-recompute-20261115.json': 'b4f6b821fbe92ebf97669c0712fbd6b1cec9466d',
    'class-frontier-cost73a-recompute-20261114.json': '12d2a80fc0f4234edfff037cee8cc44cd7d1caba',
    'class-frontier-cost73d-recompute-20261114.json': '771b84f93ea9d1d7fe34e40da296d885b1a3ee43',
    'class-frontier-cost74d-receipts-recompute-20261115.json': '06724afe0698ce93319d092521c5887da6eec0f0',
    'class-frontier-cost75b-recompute-20261115.json': '1252731811b82603dbb7bfce1405a9213c3845cc',
    'class-frontier-cost75c-recompute-20261115.json': 'f6733b0d1954dba2a7cc84e40b86620370321cd2',
    'class-frontier-cost76a-receipts-recompute-20261115.json': 'efd83f2637f83c0e1c5c477dcb0cc42162cda534',
    'class-frontier-cost78a-receipts-recompute-20261115.json': '3938bb1668c7dfb80049cdac45f8dee50514c064',
    'class-frontier-merged-cost60bwarm-cost71b-recompute-20261115.json': '0512e381ef15f2c64f2304f4aa9905a58f0e246e',
    'class-frontier-merged-recompute-20261114.json': 'c200ffd3f6caae13da7dc0bb37eadabb3739ba35',
    'class-frontier-merged-recompute-after-multiband2-68dhyg-20261115.json': '81d39ea38f5e19de7fc2aa637e42963f546baa52',
    'class-frontier-merged-recompute-after61f-63a65e-20261114.json': 'b2f2fe4b5fa862795fbceec583f8f707b96fa8b2',
    'class-frontier-merged-recompute-after65h65i-warm67b68c-20261115.json': 'fb99e8c01ec0f2a8f31c080c15afe4e352fad0b9',
    'class-frontier-merged-cost78a-69h-recompute-20261115.json': '294c4ed3d9fb26143d54ef2e45d400d1068a41dd',
    'class-frontier-unified-merge-recompute-20261115.json': 'a0789eedd5b81d1c9ea96220acfb487f38e70e08',
    'class-frontier-warm-multiband-recompute-20261115.json': '01fedcb052988bb01881b427faff87e1ed061059',
    'class-frontier-warm-multiband2-recompute-20261115.json': '0830cfc3746baa6ad5b542579dc9d657b61ac72a',
    'class2-lane-cost63cd-frontier-recompute-20261114.json': '2b67dcb5c998721ce8542e7112d75a0ed809d483',
    'class2-lane-cost65c-frontier-recompute-20261114.json': 'cefd0fecdd887028d4aac7896c77536d0ac7ef41',
    'class2-lane-cost65d-frontier-recompute-20261114.json': 'dbec777893eb5dc74d2b820fa14685e95c16c9b8',
    'class2-lane-cost75-frontier-recompute-20261114.json': '0c08ff3ff6a41c6d421884d889491487137744db',
    'class4-lane-cost78b-frontier-recompute-20261114.json': '4d9c794993ac84dc4ded9febd151f761b07e873c',
    'class4-lane-cost80b-frontier-recompute-20261114.json': '6347cb68de9019f08244cf4b334833f424c3c5e6',
}
POST70E_PINS = {
    'class-frontier-cost70e-receipts-recompute-20261115.json': 'a0171d4bb839aeb813d231c7d879d6a89452359f',
    'class-frontier-cost72c-receipts-recompute-20261115.json': '42dbb92e1505d05389e840e3368974b1c613b750',
    'class-frontier-cost73h-receipts-recompute-20261115.json': '71f79b4bef000aaa1ce16279aa8d08a1ba9f3357',
    'class-frontier-cost65l-receipts-recompute-20261115.json': '0b523e707461b1c4201218a632c3d5c821b8f7f0',
    'class-frontier-cost74g-receipts-recompute-20261115.json': 'fce4ce77a64e039709b89f2a78ece9ffff34e533',
    'class-frontier-cost69i-receipts-recompute-20261115.json': '8692a7a67fc9e51c440a91cb2e95809b7d1825e8',
    'class-frontier-merged-cost65l-74g-recompute-20261115.json': '0210953083309c1dd2d8f1cf036ec1f91e88f267',
    'class-frontier-merged-cost65l-74g-69i-recompute-20261115.json': '8d96b48273248073958b327ff91f7aecccd09944',
    'class-frontier-cost76b-receipts-recompute-20261115.json': '0c35759729663fd561574fd4c5c8ccf2e46550a5',
    'class-frontier-cost77a-receipts-recompute-20261115.json': 'a2ba7235793b051d80658818a83aa02c5a5d4958',
    'class-frontier-cost77b-receipts-recompute-20261115.json': 'b648ed068a1b9a04624b4c230e011e6fefeddb01',
    'class-frontier-cost77c-receipts-recompute-20261115.json': '7f2badce7132aa7fdf76c9ee0283bd14a9ac9e7b',
    'class-frontier-cost75d-receipts-recompute-20261115.json': 'c801e60578ee5c5272e75719e35847052ac58314',
    'class-frontier-cost77d-receipts-recompute-20261115.json': 'd19c96b7cb0a01f8fd50179b3ff77595408537d7',
    'class-frontier-merged-cost75d-77d-receipts-recompute-20261115.json': '97130384432e4a0e1e022292748f9fed1e957c0f',
    'class-frontier-cost79a-receipts-recompute-20261115.json': '7dea99ffe76d767223666241964824f005843893',
    'class-frontier-cost80d-receipts-recompute-20261115.json': '289c93373692d6627347dc9bbb9ffdc3653f508b',
    'class-frontier-cost82c-receipts-recompute-20261115.json': '4ee6aaab50b61e8d48e1d37afed373cd01094620',
    'class-frontier-cost83a-receipts-recompute-20261115.json': '74e35f224e4e46f9464bcaed14c5ea073f4bee5c',
    'class-frontier-cost83b-receipts-recompute-20261115.json': 'b089bd955efaf51933c892ca1877ca6ac8062f75',
    'class-frontier-cost83c-receipts-recompute-20261115.json': 'fc7832edce1f736ea5f15b2632d79d709fa004f4',
    'class-frontier-cost83d-receipts-recompute-20261115.json': '49cb8022bc715fa22d7c2d483160083478676caa',
}
POST70E_ORDER = [
    'class-frontier-cost70e-receipts-recompute-20261115.json',
    'class-frontier-cost71c-receipts-recompute-20261115.json',
    'class-frontier-cost70f-receipts-recompute-20261115.json',
    'class-frontier-cost72c-receipts-recompute-20261115.json',
    'class-frontier-cost73g-receipts-recompute-20261115.json',
    'class-frontier-cost70g-receipts-recompute-20261115.json',
    'class-frontier-cost73h-receipts-recompute-20261115.json',
    'class-frontier-cost65l-receipts-recompute-20261115.json',
    'class-frontier-cost74g-receipts-recompute-20261115.json',
    'class-frontier-cost69i-receipts-recompute-20261115.json',
    'class-frontier-merged-cost65l-74g-recompute-20261115.json',
    'class-frontier-merged-cost65l-74g-69i-recompute-20261115.json',
    'class-frontier-cost76b-receipts-recompute-20261115.json',
    'class-frontier-cost77a-receipts-recompute-20261115.json',
    'class-frontier-cost77b-receipts-recompute-20261115.json',
    'class-frontier-cost77c-receipts-recompute-20261115.json',
    'class-frontier-cost75d-receipts-recompute-20261115.json',
    # v4 extension: the lane-local 77d fold (1290 -> 1299) and the canonical
    # line through the merged 75d+77d fold (1296 -> 1302), 79a (-> 1304) and
    # 80d (-> 1305)
    'class-frontier-cost77d-receipts-recompute-20261115.json',
    'class-frontier-merged-cost75d-77d-receipts-recompute-20261115.json',
    'class-frontier-cost79a-receipts-recompute-20261115.json',
    'class-frontier-cost80d-receipts-recompute-20261115.json',
    # v5 extension: the cost-82c receipts fold (1305 -> 1306)
    'class-frontier-cost82c-receipts-recompute-20261115.json',
    # v6 extension: the cost-83a receipts fold (1306 -> 1309)
    'class-frontier-cost83a-receipts-recompute-20261115.json',
    # v7 extension: the cost-83b (1309 -> 1312) and cost-83c (1312 -> 1313)
    # receipts folds
    'class-frontier-cost83b-receipts-recompute-20261115.json',
    'class-frontier-cost83c-receipts-recompute-20261115.json',
    # v8 extension: the cost-83d (1313 -> 1314) receipts fold
    'class-frontier-cost83d-receipts-recompute-20261115.json',
]
UNPINNED_POST70E = [n for n in POST70E_ORDER if n not in POST70E_PINS]

pin_report = {'base': 0, 'chain': 0, 'post70e': 0}
for name, want in sorted(BASE_PINS.items()):
    s, _ = git_blob_sha(OUT / name)
    assert s == want, ('base pin', name, s, want)
    pin_report['base'] += 1
for name, want in sorted(CHAIN_PINS.items()):
    s, _ = git_blob_sha(OUT / name)
    assert s == want, ('chain pin', name, s, want)
    pin_report['chain'] += 1
for name, want in sorted(POST70E_PINS.items()):
    s, _ = git_blob_sha(OUT / name)
    assert s == want, ('post70e pin', name, s, want)
    pin_report['post70e'] += 1
n_pins = pin_report['base'] + pin_report['chain'] + pin_report['post70e']
assert n_pins == 100, n_pins
unpinned_computed = {}
for name in UNPINNED_POST70E:
    s, blen = git_blob_sha(OUT / name)
    unpinned_computed[name] = {'git_blob_sha': s, 'bytes': blen}

# ---------- 2. root inventory ----------
def win_roots_of(name):
    d = json.loads((OUT / name).read_text())
    out = []
    for rec in d.get('certificates', []):
        h = rec.get('root') or rec.get('root_hex')
        if h and HEX32.match(h) and rec.get('verdict') in (None, 'WIN7'):
            out.append(h)
    if 'root_hex' in d and 'certificates' not in d:
        out.append(d['root_hex'])
    return out

base_raw, base_by_file = [], {}
for name in sorted(BASE_PINS):
    base_by_file[name] = win_roots_of(name)
    base_raw.extend(base_by_file[name])
base_set = set(base_raw)
assert len(base_set) == 194, len(base_set)
base_dup_counts = Counter(base_raw)
intra_base_duplicates = sorted(
    {'root': h, 'files': sorted(n for n, rs in base_by_file.items() if h in rs),
     'times_listed': c}
    for h, c in base_dup_counts.items() if c > 1)
assert len(intra_base_duplicates) == 1 and intra_base_duplicates[0]['root'] \
    == '00000000000000801a02040080000000', intra_base_duplicates
assert intra_base_duplicates[0]['files'] == sorted([
    'class2-lane-cost68-win7-certificates-20261114.json',
    'class2-lane-cost75-win7-certificates-20261114.json'])

def collect_addition_roots(v, out):
    """71c-verbatim recursive root collector for convention keys."""
    if isinstance(v, dict):
        for k, x in v.items():
            if k in ('root', 'root_hex') and isinstance(x, str) and HEX32.match(x):
                out.append(x)
            elif k == 'roots' and isinstance(x, list):
                for r in x:
                    if isinstance(r, str) and HEX32.match(r):
                        out.append(r)
            else:
                collect_addition_roots(x, out)
    elif isinstance(v, list):
        for x in v:
            collect_addition_roots(x, out)

chain_names = sorted(CHAIN_PINS)
chain_roots_by_head = {}
for name in chain_names:
    d = json.loads((OUT / name).read_text())
    rr = []
    for k in d:
        if k.endswith('_addition') or k in ('merged_receipts', 'group_additions'):
            collect_addition_roots(d[k], rr)
    chain_roots_by_head[name] = sorted(set(rr))
chain_set = {int(h, 16) for n in chain_names for h in chain_roots_by_head[n]}
assert len(chain_set) == 402, len(chain_set)
base_int = {int(h, 16) for h in base_set}
overlap_base_chain = base_int & chain_set
assert len(overlap_base_chain) == 104, len(overlap_base_chain)

inventory = set(base_int) | set(chain_set)
assert len(inventory) == 492, len(inventory)

cumulative_report = []
# each fold's own published post-fold root count on ITS branch baseline
# (branch heads fork from the 73h head and exclude the sibling's roots)
own_claim = {
    'class-frontier-cost70e-receipts-recompute-20261115.json': 497,
    'class-frontier-cost71c-receipts-recompute-20261115.json': 499,
    'class-frontier-cost70f-receipts-recompute-20261115.json': 503,
    'class-frontier-cost72c-receipts-recompute-20261115.json': 512,
    'class-frontier-cost73g-receipts-recompute-20261115.json': 512 + 8,
    'class-frontier-cost70g-receipts-recompute-20261115.json': 520 + 8,
    'class-frontier-cost73h-receipts-recompute-20261115.json': 532,
    'class-frontier-cost65l-receipts-recompute-20261115.json': 532 + 2,
    'class-frontier-cost74g-receipts-recompute-20261115.json': 532 + 10,
    'class-frontier-cost69i-receipts-recompute-20261115.json': 532 + 10 + 4,
    'class-frontier-merged-cost65l-74g-recompute-20261115.json': 532 + 2 + 10,
    'class-frontier-merged-cost65l-74g-69i-recompute-20261115.json': 532 + 2 + 10 + 4,
    'class-frontier-cost76b-receipts-recompute-20261115.json': 548 + 2,
    'class-frontier-cost77a-receipts-recompute-20261115.json': 550 + 3,
    'class-frontier-cost77b-receipts-recompute-20261115.json': 553 + 4,
    'class-frontier-cost77c-receipts-recompute-20261115.json': 557 + 8,
    'class-frontier-cost75d-receipts-recompute-20261115.json': 565 + 4,
    # 77d is lane-local: its baseline is the 77c head 1290 and all 12 roots
    # are new on that branch (565 + 12 = 577, including the bit-78 root);
    # the merged fold rebases the 77d receipts on the 75d head 1296 and its
    # 11 receipts exclude bit-78 (569 + 11 = 580: the bit-78 root is the
    # 75d bit-92 root already in the 1296 inventory)
    'class-frontier-cost77d-receipts-recompute-20261115.json': 565 + 12,
    'class-frontier-merged-cost75d-77d-receipts-recompute-20261115.json': 569 + 11,
    'class-frontier-cost79a-receipts-recompute-20261115.json': 580 + 3,
    'class-frontier-cost80d-receipts-recompute-20261115.json': 583 + 4,
    'class-frontier-cost82c-receipts-recompute-20261115.json': 587 + 5,
    'class-frontier-cost83a-receipts-recompute-20261115.json': 592 + 4,
    'class-frontier-cost83b-receipts-recompute-20261115.json': 596 + 5,
    'class-frontier-cost83c-receipts-recompute-20261115.json': 601 + 2,
    'class-frontier-cost83d-receipts-recompute-20261115.json': 603 + 3,
}
# fork topology: head -> (baseline head for the own-claim arithmetic)
own_baseline = {
    'class-frontier-cost70e-receipts-recompute-20261115.json': None,
    'class-frontier-cost71c-receipts-recompute-20261115.json':
        'class-frontier-cost70e-receipts-recompute-20261115.json',
    'class-frontier-cost70f-receipts-recompute-20261115.json':
        'class-frontier-cost71c-receipts-recompute-20261115.json',
    'class-frontier-cost72c-receipts-recompute-20261115.json':
        'class-frontier-cost70f-receipts-recompute-20261115.json',
    'class-frontier-cost73g-receipts-recompute-20261115.json':
        'class-frontier-cost72c-receipts-recompute-20261115.json',
    'class-frontier-cost70g-receipts-recompute-20261115.json':
        'class-frontier-cost73g-receipts-recompute-20261115.json',
    'class-frontier-cost73h-receipts-recompute-20261115.json':
        'class-frontier-cost70g-receipts-recompute-20261115.json',
    'class-frontier-cost65l-receipts-recompute-20261115.json':
        'class-frontier-cost73h-receipts-recompute-20261115.json',
    'class-frontier-cost74g-receipts-recompute-20261115.json':
        'class-frontier-cost73h-receipts-recompute-20261115.json',
    'class-frontier-cost69i-receipts-recompute-20261115.json':
        'class-frontier-cost74g-receipts-recompute-20261115.json',
    'class-frontier-merged-cost65l-74g-recompute-20261115.json':
        'class-frontier-cost73h-receipts-recompute-20261115.json',
    'class-frontier-merged-cost65l-74g-69i-recompute-20261115.json':
        'class-frontier-merged-cost65l-74g-recompute-20261115.json',
    'class-frontier-cost76b-receipts-recompute-20261115.json':
        'class-frontier-merged-cost65l-74g-69i-recompute-20261115.json',
    'class-frontier-cost77a-receipts-recompute-20261115.json':
        'class-frontier-cost76b-receipts-recompute-20261115.json',
    'class-frontier-cost77b-receipts-recompute-20261115.json':
        'class-frontier-cost77a-receipts-recompute-20261115.json',
    'class-frontier-cost77c-receipts-recompute-20261115.json':
        'class-frontier-cost77b-receipts-recompute-20261115.json',
    'class-frontier-cost75d-receipts-recompute-20261115.json':
        'class-frontier-cost77c-receipts-recompute-20261115.json',
    'class-frontier-cost77d-receipts-recompute-20261115.json':
        'class-frontier-cost77c-receipts-recompute-20261115.json',
    'class-frontier-merged-cost75d-77d-receipts-recompute-20261115.json':
        'class-frontier-cost75d-receipts-recompute-20261115.json',
    'class-frontier-cost79a-receipts-recompute-20261115.json':
        'class-frontier-merged-cost75d-77d-receipts-recompute-20261115.json',
    'class-frontier-cost80d-receipts-recompute-20261115.json':
        'class-frontier-cost79a-receipts-recompute-20261115.json',
    'class-frontier-cost82c-receipts-recompute-20261115.json':
        'class-frontier-cost80d-receipts-recompute-20261115.json',
    'class-frontier-cost83a-receipts-recompute-20261115.json':
        'class-frontier-cost82c-receipts-recompute-20261115.json',
    'class-frontier-cost83b-receipts-recompute-20261115.json':
        'class-frontier-cost83a-receipts-recompute-20261115.json',
    'class-frontier-cost83c-receipts-recompute-20261115.json':
        'class-frontier-cost83b-receipts-recompute-20261115.json',
    'class-frontier-cost83d-receipts-recompute-20261115.json':
        'class-frontier-cost83c-receipts-recompute-20261115.json',
}
own_cum_seen = {}

def head_roots_all(name):
    d = json.loads((OUT / name).read_text())
    rr = []
    for k in d:
        if k.endswith('_addition') or k in ('merged_receipts', 'group_additions', 'cost72_fold'):
            collect_addition_roots(d[k], rr)
    return {int(h, 16) for h in rr}

for name in POST70E_ORDER:
    rr = set(head_roots_all(name))
    new = rr - inventory
    inventory |= rr
    cum = len(inventory)
    # own-branch accounting: baseline own-count + this head's roots new
    # to that baseline
    bl = own_baseline[name]
    bl_roots = set(head_roots_all(bl)) if bl else (base_int | chain_set)
    bl_own = own_cum_seen.get(bl, len(bl_roots | (set() if bl is None else set()))) \
        if bl is not None else None
    if bl is None:
        own_after = len(rr | base_int | chain_set)
    else:
        # the branch lineage of the baseline: base + chain + the roots of
        # every head on the baseline's own ancestor chain (follow the
        # own_baseline links, NOT document order: the 74g fold's baseline
        # is the 73h head and excludes the parallel 65l receipts even though
        # 65l precedes 74g in document order)
        chain_anc = []
        cur = bl
        while cur is not None:
            chain_anc.append(cur)
            cur = own_baseline[cur]
        lineage = set(base_int) | set(chain_set)
        for n in reversed(chain_anc):
            lineage |= set(head_roots_all(n))
        own_after = len(lineage | rr)
    own_cum_seen[name] = own_after
    entry = {
        'head': name, 'roots_in_head': len(rr), 'new_orbits_added': len(new),
        'audit_document_order_cumulative': cum,
        'fold_own_branch_cumulative': own_after,
        'fold_published_own_claim': own_claim[name],
        'baseline_head': bl,
        'matches_published': own_after == own_claim[name]}
    cumulative_report.append(entry)
    assert entry['matches_published'], entry
    assert own_after <= cum, entry
assert cumulative_report[-1]['audit_document_order_cumulative'] == 606
assert cumulative_report[-1]['fold_own_branch_cumulative'] == 606
assert inventory == (base_int | chain_set) | set().union(*[
    set(head_roots_all(n)) for n in POST70E_ORDER])
assert cumulative_report[-1]['audit_document_order_cumulative'] == 606

# ---------- 3. D4 orbit structure of the 606-root inventory ----------
all_roots = sorted(inventory)
d4_of = {r: canon(r) for r in all_roots}
orbits = defaultdict(list)
for r in all_roots:
    orbits[d4_of[r]].append(r)
n_orbits = len(orbits)
twin_pairs = []
for o, rs in sorted(orbits.items()):
    if len(rs) > 1:
        assert len(rs) == 2, (o, rs)
        twin_pairs.append(sorted(rs))
assert len(twin_pairs) == 11, len(twin_pairs)
# the 16 new roots (4@77b + 8@77c + 4@75d) plus the 5 roots of the 82c fold
# (v5), the 4 roots of the 83a fold (v6), the 5+2 roots of the 83b/83c
# folds (v7) and the 3 roots of the 83d fold (v8) were asserted
# D4-canonically
# disjoint from the prior inventory and pairwise-distinct in their own fold
# scripts, so the twin-pair count is unchanged at 11
assert n_orbits == 606 - 11, n_orbits

# provenance of every inventory root
root_prov = defaultdict(list)
for name in sorted(BASE_PINS):
    for h in base_by_file[name]:
        root_prov[int(h, 16)].append({'kind': 'base', 'head': name})
for name in chain_names:
    for h in chain_roots_by_head[name]:
        root_prov[int(h, 16)].append({'kind': 'chain_head', 'head': name})
for name in POST70E_ORDER:
    for r in head_roots_all(name):
        root_prov[r].append({'kind': 'post70e_head', 'head': name})

def provenance_kinds(r):
    return sorted({(p['kind'], ) for p in root_prov[r]})

twin_analysis = []
for pair in twin_pairs:
    entry = {'roots': [f'{r:032x}' for r in pair],
             'd4_orbit': f'{d4_of[pair[0]]:032x}', 'members': []}
    for r in pair:
        provs = root_prov[r]
        entry['members'].append({
            'root_hex': f'{r:032x}',
            'provenance': [{'kind': p['kind'], 'head': p['head']} for p in provs],
            'n_provenance': len(provs)})
    twin_analysis.append(entry)

# multi-provenance roots (re-listed by a later merged head)
multi_prov = [
    {'root_hex': f'{r:032x}',
     'provenance': [{'kind': p['kind'], 'head': p['head']} for p in root_prov[r]]}
    for r in sorted(all_roots) if len(root_prov[r]) > 2]

# ---------- 4. per-record geometry and record collection ----------
MIM_KEYS = ('marginal_in_manifest', 'marginal_in_manifest_merged')
HEX_KEYS = ('marginal_manifest_hexes', 'marginal_manifest_hexes_merged')

def is_root_record(x):
    if not isinstance(x, dict):
        return False
    h = x.get('root_hex') or x.get('root')
    if isinstance(h, str) and HEX32.match(h):
        return any(k in x for k in MIM_KEYS + HEX_KEYS + ('marginal',))
    if 'roots' in x and isinstance(x['roots'], list) and x['roots']:
        return any(k in x for k in MIM_KEYS + HEX_KEYS + ('marginal',))
    return False

def records_of(name):
    """Every published receipt record under the convention keys
    (*_addition / merged_receipts / group_additions / *_fold), handling all
    published shapes: per-bit dicts, root-list aggregate records, single
    dicts, record lists, and lane/bit-nested group dicts."""
    d = json.loads((OUT / name).read_text())
    recs = []

    def scan(key, v, path):
        if isinstance(v, list):
            for x in v:
                if isinstance(x, dict) and is_root_record(x):
                    recs.append((key, path, x))
                elif isinstance(x, (list, dict)):
                    scan(key, x, path + ['*'])
        elif isinstance(v, dict):
            if is_root_record(v):
                recs.append((key, path, v))
            else:
                for k2, x in v.items():
                    scan(key, x, path + [k2])

    for k in d:
        if k.endswith('_addition') or k in ('merged_receipts', 'group_additions') \
                or k.endswith('_fold'):
            scan(k, d[k], [k])
    return recs

def mim_of(rec):
    for k in MIM_KEYS:
        if rec.get(k) is not None:
            return rec[k]
    return None

def hexes_of(rec):
    for k in HEX_KEYS:
        if rec.get(k) is not None:
            return list(rec[k])
    return None

def roots_of_record(rec):
    if 'roots' in rec and isinstance(rec['roots'], list):
        return [int(h, 16) for h in rec['roots']]
    h = rec.get('root_hex') or rec.get('root')
    return [int(h, 16)]

geom_anomalies = []
hex_errata = []
n_receipt_records = 0
n_group_records = 0
for name in chain_names + POST70E_ORDER:
    for key, path, rec in records_of(name):
        if key == 'group_additions':
            n_group_records += 1
        else:
            n_receipt_records += 1
        try:
            rvs = roots_of_record(rec)
        except (TypeError, ValueError):
            geom_anomalies.append({'head': name, 'key': key, 'check': 'root_parse',
                                   'value': rec.get('root_hex') or rec.get('root')})
            continue
        cov_union = set()
        for rv in rvs:
            if popcount(rv) != 7:
                geom_anomalies.append({'head': name, 'key': key, 'root': f'{rv:032x}',
                                       'check': 'popcount7', 'value': popcount(rv)})
            cov_union |= covers(rv)
        if len(rvs) == 1:
            if len(cov_union) != 7:
                geom_anomalies.append({'head': name, 'key': key,
                                       'root': f'{rvs[0]:032x}',
                                       'check': 'covers7', 'value': len(cov_union)})
            if rec.get('covers') is not None and rec['covers'] != 7:
                geom_anomalies.append({'head': name, 'key': key,
                                       'root': f'{rvs[0]:032x}',
                                       'check': 'covers_field', 'value': rec['covers']})
            if 'd4_canonical_hex' in rec and \
                    rec['d4_canonical_hex'] != f'{canon(rvs[0]):032x}':
                geom_anomalies.append({'head': name, 'key': key,
                                       'root': f'{rvs[0]:032x}',
                                       'check': 'd4_canonical_hex',
                                       'value': rec['d4_canonical_hex']})
        mh = hexes_of(rec)
        if mh is not None:
            malformed = [h for h in mh if len(h) != 32 or not HEX32.match(h)]
            if malformed:
                # published-data erratum: count-level arithmetic still uses
                # the declared marginal_in_manifest, only the hex literal is
                # corrupt; excluded from the logical subset checks below.
                hex_errata.append({
                    'head': name, 'key': key, 'check': 'malformed_marginal_hex',
                    'value': malformed,
                    'marginal_in_manifest': mim_of(rec),
                    'n_valid_entries': len(mh) - len(malformed)})
                mh = [h for h in mh if h not in malformed]
            cov_hex = {f'{c:032x}' for c in cov_union}
            extra = sorted(set(mh) - cov_hex)
            if extra:
                geom_anomalies.append({'head': name, 'key': key,
                                       'check': 'marginal_subset_of_covers',
                                       'value': extra})
            if len(mh) != len(set(mh)):
                geom_anomalies.append({'head': name, 'key': key,
                                       'check': 'marginal_hexes_distinct',
                                       'value': len(mh)})
            m = mim_of(rec)
            if m is not None and m != len(mh) + len(malformed):
                geom_anomalies.append({'head': name, 'key': key,
                                       'check': 'mim_count', 'value': (m, len(mh))})

# ---------- 5. child-orbit closure bookkeeping ----------
child_closure_report = []
for name in chain_names + POST70E_ORDER:
    d = json.loads((OUT / name).read_text())
    child = None
    t = d.get('target', {})
    if isinstance(t, dict) and t.get('s6_child_hex'):
        child = t['s6_child_hex']
    closes = []
    if child:
        for key, path, rec in records_of(name):
            mh = hexes_of(rec)
            if mh and child in mh:
                closes.append({'key': key, 'bit': rec.get('bit'),
                               'path': '/'.join(str(x) for x in path)})
    if child or closes:
        child_closure_report.append({
            'head': name, 'child': child, 'closing_records': closes,
            'n_closing_records': len(closes),
            'declared_by_totals': (d.get('totals', {}) or {}).get('child_closed_by_bit')})

# ---------- 6. convention-external receipts ----------
def iter_receipt_dicts(name):
    d = json.loads((OUT / name).read_text())
    out = []
    def scan(v, path):
        if isinstance(v, dict):
            h = v.get('root_hex') or v.get('root')
            if isinstance(h, str) and HEX32.match(h) and (
                    any(k in v for k in ('marginal', 'marginal_in_manifest',
                                         'marginal_manifest_hexes'))):
                out.append((path, v))
            for k, x in v.items():
                scan(x, path + [k])
        elif isinstance(v, list):
            for i, x in enumerate(v):
                scan(x, path + [i])
    scan(d, [])
    return out

inventory_orbits = {d4_of[r] for r in all_roots}
convention_external = []
for name in chain_names + POST70E_ORDER:
    d = json.loads((OUT / name).read_text())
    conv_roots = set()
    for k in d:
        if k.endswith('_addition') or k in ('merged_receipts', 'group_additions'):
            rr = []
            collect_addition_roots(d[k], rr)
            conv_roots.update(int(h, 16) for h in rr)
    for path, rec in iter_receipt_dicts(name):
        h = rec.get('root_hex') or rec.get('root')
        rv = int(h, 16)
        if rv in conv_roots:
            continue
        orb = canon(rv)
        entry = {'head': name, 'path': '/'.join(str(x) for x in path),
                 'root_hex': h, 'marginal_in_manifest': rec.get('marginal_in_manifest'),
                 'd4_orbit': f'{orb:032x}',
                 'd4_twin_of_inventory': orb in inventory_orbits}
        convention_external.append(entry)
        assert entry['d4_twin_of_inventory'], entry

# ---------- 7. head arithmetic ----------
NUMTOK = re.compile(r'(?<![\w-])(\d+)(?!\w)')

def frontier_of(name):
    d = json.loads((OUT / name).read_text())
    best = None
    for k in d:
        if k.startswith('frontier') and k != 'frontier_effect' \
                and 'intermediate' not in k:
            best = (k, d[k])
    if best is None:
        return None, None
    return best

def five(s):
    """First (...) block of the baseline_main quote -> the 5 headline
    integers (numbers embedded in tokens like cost-69f are excluded)."""
    m = re.search(r'\(([^()]*)\)', s)
    assert m, s[:120]
    nums = [int(x) for x in NUMTOK.findall(m.group(1))][:5]
    assert len(nums) == 5, (s[:120], nums)
    return nums

frontier_solved = {}
for name in chain_names + POST70E_ORDER:
    k, f = frontier_of(name)
    if f is not None and 'solved_s6_in_manifest' in f:
        frontier_solved[name] = f['solved_s6_in_manifest']

# global table of every published 5-field frontier state in the corpus
STATE_FIELDS = ('solved_s6_in_manifest', 'unique_remaining_s6',
                'sum_remaining_cost', 's6_needed_by_open_classes',
                'cost_needed_by_open_classes')
state_index = {}
for name in chain_names + POST70E_ORDER:
    dd = json.loads((OUT / name).read_text())
    for kk, vv in dd.items():
        if isinstance(vv, dict) and all(f in vv for f in STATE_FIELDS):
            t = tuple(vv[f] for f in STATE_FIELDS)
            state_index.setdefault(t, []).append(f'{name}:{kk}')

arith = []
arith_anomalies = []
for name in chain_names + POST70E_ORDER:
    d = json.loads((OUT / name).read_text())
    fk, f = frontier_of(name)
    bm = d.get('baseline_main')
    if f is None or bm is None or 'solved_s6_in_manifest' not in f:
        continue
    entry = {'head': name, 'frontier_key': fk,
             'frontier_solved': f['solved_s6_in_manifest']}
    recs = records_of(name)
    own_label = name.replace('class-frontier-', '').replace('class2-lane-', '') \
                     .replace('class4-lane-', '') \
                     .replace('-recompute-20261114.json', '') \
                     .replace('-recompute-20261115.json', '') \
                     .replace('-frontier', '')
    if '(' not in bm:
        entry.update({'classification': 'no_numeric_baseline_quote',
                      'quote_status': 'unverifiable_quote',
                      'sum_mim': sum(mim_of(r) for _, _, r in recs
                                     if mim_of(r) is not None),
                      'delta': None, 'referenced_head': None})
        arith.append(entry)
        continue
    delta = f['solved_s6_in_manifest'] - five(bm)[0]
    entry.update({'baseline_quote': five(bm), 'delta': delta})
    mims = [mim_of(r) for _, _, r in recs if mim_of(r) is not None]
    mhex = set()
    for _, _, r in recs:
        mhex.update(hexes_of(r) or [])
    s = sum(mims)
    u = len(mhex)
    entry['sum_mim'] = s
    entry['union_mim'] = u
    if delta == 0 and not mims:
        entry['classification'] = 'no-op-head'
    elif u == delta and s == delta:
        entry['classification'] = 'sequential-fold-union'
    elif u == delta:
        entry['classification'] = 'parallel-batch-union'
    elif s == delta:
        entry['classification'] = 'sum-equals-delta'
    else:
        # own-label fallback: only the addition records whose key matches the
        # head's own label carry the new marginals (recompute re-listing)
        own_recs = [(k, p, r) for k, p, r in recs
                    if k == own_label + '_addition']
        os_ = sum(mim_of(r) for _, _, r in own_recs if mim_of(r) is not None)
        oh_ = set()
        for _, _, r in own_recs:
            oh_.update(hexes_of(r) or [])
        if os_ == delta and len(oh_) == delta:
            entry['classification'] = 'own-label-recompute'
            entry['own_label_sum_mim'] = os_
            entry['own_label_union_mim'] = len(oh_)
        else:
            # cross-head merge: a summary addition dict declares lane
            # marginals whose receipt records live in another head
            ext = 0
            for k in d:
                if k.endswith('_addition') and isinstance(d[k], dict):
                    for k2, v2 in d[k].items():
                        if k2.endswith('_marginal_in_manifest') \
                                and isinstance(v2, int):
                            lane = k2[:-len('_marginal_in_manifest')]
                            if lane == 'total':
                                continue
                            if not any(rk == lane + '_addition' for rk in d):
                                ext += v2
            if ext and s + ext == delta and u + ext == delta:
                entry['classification'] = 'cross-head-merge'
                entry['external_declared_mim'] = ext
            else:
                entry['classification'] = 'unclassified'
                arith_anomalies.append({'head': name, 'delta': delta,
                                        'sum': s, 'union': u, 'ext': ext,
                                        'own_label_sum': os_ if own_recs else None})
    # quote check: exact 5-field match against any published state
    entry['quote_state_matches'] = state_index.get(tuple(five(bm)), [])
    entry['quote_status'] = ('matched_published_state'
                             if entry['quote_state_matches']
                             else 'unmatched_quote')
    # prose pointer: the corpus head whose full filename is mentioned in
    # the quote text (unambiguous; short labels like 'merged' would
    # substring-match unrelated prose)
    pointer = None
    for other in chain_names + POST70E_ORDER:
        if other != name and other in bm:
            pointer = other
            break
    entry['prose_pointer_head'] = pointer
    if entry['quote_status'] == 'matched_published_state' and pointer:
        matched_heads = {m.split(':')[0] for m in entry['quote_state_matches']}
        if pointer not in matched_heads:
            entry['pointer_name_differs_from_matched_state'] = True
    arith.append(entry)

unmatched_quotes = [a for a in arith if a['quote_status'] == 'unmatched_quote']
# known erratum: 70f's baseline quote names 71c and quotes 71c's final solved
# count, but its four remaining-fields are the pre-71c baseline values; the
# quoted 5-tuple exists in no published head. Nothing else may be unmatched.
KNOWN_QUOTE_ERRATA = {
    'class-frontier-cost70f-receipts-recompute-20261115.json',
}
assert {a['head'] for a in unmatched_quotes} == KNOWN_QUOTE_ERRATA, \
    unmatched_quotes

def final_state_of(name):
    k, f = frontier_of(name)
    if f is None:
        return None
    return [f[fl] for fl in STATE_FIELDS]

quote_errata = []
for a in unmatched_quotes:
    ptr = a.get('prose_pointer_head')
    err = {'head': a['head'], 'quoted': a['baseline_quote'],
           'prose_pointer_head': ptr,
           'pointer_actual_final_state': (final_state_of(ptr)
                                          if ptr else None),
           'characterization':
               'quoted solved count matches the pointer head final state '
               'but the four remaining-fields quote the pre-lane baseline '
               'state; quoted 5-tuple matches no published head; delta '
               'arithmetic uses the correct solved baseline and reconciles '
               'with the head receipts'}
    quote_errata.append(err)

pointer_differs = [{'head': a['head'], 'prose_pointer_head': a['prose_pointer_head'],
                    'matched_states': a['quote_state_matches']}
                   for a in arith
                   if a.get('pointer_name_differs_from_matched_state')]

assert not arith_anomalies, arith_anomalies

# fork-merge head special entry
FORK_HEAD = 'class-frontier-merged-recompute-after65h65i-warm67b68c-20261115.json'
fork_entry = next((a for a in arith if a['head'] == FORK_HEAD), None)

# ---------- 7b. canonical-line hex-level exactly-once ----------
# The canonical line from the 1233 baseline to the 80d endpoint: every
# consecutive baseline-quote provenance is already verified by the state
# matching in section 7; branch heads 65l/74g/69i enter the canonical line
# exactly once through the merged-1277 head's merged_receipts. The v4
# extension continues through the merged 75d+77d (1302), 79a (1304) and
# 80d (1305) heads; the lane-local 77d head (1290 -> 1299) stays off the
# canonical line.
CANONICAL_LINE = [
    ('class-frontier-cost71c-receipts-recompute-20261115.json',
     'cost71c_addition'),
    ('class-frontier-cost70f-receipts-recompute-20261115.json',
     'cost70f_addition'),
    ('class-frontier-cost72c-receipts-recompute-20261115.json',
     'cost72c_addition'),
    ('class-frontier-cost73g-receipts-recompute-20261115.json',
     'cost73g_addition'),
    ('class-frontier-cost70g-receipts-recompute-20261115.json',
     'cost70g_addition'),
    ('class-frontier-cost73h-receipts-recompute-20261115.json',
     'cost73h_addition'),
    ('class-frontier-merged-cost65l-74g-69i-recompute-20261115.json',
     'merged_receipts'),
    ('class-frontier-cost76b-receipts-recompute-20261115.json',
     'cost76b_addition'),
    ('class-frontier-cost77a-receipts-recompute-20261115.json',
     'cost77a_addition'),
    ('class-frontier-cost77b-receipts-recompute-20261115.json',
     'cost77b_addition'),
    ('class-frontier-cost77c-receipts-recompute-20261115.json',
     'cost77c_addition'),
    ('class-frontier-cost75d-receipts-recompute-20261115.json',
     'cost75d_addition'),
    # v4: the canonical line continues through the merged 75d+77d fold (its
    # cost77d_addition holds the 11 rebased 77d receipts - the 75d receipts
    # are already claimed by the 75d_addition entry above), then 79a and 80d
    ('class-frontier-merged-cost75d-77d-receipts-recompute-20261115.json',
     'cost77d_addition'),
    ('class-frontier-cost79a-receipts-recompute-20261115.json',
     'cost79a_addition'),
    ('class-frontier-cost80d-receipts-recompute-20261115.json',
     'cost80d_addition'),
    # v5: the canonical line continues through the cost-82c fold
    ('class-frontier-cost82c-receipts-recompute-20261115.json',
     'cost82c_addition'),
    # v6: the canonical line continues through the cost-83a fold
    ('class-frontier-cost83a-receipts-recompute-20261115.json',
     'cost83a_addition'),
    # v7: the canonical line continues through the cost-83b and 83c folds
    ('class-frontier-cost83b-receipts-recompute-20261115.json',
     'cost83b_addition'),
    ('class-frontier-cost83c-receipts-recompute-20261115.json',
     'cost83c_addition'),
    # v8: the canonical line continues through the cost-83d fold
    ('class-frontier-cost83d-receipts-recompute-20261115.json',
     'cost83d_addition'),
]
canon_claims = defaultdict(list)
canon_sum = 0
canon_per_head = []
for cname, ckey in CANONICAL_LINE:
    cd = json.loads((OUT / cname).read_text())
    crecs = []

    def _scan(x):
        if isinstance(x, dict):
            if ('root_hex' in x or 'root' in x or 'roots' in x) \
                    and (hexes_of(x) is not None):
                crecs.append(x)
                return
            for y in x.values():
                _scan(y)
        elif isinstance(x, list):
            for y in x:
                _scan(y)

    _scan(cd[ckey])
    hsum = 0
    for rec in crecs:
        mh = [h for h in (hexes_of(rec) or []) if HEX32.match(h)]
        m = mim_of(rec)
        hsum += m if m is not None else 0
        for h in mh:
            canon_claims[h].append({'head': cname, 'key': ckey,
                                    'bit': rec.get('bit')})
    canon_sum += hsum
    canon_per_head.append({'head': cname, 'key': ckey,
                           'records': len(crecs), 'mim_sum': hsum})
canon_multi = {h: v for h, v in canon_claims.items() if len(v) > 1}
canon_baseline = next(a['baseline_quote'][0] for a in arith
                      if a['head'] == CANONICAL_LINE[0][0])
canon_endpoint = next(a['frontier_solved'] for a in arith
                      if a['head'] == CANONICAL_LINE[-1][0])
assert not canon_multi, sorted(canon_multi)[:5]
assert canon_sum == len(canon_claims), (canon_sum, len(canon_claims))
assert canon_sum == canon_endpoint - canon_baseline, \
    (canon_sum, canon_endpoint, canon_baseline)
canonical_line_report = {
    'baseline_solved': canon_baseline, 'endpoint_solved': canon_endpoint,
    'total_mim': canon_sum, 'distinct_marginal_hexes': len(canon_claims),
    'multi_claims': 0,
    'per_head': canon_per_head,
    'note': 'every manifest hex solved between the 1233 baseline and the '
            '1314 endpoint is claimed as a marginal by exactly one receipt '
            'record on the canonical line (branch marginals 65l/74g/69i '
            'enter once via the merged-1277 merged_receipts; the lane-local '
            '77d head 1299 is off the canonical line and its marginals are '
            'rebased on 1296 by the merged fold, so the bit-78 root - the '
            '75d bit-92 duplicate - is claimed exactly once)',
}

# ---------- 8. 75d endpoint ----------
h77 = json.loads((OUT / 'class-frontier-cost75d-receipts-recompute-20261115.json').read_text())
f77 = h77['frontier_after_cost75d']
endpoint = {
    'head': 'class-frontier-cost75d-receipts-recompute-20261115.json',
    'git_blob_sha': POST70E_PINS['class-frontier-cost75d-receipts-recompute-20261115.json'],
    'solved_s6_in_manifest': f77['solved_s6_in_manifest'],
    'unique_remaining_s6': f77['unique_remaining_s6'],
    'sum_remaining_cost': f77['sum_remaining_cost'],
    's6_needed_by_open_classes': f77['s6_needed_by_open_classes'],
    'cost_needed_by_open_classes': f77['cost_needed_by_open_classes'],
    'receipts': h77['totals']['receipts'],
    'child_closed_by_bit': h77['totals']['child_closed_by_bit'],
}
assert (endpoint['solved_s6_in_manifest'], endpoint['unique_remaining_s6'],
        endpoint['sum_remaining_cost'], endpoint['s6_needed_by_open_classes'],
        endpoint['cost_needed_by_open_classes']) == \
    (1296, 6551, 517468, 4821, 381191), endpoint
assert endpoint['receipts'] == 4 and endpoint['child_closed_by_bit'] == 12
claim = json.loads((OUT / 'class2-lane-cost75d-inflight-20261115.json').read_text())
cf = claim['fold']
assert cf['chain_head_after'] == '1296/6551/517468/4821/381191'
assert cf['receipts_folded'] == 4 and cf['publication_order'] == [12, 40, 92, 111]
# warm-hygiene fact: the bit-92 receipt cross-covers the cost-77 child row
# that the parallel cost-77d sweep has claimed in-flight at head 1290; the
# claim records the row as lost by this fold's target parent
assert cf['parents_lost_rows']['parent1'] == [
    '00000000000040801202000000200000',
    '00000000100000801202000000200000'], cf['parents_lost_rows']
assert cf['parents_after']['parent1'] == '11 rows / 866'
assert cf['output_blob_shas']['head_json'] == endpoint['git_blob_sha']
assert cf['head_json_bytes'] == 8992
sha_claim, blen_claim = git_blob_sha(
    OUT / 'class-frontier-cost75d-receipts-recompute-20261115.json')
assert sha_claim == cf['output_blob_shas']['head_json'] and blen_claim == 8992

# ---------- 8b. v4 bit-78 duplicate-root exactly-once bookkeeping ----------
h77d = json.loads((OUT / 'class-frontier-cost77d-receipts-recompute-20261115.json').read_text())
hm = json.loads((OUT / 'class-frontier-merged-cost75d-77d-receipts-recompute-20261115.json').read_text())
h75d = json.loads((OUT / 'class-frontier-cost75d-receipts-recompute-20261115.json').read_text())
r77d = {r['bit']: r for r in h77d['cost77d_addition']}
rmerged = {r['bit']: r for r in hm['cost77d_addition']}
r75d = {r['bit']: r for r in h75d['cost75d_addition']}
bit78_root = int(r77d[78]['root_hex'], 16)
bit92_root = int(r75d[92]['root_hex'], 16)
assert bit78_root == bit92_root, '77d bit-78 root must be the 75d bit-92 root'
# the merged fold's 11 receipts are exactly the 77d receipts minus bit-78
assert set(rmerged) == set(r77d) - {78}, (sorted(rmerged), sorted(r77d))
assert {int(r['root_hex'], 16) for r in rmerged.values()} \
    == {int(r['root_hex'], 16) for b, r in r77d.items() if b != 78}
# both records' marginals are sequential-publication-order differences
# from the SAME 1290 baseline, so they need not be identical: each fold
# closes its own sweep child first (77d closes its child via bit-7, 75d
# via bit-12), which removes that child from every LATER receipt's marginal
# in the same head. What must hold for the identical root:
#   * the root covers BOTH children's orbits (its deletion orbits include
#     both the 77d child and the 75d child)
#   * each head's child is claimed as a marginal by that head's child-
#     closing receipt, and NOT by the bit-78/bit-92 record
#   * the two records agree on every other manifest marginal
child77 = h77d['target']['s6_child_hex']
child75 = h75d['target']['s6_child_hex']
root_cov = covers(bit78_root)
assert int(child77, 16) in root_cov and int(child75, 16) in root_cov, \
    'the bit-78 root covers both the 77d child and the 75d child orbits'
assert r77d[7]['marginal_in_manifest'] is not None
assert child77 in r77d[7]['marginal_manifest_hexes']
assert child77 not in r77d[78]['marginal_manifest_hexes']
assert child75 in r77d[78]['marginal_manifest_hexes']
assert r75d[12]['marginal_in_manifest'] is not None
assert child75 in r75d[12]['marginal_manifest_hexes']
assert child75 not in r75d[92]['marginal_manifest_hexes']
assert child77 in r75d[92]['marginal_manifest_hexes']
shared78 = sorted(set(r77d[78]['marginal_manifest_hexes'])
                  & set(r75d[92]['marginal_manifest_hexes']))
assert len(shared78) == 1, shared78
assert r77d[78]['marginal_in_manifest'] == r75d[92]['marginal_in_manifest'] == 2
# the canonical line claims the 75d bit-92 marginals once (75d_addition);
# the lane-local 77d head is not on the canonical line, and the merged fold
# excludes bit-78, so the root is claimed exactly once on the canonical line
bit78_claim_sources = {}
for mh in set(r77d[78]['marginal_manifest_hexes']):
    for c in canon_claims[mh]:
        bit78_claim_sources.setdefault((c['head'], c['bit']), set()).add(mh)
# the 77d bit-78 record's two manifest marginals are claimed on the
# canonical line exactly once each, both by the 75d head (the shared hex
# by bit-92, the 75d-child hex by bit-12 - the 75d child closer)
assert sorted(bit78_claim_sources.keys()) == [
    ('class-frontier-cost75d-receipts-recompute-20261115.json', 12),
    ('class-frontier-cost75d-receipts-recompute-20261115.json', 92)], \
    sorted(bit78_claim_sources.keys())
for srcs in bit78_claim_sources.values():
    assert len(srcs) == 1, 'exactly-once on the canonical line'
# root inventory: bit-78 is counted exactly once (it enters through the 75d
# addition; the 77d re-listing is a duplicate, not a new inventory entry)
assert bit78_root in {int(r['root_hex'], 16) for r in r75d.values()}
inv_before_77d = set()
for n in POST70E_ORDER[:POST70E_ORDER.index(
        'class-frontier-cost77d-receipts-recompute-20261115.json')]:
    inv_before_77d |= set(head_roots_all(n))
inv_before_77d |= set(base_int) | set(chain_set)
assert bit78_root in inv_before_77d, 'the bit-78 root is pre-inventoried via 75d'
d77_new = {int(r['root_hex'], 16) for r in r77d.values()} - inv_before_77d
assert len(d77_new) == 11, len(d77_new)
assert bit78_root not in d77_new
bit78_report = {
    'root_hex': r77d[78]['root_hex'],
    'identity': '77d bit-78 root == 75d bit-92 receipt root (raw-hex identical)',
    'marginals_at_1290': 'sequential-order marginals from the same 1290 '
                        'baseline: the records share every manifest marginal '
                        'except that each fold excludes its own sweep child '
                        '(77d closes its child via bit-7 first, 75d via '
                        'bit-12 first); the root covers both child orbits',
    'canonical_line_claims': 'exactly once (75d bit-92); the merged fold '
                             'excludes bit-78 from its receipts',
    'inventory_count': 'exactly once (enters via 75d; the lane-local 77d '
                       're-listing adds 0 new inventory roots)',
    'merged_receipts': '11 == the 77d receipts minus bit-78',
}

# ---------- 8c. 80d endpoint + 79a/80d claim crosschecks ----------
h80 = json.loads((OUT / 'class-frontier-cost80d-receipts-recompute-20261115.json').read_text())
f80 = h80['frontier_after_cost80d']
endpoint80 = {
    'head': 'class-frontier-cost80d-receipts-recompute-20261115.json',
    'git_blob_sha': POST70E_PINS['class-frontier-cost80d-receipts-recompute-20261115.json'],
    'solved_s6_in_manifest': f80['solved_s6_in_manifest'],
    'unique_remaining_s6': f80['unique_remaining_s6'],
    'sum_remaining_cost': f80['sum_remaining_cost'],
    's6_needed_by_open_classes': f80['s6_needed_by_open_classes'],
    'cost_needed_by_open_classes': f80['cost_needed_by_open_classes'],
    'receipts': h80['totals']['receipts'],
    'child_closed_by_bit': h80['totals']['child_closed_by_bit'],
}
assert (endpoint80['solved_s6_in_manifest'], endpoint80['unique_remaining_s6'],
        endpoint80['sum_remaining_cost'], endpoint80['s6_needed_by_open_classes'],
        endpoint80['cost_needed_by_open_classes']) == \
    (1305, 6542, 516793, 4812, 380516), endpoint80
assert endpoint80['receipts'] == 4 and endpoint80['child_closed_by_bit'] == 48
claim80 = json.loads((OUT / 'class2-lane-cost80d-inflight-20261115.json').read_text())
cf80 = claim80['fold']
assert cf80['status'] == 'completed'
assert cf80['chain_head_after'] == '1305/6542/516793/4812/380516'
assert cf80['chain_head_before'] == '1304/6543/516873/4813/380596'
assert cf80['receipts_folded'] == 4 and cf80['publication_order'] == [48, 61, 81, 96]
assert cf80['child_orbit_closed_by_bit'] == 48
assert cf80['output_blob_shas']['head_json'] == endpoint80['git_blob_sha']
assert cf80['head_json_bytes'] == 8033
sha80, blen80 = git_blob_sha(OUT / 'class-frontier-cost80d-receipts-recompute-20261115.json')
assert sha80 == cf80['output_blob_shas']['head_json'] and blen80 == 8033
claim79 = json.loads((OUT / 'class2-lane-cost79a-inflight-20261115.json').read_text())
cf79 = claim79['fold']
assert cf79['chain_head_after'] == '1304/6543/516873/4813/380596'
assert cf79['chain_head_before'] == '1302/6545/517025/4815/380748'
assert cf79['receipts_folded'] == 3 and cf79['publication_order'] == [9, 50, 64]
assert cf79['child_orbit_closed_by_bit'] == 9
assert cf79['output_blob_shas']['head_json'] == \
    POST70E_PINS['class-frontier-cost79a-receipts-recompute-20261115.json']

# ---------- 8d. 82c endpoint + 82c claim crosscheck (v5) ----------
h82c = json.loads((OUT / 'class-frontier-cost82c-receipts-recompute-20261115.json').read_text())
f82c = h82c['frontier_after_cost82c']
endpoint82c = {
    'head': 'class-frontier-cost82c-receipts-recompute-20261115.json',
    'git_blob_sha': POST70E_PINS['class-frontier-cost82c-receipts-recompute-20261115.json'],
    'solved_s6_in_manifest': f82c['solved_s6_in_manifest'],
    'unique_remaining_s6': f82c['unique_remaining_s6'],
    'sum_remaining_cost': f82c['sum_remaining_cost'],
    's6_needed_by_open_classes': f82c['s6_needed_by_open_classes'],
    'cost_needed_by_open_classes': f82c['cost_needed_by_open_classes'],
    'receipts': h82c['totals']['receipts'],
    'child_closed_by_bit': h82c['totals']['child_closed_by_bit'],
}
assert (endpoint82c['solved_s6_in_manifest'], endpoint82c['unique_remaining_s6'],
        endpoint82c['sum_remaining_cost'], endpoint82c['s6_needed_by_open_classes'],
        endpoint82c['cost_needed_by_open_classes']) == \
    (1306, 6541, 516711, 4811, 380434), endpoint82c
assert endpoint82c['receipts'] == 5 and endpoint82c['child_closed_by_bit'] == 16
claim82c = json.loads((OUT / 'class2-lane-cost82c-inflight-20261115.json').read_text())
cf82c = claim82c['fold']
assert cf82c['status'] == 'completed'
assert cf82c['chain_head_after'] == '1306/6541/516711/4811/380434'
assert cf82c['chain_head_before'] == '1305/6542/516793/4812/380516'
assert cf82c['receipts_folded'] == 5 and cf82c['publication_order'] == [16, 37, 47, 71, 82]
assert cf82c['child_orbit_closed_by_bit'] == 16
assert cf82c['total_marginal'] == 21 and cf82c['total_marginal_in_manifest'] == 1
assert cf82c['zero_marginal_in_manifest'] == [37, 47, 71, 82]
assert cf82c['output_blob_shas']['head_json'] == endpoint82c['git_blob_sha']
assert cf82c['head_json_bytes'] == 8587
sha82c, blen82c = git_blob_sha(OUT / 'class-frontier-cost82c-receipts-recompute-20261115.json')
assert sha82c == cf82c['output_blob_shas']['head_json'] and blen82c == 8587

# ---------- 8e. 83a endpoint + 83a claim crosscheck (v6) ----------
h83a = json.loads((OUT / 'class-frontier-cost83a-receipts-recompute-20261115.json').read_text())
f83a = h83a['frontier_after_cost83a']
endpoint83a = {
    'head': 'class-frontier-cost83a-receipts-recompute-20261115.json',
    'git_blob_sha': POST70E_PINS['class-frontier-cost83a-receipts-recompute-20261115.json'],
    'solved_s6_in_manifest': f83a['solved_s6_in_manifest'],
    'unique_remaining_s6': f83a['unique_remaining_s6'],
    'sum_remaining_cost': f83a['sum_remaining_cost'],
    's6_needed_by_open_classes': f83a['s6_needed_by_open_classes'],
    'cost_needed_by_open_classes': f83a['cost_needed_by_open_classes'],
    'receipts': h83a['totals']['receipts'],
    'child_closed_by_bit': h83a['totals']['child_closed_by_bit'],
}
assert (endpoint83a['solved_s6_in_manifest'], endpoint83a['unique_remaining_s6'],
        endpoint83a['sum_remaining_cost'], endpoint83a['s6_needed_by_open_classes'],
        endpoint83a['cost_needed_by_open_classes']) == \
    (1309, 6538, 516477, 4808, 380200), endpoint83a
assert endpoint83a['receipts'] == 4 and endpoint83a['child_closed_by_bit'] == 12
claim83a = json.loads((OUT / 'class2-lane-cost83a-inflight-20261115.json').read_text())
cf83a = claim83a['fold']
assert cf83a['status'] == 'completed'
assert cf83a['chain_head_after'] == '1309/6538/516477/4808/380200'
assert cf83a['chain_head_before'] == '1306/6541/516711/4811/380434'
assert cf83a['receipts_folded'] == 4 and cf83a['publication_order'] == [12, 58, 72, 95]
assert cf83a['child_orbit_closed_by_bit'] == 12
assert cf83a['total_marginal'] == 19 and cf83a['total_marginal_in_manifest'] == 3
assert cf83a['zero_marginal_in_manifest'] == [58, 95]
assert cf83a['output_blob_shas']['head_json'] == endpoint83a['git_blob_sha']
assert cf83a['head_json_bytes'] == 8068
sha83a, blen83a = git_blob_sha(OUT / 'class-frontier-cost83a-receipts-recompute-20261115.json')
assert sha83a == cf83a['output_blob_shas']['head_json'] and blen83a == 8068

# ---------- 8f. 83b endpoint + 83b claim crosscheck (v7) ----------
h83b = json.loads((OUT / 'class-frontier-cost83b-receipts-recompute-20261115.json').read_text())
f83b = h83b['frontier_after_cost83b']
endpoint83b = {
    'head': 'class-frontier-cost83b-receipts-recompute-20261115.json',
    'git_blob_sha': POST70E_PINS['class-frontier-cost83b-receipts-recompute-20261115.json'],
    'solved_s6_in_manifest': f83b['solved_s6_in_manifest'],
    'unique_remaining_s6': f83b['unique_remaining_s6'],
    'sum_remaining_cost': f83b['sum_remaining_cost'],
    's6_needed_by_open_classes': f83b['s6_needed_by_open_classes'],
    'cost_needed_by_open_classes': f83b['cost_needed_by_open_classes'],
    'receipts': h83b['totals']['receipts'],
    'child_closed_by_bit': h83b['totals']['child_closed_by_bit'],
}
assert (endpoint83b['solved_s6_in_manifest'], endpoint83b['unique_remaining_s6'],
        endpoint83b['sum_remaining_cost'], endpoint83b['s6_needed_by_open_classes'],
        endpoint83b['cost_needed_by_open_classes']) == \
    (1312, 6535, 516227, 4805, 379950), endpoint83b
assert endpoint83b['receipts'] == 5 and endpoint83b['child_closed_by_bit'] == 9
claim83b = json.loads((OUT / 'class2-lane-cost83b-inflight-20261115.json').read_text())
cf83b = claim83b['fold']
assert cf83b['status'] == 'completed'
assert cf83b['chain_head_after'] == '1312/6535/516227/4805/379950'
assert cf83b['chain_head_before'] == '1309/6538/516477/4808/380200'
assert cf83b['receipts_folded'] == 5 and cf83b['publication_order'] == [9, 12, 58, 64, 96]
assert cf83b['child_orbit_closed_by_bit'] == 9
assert cf83b['total_marginal'] == 23 and cf83b['total_marginal_in_manifest'] == 3
assert cf83b['zero_marginal_in_manifest'] == [58, 64, 96]
assert cf83b['output_blob_shas']['head_json'] == endpoint83b['git_blob_sha']
assert cf83b['head_json_bytes'] == 8651
sha83b, blen83b = git_blob_sha(OUT / 'class-frontier-cost83b-receipts-recompute-20261115.json')
assert sha83b == cf83b['output_blob_shas']['head_json'] and blen83b == 8651

# ---------- 8g. 83c endpoint + 83c claim crosscheck (v7) ----------
h83c = json.loads((OUT / 'class-frontier-cost83c-receipts-recompute-20261115.json').read_text())
f83c = h83c['frontier_after_cost83c']
endpoint83c = {
    'head': 'class-frontier-cost83c-receipts-recompute-20261115.json',
    'git_blob_sha': POST70E_PINS['class-frontier-cost83c-receipts-recompute-20261115.json'],
    'solved_s6_in_manifest': f83c['solved_s6_in_manifest'],
    'unique_remaining_s6': f83c['unique_remaining_s6'],
    'sum_remaining_cost': f83c['sum_remaining_cost'],
    's6_needed_by_open_classes': f83c['s6_needed_by_open_classes'],
    'cost_needed_by_open_classes': f83c['cost_needed_by_open_classes'],
    'receipts': h83c['totals']['receipts'],
    'child_closed_by_bit': h83c['totals']['child_closed_by_bit'],
}
assert (endpoint83c['solved_s6_in_manifest'], endpoint83c['unique_remaining_s6'],
        endpoint83c['sum_remaining_cost'], endpoint83c['s6_needed_by_open_classes'],
        endpoint83c['cost_needed_by_open_classes']) == \
    (1313, 6534, 516144, 4804, 379867), endpoint83c
assert endpoint83c['receipts'] == 2 and endpoint83c['child_closed_by_bit'] == 16
claim83c = json.loads((OUT / 'class2-lane-cost83c-inflight-20261115.json').read_text())
cf83c = claim83c['fold']
assert cf83c['status'] == 'completed'
assert cf83c['chain_head_after'] == '1313/6534/516144/4804/379867'
assert cf83c['chain_head_before'] == '1312/6535/516227/4805/379950'
assert cf83c['receipts_folded'] == 2 and cf83c['publication_order'] == [16, 82]
assert cf83c['child_orbit_closed_by_bit'] == 16
assert cf83c['total_marginal'] == 9 and cf83c['total_marginal_in_manifest'] == 1
assert cf83c['zero_marginal_in_manifest'] == [82]
assert cf83c['output_blob_shas']['head_json'] == endpoint83c['git_blob_sha']
assert cf83c['head_json_bytes'] == 6811
sha83c, blen83c = git_blob_sha(OUT / 'class-frontier-cost83c-receipts-recompute-20261115.json')
assert sha83c == cf83c['output_blob_shas']['head_json'] and blen83c == 6811

# ---------- 8h. 83d endpoint + 83d claim crosscheck (v8) ----------
h83d = json.loads((OUT / 'class-frontier-cost83d-receipts-recompute-20261115.json').read_text())
f83d = h83d['frontier_after_cost83d']
endpoint83d = {
    'head': 'class-frontier-cost83d-receipts-recompute-20261115.json',
    'git_blob_sha': POST70E_PINS['class-frontier-cost83d-receipts-recompute-20261115.json'],
    'solved_s6_in_manifest': f83d['solved_s6_in_manifest'],
    'unique_remaining_s6': f83d['unique_remaining_s6'],
    'sum_remaining_cost': f83d['sum_remaining_cost'],
    's6_needed_by_open_classes': f83d['s6_needed_by_open_classes'],
    'cost_needed_by_open_classes': f83d['cost_needed_by_open_classes'],
    'receipts': h83d['totals']['receipts'],
    'child_closed_by_bit': h83d['totals']['child_closed_by_bit'],
}
assert (endpoint83d['solved_s6_in_manifest'], endpoint83d['unique_remaining_s6'],
        endpoint83d['sum_remaining_cost'], endpoint83d['s6_needed_by_open_classes'],
        endpoint83d['cost_needed_by_open_classes']) == \
    (1314, 6533, 516061, 4803, 379784), endpoint83d
assert endpoint83d['receipts'] == 3 and endpoint83d['child_closed_by_bit'] == 16
claim83d = json.loads((OUT / 'class2-lane-cost83d-inflight-20261115.json').read_text())
cf83d = claim83d['fold']
assert cf83d['status'] == 'completed'
assert cf83d['chain_head_after'] == '1314/6533/516061/4803/379784'
assert cf83d['chain_head_before'] == '1313/6534/516144/4804/379867'
assert cf83d['receipts_folded'] == 3 and cf83d['publication_order'] == [16, 51, 82]
assert cf83d['child_orbit_closed_by_bit'] == 16
assert cf83d['total_marginal'] == 13 and cf83d['total_marginal_in_manifest'] == 1
assert cf83d['zero_marginal_in_manifest'] == [51, 82]
assert cf83d['output_blob_shas']['head_json'] == endpoint83d['git_blob_sha']
assert cf83d['head_json_bytes'] == 7407
sha83d, blen83d = git_blob_sha(OUT / 'class-frontier-cost83d-receipts-recompute-20261115.json')
assert sha83d == cf83d['output_blob_shas']['head_json'] and blen83d == 7407

# ---------- output ----------
result = {
    'schema': 'n11-class2-lane-published-chain-roots-second-independent-audit-20261115-v8',
    'date': '2026-11-15',
    'verdict': 'AUDIT PASSED',
    'method': 'independent whole-chain audit over the published files only '
              '(no runpy chain replay, no solved-set reconstruction): 100 git '
              'blob pins asserted byte-exact (26 base certificate files + 52 '
              'pre-70e chain head JSONs + 22 pinned post-70e chain heads '
              'through the 83d endpoint), '
              'the root inventory rebuilt from the published records (194 '
              'distinct WIN7 base roots with the single intra-base duplicate '
              'root enumerated, 402 distinct receipt roots from the 52 chain '
              'head addition records, 104 base-roots re-listed by chain '
              'records), the cumulative published-root inventory reconciled '
              'at every post-70e checkpoint against each fold script\u2019s '
              'own published folded-root count (497@1233, 499@71c, 503@70f, '
              '512@72c, 520@73g, 528@70g, 532@73h, 534@65l / 542@74g / '
              '546@69i branch lines, 544@merged-65l-74g, 548@merged-65l-74g-'
              '69i, 550@76b, 553@77a, 557@77b, 565@77c, 569@75d, '
              '577@77d lane-local, 580@merged-75d-77d, 583@79a, 587@80d, '
              '592@82c, 596@83a, 601@83b, 603@83c, 606@83d), the D4 orbit structure of the '
              'full inventory '
              'audited (v8: full 606-root '
              'D4 orbits; 11 twin pairs with full provenance; the 16 roots '
              'added by the 77b/77c/75d folds plus the 5+4+5+2+3 roots added '
              'by the 82c/83a/83b/83c/83d folds are D4-disjoint from the prior '
              'inventory and pairwise orbit-distinct); multi-provenance roots '
              'enumerated), per-record geometry checked for every published '
              'receipt record and every nested group-additions record, '
              'child-orbit closure bookkeeping checked at every head '
              'declaring a child, convention-external receipts scanned (each '
              'must be a D4 twin of an inventoried orbit, keeping the orbit '
              'inventory complete as a SET), the head arithmetic re-derived '
              'from the published marginal records with zero anomalies, and '
              'the 75d / 80d / 82c / 83a / 83b / 83c / 83d endpoint heads and their '
              'completed claim fold records cross-checked byte-exact',
    'controls': {
        'pins_checked': n_pins,
        'pin_groups': pin_report,
        'unpinned_post70e_heads_computed_blob_shas': unpinned_computed,
        'base_roots': {'files': 26, 'raw_listings': len(base_raw),
                       'distinct': len(base_set),
                       'intra_base_duplicates': intra_base_duplicates},
        'chain_head_roots': {'heads': 52, 'distinct': len(chain_set),
                             'overlap_with_base': len(overlap_base_chain)},
        'inventory_at_1233': 497,
        'cumulative_by_post70e_head': cumulative_report,
        'd4_orbits': {'roots': len(all_roots), 'orbits': n_orbits,
                      'twin_pairs': len(twin_pairs),
                      'twin_analysis': twin_analysis,
                      'multi_provenance_roots': multi_prov},
        'per_record_geometry': {'receipt_records': n_receipt_records,
                                'group_records': n_group_records,
                                'anomalies': geom_anomalies,
                                'published_hex_errata': hex_errata},
        'child_closure': child_closure_report,
        'convention_external_receipts': convention_external,
        'head_arithmetic': {'heads_classified': len(arith),
                            'heads': arith,
                            'classification_counts': dict(Counter(
                                a['classification'] for a in arith)),
                            'quote_status_counts': dict(Counter(
                                a['quote_status'] for a in arith)),
                            'quote_errata': quote_errata,
                            'pointer_name_differs_cases': pointer_differs,
                            'anomalies': arith_anomalies},
        'fork_merge_head': fork_entry,
        'canonical_line_hex_exactly_once': canonical_line_report,
        'endpoint_75d': endpoint,
        'endpoint_80d': endpoint80,
        'endpoint_82c': endpoint82c,
        'claim_80d_crosscheck': 'completed 80d claim fold record matches the '
                                'published 80d head JSON byte-exact (blob '
                                'sha + 8033 bytes) and the published head '
                                'transition 1304/6543/516873/4813/380596 -> '
                                '1305/6542/516793/4812/380516 (receipts '
                                '[48, 61, 81, 96], child closed by bit-48, '
                                'second target S5 10/787 -> 9/707)',
        'claim_79a_crosscheck': 'completed 79a claim fold record matches the '
                                'published 79a head JSON (blob sha pinned) '
                                'and the head transition 1302 -> 1304 '
                                '(receipts [9, 50, 64], child closed by bit-9)',
        'claim_82c_crosscheck': 'completed 82c claim fold record matches the '
                                'published 82c head JSON byte-exact (blob '
                                'sha + 8587 bytes) and the published head '
                                'transition 1305/6542/516793/4812/380516 -> '
                                '1306/6541/516711/4811/380434 (receipts '
                                '[16, 37, 47, 71, 82], child closed by '
                                'bit-16, second target S5 9/707 -> 8/625, '
                                'totals marginal 21 / in-manifest 1, '
                                'zero-mim [37, 47, 71, 82]), also covered '
                                'by the same-day second independent '
                                'verification JSON',
        'endpoint_83a': endpoint83a,
        'claim_83a_crosscheck': 'completed 83a claim fold record matches the '
                                'published 83a head JSON byte-exact (blob '
                                'sha + 8068 bytes) and the published head '
                                'transition 1306/6541/516711/4811/380434 -> '
                                '1309/6538/516477/4808/380200 (receipts '
                                '[12, 58, 72, 95], child closed by bit-12, '
                                'second target S5 8/625 -> 7/542, totals '
                                'marginal 19 / in-manifest 3, zero-mim '
                                '[58, 95]), also covered by the same-day '
                                'second independent verification and mirror '
                                'replication JSONs',
        'endpoint_83b': endpoint83b,
        'claim_83b_crosscheck': 'completed 83b claim fold record matches the '
                                'published 83b head JSON byte-exact (blob '
                                'sha + 8651 bytes) and the published head '
                                'transition 1309/6538/516477/4808/380200 -> '
                                '1312/6535/516227/4805/379950 (receipts '
                                '[9, 12, 58, 64, 96], child closed by bit-9, '
                                'second target S5 7/542 -> 6/459, totals '
                                'marginal 23 / in-manifest 3, zero-mim '
                                '[58, 64, 96]), also covered by the same-day '
                                'second independent verification JSON',
        'endpoint_83c': endpoint83c,
        'claim_83c_crosscheck': 'completed 83c claim fold record matches the '
                                'published 83c head JSON byte-exact (blob '
                                'sha + 6811 bytes) and the published head '
                                'transition 1312/6535/516227/4805/379950 -> '
                                '1313/6534/516144/4804/379867 (receipts '
                                '[16, 82], child closed by bit-16, second '
                                'target S5 6/459 -> 5/376, totals marginal '
                                '9 / in-manifest 1, zero-mim [82]), also '
                                'covered by the same-day second independent '
                                'verification JSON',
        'endpoint_83d': endpoint83d,
        'claim_83d_crosscheck': 'completed 83d claim fold record matches the '
                                'published 83d head JSON byte-exact (blob '
                                'sha + 7407 bytes) and the published head '
                                'transition 1313/6534/516144/4804/379867 -> '
                                '1314/6533/516061/4803/379784 (receipts '
                                '[16, 51, 82], child closed by bit-16, second '
                                'target S5 5/376 -> 4/293, totals marginal '
                                '13 / in-manifest 1, zero-mim [51, 82]), '
                                'also covered by the same-day second '
                                'independent verification JSON',
        'bit78_duplicate_root_bookkeeping': bit78_report,
        'claim_75d_crosscheck': 'completed claim fold record matches the '
                                 'published 75d head JSON byte-exact (blob '
                                 'sha + 8992 bytes) and the published head '
                                 'transition 1290/6557/517923/4827/381646 -> '
                                 '1296/6551/517468/4821/381191; the claim '
                                 'records the target parent losing both the '
                                 'cost-75 child row and the cost-77 child '
                                 'row (bit-92 cross-cover), so the parallel '
                                 'cost-77d fold must follow the warm-hygiene '
                                 'pattern (cost-70g precedent)',
        'v1_supersession': 'the first published audit (v1, endpoint 77a, 88 '
                           'pins, 553 roots) remains published unchanged '
                           'as class2-lane-published-chain-roots-independent-'
                           'audit-20261115.json; the v2 output subsumed it at '
                           'the 75d endpoint (91 pins, 569 roots); the v4 '
                           'output extended the pinned chain to the 80d '
                           'endpoint (95 pins, 587 roots, 17 post-70e '
                           'heads, canonical-line exactly-once extended '
                           'to 1305); the v5 output extended it to the 82c '
                           'endpoint (96 pins, 592 roots, 18 post-70e '
                           'heads, canonical-line exactly-once extended '
                           'to 1306); the v6 output extended it to the 83a '
                           'endpoint (97 pins, 596 roots, 19 post-70e '
                           'heads, canonical-line exactly-once extended '
                           'to 1309); the v7 output extended it to the 83c '
                           'endpoint (99 pins, 603 roots, 21 post-70e '
                           'heads, canonical-line exactly-once extended '
                           'to 1313); this v8 output extends it to the 83d '
                           'endpoint (100 pins, 606 roots, 22 post-70e '
                           'heads, canonical-line exactly-once extended '
                           'to 1314)',
    },
    'interpretation_guard': 'bookkeeping audit over published receipts and '
                            'head records only; solved counts measure '
                            'manifest coverage, not the game-theoretic value '
                            'of any position; WIN7 certificates prove a win '
                            'within depth 10 from the individual 7-stone '
                            'roots only; nothing in this audit decides any '
                            'S5 parent, any class, the two-stone root {49,60} '
                            'or the 11x11 empty board: 11x11 empty board / '
                            'two-stone root {49,60} / S2 {59,60} / class 1 / '
                            'class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class2-lane-published-chain-roots-second-independent-audit-v8-20261115.json').write_text(
    json.dumps(result, indent=1, sort_keys=True) + '\n')
assert not geom_anomalies, geom_anomalies
print('AUDIT PASSED')
print('published hex errata: %d' % len(hex_errata))
print('pins %d (base %d, chain %d, post70e %d)' % (
    n_pins, pin_report['base'], pin_report['chain'], pin_report['post70e']))
print('base roots distinct %d (dup %s), chain distinct %d, overlap %d' % (
    len(base_set), [d['root'] for d in intra_base_duplicates],
    len(chain_set), len(overlap_base_chain)))
print('cumulative inventory @83d: %d roots / %d D4 orbits / %d twin pairs' % (
    len(all_roots), n_orbits, len(twin_pairs)))
print('receipt records %d, group records %d, geometry anomalies %d' % (
    n_receipt_records, n_group_records, len(geom_anomalies)))
print('convention-external receipts: %d' % len(convention_external))
print('arith heads %d, anomalies %d, quote errata %d, pointer-differs %d' % (
    len(arith), len(arith_anomalies), len(quote_errata), len(pointer_differs)))
print('child-closure heads: %d' % len(child_closure_report))
print('canonical line %d..%d: mim %d / distinct %d / multi 0 (exactly-once)' % (
    canonical_line_report['baseline_solved'],
    canonical_line_report['endpoint_solved'],
    canonical_line_report['total_mim'],
    canonical_line_report['distinct_marginal_hexes']))
