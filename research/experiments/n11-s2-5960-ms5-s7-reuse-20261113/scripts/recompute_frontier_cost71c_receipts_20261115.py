#!/usr/bin/env python3
"""Class-2 frontier recomputation folding the class2-lane cost-71c WIN7
receipts (2 WIN7-D10 bits 24, 112 of the cheapest remaining unswept child
00000000000000801202000080200000, edge cost 71, dual class-2 demand
c1=0,c2=2,c4=0 - the child is a remaining row of both open class-2
parents: the second coverable class-2 target S5
00000000000000801202000000200000 at 28 rows / 2119 and the open class-2 S5
00000000000000801202000080000000 at 43 rows / 3268) on top of the
cost-70e receipts chain head (solved 1233, 2026-11-15).

Baseline method (this fold): instead of replaying the whole runpy chain of
fold scripts, the canonical 1233 head is reconstructed independently from
published artifacts only: every published input file is asserted
byte-exact against main by git blob sha, then the solved set is rebuilt by
pure geometry as winners UNION covers(12 baseline verified certificate
files) UNION covers(class4 batch1/batch2/batch3) UNION covers(7 class2
lane certificate files) UNION covers(402 distinct receipt roots recorded
in the 52 blob-verified pre-70e head JSON addition records) - reproducing
the published 1227 merged head - and the published cost-70e receipts fold
is re-derived in its published order [0, 8, 24, 66, 79] with every
per-record marginal re-derived from the growing union and cross-checked
against the published 70e head JSON addition records; the final baseline
controls are byte-identical regeneration of the published merged-head
CSVs (git blobs 4eeca615 / 0f9905fc), the published 70e head JSON
summary and histogram (blob a0171d4b) and the published 70e head CSVs
(git blobs 33fe27c1 / 4561af13) from the reconstructed 1233 state, which
pins every remaining S5 orbit's row set, count and cost at the baseline.

The cost-71c child orbit 00000000000000801202000080200000 is genuinely
remaining at the 1233 head (a remaining row of both open class-2 parents,
held by exactly these two) and is closed by this fold itself, by the
bit-24 receipt (the first in published order; both roots cover the child
via deleting their own added stone, D4-canonicalizing to the child).

This script:
1. verifies every published input byte-exact against main by git blob
   sha (29 base inputs, 52 pre-70e head JSONs, the 70e head JSON and both
   70e head CSVs, 4 merged-head CSVs, the 70e sweep audit / manifest /
   inflight claim v3 / third independent audit, the 71c sweep audit /
   certificate manifest / inflight claim v2 / four verify records, 9 raw
   sweep batches, the v16 determinism rerun, the v15 crosscheck, 3
   published certificate files + the certificates README, the 71c audit
   and Bareiss verifier scripts, and the 6 MS5 manifest parts);
2. reconstructs the 1227 head by pure geometry with staged controls,
   regenerates the published merged-head CSVs byte-identically;
3. re-derives the published cost-70e receipts fold on that state (5
   receipts, published order, per-record marginals equal to the published
   70e head JSON addition records), reaching 1233/6614/522131/4884/385854
   with the published histogram, and regenerates the published 70e head
   CSVs byte-identically;
4. asserts the 71c child genuinely remaining at 1233 (both open class-2
   parents at 28/2119 and 43/3268 holding the child row, the child held
   by exactly these two open parents, child unsolved in-manifest, demand
   c1=0,c2=2,c4=0 re-derived, lift stones 31 against parent1 and 21
   against the second class-2 parent, the other four child stones lifting
   to closed rows, D4 one-stone lift controls);
5. re-derives the published 71c sweep audit from the nine raw batch
   JSONLs: per-batch candidate bits in order, pilot 3402 controls, 71
   candidates exactly once (== claim enumeration), 2 WIN7-D10 / 69
   REFUTED / 0 capped, node sum 94,128,613 (win sum 4,442,926), win roots
   == child | 1<<bit, 2 distinct D4 orbits, terminal range 13..17,
   batch-5 determinism rerun node-exact;
6. asserts the v15 cross-engine anchors (2 WIN loss=true node-matched,
   sum 17,030,763, refuted anchors bits 75/113/116 loss=false with raw
   verdict agreement, pilot 5949);
7. asserts both published certificates (bit24 single file, bit112 two
   parts joining to the verified true md5 - the published manifest /
   claim / audit / README join-md5 field carries a stray trailing 5,
   detected here and recorded; rows sorted-unique, header, root
   identity, sub-roots == loser mobility == len(loser_first_moves) ==
   47/56, terminal ranges, BigInt and Bareiss verify records re-read,
   d4 canonical hex == canon(root), each root minus its own added stone
   canonicalizes to the child) and the manifest totals re-summed
   (82,602 rows / 24,639,331 extraction nodes / 2 roots);
8. asserts the 2 roots are disjoint from every root whose covers
   contributed to the 1233 head (12 baseline verified files + class4
   batch1/2/3 + 8 lane certificate files + 402 chain roots + the 5
   cost-70e receipt roots) both raw-hex and D4-canonically, and mutually
   distinct D4;
9. folds the 2 receipts in published bit order [24, 112], re-deriving
   every per-record marginal from the growing union, with the
   child-orbit closure control (bit24), the
   both-open-parents-lose-the-child-row control, a set-equality control
   s_after == s_1233 UNION covers(2 roots) and a reverse-order replay
   control;
10. produces the after-cost-71c frontier + ranking CSV + top-candidates
    CSV.

Receipts only - no sweep claims are made here. In-flight sweeps of
parallel lanes (cost-65l receipts, cost-70f certificates, class4-82b,
five-row-q7 and others) are not folded by this script; the next fold must
re-fetch latest main, re-assert the canonical chain head and rebase on
it.
"""
import csv, gzip, hashlib, io, json, re
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'
CERTS = OUT / 'class2-lane-cost71c-certificates'
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
    # the cost-70e receipts fold head (the 1233 baseline of this fold) and
    # its published CSVs
    'class-frontier-cost70e-receipts-recompute-20261115.json': 'a0171d4bb839aeb813d231c7d879d6a89452359f',
    'class-frontier-s5-ranking-after-cost70e-receipts-20261115.csv': '33fe27c1e2664ac7644a1eff00df649cb38efe1c',
    'class-frontier-top-candidates-s6-after-cost70e-receipts-20261115.csv': '4561af13ce0dd743051e5f3485ea040438a3d908',
    # cost-70e lane records (inflight claim as updated to v3 by the fold)
    'class2-lane-cost70e-sweep-audit-20261115.json': '47d38c00264aae84551eaaf994a10c134ff2f60f',
    'class2-lane-cost70e-win7-certificates-20261115.json': '9f8e5a93562ea9f1ca61ee096d5064b07b782b87',
    'class2-lane-cost70e-inflight-20261115.json': '9c27cff582e84159aace369b60cfe4543e788bbf',
    'cost70e-third-independent-certificate-audit-20261115.json': '6727eb651e2ee6b978c24a7d0e898333d632e127',
}
RECORDS_71C = {
    'class2-lane-cost71c-sweep-audit-20261115.json': '0a89e14954d76691a62007b1e5c75a97aabaa663',
    'class2-lane-cost71c-win7-certificates-20261115.json': '3a09163ccfde2a3ce4e63f61ef31d42688f60b30',
    'class2-lane-cost71c-inflight-20261115.json': 'd69f144c26c2bc85c7512ec71b9e196bb39cf453',
    'class2-lane-cost71c-bit24-bigint-verify-20261115.json': 'bfb30ef703fb0f92c80851b6bd50af1878ac6e6b',
    'class2-lane-cost71c-bit24-bareiss-verify-20261115.json': 'c90369fb51b213e2c124070f10d18a1a9f09ab93',
    'class2-lane-cost71c-bit112-bigint-verify-20261115.json': '8a06717e45495ae19ba6771ab916d28c95d01b80',
    'class2-lane-cost71c-bit112-bareiss-verify-20261115.json': '861512f17141f08d9607c5a2a32a6847991fdbcd',
}
RAW_BLOBS = {
    'class2-lane-cost71c-raw-batch1-20261115.jsonl': '1079772e76dff5df68961d17733d384662a95c5b',
    'class2-lane-cost71c-raw-batch2-20261115.jsonl': '445d5b22c8f63346fe223262b73553a4d3d83d61',
    'class2-lane-cost71c-raw-batch3-20261115.jsonl': '8449541559e4714926fbb85ff6e30a351c07273b',
    'class2-lane-cost71c-raw-batch4-20261115.jsonl': 'b795e69e92529f1291feda07d1882d76247cc4b3',
    'class2-lane-cost71c-raw-batch5-20261115.jsonl': '676939e80781a74d81c026ab185005492ea9c108',
    'class2-lane-cost71c-raw-batch6-20261115.jsonl': '03048c72854b7727e8edae3f0bc76193d6de2520',
    'class2-lane-cost71c-raw-batch7-20261115.jsonl': '6aa3cb43b57e55f1b08eac8fe11755207222f79e',
    'class2-lane-cost71c-raw-batch8-20261115.jsonl': 'fe9f39f972919d4781ff27ef72febdb3cfa2e09b',
    'class2-lane-cost71c-raw-batch9-20261115.jsonl': '7abbaf1953f03ea44d6ee1178f770b35edbdb955',
    'class2-lane-cost71c-v16-determinism-rerun-20261115.jsonl': 'a76c6e8ae38459b29aa89ce62b3e0548e3ff8a80',
    'class2-lane-cost71c-v15-crosscheck-20261115.jsonl': '67174a05f4c8efa5c1ba544db8345ac8fc05cf30',
}
CERT_FILE_BLOBS = {
    'bit24-root-00000000000000801202000081200000.cert': '8d9b4459f489b3224c64b4f6bbd37b8ff2dd23e3',
    'bit112-root-00010000000000801202000080200000.cert.part1of2': '494ed0532f688d96e9a678720728bf4ba31039b1',
    'bit112-root-00010000000000801202000080200000.cert.part2of2': 'c84955f6fbc183f92be5df379aa587acbe3442b1',
    'README.md': '5f4588574e4bc944f6787d7994235823ec5f4df7',
}
SCRIPT_BLOBS = {
    'audit_cost71c_raw_sweep_20261115.py': 'e92ca426c468d895d602a8a53b4401438e6b06bc',
    'verify_cost71c_win7_bareiss_independent.py': '71e8eeeab3d52f48e8d70c1f1c5d6ed214346d7f',
}
MS5_BLOBS = {
    'ms5_s6_manifest_part1.csv': '6b30ad1b224ead35ffc999e1358e2451446adeeb',
    'ms5_s6_manifest_part2.csv': '8aff65fa2942e7be2ee1adf08ffea6a21a4a02c3',
    'ms5_s6_manifest_part3.csv': '203b0fbd071bfe5f4da8a6cd34fcf3a65670df23',
    'ms5_s6_manifest_part4.csv': '1ec608cc12842bd4472a3039fcc0514494e1960c',
    'ms5_s6_manifest_part5.csv': 'e2aad9cef9f9a4af3bc659043631558408b6672b',
    'ms5_s6_manifest_part6.csv': 'acc1a8b3869a9917be7dd1b55574c756b59b0351',
}
assert len(BASE_BLOBS) == 29 and len(CHAIN_HEADS) == 52 and len(EXTRA_BLOBS) == 11
assert len(RECORDS_71C) == 7 and len(RAW_BLOBS) == 11 and len(CERT_FILE_BLOBS) == 4
assert len(SCRIPT_BLOBS) == 2 and len(MS5_BLOBS) == 6
n_verified = 0
for blobs, sub in ((BASE_BLOBS, OUT), (CHAIN_HEADS, OUT), (EXTRA_BLOBS, OUT),
                  (RECORDS_71C, OUT), (RAW_BLOBS, OUT), (CERT_FILE_BLOBS, CERTS),
                  (SCRIPT_BLOBS, HERE / 'scripts'), (MS5_BLOBS, MS5)):
    for name, want in blobs.items():
        assert git_blob_sha(sub / name) == want, name
        n_verified += 1
print('CONTROL %d published input files byte-exact against main by git '
      'blob sha (29 base inputs + 52 pre-70e head JSONs + the 70e head '
      'JSON and 2 head CSVs + 4 merged-head CSVs + 4 cost-70e records + 7 '
      'cost-71c records + 11 raw JSONLs + 3 published certificate files '
      'and README + 2 scripts + 6 MS5 manifest parts)'
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
print('CONTROL 1227 merged head reconstructed from published artifacts by '
      'pure geometry: 402 distinct chain roots from the 52 blob-verified '
      'head JSONs, summary 1227/6620/522561/4890/386284, remaining S5 '
      'orbits 175')

# final baseline control: regenerate the published merged-head CSVs
# byte-identically from the reconstructed 1227 state
def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

AUDIT_BLOCKED = '00000000000000809082000000000000'
THIRD_TARGET = '00000000000000809102000000000000'
class2F = best(remF, 2)
class4F = best(remF, 4)
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
print('CONTROL published merged-head ranking CSV (blob 4eeca615) and '
      'top-candidates CSV (blob 0f9905fc) regenerate byte-identically '
      'from the reconstructed 1227 state')

# ---------- 3. re-derive the published cost-70e receipts fold -> 1233 ----------
head70e = json.loads((OUT / 'class-frontier-cost70e-receipts-recompute-20261115.json').read_text())
assert head70e['schema'] == 'n11-class-frontier-cost70e-receipts-recompute-20261115-v1'
add70e = head70e['cost70e_addition']
assert [a['bit'] for a in add70e] == [0, 8, 24, 66, 79]
f70e = head70e['frontier_after_cost70e']
assert (f70e['solved_s6_in_manifest'], f70e['unique_remaining_s6'],
        f70e['sum_remaining_cost'], f70e['s6_needed_by_open_classes'],
        f70e['cost_needed_by_open_classes']) == (1233, 6614, 522131, 4884, 385854)
# the 70e claim was updated to v3 by that fold: its fold record must pin
# the same head transition
claim70e = json.loads((OUT / 'class2-lane-cost70e-inflight-20261115.json').read_text())
assert claim70e['schema'] == 'n11-class2-lane-cost70e-inflight-20261115-v3'
fold70e = claim70e['fold']
assert fold70e['status'] == 'completed'
assert fold70e['chain_head_before'] == '1227/6620/522561/4890/386284'
assert fold70e['chain_head_after'] == '1233/6614/522131/4884/385854'
s_1233 = set(s_1227)
for a in add70e:
    root_v = int(a['root_hex'], 16)
    cov = covers(root_v)
    assert len(cov) == 7
    marg = cov - s_1233
    marg_m = marg & manifest
    assert len(marg) == a['marginal'], a['bit']
    assert len(marg_m) == a['marginal_in_manifest'], a['bit']
    assert sorted(f'{k:032x}' for k in marg_m) == a['marginal_manifest_hexes'], a['bit']
    s_1233 |= marg
stG, remG, uniqG, demG = summary_state(s_1233)
assert (stG['solved_s6_in_manifest'], stG['unique_remaining_s6'],
        stG['sum_remaining_cost'], stG['s6_needed_by_open_classes'],
        stG['cost_needed_by_open_classes']) == (1233, 6614, 522131, 4884, 385854)
assert stG['remaining_s5_orbits'] == 175
assert stG['hist'] == f70e['demand_histogram_open_only']
assert stG['hist']['c2=2,c4=0'] == 959
roots70e = [int(a['root_hex'], 16) for a in add70e]
cov70e = set()
for r in roots70e:
    cov70e |= covers(r)
assert s_1233 == set(s_1227) | cov70e, 'set-equality: s_1233 == s_1227 UNION covers(70e roots)'
# regenerate the published 70e head CSVs byte-identically
def ranking_text(rem):
    ranking = sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items()),
        key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                       r['remaining_s7_edge_cost'], r['s5_hex']))
    buf = io.StringIO(newline='')
    w = csv.writer(buf, lineterminator='\n')
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))
    return buf.getvalue()

def top_candidates_text(rem, dem, class2, class4):
    buf = io.StringIO(newline='')
    w = csv.writer(buf, lineterminator='\n')
    coverable = [c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED]
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         next((c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED), None)),
                        ('best coverable class-2 blocker-candidate S5', coverable[0]),
                        ('second coverable class-2 candidate S5',
                         coverable[1] if len(coverable) > 1 else None)):
        if cand is None:
            continue
        rows = rem.get(cand['s5_hex'], [])
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rows, key=lambda r: int(r['s6_s7_edge_cost'])):
            d = dem[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
    return buf.getvalue()

assert ranking_text(remG) == (OUT / 'class-frontier-s5-ranking-after-cost70e-receipts-20261115.csv').read_text(), \
    'the 70e head ranking CSV must regenerate byte-identically from the reconstructed 1233 state'
class2G, class4G = best(remG, 2), best(remG, 4)
assert top_candidates_text(remG, demG, class2G, class4G) == \
    (OUT / 'class-frontier-top-candidates-s6-after-cost70e-receipts-20261115.csv').read_text(), \
    'the 70e head top-candidates CSV must regenerate byte-identically from the reconstructed 1233 state'
print('CONTROL cost-70e receipts fold re-derived: 5 receipts in published '
      'order [0, 8, 24, 66, 79], per-record marginals equal to the '
      'published 70e head JSON addition records, summary '
      '1233/6614/522131/4884/385854 with published histogram '
      '(c2=2,c4=0 at 959), set-equality and 70e head CSVs (blobs '
      '33fe27c1 / 4561af13) regenerated byte-identically')

# ---------- 4. the cost-71c target genuinely remaining at 1233 ----------
PARENT1 = '00000000000000801202000000200000'
PARENT2 = '00000000000000801202000080000000'
CHILD = '00000000000000801202000080200000'
CHILD_V = int(CHILD, 16)
p1_rows = remG.get(PARENT1, [])
p2_rows = remG.get(PARENT2, [])
assert len(p1_rows) == 28 and sum(int(r['s6_s7_edge_cost']) for r in p1_rows) == 2119
assert len(p2_rows) == 43 and sum(int(r['s6_s7_edge_cost']) for r in p2_rows) == 3268
assert CHILD in {r['s6_hex'] for r in p1_rows} and CHILD in {r['s6_hex'] for r in p2_rows}
holders = sorted(k for k, rows in remG.items() if CHILD in {r['s6_hex'] for r in rows})
assert holders == sorted([PARENT1, PARENT2]), \
    'the child must be a remaining row of exactly the two open class-2 parents'
assert CHILD_V not in s_1233 and CHILD_V in manifest
assert classes.get(PARENT1, 0) & 2 and classes.get(PARENT2, 0) & 2
assert demG.get(CHILD) == {'c1': 0, 'c2': 2, 'c4': 0}
assert int(next(r['s6_s7_edge_cost'] for r in p1_rows if r['s6_hex'] == CHILD)) == 71
# D4 one-stone lift controls: deleting each child stone and
# D4-canonicalizing must reproduce the two open parents (stones 31 and
# 21) and closed rows for the other four stones
child_stones = [i for i in range(121) if CHILD_V >> i & 1]
assert child_stones == [21, 31, 49, 57, 60, 71]
assert f'{canon(CHILD_V & ~(1 << 31)):032x}' == PARENT1, \
    'deleting child stone 31 and canonicalizing must reproduce parent1'
assert f'{canon(CHILD_V & ~(1 << 21)):032x}' == PARENT2, \
    'deleting child stone 21 and canonicalizing must reproduce the second class-2 parent'
for st in (49, 57, 60, 71):
    h = f'{canon(CHILD_V & ~(1 << st)):032x}'
    assert h not in remG, (st, h)
assert CHILD == f'{canon(CHILD_V):032x}', 'the child must be its own D4 canonical representative'
third_rows = remG.get(THIRD_TARGET, [])
assert len(third_rows) == 2 and sum(int(r['s6_s7_edge_cost']) for r in third_rows) == 143
blocked_rows = remG.get(AUDIT_BLOCKED, [])
assert len(blocked_rows) == 10 and sum(int(r['s6_s7_edge_cost']) for r in blocked_rows) == 698
print('CONTROL child genuinely remaining at the reconstructed 1233 head: '
      'parent1 28 rows / 2119, second class-2 parent 43 rows / 3268, both '
      'hold the child row (and no other open parent does), child unsolved '
      'in-manifest, demand c1=0,c2=2,c4=0 re-derived, edge cost 71, '
      'lift stones 31 (parent1) and 21 (parent2) D4-verified with the '
      'other four child stones lifting to closed rows; third coverable '
      'class-2 target 2/143 and audit-blocked 10/698 unchanged')

# ---------- 5. claim v2 + sweep audit re-derivation from the raw batches ----------
claim = json.loads((OUT / 'class2-lane-cost71c-inflight-20261115.json').read_text())
assert claim['schema'] == 'n11-class2-lane-cost71c-inflight-20261115-v2'
assert claim['status'].startswith('completed') and 'fold pending' in claim['status']
assert 'fold' not in claim and 'pending' in claim['fold_pending_note'].lower(), \
    'the claim must record the fold as pending at fold time'
assert claim['unknown_status'].startswith('11x11 empty board: UNKNOWN')
assert claim['s5'] == PARENT1 and claim['s6_child'] == CHILD
assert claim['s6_s7_edge_cost'] == 71
assert claim['demand'] == {'c1': 0, 'c2': 2, 'c4': 0}
assert claim['candidate_count'] == 71 and len(claim['legal_candidates']) == 71
sr = claim['results']['sweep']
WIN_BITS = [24, 112]
assert sr['win7_d10_bits'] == WIN_BITS
assert sr['refuted_d10'] == 69 and sr['capped'] == 0
assert sr['candidate_nodes'] == 94128613
assert sr['batches_completed'] == 9 and sr['pilots_3402'] == 9
assert sr['determinism_rerun_batch5_node_exact'] is True
assert '1233/6614/522131/4884/385854' in claim['chain_head_at_claim']
assert 'a0171d4bb839aeb813d231c7d879d6a89452359f' in claim['chain_head_at_claim']

sweep = json.loads((OUT / 'class2-lane-cost71c-sweep-audit-20261115.json').read_text())
assert sweep['schema'] == 'n11-class2-lane-cost71c-raw-sweep-audit-20261115-v1'
assert sweep['target']['s6_child_hex'] == CHILD and sweep['target']['edge_cost'] == 71
assert sweep['target']['s5_hex'] == PARENT1
agg = sweep['aggregate']
assert agg['candidates'] == 71 and agg['win7_d10_bits'] == WIN_BITS
assert agg['refuted_d10'] == 69 and agg['capped'] == 0
assert agg['candidate_nodes'] == 94128613
WIN_NODES = {24: 457250, 112: 3985676}
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
assert len(seen_bits) == len(set(seen_bits)) == 71
assert sorted(raw_by_bit) == sorted(claim['legal_candidates']), \
    'the 71 swept bits must equal the claim legal_candidates enumeration'
assert batch_node_sum == 94128613
win_raw = sorted(b for b in raw_by_bit if raw_by_bit[b]['loss'] is True)
assert win_raw == WIN_BITS and sum(1 for b in raw_by_bit if raw_by_bit[b]['loss'] is False) == 69
assert sum(r['nodes'] for r in raw_by_bit.values()) == 94128613
assert {b: raw_by_bit[b]['nodes'] for b in WIN_BITS} == WIN_NODES
assert sum(WIN_NODES.values()) == 4442926
wr = sweep['win_roots']
assert sorted(int(k) for k in wr) == WIN_BITS
MOBILITY = {24: 47, 112: 56}
D4_WIN = {}
for bit in WIN_BITS:
    root_v = CHILD_V | (1 << bit)
    assert wr[str(bit)]['root_hex'] == f'{root_v:032x}', bit
    D4_WIN[bit] = f'{canon(root_v):032x}'
    assert wr[str(bit)]['d4_canonical_hex'] == D4_WIN[bit], bit
    assert wr[str(bit)]['root_mobility'] == MOBILITY[bit]
assert len(set(D4_WIN.values())) == 2
assert sweep['d4_duplicate_scan'] == {'roots_compared': 126,
                                     'manifest_files_scanned': 49,
                                     'duplicates': 0}
for k, v in sweep['checks'].items():
    if k == 'distinct_terminal_ranges':
        assert v == [[13, 17]], k
    else:
        assert v is True, k
print('CONTROL sweep audit re-derived from 9 raw batches: 71 candidates '
      'exactly once (== claim enumeration), 2 WIN7-D10 / 69 REFUTED / 0 '
      'capped / 94,128,613 nodes (win sum 4,442,926), roots == '
      'child|1<<bit, 2 distinct D4 orbits, pilots 3402 x9, audit checks '
      'all true, D4 duplicate scan 126 published roots 0 duplicates')

# determinism rerun: batch-5 records node-exact against the raw batch
det_recs = [json.loads(l) for l in
            (OUT / 'class2-lane-cost71c-v16-determinism-rerun-20261115.jsonl').read_text().splitlines()
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
            (OUT / 'class2-lane-cost71c-v15-crosscheck-20261115.jsonl').read_text().splitlines()
            if l.strip()]
v15_pilots = [r for r in v15_recs if r.get('control') == 'pilot_d6']
assert len(v15_pilots) == 1 and v15_pilots[0]['loss'] is False and v15_pilots[0]['nodes'] == 5949
v15_bits = {r['bit']: r for r in v15_recs if 'bit' in r}
assert sorted(v15_bits) == sorted(WIN_BITS + [75, 113, 116])
V15_WIN_NODES = {24: 2695796, 112: 14334967}
for bit in WIN_BITS:
    r = v15_bits[bit]
    assert r['loss'] is True and r['capped'] is False
    assert r['nodes'] == V15_WIN_NODES[bit]
    assert 13 <= r['terminalStoneRange'][0] <= r['terminalStoneRange'][1] <= 17
for bit in (75, 113, 116):
    assert v15_bits[bit]['loss'] is False and raw_by_bit[bit]['loss'] is False, \
        'the v15 refuted anchors must agree with the v16 raw sweep verdicts'
assert sum(V15_WIN_NODES.values()) == 17030763
assert sr['v15_crosscheck']['win_bits_loss_true'] == {str(k): v for k, v in V15_WIN_NODES.items()}
assert sr['v15_crosscheck']['pilots_5949'] == 1
print('CONTROL batch-5 determinism rerun node-exact; v15 cross-engine '
      'anchors: 2 WIN loss=true nodes 2,695,796 / 14,334,967 (sum '
      '17,030,763) agreeing with the claim, refuted anchors bits '
      '75/113/116 loss=false with raw verdict agreement, pilot 5949')

# ---------- 6. assert both published certificates ----------
certdoc = json.loads((OUT / 'class2-lane-cost71c-win7-certificates-20261115.json').read_text())
assert certdoc['schema'] == 'n11-class2-lane-cost71c-win7-certificates-20261115-v1'
assert certdoc['s5_parent_hex'] == PARENT1 and certdoc['s6_child_hex'] == CHILD
assert certdoc['win7_bits'] == WIN_BITS and certdoc['all_verify_pass'] is True
assert 'PENDING' in certdoc['fold_status']
JOIN_MD5_BIT112 = 'e38d80cfd89ccc8e48264c36a9e7701a'
certs = {c['bit']: c for c in certdoc['certificates']}
assert sorted(certs) == WIN_BITS
sums = {'rows': 0, 'extraction_nodes': 0, 'roots': 0}
v15_sum = 0
v16_sum = 0
roots71c = []
covered_orbits = set()
cert_rows_by_bit = {}
for bit in WIN_BITS:
    c = certs[bit]
    root_v = int(c['root_hex'], 16)
    assert root_v == CHILD_V | (1 << bit), bit
    roots71c.append(root_v)
    assert f'{canon(root_v):032x}' == D4_WIN[bit], bit
    assert c['loser_first_moves'] == MOBILITY[bit]
    assert c['sweep_win7_d10_nodes'] == raw_by_bit[bit]['nodes'] == WIN_NODES[bit]
    bg = c['verify']['bigint']
    assert bg['root_stones'] == 7 and bg['root_safe'] is True
    assert bg['root_mobility'] == MOBILITY[bit]
    assert bg['subroots_passed'] == MOBILITY[bit]
    assert bg['union_missing'] == 0 and bg['union_extra'] == 0
    assert bg['rows_sorted_unique'] is True
    assert bg['terminal_range'] == [13, 17]
    ba = c['verify']['bareiss']
    assert ba['root_loser_mobility'] == MOBILITY[bit]
    assert ba['subroots_passed'] == MOBILITY[bit]
    assert ba['union_missing'] == 0 and ba['union_extra'] == 0
    assert ba['terminal_stone_range'] == [13, 15, 17]
    assert ba['consumed_rows'] == c['strategy_rows']
    # each root minus its own added stone canonicalizes to the child
    assert f'{canon(root_v & ~(1 << bit)):032x}' == CHILD, bit
    chain_orbits = {f'{canon(x):032x}' for x in covers(root_v)}
    assert CHILD in chain_orbits and len(chain_orbits) == 7
    covered_orbits |= chain_orbits
    # local bytes
    if bit == 24:
        local = CERTS / 'bit24-root-00000000000000801202000081200000.cert'
        data = local.read_bytes()
        assert len(data) == c['bytes'] == 804827
        assert hashlib.md5(data).hexdigest() == c['md5']
        assert git_blob_sha(local) == c['repo_blob_sha']
    else:
        pdata = b''
        for ppath, psha, pmd5 in zip(c['repo_paths'], c['repo_blob_shas'], c['part_md5s']):
            pl = CERTS / ppath.split('/')[-1]
            pd = pl.read_bytes()
            assert git_blob_sha(pl) == psha, ppath
            assert hashlib.md5(pd).hexdigest() == pmd5, ppath
            pdata += pd
        data = pdata
        # the published manifest records the join md5 with a stray
        # trailing '5' (33 chars, not a valid md5); the true join md5 is
        # asserted here and the typo is recorded in the head JSON and
        # corrected by the claim v3 / erratum published after this fold
        assert c['join_md5_equals_whole_md5'] == JOIN_MD5_BIT112 + '5', \
            'the published manifest must carry the known stray-trailing-5 typo'
        assert hashlib.md5(data).hexdigest() == JOIN_MD5_BIT112
        assert len(data) == c['bytes'] == 2179432
    lines = data.decode().splitlines()
    assert lines[0] == 'n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS'
    assert lines[1] == 'root ' + c['root_hex']
    rows = [l for l in lines[2:] if l.strip()]
    assert len(rows) == c['strategy_rows'] and len(set(rows)) == c['strategy_rows']
    assert rows == sorted(rows), 'certificate rows must be sorted-unique'
    assert all(HEX32.match(l.split(' ')[0]) and l.split(' ')[1].isdigit()
               for l in rows), 'each row must be a 32-hex key plus a move'
    cert_rows_by_bit[bit] = rows
    sums['rows'] += c['strategy_rows']
    sums['extraction_nodes'] += c['extraction_nodes']
    sums['roots'] += 1
    v15_sum += V15_WIN_NODES[bit]
    v16_sum += WIN_NODES[bit]
    del data, lines, rows
assert len(set(roots71c)) == 2
assert sums == {'rows': 82602, 'extraction_nodes': 24639331, 'roots': 2}
assert v15_sum == 17030763 and v16_sum == 4442926
assert certdoc['totals'] == {'strategy_rows': 82602,
                             'extraction_nodes': 24639331, 'roots': 2}
assert len(covered_orbits) == 14 - 1, \
    'the two roots cover exactly 13 distinct S6 orbits (the child shared)'
# the four published verify records re-read
for bit in WIN_BITS:
    for engine, key in (('bigint', 'bigint'), ('bareiss', 'bareiss')):
        rec = json.loads((OUT / ('class2-lane-cost71c-bit%d-%s-verify-20261115.json'
                                % (bit, key))).read_text())
        assert 'independently verified' in rec['verdict']
        assert rec['root_hex'] == certs[bit]['root_hex']
        if engine == 'bigint':
            assert rec['root_stones'] == 7 and rec['root_safe'] is True
            assert rec['root_mobility'] == MOBILITY[bit]
            assert rec['subroots_passed'] == MOBILITY[bit]
            assert rec['union_missing'] == 0 and rec['union_extra'] == 0
        else:
            assert rec['root_loser_mobility'] == MOBILITY[bit]
            assert rec['subroots_passed'] == MOBILITY[bit]
            assert rec['union_missing'] == 0 and rec['union_extra'] == 0
print('CONTROL 2 published certificates asserted against local bytes: '
      'git blob shas (bit24 single file, bit112 two parts joining to the '
      'true md5 - the published manifest field carries a stray trailing 5, '
      'recorded in controls), rows sorted-unique 32-hex, header and root lines, '
      'sub-roots == loser mobility == len(loser_first_moves) == 47/56, '
      'terminal ranges [13,17] / [13,15,17], BigInt and Bareiss verify '
      'records re-read with union 0/0, each root minus its own added '
      'stone canonicalizes to the child, manifest totals re-summed '
      '82,602 rows / 24,639,331 extraction nodes / 2 roots')

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
folded_roots.update(roots70e)
assert not (set(roots71c) & folded_roots), \
    'the 2 cost-71c roots must be disjoint from every folded root'
folded_d4 = {f'{canon(r):032x}' for r in folded_roots}
d4_hits = [(bit, D4_WIN[bit]) for bit in WIN_BITS if D4_WIN[bit] in folded_d4]
assert d4_hits == [], d4_hits
assert len({D4_WIN[bit] for bit in WIN_BITS}) == 2
print('CONTROL root disjointness: 2 new roots vs %d distinct roots whose '
      'covers contributed to the 1233 head (12 baseline verified files + '
      'class4 batch1/2/3 + 8 lane certificate files + 402 chain roots + '
      'the 5 cost-70e receipt roots), raw-hex and D4-canonically '
      'verified with the chain-internal canon(); 2 distinct D4 orbits'
      % len(folded_roots))

# ---------- 8. fold the 2 receipts in published bit order on the 1233 head ----------
EXPECT = {
    24:  {'marginal': 5, 'mim': 1, 'mim_hexes': [CHILD],
          'nonmim_hexes': ['00000000000000001202000081200000',
                           '00000000000000800202000081200000',
                           '00000000000000801002000040800800',
                           '00000000000000801200000081200000']},
    112: {'marginal': 5, 'mim': 1,
          'mim_hexes': ['00000000210000003800000000000200'],
          'nonmim_hexes': ['00000000010000003800000000080200',
                           '00000000210000001800000000080200',
                           '00000000210000002800000000080200',
                           '00000000210000003000000000080200']},
}
s_cur = set(s_1233)
addition = []
zero_mim = []
child_closed_by = None
for bit in WIN_BITS:
    c = certs[bit]
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
    assert sorted(f'{k:032x}' for k in marg - marg_m) == e['nonmim_hexes'], bit
    addition.append({
        'bit': bit, 'root_hex': c['root_hex'], 'd4_canonical_hex': D4_WIN[bit],
        'sweep_nodes': raw_by_bit[bit]['nodes'], 'certified': True,
        'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
        'marginal_non_manifest_hexes': sorted(f'{k:032x}' for k in marg - marg_m),
        'rows': c['strategy_rows'], 'extraction_nodes': c['extraction_nodes'],
        'md5': (c['md5'] if bit == 24 else JOIN_MD5_BIT112),
        'sub_roots_pass': c['loser_first_moves'],
        'v15_anchor_nodes': V15_WIN_NODES[bit],
    })
    if not marg_m:
        zero_mim.append(bit)
    s_cur |= marg
assert child_closed_by == 24, \
    'the child orbit must be closed by the first receipt in published order'
cov2 = set()
for r in roots71c:
    cov2 |= covers(r)
assert s_cur == set(s_1233) | cov2, 'set-equality: s_after == s_1233 UNION covers(2 roots)'
# reverse-order replay (commutativity control)
s_rev = set(s_1233)
for bit in reversed(WIN_BITS):
    s_rev |= covers(int(certs[bit]['root_hex'], 16)) - s_rev
assert s_rev == s_cur, 'fold application must be order-independent'
total_mim = sum(a['marginal_in_manifest'] for a in addition)
total_marg = sum(a['marginal'] for a in addition)
assert total_marg == 10 and total_mim == 2
stH, remH, uniqH, demH = summary_state(s_cur)
assert stH['solved_s6_in_manifest'] == 1233 + total_mim == 1235
assert (stH['unique_remaining_s6'], stH['sum_remaining_cost'],
        stH['s6_needed_by_open_classes'], stH['cost_needed_by_open_classes']) \
        == (6612, 521988, 4882, 385711)
assert stH['remaining_s5_orbits'] == 175
assert stH['hist']['c2=2,c4=0'] == 957
assert CHILD_V in s_cur and CHILD_V in manifest
assert CHILD not in {r['s6_hex'] for r in remH.get(PARENT1, [])}
assert CHILD not in {r['s6_hex'] for r in remH.get(PARENT2, [])}
rows_after_p1 = {r['s6_hex']: int(r['s6_s7_edge_cost']) for r in remH.get(PARENT1, [])}
rows_after_p2 = {r['s6_hex']: int(r['s6_s7_edge_cost']) for r in remH.get(PARENT2, [])}
assert len(rows_after_p1) == 26 and sum(rows_after_p1.values()) == 1976
assert len(rows_after_p2) == 42 and sum(rows_after_p2.values()) == 3197
p1_lost = sorted({r['s6_hex'] for r in p1_rows} - set(rows_after_p1))
p2_lost = sorted({r['s6_hex'] for r in p2_rows} - set(rows_after_p2))
assert p1_lost == [CHILD, '00000000210000003800000000000200']
assert p2_lost == [CHILD]
third_after = remH.get(THIRD_TARGET, [])
assert len(third_after) == 2 and sum(int(r['s6_s7_edge_cost']) for r in third_after) == 143
blocked_after = remH.get(AUDIT_BLOCKED, [])
assert len(blocked_after) == 10 and sum(int(r['s6_s7_edge_cost']) for r in blocked_after) == 698
print('AFTER cost-71c receipts:', json.dumps(
    {k: v for k, v in stH.items() if k != 'hist'}))
print('total marginal=%d marginal_in_manifest=%d; child orbit closed by '
      'bit%d; parent1 %d rows / %d (was 28/2119); second class-2 parent '
      '%d rows / %d (was 43/3268)'
      % (total_marg, total_mim, child_closed_by,
         len(rows_after_p1), sum(rows_after_p1.values()),
         len(rows_after_p2), sum(rows_after_p2.values())))
print('parent1 marginal rows lost:', p1_lost)
print('second class-2 parent marginal rows lost:', p2_lost)

# ---------- 9. outputs ----------
class2 = best(remH, 2)
class4 = best(remH, 4)
result = {
    'schema': 'n11-class-frontier-cost71c-receipts-recompute-20261115-v1',
    'date': '2026-11-15',
    'baseline_main': 'class-frontier-cost70e-receipts-recompute-20261115.json '
                     '(cost-70e receipts fold head '
                     '1233/6614/522131/4884/385854, git blob sha '
                     'a0171d4bb839aeb813d231c7d879d6a89452359f); the head '
                     'JSON, both published 70e head CSVs (blobs 33fe27c1 / '
                     '4561af13), the merged-head CSVs (blobs 4eeca615 / '
                     '0f9905fc) and the 70e claim v3 fold record are '
                     're-asserted byte-exact, the 1227 merged head is '
                     'reconstructed independently by pure geometry and the '
                     'published cost-70e receipts fold is re-derived on it '
                     '(per-record marginals equal to the published 70e '
                     'head JSON addition records) before this fold extends '
                     'the chain',
    'method': 'baseline reconstruction from published artifacts only: every '
              'published input file (29 base inputs, 52 pre-70e published '
              'frontier head JSONs, the 70e head JSON and its 2 CSVs, 4 '
              'merged-head CSVs, 4 cost-70e lane records, 7 cost-71c lane '
              'records, 9 raw sweep batches, v16 determinism rerun, v15 '
              'crosscheck, 3 published certificate files + README, 2 '
              'scripts, 6 MS5 manifest parts) asserted byte-exact against '
              'main by git blob sha; the solved set rebuilt by pure '
              'geometry as winners UNION covers(12 baseline verified '
              'files) UNION covers(class4 batch1/batch2/batch3) UNION '
              'covers(7 class2 lane files) UNION covers(402 distinct '
              'receipt roots recorded in the 52 blob-verified head JSON '
              'addition records), reaching the published 1227 merged head '
              'with staged controls (638/7208/565500, 657/7189/564070, '
              '665/7181/563509 open 5398/423516, 814/7032/552811/5256/'
              '413283) and byte-identical merged-head CSV regeneration; '
              'the published cost-70e receipts fold re-derived in '
              'published order [0, 8, 24, 66, 79] with per-record '
              'marginals equal to the published 70e head JSON addition '
              'records, set-equality and byte-identical 70e head CSV '
              'regeneration, giving the 1233 baseline '
              '1233/6614/522131/4884/385854 with the published histogram; '
              'then the cost-71c child asserted genuinely remaining at '
              '1233 (both open class-2 parents '
              '00000000000000801202000000200000 at 28 rows / 2119 and '
              '00000000000000801202000080000000 at 43 rows / 3268 holding '
              'the child row, the child held by exactly these two open '
              'parents, child unsolved in-manifest, demand c1=0,c2=2,c4=0 '
              're-derived from the remaining incidences, lift stones 31 '
              'against parent1 and 21 against the second class-2 parent '
              'D4-verified, the other four child stones lifting to '
              'closed rows); the published sweep audit re-derived from '
              'the nine raw batch JSONLs (71 candidates exactly once '
              'equal to the claim enumeration, 2 WIN7-D10 / 69 '
              'REFUTED-D10 / 0 capped / 94,128,613 nodes with win sum '
              '4,442,926, roots == child | 1<<bit, 2 distinct D4 orbits, '
              'pilots 3402 x9, batch-5 determinism rerun node-exact), the '
              'v15 cross-engine anchors asserted from the published JSONL '
              '(2 WIN loss=true nodes 2,695,796 / 14,334,967 sum '
              '17,030,763, refuted anchors bits 75/113/116 loss=false '
              'with raw verdict agreement, pilot 5949), both published '
              'certificates asserted against the local certificate bytes '
              '(bit24 single file, bit112 two parts joining to the '
              'manifest md5; rows sorted-unique, sub-roots == loser '
              'mobility == len(loser_first_moves) == 47/56, terminal '
              'ranges, BigInt and Bareiss verify records re-read with '
              'union 0/0, each root minus its own added stone '
              'canonicalizes to the child) with the manifest totals '
              're-summed (82,602 rows / 24,639,331 extraction nodes / 2 '
              'roots); the 2 roots asserted disjoint from every folded '
              'root raw-hex and D4-canonically (497 distinct roots '
              'including the 5 cost-70e receipt roots), then the 2 '
              'receipts folded in published bit order [24, 112] with '
              'every per-record marginal re-derived from the growing '
              'union; the child-orbit closure (bit24), the '
              'both-open-parents-lose-the-child-row control, the '
              'set-equality control s_after == s_1233 UNION covers(2 '
              'roots) and a reverse-order replay control all hold. '
              'Receipts only - no sweep claims',
    'controls': {
        'input_files_byte_exact_vs_main': n_verified,
        'baseline_reconstruction_method': 'published head JSONs + pure '
            'geometry (no runpy chain replay); the reconstructed state '
            'regenerates the published merged-head and 70e head CSVs '
            'byte-identically',
        'staged_controls_reproduced': '638/7208/565500, 657/7189/564070, '
            '665/7181/563509 (open 5398/423516), 814/7032/552811/5256/413283',
        'chain_head_1227_reproduced': True,
        'cost70e_fold_rederived': True,
        'chain_head_1233_reproduced': True,
        'merged_csvs_regenerated_byte_identical': True,
        'cost70e_head_csvs_regenerated_byte_identical': True,
        'child_genuinely_remaining_at_baseline': True,
        'both_open_parents_held_child_row_at_baseline': True,
        'child_held_by_exactly_the_two_open_parents': True,
        'lift_stones_d4_verified': 'parent1 stone 31, parent2 stone 21',
        'sweep_rederived_from_raw_batches': True,
        'determinism_rerun_batch5_node_exact': True,
        'v15_cross_engine_anchors_verified': True,
        'certificates_bytes_md5_blobsha_verified': True,
        'bit112_parts_join_whole_md5': True,
        'verify_records_reread': True,
        'manifest_totals_resummed': True,
        'bit112_join_md5_typo_detected': 'the published manifest / claim v2 / '
            'sweep audit / certificates README record the bit112 join md5 as '
            'e38d80cfd89ccc8e48264c36a9e7701a5 (33 chars, stray trailing 5); '
            'the true 32-char join md5 e38d80cfd89ccc8e48264c36a9e7701a is '
            'asserted here from the joined part bytes; part md5s, the join '
            'and the certificate bytes are unaffected; corrected by the '
            'claim v3 fold record and the md5 erratum',
        'root_disjointness_vs_all_folded_roots': True,
        'd4_duplicate_scan_published_audit': '49 manifests / 126 roots / 0 '
                                             'duplicates (sweep audit, '
                                             're-asserted here)',
        'child_orbit_closure': 'closed by the bit-24 receipt (first in '
                               'published order), of this fold',
        'both_open_parents_lost_child_row': True,
        'set_equality_after_2': 's == s_1233 UNION covers(2 cost-71c roots)',
        'reverse_order_replay_identical': True,
    },
    'target': {
        's5_parent_hex': PARENT1, 's6_child_hex': CHILD, 'edge_cost': 71,
        'open_parents': [PARENT1, PARENT2],
        'demand_at_baseline_1233': {'c1': 0, 'c2': 2, 'c4': 0},
        'child_orbit_closure': 'closed by the bit-24 receipt of this fold',
        'candidates': 71, 'win7_d10': 2, 'refuted_d10': 69, 'capped': 0,
        'candidate_nodes': 94128613,
        'remaining_rows_after': {
            'class2_parent1_orbits': len(rows_after_p1),
            'class2_parent1_edge_cost': sum(rows_after_p1.values()),
            'class2_parent2_orbits': len(rows_after_p2),
            'class2_parent2_edge_cost': sum(rows_after_p2.values()),
            'parent1_rows_lost': p1_lost,
            'parent2_rows_lost': p2_lost,
        },
    },
    'cost71c_addition': addition,
    'totals': {
        'receipts': 2,
        'total_marginal': total_marg,
        'total_marginal_in_manifest': total_mim,
        'zero_marginal_in_manifest': ['bit%d' % b for b in zero_mim],
        'child_closed_by_bit': child_closed_by,
        'certificate_rows': sums['rows'],
        'certificate_bytes': 804827 + 2179432,
        'certificate_extraction_nodes': sums['extraction_nodes'],
        'certificate_sub_roots': 47 + 56,
        'v15_crosscheck_nodes_sum': v15_sum,
        'v16_sweep_win_nodes_sum': v16_sum,
    },
    'frontier_after_cost71c': {
        'solved_s6_in_manifest': stH['solved_s6_in_manifest'],
        'remaining_s5_orbits': stH['remaining_s5_orbits'],
        'unique_remaining_s6': stH['unique_remaining_s6'],
        'sum_remaining_cost': stH['sum_remaining_cost'],
        's6_needed_by_open_classes': stH['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': stH['cost_needed_by_open_classes'],
        'demand_histogram_open_only': stH['hist'],
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
        'cost70f': 'cost-70f WIN7 certificates + sweep audit + v15 '
                   'crosscheck landed on main (merge ec7149cf series) but '
                   'no receipts fold landed; not folded here',
        'parallel_lanes': 'in-flight sweeps/receipts on parallel lanes '
                          '(class4-82b, five-row-q7 and others) are not '
                          'folded here; their folds must re-fetch latest '
                          'main, re-assert the canonical chain head and '
                          'rebase on this new head',
        'sterile_sweeps': 'cost-65k/73f/74f/74c/75/79/79b/70d and other '
                          'sterile sweeps recorded (all REFUTED-D10, 0 '
                          'WIN7-D10, frontier unchanged); no receipts to '
                          'fold',
        'next_fold_baseline': 'this chain head (see frontier_after_cost71c) '
                              'is the new canonical baseline for all '
                              'subsequent folds; assert it before extending',
    },
    'interpretation_guard': 'bookkeeping over published receipts; solved counts '
                            'measure manifest coverage, not the game-theoretic '
                            'value of any position; REFUTED-D10 sweeps prove '
                            'only absence of WIN7-D10; WIN7 certificates prove '
                            'a win within depth 10 from the individual '
                            '7-stone roots only; closing the cost-71c child '
                            'orbit removes the child from both open class-2 '
                            'parents remaining rows but does not solve '
                            'either S5 parent and does not decide class 2 or '
                            'class 4; 11x11 empty board / two-stone root '
                            '{49,60} / S2 {59,60} / class 2 / class 4 remain '
                            'UNKNOWN',
}
(OUT / 'class-frontier-cost71c-receipts-recompute-20261115.json').write_text(
    json.dumps(result, indent=1) + '\n')
print('written class-frontier-cost71c-receipts-recompute-20261115.json')

assert ranking_text(remH) != (OUT / 'class-frontier-s5-ranking-after-cost70e-receipts-20261115.csv').read_text()
(OUT / 'class-frontier-s5-ranking-after-cost71c-receipts-20261115.csv').write_text(
    ranking_text(remH))
with (OUT / 'class-frontier-top-candidates-s6-after-cost71c-receipts-20261115.csv').open(
        'w', newline='') as f:
    f.write(top_candidates_text(remH, demH, class2, class4))
print('written ranking + top-candidates CSVs (after-cost71c-receipts)')
print('next class-2 candidates:', json.dumps(class2[:3]))
print('best class-4:', json.dumps(class4[0]))
