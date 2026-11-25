#!/usr/bin/env python3
"""Class-2 frontier recomputation folding the class2-lane cost-70e WIN7
receipts (5 WIN7-D10 bits 0, 8, 24, 66, 79 of the cheapest remaining
unswept child 00000000000000801202000000200004, edge cost 70, dual class-2
demand c1=0,c2=2,c4=0 - the child is a remaining row of both open class-2
parents: the second coverable class-2 target S5
00000000000000801202000000200000 at 31 rows / 2334 and the open class-2 S5
00000000000000003800000008400000 at 49 rows / 3625) on top of the merged
cost-78a+69h chain head (solved 1227, 2026-11-15).

Baseline method (this fold): instead of replaying the whole runpy chain of
fold scripts (which regenerates every intermediate head byte-identically
but is heavy), the canonical 1227 head is reconstructed independently from
published artifacts only: every published input file (28 base inputs + 52
published frontier head JSONs + the cost-70e lane files) is asserted
byte-exact against main by git blob sha, then the solved set is rebuilt by
pure geometry as winners UNION covers(12 baseline verified certificate
files) UNION covers(class4 batch1/batch2/batch3) UNION covers(7 class2
lane certificate files) UNION covers(all receipt roots recorded in the 52
blob-verified head JSON addition records). Staged controls reproduce the
published 638 / 657 / 665 / 814 intermediate frontiers exactly; the final
control is byte-identical regeneration of the published merged-head
ranking and top-candidates CSVs (git blob 4eeca615 / 0f9905fc, identical
to the cost-69h-receipts CSVs) from the reconstructed state, which pins
every remaining S5 orbit's row set, count and cost, plus the histogram and
parent-row equality with the published merged head JSON (blob 294c4ed3,
equal-numbered to the parallel-rebased cost-69h head JSON blob d25eb3a0).

The cost-70e child orbit 00000000000000801202000000200004 is genuinely
remaining at the 1227 head (a remaining row of both open class-2 parents)
and is closed by this fold itself, by the bit-0 receipt (the first in
published order; all five roots cover the child via deleting their own
added stone).

This script:
1. verifies every published input byte-exact against main by git blob
   sha (28 base inputs, 52 head JSONs, 4 published CSVs, the cost-70e
   sweep audit / claim v2 / certificate manifest / third independent
   audit, 9 raw sweep batches, the v16 determinism rerun, the v15
   cross-engine check, 10 certificate parts + 5 whole certificates, and
   the two cost-70e scripts);
2. reconstructs the 1227 head by pure geometry with staged controls and
   regenerates the published merged-head CSVs byte-identically;
3. asserts the child genuinely remaining at 1227 (both open class-2
   parents at 31/2334 and 49/3625 holding the child row, the child held
   by exactly these two open parents, child unsolved in-manifest, demand
   c1=0,c2=2,c4=0 re-derived, lift stones 2 against parent1 and 21
   against the second class-2 parent, D4 one-stone lift controls);
4. re-derives the published sweep audit from the nine raw batch JSONLs:
   per-batch candidate bits in order, pilot 3402 controls, 70 candidates
   exactly once (== claim enumeration), 5 WIN7-D10 / 65 REFUTED / 0
   capped, node sum 83,656,928 (win sum 11,657,011), win roots ==
   child | 1<<bit, 5 distinct D4 orbits, terminal range 13..17, batch-5
   determinism rerun node-exact;
5. asserts the v15 cross-engine anchors (5 WIN loss=true node-matched to
   the certificate manifest, sum 27,246,682, refuted anchors bits
   75/86/113 loss=false with raw verdict agreement, pilots 5949 x2);
6. asserts all five published certificates against the local certificate
   bytes (all bits split 2 parts: parts-join-whole, md5, sha256, git blob
   shas, rows sorted-unique, header, root identity, sub-roots == loser
   mobility == len(loser_first_moves) == 60/63/56/49/52, terminal 13..17,
   fbt_drops 0, d4_canonical_hex == canon(root), d4 parent orbits
   canon-invariant, equal to the chain covers() orbit sets and each
   containing the child, v15 anchor node match, v16 sweep node match,
   BigInt verifier union 0/0) and the manifest totals re-summed
   (236,784 rows / 8,564,174 bytes / 20,246,025 extraction nodes / 280
   sub-roots);
7. cross-checks the published third independent exact-geometry
   certificate audit (status PASS, per-certificate rows / mobility /
   terminal ranges / parent orbits equal to this chain's covers() orbit
   sets, shared parent orbit == the child, worklist parents covered by
   the right receipt, proven_win [0, 8, 24, 66, 79]);
8. asserts the 5 roots are disjoint from every root whose covers
   contributed to the 1227 head (12 baseline verified files + class4
   batch1/2/3 + 8 lane certificate files + the 402 distinct chain roots)
   both raw-hex and D4-canonically, and mutually distinct D4;
9. folds the 5 receipts in published bit order [0, 8, 24, 66, 79],
   re-deriving every per-record marginal from the growing union, with
   the child-orbit closure control (bit0), the
   both-open-parents-lose-the-child-row control, a set-equality control
   s_after == s_1227 UNION covers(5 roots) and a reverse-order replay
   control;
10. produces the after-cost-70e frontier + ranking CSV + top-candidates
    CSV.

Receipts only - no sweep claims are made here. In-flight sweeps of
parallel lanes (cost-65l receipts, class4-82b, five-row-q7 and others)
are not folded by this script; the next fold must re-fetch latest main,
re-assert the canonical chain head and rebase on it.
"""
import csv, gzip, hashlib, io, json, re
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'
CERTS = OUT / 'class2-lane-cost70e-certificates'
MS5 = HERE.parent / 'n11-s2-5960-milestone5-20261112' / 'output'

def git_blob_sha(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()

# ---------- geometry (verbatim) ----------
def images(mask):
    result = [0] * 8
    for p in range(121):
        if mask >> p & 1:
            x, y = p % 11, p // 11
            coords = ((x,y), (y,10-x), (10-x,10-y), (10-y,x),
                      (10-x,y), (x,10-y), (y,x), (10-y,10-x))
            for i, (a,b) in enumerate(coords):
                result[i] |= 1 << (11*b+a)
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

# ---------- 1. published inputs byte-exact against main ----------
BASE_BLOBS = {
    'win7-reuse-hits.csv.gz': '9fdad0e922c00af813c5c398277f2bddaa3283cd',
    's5-remaining-after-reuse.csv.gz': '953eec41cab43f19849f31e5879cf5de932d9d3f',
    's5-s6-remaining-incidences.csv.gz': '7f0d7f4ab87585515d67a393464b2472e5171001',
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
CHAIN_HEADS = {
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
EXTRA_BLOBS = {
    # the merged-head CSVs and the cost-69h-receipts CSVs are byte-identical
    # files (same git blobs): one regeneration pins all four
    'class-frontier-s5-ranking-after-merged-cost78a-69h-20261115.csv': '4eeca6155838169050804eb31a34db4a0681ec05',
    'class-frontier-top-candidates-s6-after-merged-cost78a-69h-20261115.csv': '0f9905fcb9190cbbda3b6581466b50373308fe60',
    'class-frontier-s5-ranking-after-cost69h-receipts-20261115.csv': '4eeca6155838169050804eb31a34db4a0681ec05',
    'class-frontier-top-candidates-s6-after-cost69h-receipts-20261115.csv': '0f9905fcb9190cbbda3b6581466b50373308fe60',
    'class2-lane-cost70e-sweep-audit-20261115.json': '47d38c00264aae84551eaaf994a10c134ff2f60f',
    'class2-lane-cost70e-win7-certificates-20261115.json': '9f8e5a93562ea9f1ca61ee096d5064b07b782b87',
    'class2-lane-cost70e-inflight-20261115.json': '9c27cff582e84159aace369b60cfe4543e788bbf',  # v3 retired claim (v2 b857b635 is history)
    'cost70e-third-independent-certificate-audit-20261115.json': '6727eb651e2ee6b978c24a7d0e898333d632e127',
}
RAW_BLOBS = {
    'class2-lane-cost70e-raw-batch1-20261115.jsonl': 'a2f65981e993c340ca7e108f4707541ebf802dc9',
    'class2-lane-cost70e-raw-batch2-20261115.jsonl': 'a83fb33729ef07fb6179c228f75509eba97d960f',
    'class2-lane-cost70e-raw-batch3-20261115.jsonl': '91eaf9a635ff0203d2dc0d60f1b750c7d32e108e',
    'class2-lane-cost70e-raw-batch4-20261115.jsonl': '1e653a5c7af0d1fbc29bc060163f7edfe35b9ce5',
    'class2-lane-cost70e-raw-batch5-20261115.jsonl': 'b15c573b0873980fed697c400b44c2efd76d5193',
    'class2-lane-cost70e-raw-batch6-20261115.jsonl': '7fc8be4a980415a652c3c9ced837b7728bc58fb2',
    'class2-lane-cost70e-raw-batch7-20261115.jsonl': 'c4a20622d60d0db85094f85e541a181f325fa212',
    'class2-lane-cost70e-raw-batch8-20261115.jsonl': '768d6f5f50bb9e717ba71089d8e1af14bdc94649',
    'class2-lane-cost70e-raw-batch9-20261115.jsonl': '9b121af5928b349073e76c32a4f666e539ae57b9',
    'class2-lane-cost70e-v16-determinism-rerun-20261115.jsonl': '58869e043ac22c35d9ae1ad91397d2fc5c05519c',
    'class2-lane-cost70e-v15-crosscheck-20261115.jsonl': '7ca1f1319ca90beaa3fac28343c907ede238b6d0',
}
CERT_FILE_BLOBS = {
    'bit0-root-00000000000000801202000000200005.cert': 'c7facf8387835264615662fca95f36aef7263282',
    'bit0-root-00000000000000801202000000200005.cert.part1of2': '38dc49aafd1113d43e6f03d068d6444fdbbbdd97',
    'bit0-root-00000000000000801202000000200005.cert.part2of2': '1ca00ce2d035cde69f539bc4a37a0c3c5338cbcd',
    'bit24-root-00000000000000801202000001200004.cert': 'bb7c60f0c47d46a21c4d019015d996f97255c84c',
    'bit24-root-00000000000000801202000001200004.cert.part1of2': '243590408eeccec444f616f27b184493d9fb694d',
    'bit24-root-00000000000000801202000001200004.cert.part2of2': '21eea0742337d3b41ab20fda5ff2eafdfa0e408e',
    'bit66-root-00000000000000841202000000200004.cert': 'a153e127511ab130a050e0b903878bd68f4de3b8',
    'bit66-root-00000000000000841202000000200004.cert.part1of2': '356bba6d29a980e5787e47fe87ff28841fd21994',
    'bit66-root-00000000000000841202000000200004.cert.part2of2': 'de75100b1cb970592dcde62c13eac51c08aef26e',
    'bit79-root-00000000000080801202000000200004.cert': 'f9589110897c745dd547119240514680f0afd938',
    'bit79-root-00000000000080801202000000200004.cert.part1of2': '97dbce6f3d96c92e46f7761e536bdcc8bc753847',
    'bit79-root-00000000000080801202000000200004.cert.part2of2': '793daa26e1322febd36dfa4973ec34574e2715eb',
    'bit8-root-00000000000000801202000000200104.cert': 'db704bb5baf17371972475dc80236755059ef7ee',
    'bit8-root-00000000000000801202000000200104.cert.part1of2': '04d7ddbb502bf3489abd40cc644bef0a89cc672a',
    'bit8-root-00000000000000801202000000200104.cert.part2of2': 'c45d058decb340a669bf299758ad9a7efce64c6b',
}
SCRIPT_BLOBS = {
    'cert_driver70e.ts': '085fe754404f2df3abe8affc50a53e03395f8d7d',
    'audit_cost70e_certificates_third_independent_20261115.mjs': '0b4b9a5094a63594d525079b1218d206425853ba',
}
assert len(BASE_BLOBS) == 29 and len(CHAIN_HEADS) == 52 and len(EXTRA_BLOBS) == 8
assert len(RAW_BLOBS) == 11 and len(CERT_FILE_BLOBS) == 15 and len(SCRIPT_BLOBS) == 2
n_verified = 0
for blobs, sub in ((BASE_BLOBS, OUT), (CHAIN_HEADS, OUT), (EXTRA_BLOBS, OUT),
                  (RAW_BLOBS, OUT), (CERT_FILE_BLOBS, CERTS),
                  (SCRIPT_BLOBS, HERE / 'scripts')):
    for name, want in blobs.items():
        assert git_blob_sha(sub / name) == want, name
        n_verified += 1
print('CONTROL %d published input files byte-exact against main by git '
      'blob sha (28 base inputs + 52 head JSONs incl. the merged head + 4 '
      'CSVs + 4 cost-70e records + 11 raw JSONLs + 15 certificate files '
      '+ 2 scripts)'
      % n_verified)

# ---------- 2. reconstruct the 1227 head by pure geometry ----------
BASELINE_VERIFIED = (
    'priority-certificates-verified.json',
    'class2-certificates-verified.json',
    'class2-next-certificates-verified.json',
    'class2-next2-certificates-verified.json',
    'class2-next3-certificates-verified.json',
    'class2-next4-certificates-verified.json',
    'class2-batch5-certificates-verified.json',
    'class2-batch3-certificates-verified.json',
    'class2-batch2-certificates-verified.json',
    'class2-batch2b-certificates-verified.json',
    'class2-batch1-certificates-verified.json',
    'class2-batch1b-certificates-verified.json',
)
LOSS6 = (
    '00000000000000809202000400000000',
    '00000000000000003800004008000008',
    '00000000000000805202000000002000',
)

winners = set()
with gzip.open(OUT / 'win7-reuse-hits.csv.gz', 'rt', newline='') as f:
    for row in csv.DictReader(f):
        winners.add(int(row['s6_hex'], 16))

def roots_of(name):
    return [int(rec['root'], 16) for rec in
            json.loads((OUT / name).read_text())['certificates']
            if rec.get('verdict') == 'WIN7']

batch1 = roots_of('class4-batch1-certificates-verified.json')
batch2 = roots_of('class4-batch2-certificates-verified.json')
bit37 = int(json.loads((OUT / 'class4-batch3-bit37-certificate.json').read_text())['root_hex'], 16)
child34 = [int(c['root'], 16) for c in
           json.loads((OUT / 'class4-batch3-win7-certificates-20261114.json').read_text())['certificates']]
child5 = [int(c['root'], 16) for c in
          json.loads((OUT / 'class4-batch3-win7-certificates-child5-20261114.json').read_text())['certificates']]
child7 = [int(c['root_hex'], 16) for c in
          json.loads((OUT / 'class4-batch3-win7-certificates-child7-20261114.json').read_text())['certificates']]
LANE_FILES = (
    'class2-lane-cost60-win7-certificates-20261114.json',
    'class2-lane-cost61-win7-certificates-20261114.json',
    'class2-lane-cost61b-win7-certificates-20261114.json',
    'class2-lane-cost64-win7-certificates-20261114.json',
    'class2-lane-cost65-win7-certificates-20261114.json',
    'class2-lane-cost68-win7-certificates-20261114.json',
    'class2-lane-cost58-win7-certificates-20261114.json',
    'class2-lane-cost75-win7-certificates-20261114.json',
)

manifest = set()
for path in sorted(MS5.glob('ms5_s6_manifest_part*.csv')):
    with path.open(newline='') as f:
        manifest.update(int(row['hex'], 16) for row in csv.DictReader(f))
classes = {}
with gzip.open(OUT / 's5-remaining-after-reuse.csv.gz', 'rt', newline='') as f:
    for row in csv.DictReader(f):
        classes[row['s5_hex']] = int(row['classes'])
incidences = []
with gzip.open(OUT / 's5-s6-remaining-incidences.csv.gz', 'rt', newline='') as f:
    incidences = list(csv.DictReader(f))
print('inputs: %d incidences, %d winners, %d classes, %d manifest'
      % (len(incidences), len(winners), len(classes), len(manifest)))

loss = {int(x, 16) for x in LOSS6}
rejected = {r['s5_hex'] for r in incidences if int(r['s6_hex'], 16) in loss}

def frontier(solved):
    remaining = defaultdict(list)
    for row in incidences:
        if row['s5_hex'] not in rejected and int(row['s6_hex'], 16) not in solved:
            remaining[row['s5_hex']].append(row)
    unique = {r['s6_hex']: int(r['s6_s7_edge_cost'])
              for rows in remaining.values() for r in rows}
    demand = defaultdict(lambda: {'c1': 0, 'c2': 0, 'c4': 0})
    for s5, rows in remaining.items():
        bits = classes.get(s5, 0)
        for row in rows:
            d = demand[row['s6_hex']]
            if bits & 1: d['c1'] += 1
            if bits & 2: d['c2'] += 1
            if bits & 4: d['c4'] += 1
    open_only = {k: v for k, v in demand.items() if v['c1'] == 0}
    return remaining, unique, demand, open_only

def summary_state(solved):
    remaining, unique, demand, open_only = frontier(solved)
    hist = defaultdict(int)
    for v in open_only.values():
        hist[f"c2={v['c2']},c4={v['c4']}"] += 1
    state = {
        'solved_s6_in_manifest': len(solved & manifest),
        'remaining_s5_orbits': len(remaining),
        'unique_remaining_s6': len(unique),
        'sum_remaining_cost': sum(unique.values()),
        's6_needed_by_open_classes': len(open_only),
        'cost_needed_by_open_classes': sum(int(unique[k]) for k in open_only),
        'hist': dict(sorted(hist.items())),
    }
    return state, remaining, unique, demand

# staged controls (published intermediate frontiers)
s0 = set(winners)
for name in BASELINE_VERIFIED:
    for r in roots_of(name):
        s0 |= covers(r)
st0, _, _, _ = summary_state(s0)
assert st0['solved_s6_in_manifest'] == 638 and st0['unique_remaining_s6'] == 7208
assert st0['sum_remaining_cost'] == 565500
s1 = s0 | set().union(*(covers(r) for r in batch1))
st1, _, _, _ = summary_state(s1)
assert st1['solved_s6_in_manifest'] == 657 and st1['unique_remaining_s6'] == 7189
assert st1['sum_remaining_cost'] == 564070
s2 = s1 | set().union(*(covers(r) for r in batch2))
st2, _, _, _ = summary_state(s2)
assert st2['solved_s6_in_manifest'] == 665 and st2['unique_remaining_s6'] == 7181
assert st2['sum_remaining_cost'] == 563509
assert st2['s6_needed_by_open_classes'] == 5398
assert st2['cost_needed_by_open_classes'] == 423516
b37 = json.loads((OUT / 'class4-batch3-bit37-certificate.json').read_text())
assert set(int(h, 16) for h in b37['frontier_effect']['covers_canonical_s6']) == covers(bit37)
s3 = s2 | set().union(*(covers(r) for r in [bit37] + child34 + child5 + child7))
s10 = set(s3)
for n in LANE_FILES[:7]:
    s10 |= set().union(*(covers(r) for r in roots_of(n)))
st10, _, _, _ = summary_state(s10)
assert (st10['solved_s6_in_manifest'], st10['unique_remaining_s6'],
        st10['sum_remaining_cost'], st10['s6_needed_by_open_classes'],
        st10['cost_needed_by_open_classes']) == (814, 7032, 552811, 5256, 413283)
print('CONTROL staged controls reproduced: baseline 638/7208/565500, '
      'after_batch1 657/7189/564070, after_batch2 665/7181/563509 '
      '(open 5398/423516), bit37 covers == published frontier_effect, '
      'after class4 batch3 + lanes through cost-58: 814/7032/552811/5256/413283')

# chain roots: every receipt root recorded in the 52 blob-verified head
# JSON addition records (addition / merged_receipts / group_additions)
HEX32 = re.compile(r'^[0-9a-f]{32}$')

def collect_addition_roots(v, out):
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

chain_roots = set()
per_head_roots = {}
for name in sorted(CHAIN_HEADS):
    d = json.loads((OUT / name).read_text())
    roots = []
    for k in d:
        if k.endswith('_addition') or k in ('merged_receipts', 'group_additions'):
            collect_addition_roots(d[k], roots)
    per_head_roots[name] = sorted(set(roots))
    chain_roots.update(int(h, 16) for h in per_head_roots[name])
assert len(chain_roots) == 402, len(chain_roots)
s_1227 = set(s10)
for r in chain_roots:
    s_1227 |= covers(r)
stF, remF, uniqF, demF = summary_state(s_1227)
assert (stF['solved_s6_in_manifest'], stF['unique_remaining_s6'],
        stF['sum_remaining_cost'], stF['s6_needed_by_open_classes'],
        stF['cost_needed_by_open_classes']) == (1227, 6620, 522561, 4890, 386284)
assert stF['remaining_s5_orbits'] == 175
print('CONTROL 1227 head reconstructed from published artifacts by pure '
      'geometry: 402 distinct chain roots from the 52 blob-verified head '
      'JSONs, summary 1227/6620/522561/4890/386284, remaining S5 orbits 175')

# head JSON number controls: 78a head 1225, 69h rebased head and merged
# head both 1227, equal to the reconstructed state
head78a = json.loads((OUT / 'class-frontier-cost78a-receipts-recompute-20261115.json').read_text())
f78 = head78a['frontier_after_cost78a']
assert (f78['solved_s6_in_manifest'], f78['unique_remaining_s6'],
        f78['sum_remaining_cost'], f78['s6_needed_by_open_classes'],
        f78['cost_needed_by_open_classes']) == (1225, 6622, 522699, 4892, 386422)
head69h = json.loads((OUT / 'class-frontier-cost69h-receipts-recompute-20261115.json').read_text())
f69 = head69h['frontier_after_cost69h']
headM = json.loads((OUT / 'class-frontier-merged-cost78a-69h-recompute-20261115.json').read_text())
fM = headM['frontier_after_merged']
for f in (f69, fM):
    assert (f['solved_s6_in_manifest'], f['unique_remaining_s6'],
            f['sum_remaining_cost'], f['s6_needed_by_open_classes'],
            f['cost_needed_by_open_classes']) == (1227, 6620, 522561, 4890, 386284)
assert f69['demand_histogram_open_only'] == fM['demand_histogram_open_only'] == stF['hist']
assert fM['demand_histogram_open_only']['c2=2,c4=0'] == 965

# final baseline control: regenerate the published merged-head CSVs
# byte-identically from the reconstructed 1227 state
def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2F = best(remF, 2)
class4F = best(remF, 4)
AUDIT_BLOCKED = '00000000000000809082000000000000'
rankingF = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in remF.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
buf = io.StringIO(newline='')
w = csv.writer(buf, lineterminator='\n')
w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
for r in rankingF:
    w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                r['remaining_s7_edge_cost']))
assert buf.getvalue() == (OUT / 'class-frontier-s5-ranking-after-merged-cost78a-69h-20261115.csv').read_text(), \
    'the merged-head ranking CSV must regenerate byte-identically from the reconstructed 1227 state'
buf = io.StringIO(newline='')
w = csv.writer(buf, lineterminator='\n')
coverableF = [c for c in class2F if c['s5_hex'] != AUDIT_BLOCKED]
for label, cand in (('best class-4 blocker-candidate S5', class4F[0]),
                    ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                     next((c for c in class2F if c['s5_hex'] == AUDIT_BLOCKED), None)),
                    ('best coverable class-2 blocker-candidate S5', coverableF[0]),
                    ('second coverable class-2 candidate S5',
                     coverableF[1] if len(coverableF) > 1 else None)):
    if cand is None:
        continue
    rows = remF.get(cand['s5_hex'], [])
    w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
    w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
    for row in sorted(rows, key=lambda r: int(r['s6_s7_edge_cost'])):
        d = demF[row['s6_hex']]
        w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                    f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
assert buf.getvalue() == (OUT / 'class-frontier-top-candidates-s6-after-merged-cost78a-69h-20261115.csv').read_text(), \
    'the merged-head top-candidates CSV must regenerate byte-identically from the reconstructed 1227 state'
print('CONTROL published merged-head ranking CSV (blob 4eeca615) and '
      'top-candidates CSV (blob 0f9905fc; both identical to the '
      'cost-69h-receipts CSVs) regenerated byte-identically from the '
      'reconstructed 1227 state')

# ---------- 3. the cost-70e target genuinely remaining at 1227 ----------
PARENT1 = '00000000000000801202000000200000'
PARENT2 = '00000000000000003800000008400000'
CHILD = '00000000000000801202000000200004'
CHILD_V = int(CHILD, 16)
THIRD_TARGET = '00000000000000809102000000000000'
p1_rows = remF.get(PARENT1, [])
p2_rows = remF.get(PARENT2, [])
assert len(p1_rows) == 31 and sum(int(r['s6_s7_edge_cost']) for r in p1_rows) == 2334
assert len(p2_rows) == 49 and sum(int(r['s6_s7_edge_cost']) for r in p2_rows) == 3625
assert CHILD in {r['s6_hex'] for r in p1_rows} and CHILD in {r['s6_hex'] for r in p2_rows}
holders = sorted(k for k, rows in remF.items() if CHILD in {r['s6_hex'] for r in rows})
assert holders == sorted([PARENT1, PARENT2]), \
    'the child must be a remaining row of exactly the two open class-2 parents'
assert CHILD_V not in s_1227 and CHILD_V in manifest
assert classes.get(PARENT1, 0) & 2 and classes.get(PARENT2, 0) & 2
assert demF.get(CHILD) == {'c1': 0, 'c2': 2, 'c4': 0}
# D4 one-stone lift controls: deleting the child's own lift stones and
# D4-canonicalizing must reproduce the open parents bit-exact
assert f'{canon(CHILD_V & ~(1 << 2)):032x}' == PARENT1, \
    'deleting child stone 2 and canonicalizing must reproduce parent1'
assert f'{canon(CHILD_V & ~(1 << 21)):032x}' == PARENT2, \
    'deleting child stone 21 and canonicalizing must reproduce the second class-2 parent'
third_rows = remF.get(THIRD_TARGET, [])
assert len(third_rows) == 2 and sum(int(r['s6_s7_edge_cost']) for r in third_rows) == 143
blocked_rows = remF.get(AUDIT_BLOCKED, [])
assert len(blocked_rows) == 10 and sum(int(r['s6_s7_edge_cost']) for r in blocked_rows) == 698
print('CONTROL child genuinely remaining at the reconstructed 1227 head: '
      'parent1 31 rows / 2334, second class-2 parent 49 rows / 3625, both '
      'hold the child row (and no other open parent does), child unsolved '
      'in-manifest, demand c1=0,c2=2,c4=0 re-derived, lift stones 2 '
      '(parent1) and 21 (parent2) D4-verified; third coverable class-2 '
      'target 2/143 and audit-blocked 10/698 unchanged')

# ---------- 4. claim v2/v3 + sweep audit re-derivation from the raw batches ----------
claim = json.loads((OUT / 'class2-lane-cost70e-inflight-20261115.json').read_text())
assert claim['schema'] in ('n11-class2-lane-cost70e-inflight-20261115-v2',
                           'n11-class2-lane-cost70e-inflight-20261115-v3')
assert claim['status'] == 'completed'
assert claim['s5'] == PARENT1 and claim['s6_child'] == CHILD
assert claim['s6_s7_edge_cost'] == 70
assert claim['demand'] == {'c1': 0, 'c2': 2, 'c4': 0}
assert claim['candidate_count'] == 70 and len(claim['legal_candidates']) == 70
sr = claim['sweep_results']
WIN_BITS = [0, 8, 24, 66, 79]
assert sr['candidates'] == 70 and sr['win7_d10_bits'] == WIN_BITS
assert sr['refuted_d10'] == 65 and sr['capped'] == 0
assert sr['total_nodes'] == 83656928
assert sr['terminal_stone_range_all'] == [13, 17]
assert sr['pilots_3402'] == 9 and sr['determinism_rerun_batch5_node_exact'] is True
assert '1227/6620/522561/4890/386284' in claim['chain_head_at_claim']
wc = claim['win7_certificates']
assert ('PENDING' in wc['fold'] or 'COMPLETED' in wc['fold']) and \
    '9f8e5a93562ea9f1ca61ee096d5064b07b782b87' in wc['manifest']

sweep = json.loads((OUT / 'class2-lane-cost70e-sweep-audit-20261115.json').read_text())
assert sweep['schema'] == 'n11-class2-lane-cost70e-raw-sweep-audit-20261115-v1'
assert sweep['target']['s6_child_hex'] == CHILD and sweep['target']['edge_cost'] == 70
assert sweep['target']['s5_hex'] == PARENT1
agg = sweep['aggregate']
assert agg['candidates'] == 70 and agg['win7_d10_bits'] == WIN_BITS
assert agg['refuted_d10'] == 65 and agg['capped'] == 0
assert agg['candidate_nodes'] == 83656928
WIN_NODES = {0: 4596984, 8: 1333433, 24: 2197162, 66: 1763979, 79: 1765453}
assert agg['win7_d10_nodes'] == {str(k): v for k, v in WIN_NODES.items()}
raw_by_bit = {}
seen_bits = []
batch_node_sum = 0
for brec in sweep['batches']:
    b = brec['batch']
    lines = (OUT / brec['file']).read_text().splitlines()
    recs = [json.loads(l) for l in lines if l.strip()]
    pilots = [r for r in recs if r.get('control') == 'pilot_d6']
    assert len(pilots) == 1 and pilots[0]['loss'] is False and pilots[0]['nodes'] == 3402
    cands = [r for r in recs if 'bit' in r]
    assert [r['bit'] for r in cands] == brec['candidate_bits']
    assert brec['candidate_bits'] == claim['engine']['batch_bits'][f'batch{b}']
    assert sum(r['nodes'] for r in cands) == brec['nodes']
    batch_node_sum += brec['nodes']
    for r in cands:
        assert r['capped'] is False and isinstance(r['loss'], bool)
        assert 13 <= r['terminalStoneRange'][0] <= r['terminalStoneRange'][1] <= 17
        raw_by_bit[r['bit']] = r
        seen_bits.append(r['bit'])
assert len(seen_bits) == len(set(seen_bits)) == 70
assert sorted(raw_by_bit) == sorted(claim['legal_candidates']), \
    'the 70 swept bits must equal the claim legal_candidates enumeration'
assert batch_node_sum == 83656928
win_raw = sorted(b for b in raw_by_bit if raw_by_bit[b]['loss'] is True)
assert win_raw == WIN_BITS and sum(1 for b in raw_by_bit if raw_by_bit[b]['loss'] is False) == 65
assert sum(r['nodes'] for r in raw_by_bit.values()) == 83656928
assert {b: raw_by_bit[b]['nodes'] for b in WIN_BITS} == WIN_NODES
assert sum(WIN_NODES.values()) == 11657011
wr = sweep['win_roots']
assert sorted(int(k) for k in wr) == WIN_BITS
MOBILITY = {0: 60, 8: 63, 24: 56, 66: 49, 79: 52}
for bit in WIN_BITS:
    root_v = CHILD_V | (1 << bit)
    assert wr[str(bit)]['root_hex'] == f'{root_v:032x}', bit
    assert wr[str(bit)]['d4_canonical_hex'] == f'{canon(root_v):032x}', bit
    assert wr[str(bit)]['root_mobility'] == MOBILITY[bit]
assert len({wr[str(b)]['d4_canonical_hex'] for b in WIN_BITS}) == 5
assert sweep['d4_duplicate_scan']['duplicates'] == 0
print('CONTROL sweep audit re-derived from 9 raw batches: 70 candidates '
      'exactly once (== claim enumeration), 5 WIN7-D10 / 65 REFUTED / 0 '
      'capped / 83,656,928 nodes (win sum 11,657,011), roots == '
      'child|1<<bit, 5 distinct D4 orbits, pilots 3402 x9')

# determinism rerun: batch-5 records node-exact against the raw batch
det_recs = [json.loads(l) for l in
            (OUT / 'class2-lane-cost70e-v16-determinism-rerun-20261115.jsonl').read_text().splitlines()
            if l.strip()]
det_by_bit = {r['bit']: r for r in det_recs if 'bit' in r}
batch5_bits = next(x['candidate_bits'] for x in sweep['batches'] if x['batch'] == 5)
assert sorted(det_by_bit) == sorted(batch5_bits)
for bit in batch5_bits:
    a, b_ = det_by_bit[bit], raw_by_bit[bit]
    assert a['loss'] == b_['loss'] and a['nodes'] == b_['nodes'] and a['capped'] == b_['capped'], bit
    assert a['terminalStoneRange'] == b_['terminalStoneRange'], bit
det_pilots = [r for r in det_recs if r.get('control') == 'pilot_d6']
assert len(det_pilots) == 1 and det_pilots[0]['loss'] is False and det_pilots[0]['nodes'] == 3402

# v15 cross-engine anchors
v15_recs = [json.loads(l) for l in
            (OUT / 'class2-lane-cost70e-v15-crosscheck-20261115.jsonl').read_text().splitlines()
            if l.strip()]
v15_pilots = [r for r in v15_recs if r.get('control') == 'pilot_d6']
assert len(v15_pilots) == 2 and all(p['loss'] is False and p['nodes'] == 5949 for p in v15_pilots)
v15_bits = {r['bit']: r for r in v15_recs if 'bit' in r}
assert sorted(v15_bits) == sorted(WIN_BITS + [75, 86, 113])
certdoc0 = json.loads((OUT / 'class2-lane-cost70e-win7-certificates-20261115.json').read_text())
certs0 = certdoc0['certificates']
for bit in WIN_BITS:
    r = v15_bits[bit]
    assert r['loss'] is True and r['capped'] is False
    assert r['nodes'] == certs0[str(bit)]['v15_anchor_crosscheck']['nodes']
    assert certs0[str(bit)]['v15_anchor_crosscheck']['loss'] is True
    assert 13 <= r['terminalStoneRange'][0] <= r['terminalStoneRange'][1] <= 17
for bit in (75, 86, 113):
    assert v15_bits[bit]['loss'] is False and raw_by_bit[bit]['loss'] is False, \
        'the v15 refuted anchors must agree with the v16 raw sweep verdicts'
assert sum(v15_bits[b]['nodes'] for b in WIN_BITS) == 27246682
print('CONTROL batch-5 determinism rerun node-exact; v15 cross-engine '
      'anchors: 5 WIN loss=true node-matched to the certificate manifest '
      '(sum 27,246,682), refuted anchors bits 75/86/113 loss=false with '
      'raw verdict agreement, pilots 5949 x2')

# ---------- 5. assert all five published certificates ----------
certdoc = certdoc0
assert certdoc['schema'] == 'n11-class2-lane-cost70e-win7-certificates-20261115-v1'
assert certdoc['child_hex'] == CHILD and certdoc['edge_cost'] == 70
assert certdoc['s5_target'] == PARENT1
lp = certdoc['lift_parents']
assert lp['class2_parent1'] == {'hex': PARENT1, 'lift_stone': 2}
assert lp['class2_parent2'] == {'hex': PARENT2, 'lift_stone': 21}
certs = certdoc['certificates']
assert sorted(int(k) for k in certs) == WIN_BITS
sums = {'rows': 0, 'extraction_nodes': 0, 'sub_roots_total': 0, 'bytes': 0}
v15_sum = 0
v16_sum = 0
roots70e = []
covered_orbits = set()
d4_orbit_of = {}
for bit in WIN_BITS:
    c = certs[str(bit)]
    assert c['bit'] == bit and c['verdict'] == 'WIN7' and c['child_hex'] == CHILD
    root_v = int(c['root_hex'], 16)
    assert root_v == CHILD_V | (1 << bit), bit
    roots70e.append(root_v)
    d4_orbit_of[bit] = f'{canon(root_v):032x}'
    assert d4_orbit_of[bit] == c['d4_canonical_hex']
    assert c['fbt_drops'] == 0 and c['rows_sorted_unique'] is True
    assert c['sub_roots_total'] == c['root_check']['loser_mobility'] == len(c['loser_first_moves'])
    assert c['sub_roots_total'] == MOBILITY[bit]
    assert c['root_check']['stones'] == 7 and c['root_check']['match'] is True
    assert c['terminal_range'] == [13, 17]
    assert c['v16_sweep_nodes'] == raw_by_bit[bit]['nodes'] == WIN_NODES[bit]
    assert c['v15_anchor_crosscheck']['loss'] is True
    assert c['v15_anchor_crosscheck']['nodes'] == v15_bits[bit]['nodes']
    bg = c['bigint_verification']
    assert bg['subroots_passed'] == c['sub_roots_total']
    assert bg['union_missing'] == 0 and bg['union_extra'] == 0
    assert bg['terminal_range'] == [13, 17]
    assert 'class4_child1_cert_extractor_exact_v16.ts' in c['extraction']
    # d4 parent orbits: canon-invariant and equal to the covers() orbit set
    chain_orbits = {f'{canon(x):032x}' for x in covers(root_v)}
    assert sorted(c['d4_parent_orbits']) == sorted(chain_orbits), bit
    assert CHILD in c['d4_parent_orbits'], \
        'each root minus its own added stone canonicalizes to the child'
    assert len(c['d4_parent_orbits']) == 7
    # local bytes: whole file assembled from its two published parts
    base = c['path'].split('/')[-1]
    local = CERTS / base
    parts = c['storage']['parts']
    assert c['storage']['layout'].startswith('split 2 parts')
    assert len(parts) == 2
    pdata = b''
    for p in parts:
        pl = CERTS / p['path'].split('/')[-1]
        pd = pl.read_bytes()
        assert len(pd) == p['bytes'] and hashlib.md5(pd).hexdigest() == p['md5']
        assert git_blob_sha(pl) == p['git_blob_sha'], p['path']
        pdata += pd
    data = local.read_bytes()
    assert pdata == data, 'the two published parts must join to the whole certificate'
    assert len(data) == c['bytes']
    assert hashlib.md5(data).hexdigest() == c['md5']
    assert hashlib.sha256(data).hexdigest() == c['sha256']
    assert git_blob_sha(local) == c['whole_git_blob_sha']
    lines = data.decode().splitlines()
    assert lines[0] == 'n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS'
    assert lines[1] == 'root ' + c['root_hex']
    rows = [l for l in lines[2:] if l.strip()]
    assert len(rows) == c['rows'] and len(set(rows)) == c['rows']
    assert rows == sorted(rows), 'certificate rows must be sorted-unique'
    del data, pdata, lines, rows
    sums['rows'] += c['rows']
    sums['extraction_nodes'] += c['extraction_nodes']
    sums['sub_roots_total'] += c['sub_roots_total']
    sums['bytes'] += c['bytes']
    v15_sum += c['v15_anchor_crosscheck']['nodes']
    v16_sum += c['v16_sweep_nodes']
    covered_orbits |= chain_orbits
assert len(set(roots70e)) == 5
assert sums == {'rows': 236784, 'extraction_nodes': 20246025,
                'sub_roots_total': 280, 'bytes': 8564174}
assert v15_sum == 27246682 and v16_sum == 11657011
t = certdoc['totals']
assert t == {'certificates': 5, 'rows': 236784, 'bytes': 8564174,
              'extraction_nodes': 20246025, 'sub_roots': 280,
              'v15_crosscheck_nodes_sum': 27246682,
              'v16_sweep_win_nodes_sum': 11657011}
ctl = certdoc['controls']
for k in ('remote_blob_shas_verified', 'root_identity_child_or_bit',
          'sub_roots_equal_bareiss_mobility', 'per_move_extraction_ok_all',
          'all_bits_parts_join_whole_md5', 'win_bits_v15_v16_agree',
          'regeneration_byte_exact_after_sandbox_reset'):
    assert ctl[k] is True, k
print('CONTROL 5 published certificates asserted against local bytes: '
      'md5 x sha256 x git blob shas (all bits parts-join-whole), rows '
      'sorted-unique, sub-roots == loser mobility == len(loser_first_moves) '
      '== 60/63/56/49/52, terminal 13..17, fbt_drops 0, d4 parent orbits '
      'canon-invariant == covers() orbit sets (7 each) all containing the '
      'child, BigInt verifier union 0/0, v15/v16 node-matched; manifest '
      'totals re-summed 236,784 rows / 8,564,174 bytes / 20,246,025 '
      'extraction nodes / 280 sub-roots')

# ---------- 6. third independent exact-geometry audit cross-check ----------
audit = json.loads((OUT / 'cost70e-third-independent-certificate-audit-20261115.json').read_text())
assert audit['schema'] == 'n11-class2-cost70e-third-independent-certificate-audit-20261115-v1'
assert audit['status'] == 'PASS'
assert '1227/6620/522561/4890/386284' in audit['baseline']['frontier_head_at_audit_start']
assert len(audit['certificates']) == 5
audit_by_bit = {a['bit']: a for a in audit['certificates']}
for bit in WIN_BITS:
    a = audit_by_bit[bit]
    c = certs[str(bit)]
    assert a['root_hex'] == c['root_hex'] and a['d4_canonical_hex'] == c['d4_canonical_hex']
    assert a['rows'] == c['rows'] and a['root_mobility'] == c['sub_roots_total']
    assert a['terminal_range'] == c['terminal_range'] == [13, 17]
    assert a['missing'] == 0 and a['extra'] == 0
    chain_orbits = {f'{canon(x):032x}' for x in covers(int(c['root_hex'], 16))}
    assert sorted(a['parent_orbits']) == sorted(chain_orbits), bit
    assert CHILD in a['parent_orbits']
at = audit['totals']
assert at == {'certificates': 5, 'rows': 236784, 'unique_dag_states': 360663,
               'winner_states': 236784, 'loser_states': 74744,
               'loser_reply_edges': 347244, 'terminal_states': 49135,
               'sub_roots': 280}
apl = audit['parent_lift']
assert apl['unique_s6_parent_orbits'] == 31
assert apl['shared_parent_orbits'] == [{'hex': CHILD, 'bits': WIN_BITS}]
assert apl['worklist_membership_hits'] == 11
covered_all = covered_orbits
assert len(covered_all) == 31, \
    'the five roots cover exactly 31 distinct S6 orbits (the child shared)'
for wpar in apl['worklist_parents']:
    for b in wpar['bits']:
        assert wpar['hex'] in {f'{canon(x):032x}' for x in covers(int(certs[str(b)]['root_hex'], 16))}, \
            (wpar['hex'], b)
cs6 = audit['child_s6']
assert cs6['hex'] == CHILD and cs6['proven_win'] is True
assert cs6['winning_moves_to_distinct_second_to_move_loss_roots'] == WIN_BITS
op = {p['s5_hex']: p for p in cs6['open_s5_parents']}
assert set(op) == {PARENT1, PARENT2}
assert op[PARENT1]['remaining_s6_orbits'] == 31 and op[PARENT1]['remaining_s7_edge_cost'] == 2334
assert op[PARENT2]['remaining_s6_orbits'] == 49 and op[PARENT2]['remaining_s7_edge_cost'] == 3625
print('CONTROL third independent exact-geometry audit cross-checked: '
      'status PASS, per-certificate rows/mobility/terminal/parent-orbits '
      'equal to this chain covers() sets (31 distinct covered orbits, '
      'child shared by all five bits), worklist parents covered by the '
      'right receipt, shared parent orbit == the child, proven_win '
      '[0, 8, 24, 66, 79]')

# ---------- 7. root disjointness vs every folded root ----------
folded_roots = set()
for name in BASELINE_VERIFIED:
    folded_roots.update(roots_of(name))
folded_roots.update(batch1)
folded_roots.update(batch2)
folded_roots.update([bit37] + child34 + child5 + child7)
for n in LANE_FILES:
    folded_roots.update(roots_of(n))
folded_roots.update(chain_roots)
assert not (set(roots70e) & folded_roots), \
    'the 5 cost-70e roots must be disjoint from every folded root'
folded_d4 = {f'{canon(r):032x}' for r in folded_roots}
d4_hits = [(bit, d4_orbit_of[bit]) for bit in WIN_BITS
           if d4_orbit_of[bit] in folded_d4]
assert d4_hits == [], d4_hits
assert len({d4_orbit_of[bit] for bit in WIN_BITS}) == 5
print('CONTROL root disjointness: 5 new roots vs %d distinct roots whose '
      'covers contributed to the 1227 head (12 baseline verified files + '
      'class4 batch1/2/3 + 8 lane certificate files + 402 chain roots), '
      'raw-hex and D4-canonically verified with the chain-internal '
      'canon(); 5 distinct D4 orbits' % len(folded_roots))

# ---------- 8. fold the 5 receipts in published bit order on the 1227 head ----------
EXPECT = {
    0:  {'marginal': 5, 'mim': 1, 'mim_hexes': [CHILD]},
    8:  {'marginal': 5, 'mim': 1,
         'mim_hexes': ['00000000000000801202000000000104']},
    24: {'marginal': 6, 'mim': 2,
         'mim_hexes': ['00000000000000003800000009400000',
                       '00000000000000801202000001200000']},
    66: {'marginal': 6, 'mim': 2,
         'mim_hexes': ['00000000000000003800000008400040',
                       '00000000000000841202000000200000']},
    79: {'marginal': 4, 'mim': 0, 'mim_hexes': []},
}
s_cur = set(s_1227)
addition = []
zero_mim = []
child_closed_by = None
for bit in WIN_BITS:
    c = certs[str(bit)]
    root = int(c['root_hex'], 16)
    cov = covers(root)
    assert len(cov) == 7 and CHILD_V in cov
    marg = cov - s_cur
    marg_m = marg & manifest
    if CHILD_V in marg_m:
        assert child_closed_by is None, 'the child must be closed exactly once'
        child_closed_by = bit
    e = EXPECT[bit]
    assert len(marg) == e['marginal'] and len(marg_m) == e['mim'], bit
    assert sorted(f'{k:032x}' for k in marg_m) == e['mim_hexes'], bit
    addition.append({
        'bit': bit, 'root_hex': c['root_hex'], 'd4_canonical_hex': c['d4_canonical_hex'],
        'sweep_nodes': raw_by_bit[bit]['nodes'], 'certified': True,
        'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
        'marginal_non_manifest_hexes': sorted(f'{k:032x}' for k in marg - marg_m),
        'rows': c['rows'], 'extraction_nodes': c['extraction_nodes'],
        'md5': c['md5'], 'sub_roots_pass': c['sub_roots_total'],
        'v15_anchor_nodes': c['v15_anchor_crosscheck']['nodes'],
    })
    if not marg_m:
        zero_mim.append(bit)
    s_cur |= marg
assert child_closed_by == 0, \
    'the child orbit must be closed by the first receipt in published order'
cov5 = set()
for r in roots70e:
    cov5 |= covers(r)
assert s_cur == set(s_1227) | cov5, 'set-equality: s_after == s_1227 UNION covers(5 roots)'
# reverse-order replay (commutativity control)
s_rev = set(s_1227)
for bit in reversed(WIN_BITS):
    s_rev |= covers(int(certs[str(bit)]['root_hex'], 16)) - s_rev
assert s_rev == s_cur, 'fold application must be order-independent'
total_mim = sum(a['marginal_in_manifest'] for a in addition)
total_marg = sum(a['marginal'] for a in addition)
assert total_marg == 26 and total_mim == 6
stG, remG, uniqG, demG = summary_state(s_cur)
assert stG['solved_s6_in_manifest'] == 1227 + total_mim == 1233
assert (stG['unique_remaining_s6'], stG['sum_remaining_cost'],
        stG['s6_needed_by_open_classes'], stG['cost_needed_by_open_classes']) \
        == (6614, 522131, 4884, 385854)
assert stG['hist']['c2=2,c4=0'] == 959
assert CHILD_V in s_cur and CHILD_V in manifest
assert CHILD not in {r['s6_hex'] for r in remG.get(PARENT1, [])}
assert CHILD not in {r['s6_hex'] for r in remG.get(PARENT2, [])}
rows_after_p1 = {r['s6_hex']: int(r['s6_s7_edge_cost']) for r in remG.get(PARENT1, [])}
rows_after_p2 = {r['s6_hex']: int(r['s6_s7_edge_cost']) for r in remG.get(PARENT2, [])}
assert len(rows_after_p1) == 28 and sum(rows_after_p1.values()) == 2119
assert len(rows_after_p2) == 45 and sum(rows_after_p2.values()) == 3340
p1_lost = sorted({r['s6_hex'] for r in p1_rows} - set(rows_after_p1))
p2_lost = sorted({r['s6_hex'] for r in p2_rows} - set(rows_after_p2))
assert CHILD in p1_lost and CHILD in p2_lost
third_after = remG.get(THIRD_TARGET, [])
assert len(third_after) == 2 and sum(int(r['s6_s7_edge_cost']) for r in third_after) == 143
blocked_after = remG.get(AUDIT_BLOCKED, [])
assert len(blocked_after) == 10 and sum(int(r['s6_s7_edge_cost']) for r in blocked_after) == 698
print('AFTER cost-70e receipts:', json.dumps(
    {k: v for k, v in stG.items() if k != 'hist'}))
print('total marginal=%d marginal_in_manifest=%d; zero-mim receipts: %s; '
      'child orbit closed by bit%d; parent1 %d rows / %d (was 31/2334); '
      'second class-2 parent %d rows / %d (was 49/3625)'
      % (total_marg, total_mim, zero_mim or 'none', child_closed_by,
         len(rows_after_p1), sum(rows_after_p1.values()),
         len(rows_after_p2), sum(rows_after_p2.values())))
print('parent1 marginal rows lost:', p1_lost)
print('second class-2 parent marginal rows lost:', p2_lost)

# ---------- 9. outputs ----------
class2 = best(remG, 2)
class4 = best(remG, 4)
result = {
    'schema': 'n11-class-frontier-cost70e-receipts-recompute-20261115-v1',
    'date': '2026-11-15',
    'baseline_main': 'class-frontier-merged-cost78a-69h-recompute-20261115.json '
                     '(merged cost-78a+69h chain head '
                     '1227/6620/522561/4890/386284, git blob sha '
                     '294c4ed3d9fb26143d54ef2e45d400d1068a41dd, equal-numbered '
                     'to the parallel-rebased cost-69h head '
                     'class-frontier-cost69h-receipts-recompute-20261115.json '
                     'blob d25eb3a00f73cf9ca34fc2816d28045c1e23f3ae); both '
                     'head JSONs and both published merged-head CSVs (blobs '
                     '4eeca615 / 0f9905fc) are re-asserted byte-exact and '
                     'the 1227 head is reconstructed independently here '
                     'from published artifacts by pure geometry (see '
                     'method)',
    'method': 'baseline reconstruction from published artifacts only: every '
              'published input file (28 base inputs, 52 published frontier '
              'head JSONs, 4 published CSVs, the cost-70e sweep audit / '
              'claim v2 / certificate manifest / third independent audit, '
              '9 raw sweep batches, v16 determinism rerun, v15 crosscheck, '
              '10 certificate parts + 5 whole certificates, 2 cost-70e '
              'scripts) asserted byte-exact against main by git blob sha; '
              'the solved set rebuilt by pure geometry as winners UNION '
              'covers(12 baseline verified files) UNION covers(class4 '
              'batch1/batch2/batch3) UNION covers(7 class2 lane files) '
              'UNION covers(402 distinct receipt roots recorded in the 52 '
              'blob-verified head JSON addition records); staged controls '
              'reproduce the published 638/7208/565500, 657/7189/564070, '
              '665/7181/563509 (open 5398/423516) and 814/7032/552811/5256/'
              '413283 intermediate frontiers exactly, bit37 covers == its '
              'published frontier_effect; final controls: summary '
              '1227/6620/522561/4890/386284 with 175 remaining S5 orbits, '
              'histogram equal to the published merged head JSON '
              '(c2=2,c4=0 at 965), and byte-identical regeneration of the '
              'published merged-head ranking and top-candidates CSVs from '
              'the reconstructed state; then the cost-70e child asserted '
              'genuinely remaining at 1227 (both open class-2 parents '
              '00000000000000801202000000200000 at 31 rows / 2334 and '
              '00000000000000003800000008400000 at 49 rows / 3625 holding '
              'the child row, the child held by exactly these two open '
              'parents, child unsolved in-manifest, demand c1=0,c2=2,c4=0 '
              're-derived from the remaining incidences, lift stones 2 '
              'against parent1 and 21 against the second class-2 parent '
              'D4-verified); the published sweep audit re-derived from the '
              'nine raw batch JSONLs (70 candidates exactly once equal to '
              'the claim enumeration, 5 WIN7-D10 / 65 REFUTED-D10 / 0 '
              'capped / 83,656,928 nodes with win sum 11,657,011, roots == '
              'child | 1<<bit, 5 distinct D4 orbits, pilots 3402 x9, '
              'batch-5 determinism rerun node-exact), the v15 cross-engine '
              'anchors asserted from the published JSONL (5 WIN loss=true '
              'node-matched sum 27,246,682, refuted anchors bits 75/86/113 '
              'loss=false with raw verdict agreement, pilots 5949 x2), all '
              'five published certificates asserted against the local '
              'certificate bytes (all bits split 2 parts: parts-join-whole, '
              'md5, sha256, git blob shas, rows sorted-unique, sub-roots == '
              'loser mobility == len(loser_first_moves) == 60/63/56/49/52, '
              'terminal 13..17, fbt_drops 0, d4 canonical hex == '
              'canon(root), d4 parent orbits canon-invariant, equal to this '
              "chain's covers() orbit sets and each containing the child, "
              'v15/v16 node match, BigInt verifier union 0/0) with the '
              'manifest totals re-summed (236,784 rows / 8,564,174 bytes / '
              '20,246,025 extraction nodes / 280 sub-roots), the published '
              'third independent exact-geometry certificate audit '
              'cross-checked (status PASS, per-certificate rows / mobility '
              '/ terminal ranges / parent orbits equal to this chain '
              'covers() sets, 31 distinct covered orbits with the child '
              'shared by all five bits, worklist parents covered by the '
              'right receipt, proven_win [0, 8, 24, 66, 79]), the 5 roots '
              'asserted disjoint from every root whose covers contributed '
              'to the 1227 head both raw-hex and D4-canonically and '
              'mutually distinct D4, then the 5 receipts folded in '
              'published bit order [0, 8, 24, 66, 79] with every '
              'per-record marginal re-derived from the growing union; the '
              'child-orbit closure (bit0), the '
              'both-open-parents-lose-the-child-row control, the '
              'set-equality control s_after == s_1227 UNION covers(5 '
              'roots) and a reverse-order replay control all hold. '
              'Receipts only - no sweep claims',
    'controls': {
        'input_files_byte_exact_vs_main': n_verified,
        'baseline_reconstruction_method': 'published head JSONs + pure '
            'geometry (no runpy chain replay); the reconstructed state '
            'regenerates the published merged-head CSVs byte-identically',
        'staged_controls_reproduced': '638/7208/565500, 657/7189/564070, '
            '665/7181/563509 (open 5398/423516), 814/7032/552811/5256/413283',
        'chain_head_1227_reproduced': True,
        'merged_csvs_regenerated_byte_identical': True,
        'child_genuinely_remaining_at_baseline': True,
        'both_open_parents_held_child_row_at_baseline': True,
        'child_held_by_exactly_the_two_open_parents': True,
        'lift_stones_d4_verified': 'parent1 stone 2, parent2 stone 21',
        'sweep_rederived_from_raw_batches': True,
        'determinism_rerun_batch5_node_exact': True,
        'v15_cross_engine_anchors_verified': True,
        'certificates_bytes_md5_sha256_blobsha_verified': True,
        'all_bits_parts_join_whole': True,
        'bigint_verifier_union_zero': True,
        'manifest_totals_resummed': True,
        'third_independent_audit_cross_checked': True,
        'root_disjointness_vs_all_folded_roots': True,
        'child_orbit_closure': 'closed by the bit-0 receipt (first in '
                               'published order), of this fold',
        'both_open_parents_lost_child_row': True,
        'set_equality_after_5': 's == s_1227 UNION covers(5 cost-70e roots)',
        'reverse_order_replay_identical': True,
    },
    'target': {
        's5_parent_hex': PARENT1, 's6_child_hex': CHILD, 'edge_cost': 70,
        'open_parents': [PARENT1, PARENT2],
        'demand_at_baseline_1227': {'c1': 0, 'c2': 2, 'c4': 0},
        'child_orbit_closure': 'closed by the bit-0 receipt of this fold',
        'candidates': 70, 'win7_d10': 5, 'refuted_d10': 65, 'capped': 0,
        'candidate_nodes': 83656928,
        'remaining_rows_after': {
            'class2_parent1_orbits': len(rows_after_p1),
            'class2_parent1_edge_cost': sum(rows_after_p1.values()),
            'class2_parent2_orbits': len(rows_after_p2),
            'class2_parent2_edge_cost': sum(rows_after_p2.values()),
            'parent1_rows_lost': p1_lost,
            'parent2_rows_lost': p2_lost,
        },
    },
    'cost70e_addition': addition,
    'totals': {
        'receipts': 5,
        'total_marginal': total_marg,
        'total_marginal_in_manifest': total_mim,
        'zero_marginal_in_manifest': ['bit%d' % b for b in zero_mim],
        'child_closed_by_bit': child_closed_by,
        'certificate_rows': sums['rows'],
        'certificate_bytes': sums['bytes'],
        'certificate_extraction_nodes': sums['extraction_nodes'],
        'certificate_sub_roots': sums['sub_roots_total'],
        'v15_crosscheck_nodes_sum': v15_sum,
        'v16_sweep_win_nodes_sum': v16_sum,
    },
    'frontier_after_cost70e': {
        'solved_s6_in_manifest': stG['solved_s6_in_manifest'],
        'remaining_s5_orbits': stG['remaining_s5_orbits'],
        'unique_remaining_s6': stG['unique_remaining_s6'],
        'sum_remaining_cost': stG['sum_remaining_cost'],
        's6_needed_by_open_classes': stG['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': stG['cost_needed_by_open_classes'],
        'demand_histogram_open_only': stG['hist'],
        'best_class2': class2[0],
        'audit_blocked_class2': next((c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED), None),
        'best_coverable_class2': next(c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED),
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'outstanding_not_folded': {
        'cost65l': '2 WIN7-D10 receipts (bits 21/48) with extraction/verify '
                   'artifacts but no certificate bodies on main; not folded',
        'parallel_lanes': 'in-flight sweeps/receipts on parallel lanes '
                          '(class4-82b, five-row-q7 and others) are not '
                          'folded here; their folds must re-fetch latest '
                          'main, re-assert the canonical chain head and '
                          'rebase on this new head',
        'sterile_sweeps': 'cost-65k/73f/74f/74c/75/79/79b/70d and other '
                          'sterile sweeps recorded (all REFUTED-D10, 0 '
                          'WIN7-D10, frontier unchanged); no receipts to '
                          'fold',
        'next_fold_baseline': 'this chain head (see frontier_after_cost70e) '
                              'is the new canonical baseline for all '
                              'subsequent folds; assert it before extending',
    },
    'interpretation_guard': 'bookkeeping over published receipts; solved counts '
                            'measure manifest coverage, not the game-theoretic '
                            'value of any position; REFUTED-D10 sweeps prove '
                            'only absence of WIN7-D10; WIN7 certificates prove '
                            'a win within depth 10 from the individual '
                            '7-stone roots only; closing the cost-70e child '
                            'orbit removes the child from both open class-2 '
                            'parents remaining rows but does not solve '
                            'either S5 parent and does not decide class 2 or '
                            'class 4; 11x11 empty board / two-stone root '
                            '{49,60} / S2 {59,60} / class 2 / class 4 remain '
                            'UNKNOWN',
}
(OUT / 'class-frontier-cost70e-receipts-recompute-20261115.json').write_text(
    json.dumps(result, indent=1) + '\n')
print('written class-frontier-cost70e-receipts-recompute-20261115.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in remG.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost70e-receipts-20261115.csv').open(
        'w', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

with (OUT / 'class-frontier-top-candidates-s6-after-cost70e-receipts-20261115.csv').open(
        'w', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    coverable = [c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED]
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         next((c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED), None)),
                        ('best coverable class-2 blocker-candidate S5', coverable[0]),
                        ('second coverable class-2 candidate S5',
                         coverable[1] if len(coverable) > 1 else None)):
        if cand is None:
            continue
        rows = remG.get(cand['s5_hex'], [])
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rows, key=lambda r: int(r['s6_s7_edge_cost'])):
            d = demG[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-cost70e-receipts)')
