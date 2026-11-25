#!/usr/bin/env python3
"""Independent whole-chain audit of the published fold-chain root inventory
and head bookkeeping (2026-11-15).

Pure-stdlib, published-files-only audit: re-fetches nothing, runs no runpy
chain, re-derives no solved sets. It re-reads the 26 blob-verified base
certificate files, the 52 blob-verified pre-70e chain head JSONs and the 39
post-70e chain head JSONs, and checks:

1. 117 published git blob pins byte-exact (26 base + 52 chain heads + 39
   pinned post-70e heads through the reconciled canonical-1405 endpoint,
   including
   the four v2 pin proposals 71c/70f/73g/70g, now pinned, the 77b/77c
   heads pinned from the 77c baseline quote and the 77d claim's
   chain_head_at_claim, the 75d head pinned from the completed 75d
   claim's output_blob_shas, the 77d / merged-75d-77d / 79a / 80d /
   82c / 83a / 83b / 83c / 83d / 84a / 62a / 58c / 63h / 63i heads
   pinned from their completed claim fold records plus the merged
   63h+63i head pinned from the 63h claim reconciliation record, the
   63j / 65m / 67d / 70g-20261116 heads pinned from their completed
   claim fold records, the merged 63h+63i+63j+65m+67d head pinned from
   the reconciled head's canonical-1400 fork_record quote, and the
   reconciled head pinned from the second-independent-verification
   record and the 76d claim; the merged 63h+63i+63j+65m head's sha is a
   measured pin (the published main file's own git blob sha, no
   successor JSON quotes it));
2. the root inventory: 194 distinct WIN7 base roots (with the single
   intra-base duplicate root enumerated), 402 distinct receipt roots
   recorded in the 52 chain head addition records, and the cumulative
   published-root inventory at every post-70e checkpoint
   (497@1233 ... 569@75d, 577@77d lane-local, 580@merged-75d-77d, 583@79a,
   587@80d, 592@82c, 596@83a, 601@83b, 603@83c, 606@83d, 610@84a,
   616@62a, 649@58c, 650@63h lane-local, 667@63i, 668@merged, 696@63j
   own-branch, 704@65m, 705@merged-4 / 705@67d, 706@merged-5,
   712@70g-fork lane-local, 713@reconciled)
   reconciled
   against each fold's own published folded-root count;
3. D4 orbit structure of the full 713-root inventory: twin pairs
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
   stale-baseline-quote / unverifiable-quote) and the delta arithmetic is
   re-derived from the published marginal records; anomalies must be zero;
   the fork heads (no baseline_main; a fork_record) are classified
   fork-merge-rebase / fork-reconcile with the external-branch mim
   re-derived from the named branch heads' own addition records; the two
   v12 stale-baseline heads (67d, 70g) quote the superseded 63j head
   state 1394 while their completed claims' chain_head_before documents
   the actual baselines (the 65m head 1396 and the 67d branch-D head
   1398), and the corrected-baseline delta arithmetic must reconcile
   exactly;
8. the 77a/77b/77c/75d/77d/79a/80d/82c/83a/83b/83c/83d/84a/62a/58c/63h/
   63i/63j/65m/67d/70g-20261116/merged endpoint heads and
   their completed-
   claim fold records; the merged 75d+77d head cross-checked against the
   77d claim's merged_fold record; the 58c endpoint keeps the published
   head totals.receipts field (the static sweep count 34) separate from
   the 33 folded addition records (the bit-76 certificate is excluded by
   the BigInt verifier terminal guard, as documented in the claim); the
   63h claim was opened at the 1326 head and re-based on the parallel 58c
   fold (both the head JSON rebase_note and the claim fold record assert
   the re-based 1360 baseline); the 63i endpoint head and its completed
   claim fold record, and the merged 63h+63i head that reconciles the
   two-branch receipts fork at the 58c head 1360 (the single 63h bit-89
   receipt re-folded on the 63i branch head 1367; both branch heads
   superseded), cross-checked against the 63h claim reconciliation
   record; the bit-78 duplicate root (== the 75d
   bit-92 receipt root, raw-hex identical) gets an explicit exactly-once
   bookkeeping control (root identity, sequential-marginal convention at
   the shared 1290 baseline, single canonical-line claim via 75d bit-92,
   single inventory entry, merged receipts == 77d receipts minus bit-78);
   the v12 extension: the 63j (29 receipts) / 65m (8) / 67d (1) / 70g (7)
   endpoint heads and their completed claim fold records byte-exact, the
   second receipts fork at the 65m head 1396 (branch C: the 63h bit-89
   receipt re-folded on 1396 by the merged-4 head; branch D: the 67d
   bit-97 receipt on 1396) reconciled by the merged-5 canonical-1400
   head, the cost-70g fork head 1403 (folded on the superseded branch-D
   1398 head) re-based onto the canonical 1400 baseline by the reconciled
   head, and the published second-independent-verification record
   cross-checked against the reconciled head byte-exact (blob sha +
   bytes + both CSV blob shas); the stale method/controls prose of the
   four v12 sweep heads (template-copied numbers contradicting their own
   structured records) recorded as published prose errata.

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
    'class-frontier-cost71c-receipts-recompute-20261115.json': '61af2eb311f938f5ee5bf2bb20d8c1a76787dc87',
    'class-frontier-cost70f-receipts-recompute-20261115.json': '4d0f130e975b6a7bec4759387bd6d54dfe2b6a18',
    'class-frontier-cost72c-receipts-recompute-20261115.json': '42dbb92e1505d05389e840e3368974b1c613b750',
    'class-frontier-cost73g-receipts-recompute-20261115.json': 'e4fb98dc8670fbb85786ab02f017a0a95e357648',
    'class-frontier-cost70g-receipts-recompute-20261115.json': '73890fe34580ec2f869a97a00b3e6400eda30c0a',
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
    'class-frontier-cost84a-receipts-recompute-20261115.json': 'f5624e99f8603ea612a862ed63539011989b5506',
    'class-frontier-cost62a-receipts-recompute-20261116.json': '3989e9ddfa43d0951a9a58c10919ce5087eb8733',
    'class-frontier-cost58c-receipts-recompute-20261116.json': '62a411bb1a6debc33782c07062843650c556c747',
    'class-frontier-cost63h-receipts-recompute-20261115.json': '647498b995770ff87b12e868a5b89015c26be51e',
    'class-frontier-cost63i-receipts-recompute-20261116.json': 'db0288f15f1538293e66146542a938c9ebf8b91c',
    'class-frontier-merged-cost63h-63i-recompute-20261116.json': 'c3ff50364499014a7096151bd9893a6510386c05',
    # v12 pins: the 63j/65m/67d/70g-20261116 heads from their completed
    # claim fold records' output_blob_shas; the merged-4 head's sha is
    # measured from the published main file (no successor JSON quotes
    # it); the merged-5 head from the reconciled head's canonical-1400
    # fork_record quote; the reconciled head from the published
    # second-independent-verification record (and the 76d claim)
    'class-frontier-cost63j-receipts-recompute-20261116.json': '35236daf18e6207d2ed20c168bb8a6111f17d4e8',
    'class-frontier-cost65m-receipts-recompute-20261116.json': '9798a9fc53b2277b17744737511354b1a830c4d2',
    'class-frontier-merged-cost63h-63i-63j-65m-recompute-20261116.json': 'a4cc8e95145a8796ff53b7686bf9cffc3d6e24cb',
    'class-frontier-cost67d-receipts-recompute-20261116.json': '304c6afe68697ee63162a9de5e91fe2b230255c3',
    'class-frontier-merged-cost63h-63i-63j-65m-67d-recompute-20261116.json': '777474faf6730242b7e0080bfcdad390cca3a0ee',
    'class-frontier-cost70g-receipts-recompute-20261116.json': '8eb71c91bd39f5899171dd588156e0c10a763c63',
    'class-frontier-reconciled-canonical1400-cost70g-recompute-20261116.json': 'b3ad19d7bfd48c771d5a6827707a9f26940dc1bb',
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
    'class-frontier-cost77d-receipts-recompute-20261115.json',
    'class-frontier-merged-cost75d-77d-receipts-recompute-20261115.json',
    'class-frontier-cost79a-receipts-recompute-20261115.json',
    'class-frontier-cost80d-receipts-recompute-20261115.json',
    'class-frontier-cost82c-receipts-recompute-20261115.json',
    'class-frontier-cost83a-receipts-recompute-20261115.json',
    'class-frontier-cost83b-receipts-recompute-20261115.json',
    'class-frontier-cost83c-receipts-recompute-20261115.json',
    'class-frontier-cost83d-receipts-recompute-20261115.json',
    'class-frontier-cost84a-receipts-recompute-20261115.json',
    'class-frontier-cost62a-receipts-recompute-20261116.json',
    # v10 extension: the cost-58c (1326 -> 1360) and cost-63h
    # (1360 -> 1362) receipts folds
    'class-frontier-cost58c-receipts-recompute-20261116.json',
    'class-frontier-cost63h-receipts-recompute-20261115.json',
    # v11 extension: the cost-63i (1360 -> 1367) receipts fold and the
    # merged 63h+63i fold (1367 -> 1369) that reconciles the two-branch
    # receipts fork at the 58c head 1360
    'class-frontier-cost63i-receipts-recompute-20261116.json',
    'class-frontier-merged-cost63h-63i-recompute-20261116.json',
    # v12 extension: the second receipts fork at the 63i head 1367 -
    # branch B (63j 1367 -> 1394, then 65m 1394 -> 1396), branch C (the
    # 63h bit-89 receipt re-folded on the 65m head 1396 -> 1398), branch
    # D (the 67d bit-97 receipt on the 65m head 1396 -> 1398), the
    # merged-5 canonical 1400 head (both branch C and branch D receipts
    # on the 1396 baseline), the cost-70g fork head 1403 (7 receipts on
    # the superseded branch-D 1398 head), and the reconciled canonical
    # 1405 head (the 7 receipts re-based on the canonical 1400 baseline)
    'class-frontier-cost63j-receipts-recompute-20261116.json',
    'class-frontier-cost65m-receipts-recompute-20261116.json',
    'class-frontier-merged-cost63h-63i-63j-65m-recompute-20261116.json',
    'class-frontier-cost67d-receipts-recompute-20261116.json',
    'class-frontier-merged-cost63h-63i-63j-65m-67d-recompute-20261116.json',
    'class-frontier-cost70g-receipts-recompute-20261116.json',
    'class-frontier-reconciled-canonical1400-cost70g-recompute-20261116.json',
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
assert n_pins == 117, n_pins
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
    'class-frontier-cost77c-receipts-recompute-20261115.json': 553 + 4 + 8,
    'class-frontier-cost75d-receipts-recompute-20261115.json': 553 + 4 + 8 + 4,
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
    'class-frontier-cost84a-receipts-recompute-20261115.json': 603 + 3 + 4,
    'class-frontier-cost62a-receipts-recompute-20261116.json': 603 + 3 + 4 + 6,
    'class-frontier-cost58c-receipts-recompute-20261116.json': 616 + 33,
    'class-frontier-cost63h-receipts-recompute-20261115.json': 616 + 33 + 1,
    'class-frontier-cost63i-receipts-recompute-20261116.json': 616 + 33 + 18,
    # the merged fold re-folds the single 63h bit-89 receipt on top of
    # the 63i branch head (667 + 1)
    'class-frontier-merged-cost63h-63i-recompute-20261116.json': 616 + 33 + 18 + 1,
    # v12: the second receipts fork - the 63j/65m folds run on the 63i
    # branch lineage (their claims fold on the 1367/1394 heads without a
    # re-base onto the merged 1369 head, as documented by the merged-4
    # fork_record); the merged-4 head re-folds the 63h bit-89 receipt on
    # the 65m head (704 + 1); the 67d fold runs on the 65m head (704+1);
    # the merged-5 head folds both the 63h and 67d receipts on the 1396
    # baseline on the 67d lineage (705 + 1); the 70g fold runs on the
    # superseded branch-D 1398 head (705 + 7); the reconciled head
    # re-folds the 7 70g receipts on the canonical 1400 baseline
    # (706 + 7)
    'class-frontier-cost63j-receipts-recompute-20261116.json':
        616 + 33 + 18 + 29,
    'class-frontier-cost65m-receipts-recompute-20261116.json':
        616 + 33 + 18 + 29 + 8,
    'class-frontier-merged-cost63h-63i-63j-65m-recompute-20261116.json':
        616 + 33 + 18 + 29 + 8 + 1,
    'class-frontier-cost67d-receipts-recompute-20261116.json':
        616 + 33 + 18 + 29 + 8 + 1,
    'class-frontier-merged-cost63h-63i-63j-65m-67d-recompute-20261116.json':
        616 + 33 + 18 + 29 + 8 + 1 + 1,
    'class-frontier-cost70g-receipts-recompute-20261116.json':
        616 + 33 + 18 + 29 + 8 + 1 + 7,
    'class-frontier-reconciled-canonical1400-cost70g-recompute-20261116.json':
        616 + 33 + 18 + 29 + 8 + 1 + 1 + 7,
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
    'class-frontier-cost84a-receipts-recompute-20261115.json':
        'class-frontier-cost83d-receipts-recompute-20261115.json',
    'class-frontier-cost62a-receipts-recompute-20261116.json':
        'class-frontier-cost84a-receipts-recompute-20261115.json',
    'class-frontier-cost58c-receipts-recompute-20261116.json':
        'class-frontier-cost62a-receipts-recompute-20261116.json',
    'class-frontier-cost63h-receipts-recompute-20261115.json':
        'class-frontier-cost58c-receipts-recompute-20261116.json',
    'class-frontier-cost63i-receipts-recompute-20261116.json':
        'class-frontier-cost58c-receipts-recompute-20261116.json',
    'class-frontier-merged-cost63h-63i-recompute-20261116.json':
        'class-frontier-cost63i-receipts-recompute-20261116.json',
    # v12: the second receipts fork baselines (the 63j/65m folds claim the
    # 63i-branch lineage; the merged-4 head claims the 65m head lineage
    # plus the 63h receipt; the 67d fold claims the 65m head lineage;
    # the merged-5 head claims the 67d lineage plus the 63h receipt; the
    # 70g fold claims the 67d branch-D lineage; the reconciled head
    # claims the merged-5 canonical lineage plus the 7 re-based receipts)
    'class-frontier-cost63j-receipts-recompute-20261116.json':
        'class-frontier-cost63i-receipts-recompute-20261116.json',
    'class-frontier-cost65m-receipts-recompute-20261116.json':
        'class-frontier-cost63j-receipts-recompute-20261116.json',
    'class-frontier-merged-cost63h-63i-63j-65m-recompute-20261116.json':
        'class-frontier-cost65m-receipts-recompute-20261116.json',
    'class-frontier-cost67d-receipts-recompute-20261116.json':
        'class-frontier-cost65m-receipts-recompute-20261116.json',
    'class-frontier-merged-cost63h-63i-63j-65m-67d-recompute-20261116.json':
        'class-frontier-cost67d-receipts-recompute-20261116.json',
    'class-frontier-cost70g-receipts-recompute-20261116.json':
        'class-frontier-cost67d-receipts-recompute-20261116.json',
    'class-frontier-reconciled-canonical1400-cost70g-recompute-20261116.json':
        'class-frontier-merged-cost63h-63i-63j-65m-67d-recompute-20261116.json',
}
own_cum_seen = {}

def head_roots_all(name):
    d = json.loads((OUT / name).read_text())
    rr = []
    for k in d:
        if k.endswith('_addition') or k in ('merged_receipts', 'group_additions', 'cost72_fold') \
                or re.fullmatch(r'[a-z0-9]+_addition_on_[a-z0-9]+', k):
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
assert cumulative_report[-1]['audit_document_order_cumulative'] == 713
assert cumulative_report[-1]['fold_own_branch_cumulative'] == 713
assert inventory == (base_int | chain_set) | set().union(*[
    set(head_roots_all(n)) for n in POST70E_ORDER])
assert cumulative_report[-1]['audit_document_order_cumulative'] == 713

# ---------- 3. D4 orbit structure of the 713-root inventory ----------
# the 29 new roots of the 63j fold, the 8 of the 65m fold, the single
# 67d root and the 7 cost-70g roots were asserted raw- and D4-disjoint
# from their own fold lineage inventories by their own fold scripts (the
# merged-4 fold additionally asserts the 63h root disjoint from the 704
# branch-B roots and the cover overlap between the branches zero; the
# merged-5 fold asserts the 67d root disjoint from the 705 folded roots;
# the reconciled fold asserts the 7 roots disjoint from all 706 and the
# cover overlap with the 63h cover zero), so the twin-pair count is
# expected unchanged at 11
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
assert n_orbits == 713 - 11, n_orbits

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
                or k.endswith('_fold') \
                or re.fullmatch(r'[a-z0-9]+_addition_on_[a-z0-9]+', k):
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
# v12: a root with a non-trivial D4 stabilizer has fewer than 7 distinct
# deletion-cover orbits; such records declare their own computed covers
# value and are listed here instead of tripping the covers7 rule (the
# 63j bit-93 root is the first such record in the corpus)
symmetric_covers_exceptions = []
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
            if rec.get('covers') is not None:
                # the record declares its own computed covers value: the
                # audit re-derives it exactly (7 for generic roots, fewer
                # for roots with a non-trivial D4 stabilizer)
                if len(cov_union) != rec['covers']:
                    geom_anomalies.append({'head': name, 'key': key,
                                           'root': f'{rvs[0]:032x}',
                                           'check': 'covers_field',
                                           'value': (rec['covers'], len(cov_union))})
                if len(cov_union) != 7:
                    symmetric_covers_exceptions.append({
                        'head': name, 'key': key, 'bit': rec.get('bit'),
                        'root_hex': f'{rvs[0]:032x}',
                        'covers': len(cov_union),
                        'note': 'the root has a non-trivial D4 stabilizer: '
                                'its 7 deletion covers fall into %d distinct '
                                'D4 orbits, matching the record\'s declared '
                                'covers value' % len(cov_union)})
            elif len(cov_union) != 7:
                geom_anomalies.append({'head': name, 'key': key,
                                       'root': f'{rvs[0]:032x}',
                                       'check': 'covers7', 'value': len(cov_union)})
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

# v11: the merged 63h+63i head declares child_closed_by_bit 89 in its
# totals but carries no target record; its child is the 63h sweep child
# (published in the pinned 63h head) and the single
# cost63h_addition_on_1367 receipt record closes it
_merged_head_name = 'class-frontier-merged-cost63h-63i-recompute-20261116.json'
_dm = json.loads((OUT / _merged_head_name).read_text())
_d63h_child = json.loads(
    (OUT / 'class-frontier-cost63h-receipts-recompute-20261115.json')
    .read_text())['target']['s6_child_hex']
assert (_dm.get('totals', {}) or {}).get('child_closed_by_bit') == 89
_mrec = _dm['cost63h_addition_on_1367']
assert _mrec['bit'] == 89 \
    and _d63h_child in _mrec['marginal_manifest_hexes']
child_closure_report.append({
    'head': _merged_head_name, 'child': _d63h_child,
    'closing_records': [{'key': 'cost63h_addition_on_1367', 'bit': 89,
                         'path': 'cost63h_addition_on_1367'}],
    'n_closing_records': 1,
    'declared_by_totals': 89})

# v12: the merged-4 head declares child_closed_by_bit 89 in its totals
# with no target record; its child is the same 63h sweep child and its
# single cost63h_addition_on_1396 receipt record closes it
_m4_name = 'class-frontier-merged-cost63h-63i-63j-65m-recompute-20261116.json'
_m4 = json.loads((OUT / _m4_name).read_text())
assert (_m4.get('totals', {}) or {}).get('child_closed_by_bit') == 89
_m4rec = _m4['cost63h_addition_on_1396']
assert _m4rec['bit'] == 89 and _d63h_child in _m4rec['marginal_manifest_hexes']
child_closure_report.append({
    'head': _m4_name, 'child': _d63h_child,
    'closing_records': [{'key': 'cost63h_addition_on_1396', 'bit': 89,
                         'path': 'cost63h_addition_on_1396'}],
    'n_closing_records': 1,
    'declared_by_totals': 89})

# v12: the merged-5 head declares both children (child_closed_by_bits:
# cost63h 89 / cost67d 97); its two receipt records close them
_m5_name = 'class-frontier-merged-cost63h-63i-63j-65m-67d-recompute-20261116.json'
_m5 = json.loads((OUT / _m5_name).read_text())
_d67d_child = json.loads(
    (OUT / 'class-frontier-cost67d-receipts-recompute-20261116.json')
    .read_text())['target']['s6_child_hex']
assert _m5['totals']['child_closed_by_bits'] == {
    'cost63h_child': 89, 'cost67d_child': 97}
_m5_63h = _m5['cost63h_addition_on_1396']
_m5_67d = _m5['cost67d_addition_on_1396']
assert _m5_63h['bit'] == 89 and _d63h_child in _m5_63h['marginal_manifest_hexes']
assert _m5_67d['bit'] == 97 and _d67d_child in _m5_67d['marginal_manifest_hexes']
child_closure_report.append({
    'head': _m5_name, 'children': {'cost63h': _d63h_child,
                                   'cost67d': _d67d_child},
    'closing_records': [
        {'key': 'cost63h_addition_on_1396', 'bit': 89,
         'path': 'cost63h_addition_on_1396'},
        {'key': 'cost67d_addition_on_1396', 'bit': 97,
         'path': 'cost67d_addition_on_1396'}],
    'n_closing_records': 2,
    'declared_by_totals': {'cost63h_child': 89, 'cost67d_child': 97}})

# v12: the reconciled head declares child_closed_by_bit 18; its child is
# the cost-70g sweep child (published in the pinned 70g fork head) and
# the bit-18 record of cost70g_addition_on_canonical1400 closes it
_rec_name = ('class-frontier-reconciled-canonical1400-cost70g-'
             'recompute-20261116.json')
_rec = json.loads((OUT / _rec_name).read_text())
assert (_rec.get('totals', {}) or {}).get('child_closed_by_bit') == 18
_d70g_child = json.loads(
    (OUT / 'class-frontier-cost70g-receipts-recompute-20261116.json')
    .read_text())['target']['s6_child_hex']
_rec18 = next(r for r in _rec['cost70g_addition_on_canonical1400']
              if r['bit'] == 18)
assert _d70g_child in _rec18['marginal_manifest_hexes']
child_closure_report.append({
    'head': _rec_name, 'child': _d70g_child,
    'closing_records': [
        {'key': 'cost70g_addition_on_canonical1400', 'bit': 18,
         'path': 'cost70g_addition_on_canonical1400[bit18]'}],
    'n_closing_records': 1,
    'declared_by_totals': 18})

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
        if k.endswith('_addition') or k in ('merged_receipts', 'group_additions') \
                or re.fullmatch(r'[a-z0-9]+_addition_on_[a-z0-9]+', k):
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
# v12: fork heads carry no baseline_main; the fork_record quotes the
# shared baseline state in slash form (the first 5-field slash tuple in
# the first fork_record value that contains one: the merged-63h-63i and
# merged-4 heads quote the 58c head 1360 via common_baseline, the merged-5
# head quotes the 65m head 1396 via common_baseline, the reconciled head
# quotes the merged-5 canonical 1400 head via canonical_1400). The delta
# splits into this head's own re-folded receipt marginals plus the
# marginals folded on the other branches; the external share must equal
# the sum of the named branch heads' own addition-record mims,
# re-derived here from those heads' published records
FORK_BRANCH_HEADS = {
    'class-frontier-merged-cost63h-63i-recompute-20261116.json': [
        'class-frontier-cost63i-receipts-recompute-20261116.json'],
    # the merged-4 head folds on the 1360-baseline fork: the 63i (7),
    # 63j (27) and 65m (2) branch receipts are external to it
    'class-frontier-merged-cost63h-63i-63j-65m-recompute-20261116.json': [
        'class-frontier-cost63i-receipts-recompute-20261116.json',
        'class-frontier-cost63j-receipts-recompute-20261116.json',
        'class-frontier-cost65m-receipts-recompute-20261116.json'],
    # the merged-5 head folds both branch receipts (63h, 67d) on the
    # shared 1396 baseline: no external share
    'class-frontier-merged-cost63h-63i-63j-65m-67d-recompute-20261116.json': [],
    # the reconciled head re-folds the 7 70g receipts on the canonical
    # 1400 baseline: no external share
    'class-frontier-reconciled-canonical1400-cost70g-recompute-20261116.json': [],
}
# v12: two sweep heads quote a stale baseline_main state: their fold
# scripts copied the 63j head's baseline quote without updating it. The
# 67d fold ran on the 65m head 1396 and the 70g fold on the 67d branch-D
# head 1398, both documented by their completed claims' chain_head_before
# (cross-asserted in section 8); the corrected-baseline delta arithmetic
# must reconcile exactly with the head's own receipt records
STALE_BASELINE = {
    'class-frontier-cost67d-receipts-recompute-20261116.json':
        'class-frontier-cost65m-receipts-recompute-20261116.json',
    'class-frontier-cost70g-receipts-recompute-20261116.json':
        'class-frontier-cost67d-receipts-recompute-20261116.json',
}
for name in chain_names + POST70E_ORDER:
    d = json.loads((OUT / name).read_text())
    fk, f = frontier_of(name)
    bm = d.get('baseline_main')
    if bm is None and 'fork_record' in d and f is not None \
            and 'solved_s6_in_manifest' in f:
        # fork head (merged 63h+63i / merged-4 / merged-5 / reconciled):
        # no baseline_main quote; the fork_record quotes the shared
        # baseline state in slash form; the delta splits into the
        # parallel-branch marginals folded by the named branch heads
        # plus this head's own re-folded receipt marginals
        recs = records_of(name)
        fr_text = next(
            (v for v in d['fork_record'].values()
             if isinstance(v, str)
             and re.search(r'(\d+/){4}\d+', v)), None)
        assert fr_text, name
        m5 = re.search(r'(\d+)/(\d+)/(\d+)/(\d+)/(\d+)', fr_text)
        assert m5, name
        base5 = tuple(int(x) for x in m5.groups())
        entry = {'head': name, 'frontier_key': fk,
                 'frontier_solved': f['solved_s6_in_manifest'],
                 'baseline_quote': list(base5),
                 'delta': f['solved_s6_in_manifest'] - base5[0]}
        own_mims = [mim_of(r) for _, _, r in recs
                    if mim_of(r) is not None]
        own_hex = set()
        for _, _, r in recs:
            own_hex.update(hexes_of(r) or [])
        entry['sum_mim'] = sum(own_mims)
        entry['union_mim'] = len(own_hex)
        entry['classification'] = (
            'fork-reconcile' if name ==
            'class-frontier-reconciled-canonical1400-cost70g-'
            'recompute-20261116.json' else 'fork-merge-rebase')
        branch_mim = 0
        for bh in FORK_BRANCH_HEADS[name]:
            branch_mim += sum(mim_of(r) for _, _, r in records_of(bh)
                              if mim_of(r) is not None)
        entry['external_branch_mim'] = entry['delta'] - entry['sum_mim']
        assert entry['external_branch_mim'] == branch_mim, entry
        entry['external_branch_heads'] = list(FORK_BRANCH_HEADS[name])
        entry['quote_state_matches'] = state_index.get(base5, [])
        entry['quote_status'] = ('matched_published_state'
                                 if entry['quote_state_matches']
                                 else 'unmatched_quote')
        pointer = None
        for other in chain_names + POST70E_ORDER:
            if other != name and other in fr_text:
                pointer = other
                break
        entry['prose_pointer_head'] = pointer
        assert entry['quote_status'] == 'matched_published_state', entry
        arith.append(entry)
        continue
    if f is None or bm is None or 'solved_s6_in_manifest' not in f:
        continue
    entry = {'head': name, 'frontier_key': fk,
             'frontier_solved': f['solved_s6_in_manifest']}
    recs = records_of(name)
    own_label = name.replace('class-frontier-', '').replace('class2-lane-', '') \
                     .replace('class4-lane-', '') \
                     .replace('-recompute-20261114.json', '') \
                     .replace('-recompute-20261115.json', '') \
                     .replace('-recompute-20261116.json', '') \
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
    if name in STALE_BASELINE:
        # v12: the quote is a stale copy of the 63j head's baseline quote;
        # the corrected baseline head is declared by the table and its
        # frontier state re-derived here; the corrected delta arithmetic
        # must reconcile with the head's own records exactly
        corr_head = STALE_BASELINE[name]
        _, cf2 = frontier_of(corr_head)
        assert cf2 is not None and 'solved_s6_in_manifest' in cf2, name
        corr5 = [cf2[fl] for fl in STATE_FIELDS]
        entry['classification'] = 'stale-baseline-quote'
        entry['corrected_baseline_head'] = corr_head
        entry['corrected_baseline_state'] = corr5
        entry['delta_from_quoted_baseline'] = delta
        entry['delta'] = f['solved_s6_in_manifest'] - corr5[0]
        assert entry['delta'] == s == u, entry
        assert corr5 != list(five(bm)), entry
    elif delta == 0 and not mims:
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

# v12: stale-baseline quote errata - the quoted 5-tuple is a published
# state (the 63j head 1394), but it is not the fold's actual baseline;
# the corrected baseline (from the completed claim's chain_head_before,
# cross-asserted in section 8) reconciles the delta arithmetic exactly
stale_baseline_errata = []
for a in arith:
    if a.get('classification') == 'stale-baseline-quote':
        stale_baseline_errata.append({
            'head': a['head'],
            'quoted_state': a['baseline_quote'],
            'quote_matches': a['quote_state_matches'],
            'delta_from_quoted_baseline': a['delta_from_quoted_baseline'],
            'corrected_baseline_head': a['corrected_baseline_head'],
            'corrected_baseline_state': a['corrected_baseline_state'],
            'corrected_delta': a['delta'],
            'characterization':
                'the baseline_main quote is a stale copy of the 63j head '
                'baseline quote (a published state, so the quote matches '
                'a real head - the 63j head - not the fold\'s actual '
                'baseline); the fold\'s completed claim chain_head_before '
                'documents the actual baseline, and the corrected-baseline '
                'delta equals the head\'s own sum and union of receipt '
                'marginals exactly'})

assert not arith_anomalies, arith_anomalies

# fork-merge head special entry
FORK_HEAD = 'class-frontier-merged-recompute-after65h65i-warm67b68c-20261115.json'
fork_entry = next((a for a in arith if a['head'] == FORK_HEAD), None)

# v11: the merged 63h+63i fork head entry (fork-merge-rebase)
MERGED63_HEAD = 'class-frontier-merged-cost63h-63i-recompute-20261116.json'
fork63_entry = next((a for a in arith if a['head'] == MERGED63_HEAD),
                    None)
assert fork63_entry is not None
assert fork63_entry['classification'] == 'fork-merge-rebase'
assert fork63_entry['baseline_quote'] == [1360, 6488, 512785, 4758, 376508]
assert fork63_entry['delta'] == 9
assert fork63_entry['sum_mim'] == 2 and fork63_entry['union_mim'] == 2
assert fork63_entry['external_branch_mim'] == 7

# v12: the merged-4 fork head entry (branch C of the second receipts
# fork): the 63h bit-89 receipt re-folded on the 65m head 1396
MERGED4_HEAD = 'class-frontier-merged-cost63h-63i-63j-65m-recompute-20261116.json'
fork4_entry = next((a for a in arith if a['head'] == MERGED4_HEAD), None)
assert fork4_entry is not None
assert fork4_entry['classification'] == 'fork-merge-rebase'
assert fork4_entry['baseline_quote'] == [1360, 6488, 512785, 4758, 376508]
assert fork4_entry['delta'] == 38
assert fork4_entry['sum_mim'] == 2 and fork4_entry['union_mim'] == 2
assert fork4_entry['external_branch_mim'] == 36
assert fork4_entry['external_branch_heads'] == [
    'class-frontier-cost63i-receipts-recompute-20261116.json',
    'class-frontier-cost63j-receipts-recompute-20261116.json',
    'class-frontier-cost65m-receipts-recompute-20261116.json']

# v12: the merged-5 canonical-1400 fork head entry: both branch receipts
# (63h, 67d) folded on the shared 1396 baseline, no external share
MERGED5_HEAD = ('class-frontier-merged-cost63h-63i-63j-65m-67d-'
                'recompute-20261116.json')
fork5_entry = next((a for a in arith if a['head'] == MERGED5_HEAD), None)
assert fork5_entry is not None
assert fork5_entry['classification'] == 'fork-merge-rebase'
assert fork5_entry['baseline_quote'] == [1396, 6452, 510115, 4722, 373838]
assert fork5_entry['delta'] == 4
assert fork5_entry['sum_mim'] == 4 and fork5_entry['union_mim'] == 4
assert fork5_entry['external_branch_mim'] == 0

# v12: the reconciled canonical-1405 head entry (fork-reconcile): the 7
# cost-70g receipts re-based from the superseded branch-D 1398 head onto
# the canonical 1400 baseline
RECONCILED_HEAD = ('class-frontier-reconciled-canonical1400-cost70g-'
                  'recompute-20261116.json')
reconciled_entry = next((a for a in arith if a['head'] == RECONCILED_HEAD),
                       None)
assert reconciled_entry is not None
assert reconciled_entry['classification'] == 'fork-reconcile'
assert reconciled_entry['baseline_quote'] == [1400, 6448, 509842, 4718, 373565]
assert reconciled_entry['delta'] == 5
assert reconciled_entry['sum_mim'] == 5 and reconciled_entry['union_mim'] == 5
assert reconciled_entry['external_branch_mim'] == 0

# v12: the two stale-baseline sweep head entries
stale67d_entry = next(
    (a for a in arith
     if a['head'] == 'class-frontier-cost67d-receipts-recompute-20261116.json'),
    None)
assert stale67d_entry is not None
assert stale67d_entry['classification'] == 'stale-baseline-quote'
assert stale67d_entry['baseline_quote'] == [1394, 6454, 510249, 4724, 373972]
assert stale67d_entry['corrected_baseline_state'] == \
    [1396, 6452, 510115, 4722, 373838]
assert stale67d_entry['delta'] == 2
assert stale67d_entry['sum_mim'] == 2 and stale67d_entry['union_mim'] == 2
stale70g_entry = next(
    (a for a in arith
     if a['head'] == 'class-frontier-cost70g-receipts-recompute-20261116.json'),
    None)
assert stale70g_entry is not None
assert stale70g_entry['classification'] == 'stale-baseline-quote'
assert stale70g_entry['baseline_quote'] == [1394, 6454, 510249, 4724, 373972]
assert stale70g_entry['corrected_baseline_state'] == \
    [1398, 6450, 509974, 4720, 373697]
assert stale70g_entry['delta'] == 5
assert stale70g_entry['sum_mim'] == 5 and stale70g_entry['union_mim'] == 5

# ---------- 7b. canonical-line hex-level exactly-once ----------
# The canonical line from the 1233 baseline to the 83a endpoint: every
# consecutive baseline-quote provenance is already verified by the state
# matching in section 7; branch heads 65l/74g/69i enter the canonical line
# exactly once through the merged-1277 head's merged_receipts; the deferred
# 75d fold is rebased on the 77c head per its deferral note. The extension
# through the 80d endpoint continues via the merged 75d+77d head's
# cost77d_addition (the 11 rebased 77d receipts; the lane-local 77d head
# 1290 -> 1299 stays off the canonical line), then the 79a, 80d, 82c,
# 83a, 83b, 83c and 83d folds.
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
    ('class-frontier-merged-cost75d-77d-receipts-recompute-20261115.json',
     'cost77d_addition'),
    ('class-frontier-cost79a-receipts-recompute-20261115.json',
     'cost79a_addition'),
    ('class-frontier-cost80d-receipts-recompute-20261115.json',
     'cost80d_addition'),
    ('class-frontier-cost82c-receipts-recompute-20261115.json',
     'cost82c_addition'),
    ('class-frontier-cost83a-receipts-recompute-20261115.json',
     'cost83a_addition'),
    ('class-frontier-cost83b-receipts-recompute-20261115.json',
     'cost83b_addition'),
    ('class-frontier-cost83c-receipts-recompute-20261115.json',
     'cost83c_addition'),
    ('class-frontier-cost83d-receipts-recompute-20261115.json',
     'cost83d_addition'),
    ('class-frontier-cost84a-receipts-recompute-20261115.json',
     'cost84a_addition'),
    ('class-frontier-cost62a-receipts-recompute-20261116.json',
     'cost62a_addition'),
    # v10: the canonical line continues through the cost-58c fold
    ('class-frontier-cost58c-receipts-recompute-20261116.json',
     'cost58c_addition'),
    # v11: the receipts chain forks at the 58c head 1360 into the
    # lane-local 63h branch (1360 -> 1362) and the 63i branch
    # (1360 -> 1367); the merged fold re-folds the single 63h bit-89
    # receipt on top of the 1367 head, so the canonical line continues
    # through the 63i head and the merged head while the lane-local
    # 63h head 1362 stays off the line (the 77d precedent)
    ('class-frontier-cost63i-receipts-recompute-20261116.json',
     'cost63i_addition'),
    ('class-frontier-merged-cost63h-63i-recompute-20261116.json',
     'cost63h_addition_on_1367'),
    # v12: the canonical line continues through the cost-63j (29 receipts,
    # 1367 -> 1394) and cost-65m (8 receipts, 1394 -> 1396) folds on the
    # 63i-branch lineage, then to the canonical 1400 head: the merged-5
    # head folds both branch-C (the 63h bit-89 receipt, whose two
    # marginals are already claimed on the line by the merged-1369 head,
    # so its record is NOT re-claimed here) and branch-D (the 67d bit-97
    # receipt) additions on the 1396 baseline; the cost-70g fork head
    # 1403 stays off the canonical line (its 7 receipts were folded on
    # the superseded branch-D 1398 head), and the reconciled canonical
    # 1405 head claims the 7 re-based receipts on the 1400 baseline
    # (the 77d precedent: lane-local heads stay off the line and their
    # receipts are re-based by the reconciliation fold)
    ('class-frontier-cost63j-receipts-recompute-20261116.json',
     'cost63j_addition'),
    ('class-frontier-cost65m-receipts-recompute-20261116.json',
     'cost65m_addition'),
    ('class-frontier-merged-cost63h-63i-63j-65m-67d-recompute-20261116.json',
     'cost67d_addition_on_1396'),
    ('class-frontier-reconciled-canonical1400-cost70g-recompute-20261116.json',
     'cost70g_addition_on_canonical1400'),
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
            '1405 endpoint is claimed as a marginal by exactly one receipt '
            'record on the canonical line (branch marginals 65l/74g/69i '
            'enter once via the merged-1277 merged_receipts; the lane-local '
            '77d head 1299 is off the canonical line and its marginals are '
            'rebased on 1296 by the merged fold, so the bit-78 root - the '
            '75d bit-92 duplicate - is claimed exactly once; the lane-local '
            '63h head 1362 is off the canonical line and its single bit-89 '
            'receipt is re-based on 1367 by the merged 63h+63i fold, so the '
            '63h child and bonus-orbit marginals are claimed exactly once; '
            'the second receipts fork is claimed on the line through the '
            '63j and 65m heads, the 67d record of the merged-5 canonical '
            '1400 head - the 63h marginals are already claimed at the '
            'merged-1369 head, and the merged-4 head adds no new marginal '
            'beyond the 65m head - and the 7 re-based cost-70g receipts of '
            'the reconciled head; the lane-local 70g fork head 1403 stays '
            'off the line, so its receipts are claimed exactly once)',
}

# ---------- 7c. bit-78 duplicate-root exactly-once bookkeeping ----------
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

# ---------- 8. endpoint heads and completed-claim fold records ----------
# claim filename overrides: the 62a claim file follows the landing
# lane's 20261116 date suffix instead of the 20261115 convention
CLAIM_NAME_OVERRIDES = {
    '62a': 'class2-lane-cost62a-inflight-20261116.json',
    # v12: the four new sweep claims follow the 20261116 date suffix
    '63j': 'class2-lane-cost63j-inflight-20261116.json',
    '65m': 'class2-lane-cost65m-inflight-20261116.json',
    '67d': 'class2-lane-cost67d-inflight-20261116.json',
    '70g': 'class2-lane-cost70g-inflight-20261116.json',
}
ENDPOINT_CHECKS = [
    ('77a', 'class-frontier-cost77a-receipts-recompute-20261115.json',
     'frontier_after_cost77a',
     (1282, 6565, 518522, 4835, 382245), 3, 40, [40, 64, 111],
     '1282/6565/518522/4835/382245', 7554),
    ('77b', 'class-frontier-cost77b-receipts-recompute-20261115.json',
     'frontier_after_cost77b',
     (1286, 6561, 518211, 4831, 381934), 4, 9, [9, 12, 59, 105],
     '1286/6561/518211/4831/381934', 8073),
    ('77c', 'class-frontier-cost77c-receipts-recompute-20261115.json',
     'frontier_after_cost77c',
     (1290, 6557, 517923, 4827, 381646), 8, 10,
     [10, 40, 50, 54, 58, 95, 96, 111],
     '1290/6557/517923/4827/381646', 10558),
    ('75d', 'class-frontier-cost75d-receipts-recompute-20261115.json',
     'frontier_after_cost75d',
     (1296, 6551, 517468, 4821, 381191), 4, 12, [12, 40, 92, 111],
     '1296/6551/517468/4821/381191', 8992),
    # the lane-local 77d endpoint (1290 -> 1299): superseded on the
    # canonical line by the merged 75d+77d fold, but its own head record
    # and completed claim must still be internally consistent
    ('77d', 'class-frontier-cost77d-receipts-recompute-20261115.json',
     'frontier_after_cost77d',
     (1299, 6548, 517249, 4818, 380972), 12, 7,
     [7, 12, 39, 58, 62, 64, 66, 78, 94, 96, 108, 111],
     '1299/6548/517249/4818/380972', 13128),
    ('79a', 'class-frontier-cost79a-receipts-recompute-20261115.json',
     'frontier_after_cost79a',
     (1304, 6543, 516873, 4813, 380596), 3, 9, [9, 50, 64],
     '1304/6543/516873/4813/380596', 7452),
    ('80d', 'class-frontier-cost80d-receipts-recompute-20261115.json',
     'frontier_after_cost80d',
     (1305, 6542, 516793, 4812, 380516), 4, 48, [48, 61, 81, 96],
     '1305/6542/516793/4812/380516', 8033),
    ('82c', 'class-frontier-cost82c-receipts-recompute-20261115.json',
     'frontier_after_cost82c',
     (1306, 6541, 516711, 4811, 380434), 5, 16, [16, 37, 47, 71, 82],
     '1306/6541/516711/4811/380434', 8587),
    ('83a', 'class-frontier-cost83a-receipts-recompute-20261115.json',
     'frontier_after_cost83a',
     (1309, 6538, 516477, 4808, 380200), 4, 12, [12, 58, 72, 95],
     '1309/6538/516477/4808/380200', 8068),
    ('83b', 'class-frontier-cost83b-receipts-recompute-20261115.json',
     'frontier_after_cost83b',
     (1312, 6535, 516227, 4805, 379950), 5, 9, [9, 12, 58, 64, 96],
     '1312/6535/516227/4805/379950', 8651),
    ('83c', 'class-frontier-cost83c-receipts-recompute-20261115.json',
     'frontier_after_cost83c',
     (1313, 6534, 516144, 4804, 379867), 2, 16, [16, 82],
     '1313/6534/516144/4804/379867', 6811),
    ('83d', 'class-frontier-cost83d-receipts-recompute-20261115.json',
     'frontier_after_cost83d',
     (1314, 6533, 516061, 4803, 379784), 3, 16, [16, 51, 82],
     '1314/6533/516061/4803/379784', 7407),
    ('84a', 'class-frontier-cost84a-receipts-recompute-20261115.json',
     'frontier_after_cost84a',
     (1318, 6530, 515822, 4800, 379545), 4, 1, [1, 62, 70, 90],
     '1318/6530/515822/4800/379545', 7935),
    ('62a', 'class-frontier-cost62a-receipts-recompute-20261116.json',
     'frontier_after_cost62a',
     (1326, 6522, 515251, 4792, 378974), 6, 7, [7, 15, 35, 76, 81, 98],
     '1326/6522/515251/4792/378974', 9434),
    # v12: the four second-fork sweep endpoints
    ('63j', 'class-frontier-cost63j-receipts-recompute-20261116.json',
     'frontier_after_cost63j',
     (1394, 6454, 510249, 4724, 373972), 29, 1,
     [1, 3, 4, 7, 9, 11, 16, 17, 18, 34, 35, 44, 45, 52, 54, 68, 73, 78,
      81, 87, 88, 92, 93, 99, 102, 103, 105, 107, 113],
     '1394/6454/510249/4724/373972', 23315),
    ('65m', 'class-frontier-cost65m-receipts-recompute-20261116.json',
     'frontier_after_cost65m',
     (1396, 6452, 510115, 4722, 373838), 8, 21,
     [21, 22, 28, 35, 44, 67, 76, 83],
     '1396/6452/510115/4722/373838', 10414),
    ('67d', 'class-frontier-cost67d-receipts-recompute-20261116.json',
     'frontier_after_cost67d',
     (1398, 6450, 509974, 4720, 373697), 1, 97, [97],
     '1398/6450/509974/4720/373697', 6232),
    ('70g', 'class-frontier-cost70g-receipts-recompute-20261116.json',
     'frontier_after_cost70g',
     (1403, 6445, 509589, 4715, 373312), 7, 18,
     [18, 24, 28, 59, 89, 112, 120],
     '1403/6445/509589/4715/373312', 9896),
]
endpoints = {}
claim_crosschecks = []
for tag, hname, fkey, nums, nrec, closebit, order, head_after, nbytes \
        in ENDPOINT_CHECKS:
    hd = json.loads((OUT / hname).read_text())
    fd = hd[fkey]
    ep = {
        'head': hname,
        'git_blob_sha': POST70E_PINS[hname],
        'solved_s6_in_manifest': fd['solved_s6_in_manifest'],
        'unique_remaining_s6': fd['unique_remaining_s6'],
        'sum_remaining_cost': fd['sum_remaining_cost'],
        's6_needed_by_open_classes': fd['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': fd['cost_needed_by_open_classes'],
        'receipts': hd['totals']['receipts'],
        'child_closed_by_bit': hd['totals']['child_closed_by_bit'],
    }
    assert (ep['solved_s6_in_manifest'], ep['unique_remaining_s6'],
            ep['sum_remaining_cost'], ep['s6_needed_by_open_classes'],
            ep['cost_needed_by_open_classes']) == nums, ep
    assert ep['receipts'] == nrec and ep['child_closed_by_bit'] == closebit
    claim_name = CLAIM_NAME_OVERRIDES.get(
        tag, 'class2-lane-cost%s-inflight-20261115.json' % tag)
    claim = json.loads((OUT / claim_name).read_text())
    cf = claim['fold']
    assert cf['chain_head_after'] == head_after
    assert cf['receipts_folded'] == nrec \
        and cf['publication_order'] == order
    assert cf['output_blob_shas']['head_json'] == ep['git_blob_sha']
    assert cf['head_json_bytes'] == nbytes
    sha_c, blen_c = git_blob_sha(OUT / hname)
    assert sha_c == cf['output_blob_shas']['head_json'] and blen_c == nbytes
    endpoints['endpoint_cost%s' % tag] = ep
    claim_crosschecks.append(
        'cost-%s completed claim fold record matches the published head '
        'JSON byte-exact (blob sha + %d bytes); head transition ends at %s'
        % (tag, nbytes, head_after))

# ---------- 8b. merged 75d+77d head crosscheck ----------
# The merged fold's claim lives inside the 77d claim JSON's merged_fold
# record (no separate claim file); its head is pinned and its own
# arithmetic is covered by sections 2/3/7 plus the canonical line.
merged_head = 'class-frontier-merged-cost75d-77d-receipts-recompute-20261115.json'
hmg = json.loads((OUT / merged_head).read_text())
fmg = hmg['frontier_after_merged_75d_77d']
endpoint_merged = {
    'head': merged_head,
    'git_blob_sha': POST70E_PINS[merged_head],
    'solved_s6_in_manifest': fmg['solved_s6_in_manifest'],
    'unique_remaining_s6': fmg['unique_remaining_s6'],
    'sum_remaining_cost': fmg['sum_remaining_cost'],
    's6_needed_by_open_classes': fmg['s6_needed_by_open_classes'],
    'cost_needed_by_open_classes': fmg['cost_needed_by_open_classes'],
    'receipts': hmg['totals']['receipts'],
    'child_closed_by_bit': hmg['totals']['child_closed_by_bit'],
    'child_already_closed_by': hmg['totals']['child_already_closed_by'],
}
assert (endpoint_merged['solved_s6_in_manifest'],
        endpoint_merged['unique_remaining_s6'],
        endpoint_merged['sum_remaining_cost'],
        endpoint_merged['s6_needed_by_open_classes'],
        endpoint_merged['cost_needed_by_open_classes']) == \
    (1302, 6545, 517025, 4815, 380748), endpoint_merged
assert endpoint_merged['receipts'] == 11
assert endpoint_merged['child_closed_by_bit'] is None
assert endpoint_merged['child_already_closed_by'] == \
    'cost-75d bit-92 (cross-cover)'
mf = json.loads(
    (OUT / 'class2-lane-cost77d-inflight-20261115.json').read_text())['merged_fold']
assert mf['status'].startswith('completed')
assert mf['chain_head_before'] == '1296/6551/517468/4821/381191'
assert mf['chain_head_after'] == '1302/6545/517025/4815/380748'
assert mf['receipts_folded'] == 11
assert mf['excluded_receipt'].startswith('bit78')
assert mf['output_blob_shas']['head_json'] == endpoint_merged['git_blob_sha']
assert mf['head_json_bytes'] == 12460
sha_m, blen_m = git_blob_sha(OUT / merged_head)
assert sha_m == mf['output_blob_shas']['head_json'] and blen_m == 12460
endpoints['endpoint_merged_75d_77d'] = endpoint_merged
claim_crosschecks.append(
    'merged-75d-77d completed merged_fold record (inside the 77d claim) '
    'matches the published merged head JSON byte-exact (blob sha + 12460 '
    'bytes); head transition 1296/6551/517468/4821/381191 -> '
    '1302/6545/517025/4815/380748 with the bit-78 receipt excluded')

# ---------- 8k. 58c endpoint + 58c claim crosscheck (v10) ----------
# the 58c fold closes the cost-58 child row of the second candidate S5
# parent: 33 receipts folded from 34 sweep WIN7 certificates (the bit-76
# certificate has terminal range 11..17 and is rejected by the BigInt
# verifier's 13..17 guard, so the head's published totals.receipts field
# - a static copy of the sweep count - is 34 while the addition records
# and the claim's receipts_folded are 33)
h58c = json.loads(
    (OUT / 'class-frontier-cost58c-receipts-recompute-20261116.json').read_text())
f58c = h58c['frontier_after_cost58c']
endpoint58c = {
    'head': 'class-frontier-cost58c-receipts-recompute-20261116.json',
    'git_blob_sha': POST70E_PINS[
        'class-frontier-cost58c-receipts-recompute-20261116.json'],
    'solved_s6_in_manifest': f58c['solved_s6_in_manifest'],
    'unique_remaining_s6': f58c['unique_remaining_s6'],
    'sum_remaining_cost': f58c['sum_remaining_cost'],
    's6_needed_by_open_classes': f58c['s6_needed_by_open_classes'],
    'cost_needed_by_open_classes': f58c['cost_needed_by_open_classes'],
    'receipts': h58c['totals']['receipts'],
    'child_closed_by_bit': h58c['totals']['child_closed_by_bit'],
}
assert (endpoint58c['solved_s6_in_manifest'],
        endpoint58c['unique_remaining_s6'], endpoint58c['sum_remaining_cost'],
        endpoint58c['s6_needed_by_open_classes'],
        endpoint58c['cost_needed_by_open_classes']) == \
    (1360, 6488, 512785, 4758, 376508), endpoint58c
assert endpoint58c['receipts'] == 34
assert endpoint58c['child_closed_by_bit'] == 1
recs58c = h58c['cost58c_addition']
assert len(recs58c) == 33, len(recs58c)
bits58c = [r['bit'] for r in recs58c]
assert bits58c == [1, 3, 6, 18, 22, 24, 32, 35, 42, 43, 44, 56, 66, 67,
                   73, 75, 78, 79, 86, 88, 89, 91, 92, 99, 102, 103, 105,
                   109, 114, 116, 117, 118, 120], bits58c
assert 76 not in bits58c
# the sweep's 34 published certificate files are exactly the 33 folded
# receipt roots plus the excluded bit-76 certificate
certs58c = sorted(p.name for p in
                  (OUT / 'class2-lane-cost58c-certificates').iterdir())
assert len(certs58c) == 34, len(certs58c)
cert_bits58c = {int(c.split('-')[0][3:]) for c in certs58c}
assert cert_bits58c == set(bits58c) | {76}, sorted(cert_bits58c)
claim58c = json.loads(
    (OUT / 'class2-lane-cost58c-inflight-20261116.json').read_text())
cf58c = claim58c['fold']
assert cf58c['status'] == 'completed'
assert cf58c['chain_head_before'] == '1326/6522/515251/4792/378974'
assert cf58c['chain_head_after'] == '1360/6488/512785/4758/376508'
assert cf58c['receipts_folded'] == 33
# the 58c claim records publication_order as a prose string (newer claim
# schema): the folded bit list and the bit-76 exclusion note are asserted
assert isinstance(cf58c['publication_order'], str)
assert cf58c['publication_order'].startswith(
    '[1,3,6,18,22,24,32,35,42,43,44,56,66,67,73,75,78,79,86,88,89,91,'
    '92,99,102,103,105,109,114,116,117,118,120]')
assert 'bit76 excluded' in cf58c['publication_order']
assert cf58c['total_marginal'] == 166
assert cf58c['total_marginal_in_manifest'] == 34
assert cf58c['zero_marginal_in_manifest'] == [42, 44, 56, 91, 99, 105,
                                              109, 118]
assert cf58c['child_orbit_closed_by_bit'] == 1
assert cf58c['parents_after'] == {'parent1': '21 rows / 1454',
                                  'parent2': '27 rows / 1915'}
assert cf58c['output_blob_shas']['head_json'] == endpoint58c['git_blob_sha']
assert cf58c['head_json_bytes'] == 26118
sha58c, blen58c = git_blob_sha(
    OUT / 'class-frontier-cost58c-receipts-recompute-20261116.json')
assert sha58c == cf58c['output_blob_shas']['head_json'] and blen58c == 26118
endpoints['endpoint_cost58c'] = endpoint58c
claim_crosschecks.append(
    'cost-58c completed claim fold record matches the published head JSON '
    'byte-exact (blob sha + 26118 bytes); head transition ends at '
    '1360/6488/512785/4758/376508 with 33 receipts folded (the published '
    'head totals.receipts field is the static sweep count 34; the bit-76 '
    'certificate is excluded by the BigInt verifier terminal guard, as '
    'documented in the claim publication_order note)')

# ---------- 8l. 63h endpoint + 63h claim crosscheck (v10) ----------
# the 63h sweep found a single WIN7-D10 (bit-89) among its 63 candidates;
# the remaining 62 are REFUTED-D10 (absence of a winner win within depth
# 10 only). The claim was opened at the 1326 chain head; the parallel 58c
# fold landed mid-sweep, so the receipt folds on the re-based 58c head
# 1360 (documented by the head JSON rebase_note and the claim fold record)
h63h = json.loads(
    (OUT / 'class-frontier-cost63h-receipts-recompute-20261115.json').read_text())
f63h = h63h['frontier_after_cost63h']
endpoint63h = {
    'head': 'class-frontier-cost63h-receipts-recompute-20261115.json',
    'git_blob_sha': POST70E_PINS[
        'class-frontier-cost63h-receipts-recompute-20261115.json'],
    'solved_s6_in_manifest': f63h['solved_s6_in_manifest'],
    'unique_remaining_s6': f63h['unique_remaining_s6'],
    'sum_remaining_cost': f63h['sum_remaining_cost'],
    's6_needed_by_open_classes': f63h['s6_needed_by_open_classes'],
    'cost_needed_by_open_classes': f63h['cost_needed_by_open_classes'],
    'receipts': h63h['totals']['receipts'],
    'child_closed_by_bit': h63h['totals']['child_closed_by_bit'],
}
assert (endpoint63h['solved_s6_in_manifest'],
        endpoint63h['unique_remaining_s6'], endpoint63h['sum_remaining_cost'],
        endpoint63h['s6_needed_by_open_classes'],
        endpoint63h['cost_needed_by_open_classes']) == \
    (1362, 6486, 512653, 4756, 376376), endpoint63h
assert endpoint63h['receipts'] == 1
assert endpoint63h['child_closed_by_bit'] == 89
recs63h = h63h['cost63h_addition']
assert len(recs63h) == 1 and recs63h[0]['bit'] == 89
# the single receipt claims the sweep child orbit and the bonus orbit as
# its two manifest marginals
assert h63h['target']['s6_child_hex'] in recs63h[0]['marginal_manifest_hexes']
assert recs63h[0]['marginal_in_manifest'] == 2
certs63h = sorted(p.name for p in
                  (OUT / 'class2-lane-cost63h-certificates').iterdir())
assert certs63h == ['bit89-root-00000000020000801202000040080000.cert'], certs63h
claim63h = json.loads(
    (OUT / 'class2-lane-cost63h-inflight-20261115.json').read_text())
cf63h = claim63h['fold']
assert cf63h['status'] == 'completed'
# the claim was opened at the 1326 head (chain_head_at_claim) and folded on
# the re-based 1360 head; the fold record documents the rebase
assert claim63h['chain_head_at_claim'].startswith('1326/')
assert cf63h['chain_head_before'] == '1360/6488/512785/4758/376508'
assert cf63h['chain_head_after'] == '1362/6486/512653/4756/376376'
assert cf63h['receipts_folded'] == 1
assert isinstance(cf63h['publication_order'], str)
assert cf63h['publication_order'].startswith('[89]')
assert '62 candidates are REFUTED-D10' in cf63h['publication_order']
assert cf63h['total_marginal'] == 5
assert cf63h['total_marginal_in_manifest'] == 2
assert cf63h['zero_marginal_in_manifest'] == []
assert cf63h['child_orbit_closed_by_bit'] == 89
assert cf63h['parents_after'] == {'parent1': '20 rows / 1391',
                                  'parent2': '68 rows / 5202',
                                  'parent3': '75 rows / 5416'}
assert cf63h['output_blob_shas']['head_json'] == endpoint63h['git_blob_sha']
assert cf63h['head_json_bytes'] == 6852
sha63h, blen63h = git_blob_sha(
    OUT / 'class-frontier-cost63h-receipts-recompute-20261115.json')
assert sha63h == cf63h['output_blob_shas']['head_json'] and blen63h == 6852
assert '1360/6488/512785/4758/376508' in h63h['rebase_note']
assert '1360/6488/512785/4758/376508' in cf63h['rebase_note']
endpoints['endpoint_cost63h'] = endpoint63h
claim_crosschecks.append(
    'cost-63h completed claim fold record matches the published head JSON '
    'byte-exact (blob sha + 6852 bytes); head transition (re-based) ends at '
    '1362/6486/512653/4756/376376 with the single bit-89 WIN7 receipt '
    '(child orbit closed, two manifest marginals); the claim was opened at '
    'the 1326 head and re-based on the parallel 58c fold per both the '
    'head JSON rebase_note and the claim fold record')

# ---------- 8m. 63i endpoint + 63i claim crosscheck (v11) ----------
# the 63i sweep (parallel lane) found 18 WIN7-D10 among its 63 candidates;
# the remaining 45 are REFUTED-D10 (absence of a winner win within depth
# 10 only). The fold runs on the 58c chain head 1360 (its own claim
# baseline); the 18 receipts close the cost-63 child orbit via bit-30.
h63i = json.loads(
    (OUT / 'class-frontier-cost63i-receipts-recompute-20261116.json')
    .read_text())
f63i = h63i['frontier_after_cost63i']
endpoint63i = {
    'head': 'class-frontier-cost63i-receipts-recompute-20261116.json',
    'git_blob_sha': POST70E_PINS[
        'class-frontier-cost63i-receipts-recompute-20261116.json'],
    'solved_s6_in_manifest': f63i['solved_s6_in_manifest'],
    'unique_remaining_s6': f63i['unique_remaining_s6'],
    'sum_remaining_cost': f63i['sum_remaining_cost'],
    's6_needed_by_open_classes': f63i['s6_needed_by_open_classes'],
    'cost_needed_by_open_classes': f63i['cost_needed_by_open_classes'],
    'receipts': h63i['totals']['receipts'],
    'child_closed_by_bit': h63i['totals']['child_closed_by_bit'],
}
assert (endpoint63i['solved_s6_in_manifest'],
        endpoint63i['unique_remaining_s6'], endpoint63i['sum_remaining_cost'],
        endpoint63i['s6_needed_by_open_classes'],
        endpoint63i['cost_needed_by_open_classes']) == \
    (1367, 6481, 512295, 4751, 376018), endpoint63i
assert endpoint63i['receipts'] == 18
assert endpoint63i['child_closed_by_bit'] == 30
recs63i = h63i['cost63i_addition']
bits63i = [r['bit'] for r in recs63i]
assert bits63i == [30, 32, 41, 45, 54, 61, 62, 66, 77, 81, 99, 105, 107,
                   112, 114, 116, 119, 120], bits63i
assert h63i['target']['s6_child_hex'] in \
    recs63i[0]['marginal_manifest_hexes']
assert recs63i[0]['marginal_in_manifest'] == 1
certs63i = sorted(p.name for p in
                  (OUT / 'class2-lane-cost63i-certificates').iterdir())
assert len(certs63i) == 18, len(certs63i)
cert_bits63i = {int(c.split('-')[0][3:]) for c in certs63i}
assert cert_bits63i == set(bits63i), sorted(cert_bits63i)
claim63i = json.loads(
    (OUT / 'class2-lane-cost63i-inflight-20261116.json').read_text())
cf63i = claim63i['fold']
assert cf63i['status'] == 'completed'
assert cf63i['chain_head_before'] == '1360/6488/512785/4758/376508'
assert cf63i['chain_head_after'] == '1367/6481/512295/4751/376018'
assert cf63i['receipts_folded'] == 18
assert cf63i['publication_order'] == bits63i
assert cf63i['total_marginal'] == 80
assert cf63i['total_marginal_in_manifest'] == 7
assert cf63i['zero_marginal_in_manifest'] == [32, 41, 54, 61, 62, 77, 81,
                                              99, 105, 114, 116]
assert cf63i['child_orbit_closed_by_bit'] == 30
assert cf63i['parents_after'] == {'parent1': '17 rows / 1185',
                                  'parent2': '24 rows / 1704'}
assert cf63i['output_blob_shas']['head_json'] == endpoint63i['git_blob_sha']
assert cf63i['head_json_bytes'] == 16455
sha63i, blen63i = git_blob_sha(
    OUT / 'class-frontier-cost63i-receipts-recompute-20261116.json')
assert sha63i == cf63i['output_blob_shas']['head_json'] \
    and blen63i == 16455
# the 63i head totals zero-marginal list (bit-prefixed strings) is the
# claim's zero_marginal_in_manifest (plain bits)
zm63i = h63i['totals']['zero_marginal_in_manifest']
assert [int(z[len('bit'):]) for z in zm63i] == \
    cf63i['zero_marginal_in_manifest'], zm63i
endpoints['endpoint_cost63i'] = endpoint63i
claim_crosschecks.append(
    'cost-63i completed claim fold record matches the published head JSON '
    'byte-exact (blob sha + 16455 bytes); head transition ends at '
    '1367/6481/512295/4751/376018 with 18 WIN7 receipts folded (child '
    'orbit closed by bit-30; the other 45 candidates are REFUTED-D10)')

# ---------- 8n. merged 63h+63i head + reconciliation crosscheck (v11) ----
# the receipts chain forked at the 58c head 1360: the lane-local 63h fold
# (1360 -> 1362) and the parallel 63i fold (1360 -> 1367). The merged fold
# re-folds the single 63h bit-89 receipt on top of the 1367 head, so the
# merged head supersedes both branch heads as the canonical baseline.
merged63_name = 'class-frontier-merged-cost63h-63i-recompute-20261116.json'
hm63 = json.loads((OUT / merged63_name).read_text())
fm63 = hm63['frontier_after_merged']
endpoint_merged63 = {
    'head': merged63_name,
    'git_blob_sha': POST70E_PINS[merged63_name],
    'solved_s6_in_manifest': fm63['solved_s6_in_manifest'],
    'unique_remaining_s6': fm63['unique_remaining_s6'],
    'sum_remaining_cost': fm63['sum_remaining_cost'],
    's6_needed_by_open_classes': fm63['s6_needed_by_open_classes'],
    'cost_needed_by_open_classes': fm63['cost_needed_by_open_classes'],
    'receipts': hm63['totals']['receipts_folded_here'],
    'child_closed_by_bit': hm63['totals']['child_closed_by_bit'],
}
assert (endpoint_merged63['solved_s6_in_manifest'],
        endpoint_merged63['unique_remaining_s6'],
        endpoint_merged63['sum_remaining_cost'],
        endpoint_merged63['s6_needed_by_open_classes'],
        endpoint_merged63['cost_needed_by_open_classes']) == \
    (1369, 6479, 512163, 4749, 375886), endpoint_merged63
assert endpoint_merged63['receipts'] == 1
assert endpoint_merged63['child_closed_by_bit'] == 89
mrec63 = hm63['cost63h_addition_on_1367']
assert mrec63['root_hex'] == '00000000020000801202000040080000'
# the re-folded receipt is the 63h head's published bit-89 record: same
# root, same covers/marginal structure, rebased on the 1367 head
hrec63h = json.loads(
    (OUT / 'class-frontier-cost63h-receipts-recompute-20261115.json')
    .read_text())['cost63h_addition'][0]
assert mrec63['root_hex'] == hrec63h['root_hex']
assert mrec63['covers'] == hrec63h['covers'] == 7
assert mrec63['marginal_manifest_hexes'] == \
    hrec63h['marginal_manifest_hexes']
assert mrec63['marginal_in_manifest'] == \
    hrec63h['marginal_in_manifest'] == 2
assert hm63['totals']['merged_fold_receipts_total'] == 19
assert hm63['totals']['marginal'] == 5
assert hm63['totals']['marginal_in_manifest'] == 2
# the fork record quotes all three involved head states
assert '1360/6488/512785/4758/376508' in hm63['fork_record']['common_baseline']
assert '1362/6486/512653/4756/376376' in hm63['fork_record']['branch_63h']
assert '1367/6481/512295/4751/376018' in hm63['fork_record']['branch_63i']
assert hm63['parents_at_merged_head'] == {
    'second_candidate_s5': {
        's5_hex': '00000000000000801202000040000000',
        'rows': 16, 'edge_cost': 1122},
    'dual_class2_4_s5': {
        's5_hex': '00000000000000801202000000080000',
        'rows': 68, 'edge_cost': 5202},
    'class4_s5': {
        's5_hex': '00000000000000003800000001800000',
        'rows': 75, 'edge_cost': 5416},
    'cost63i_second_parent': {
        's5_hex': '00000000000000403800000008000000',
        'rows': 24, 'edge_cost': 1704}}
# the 63h claim's reconciliation record documents the merged head with
# its git blob sha; assert it byte-exact against the published file
recon = json.loads(
    (OUT / 'class2-lane-cost63h-inflight-20261115.json')
    .read_text())['reconciliation']
assert '1369/6479/512163/4749/375886' in recon['merged_head']
assert endpoint_merged63['git_blob_sha'] in recon['merged_head']
sha_m63, blen_m63 = git_blob_sha(OUT / merged63_name)
assert sha_m63 == endpoint_merged63['git_blob_sha']
assert blen_m63 == 6135
endpoints['endpoint_merged_63h_63i'] = endpoint_merged63
claim_crosschecks.append(
    'merged 63h+63i head pinned and cross-checked against the 63h claim '
    'reconciliation record: the single bit-89 63h receipt re-folded on the '
    '63i branch head 1367 (same root/covers/manifest marginals as the '
    'lane-local 63h record), head 1369/6479/512163/4749/375886 with the '
    'child orbit closed by bit-89 and the 19 merged receipts total; both '
    'branch heads (1362, 1367) superseded as canonical baselines')

# ---------- 8o. v12 sweep claim fold-detail crosschecks (63j/65m/67d/70g) --
V12_SWEEP_CLAIMS = {
    '63j': ('class2-lane-cost63j-inflight-20261116.json',
            'class-frontier-cost63j-receipts-recompute-20261116.json',
            'cost63j_addition', 138, 27,
            [7, 44, 54, 73, 81, 93, 102, 107], 1,
            {'parent1': '10 rows / 704', 'parent2': '31 rows / 2351'},
            '1367/6481/512295/4751/376018'),
    '65m': ('class2-lane-cost65m-inflight-20261116.json',
            'class-frontier-cost65m-receipts-recompute-20261116.json',
            'cost65m_addition', 35, 2,
            [22, 28, 44, 67, 76, 83], 21,
            {'parent1': '9 rows / 639', 'parent2': '46 rows / 3448'},
            '1394/6454/510249/4724/373972'),
    '67d': ('class2-lane-cost67d-inflight-20261116.json',
            'class-frontier-cost67d-receipts-recompute-20261116.json',
            'cost67d_addition', 5, 2,
            [], 97,
            {'parent1': '8 rows / 572', 'parent2': '82 rows / 6269'},
            '1396/6452/510115/4722/373838'),
    '70g': ('class2-lane-cost70g-inflight-20261116.json',
            'class-frontier-cost70g-receipts-recompute-20261116.json',
            'cost70g_addition', 33, 5,
            [59, 89, 112], 18,
            {'parent1': '7 rows / 502', 'parent2': '48 rows / 3885'},
            '1398/6450/509974/4720/373697'),
}
for tag, (cname, hname, akey, tm, tmm, zm, closebit, pa, before) in \
        sorted(V12_SWEEP_CLAIMS.items()):
    claim = json.loads((OUT / cname).read_text())
    cf = claim['fold']
    assert cf['status'] == 'completed', (tag, cf['status'])
    assert cf['chain_head_before'] == before, (tag, cf['chain_head_before'])
    assert cf['total_marginal'] == tm
    assert cf['total_marginal_in_manifest'] == tmm
    assert cf['zero_marginal_in_manifest'] == zm
    assert cf['child_orbit_closed_by_bit'] == closebit
    assert cf['parents_after'] == pa
    hd = json.loads((OUT / hname).read_text())
    recs = hd[akey]
    assert [r['bit'] for r in recs] == cf['publication_order'], tag
    # the head totals zero-marginal list (bit-prefixed strings) is the
    # claim's zero_marginal_in_manifest (plain bits)
    zmh = hd['totals']['zero_marginal_in_manifest']
    assert [int(z[len('bit'):]) for z in zmh] == zm, (tag, zmh)
    # the head addition records' mim sum equals the claim's totals
    assert sum(r['marginal_in_manifest'] for r in recs) == tmm, tag
    assert sum(r['marginal'] for r in recs) == tm, tag
    # the certificates directory holds exactly the folded receipt roots,
    # except the shared cost-70g directory: it also holds the eight
    # certificates of the earlier pre-70e-era cost-70g fold (20261115,
    # child 00000000000100809002000000000800), whose receipt bits are
    # disjoint from this fold's
    cdir = OUT / ('class2-lane-cost%s-certificates' % tag)
    certs = sorted(p.name for p in cdir.iterdir())
    cert_bits = {int(c.split('-')[0][3:]) for c in certs}
    if tag == '70g':
        old70g_bits = {r['bit'] for r in json.loads(
            (OUT / 'class-frontier-cost70g-receipts-recompute-20261115.json')
            .read_text())['cost70g_addition']}
        assert old70g_bits == {9, 20, 29, 34, 62, 70, 76, 119}, \
            sorted(old70g_bits)
        assert cert_bits == set(cf['publication_order']) | old70g_bits, \
            (tag, cert_bits)
        assert len(certs) == 15, len(certs)
    else:
        assert cert_bits == set(cf['publication_order']), (tag, cert_bits)
    if tag in ('67d', '70g'):
        # the stale-baseline heads: the claim's chain_head_before documents
        # the corrected baseline asserted by the section-7 arith entries
        corr = next(a for a in arith
                    if a['head'] == hname and a.get('classification')
                    == 'stale-baseline-quote')
        assert '/'.join(str(x) for x in corr['corrected_baseline_state']) \
            == before, (tag, before)
    endpoints['endpoint_cost%s' % tag]['claim_fold_details_checked'] = {
        'chain_head_before': before, 'total_marginal': tm,
        'total_marginal_in_manifest': tmm,
        'zero_marginal_in_manifest': zm, 'parents_after': pa,
        'certificates_dir': ('class2-lane-cost%s-certificates' % tag),
        'certificates': len(certs)}
    claim_crosschecks.append(
        'cost-%s completed claim fold record detail cross-check: '
        'chain_head_before %s, %d receipts (publication order matches the '
        'head addition records bit-for-bit), total_marginal %d / '
        'in_manifest %d, zero-marginal bits %s, child closed by bit %d, '
        'parents_after %s, and the certificates directory holds exactly '
        'the folded receipt roots' % (
            tag, before, len(recs), tm, tmm, zm, closebit, pa))

# ---------- 8p. merged-4 head crosscheck (v12) ----------
# the second receipts fork: branch B (63j 1367 -> 1394, then 65m
# -> 1396) and branch A (the merged-1369 head); the merged-4 head
# re-folds the single 63h bit-89 receipt on top of the 65m head 1396
h_m4 = json.loads((OUT / MERGED4_HEAD).read_text())
f_m4 = h_m4['frontier_after_merged']
endpoint_m4 = {
    'head': MERGED4_HEAD,
    'git_blob_sha': POST70E_PINS[MERGED4_HEAD],
    'solved_s6_in_manifest': f_m4['solved_s6_in_manifest'],
    'unique_remaining_s6': f_m4['unique_remaining_s6'],
    'sum_remaining_cost': f_m4['sum_remaining_cost'],
    's6_needed_by_open_classes': f_m4['s6_needed_by_open_classes'],
    'cost_needed_by_open_classes': f_m4['cost_needed_by_open_classes'],
    'receipts': h_m4['totals']['receipts_folded_here'],
    'child_closed_by_bit': h_m4['totals']['child_closed_by_bit'],
}
assert (endpoint_m4['solved_s6_in_manifest'],
        endpoint_m4['unique_remaining_s6'], endpoint_m4['sum_remaining_cost'],
        endpoint_m4['s6_needed_by_open_classes'],
        endpoint_m4['cost_needed_by_open_classes']) == \
    (1398, 6450, 509983, 4720, 373706), endpoint_m4
assert endpoint_m4['receipts'] == 1
assert endpoint_m4['child_closed_by_bit'] == 89
assert h_m4['totals']['merged_fold_receipts_total'] == 56
assert h_m4['totals']['marginal_in_manifest'] == 2
# the re-folded receipt is the published 63h bit-89 record (same root,
# covers and manifest marginals as at the merged-1369 head and the
# lane-local 63h head)
r_m4 = h_m4['cost63h_addition_on_1396']
assert r_m4['root_hex'] == '00000000020000801202000040080000'
assert r_m4['covers'] == 7 and r_m4['marginal_in_manifest'] == 2
assert r_m4['marginal_manifest_hexes'] == mrec63['marginal_manifest_hexes']
assert r_m4['marginal_manifest_hexes'] == hrec63h['marginal_manifest_hexes']
# the fork record quotes the branch head states and their blob shas
fr4 = h_m4['fork_record']
assert '1360/6488/512785/4758/376508' in fr4['common_baseline']
assert '1367/6481/512295/4751/376018' in fr4['common_baseline']
assert '1369/6479/512163/4749/375886' in fr4['branch_A_merged_63h_63i']
assert 'c3ff50364499014a7096151bd9893a6510386c05' in fr4['branch_A_merged_63h_63i']
assert '1367 -> 1394' in fr4['branch_B_63j_65m']
assert '1394 -> 1396' in fr4['branch_B_63j_65m']
assert '35236daf18e6207d2ed20c168bb8a6111f17d4e8' in fr4['branch_B_63j_65m']
assert '9798a9fc53b2277b17744737511354b1a830c4d2' in fr4['branch_B_63j_65m']
assert h_m4['parents_at_merged_head'] == {
    'second_candidate_s5': {
        's5_hex': '00000000000000801202000040000000',
        'rows': 8, 'edge_cost': 576},
    'dual_class2_4_s5': {
        's5_hex': '00000000000000801202000000080000',
        'rows': 68, 'edge_cost': 5202},
    'class4_s5': {
        's5_hex': '00000000000000003800000001800000',
        'rows': 75, 'edge_cost': 5416},
    'cost63i_second_parent': {
        's5_hex': '00000000000000403800000008000000',
        'rows': 24, 'edge_cost': 1704}}
sha_m4, blen_m4 = git_blob_sha(OUT / MERGED4_HEAD)
assert sha_m4 == endpoint_m4['git_blob_sha'] and blen_m4 == 7265
# the merged-5 head's fork record quotes this head's state
h_m5x = json.loads((OUT / MERGED5_HEAD).read_text())
assert '1398/6450/509983/4720/373706' in \
    h_m5x['fork_record']['branch_C_merged_63h_63i_63j_65m']
assert MERGED4_HEAD in \
    h_m5x['fork_record']['branch_C_merged_63h_63i_63j_65m']
endpoints['endpoint_merged_63h_63i_63j_65m'] = endpoint_m4
claim_crosschecks.append(
    'merged 63h+63i+63j+65m head (branch C of the second receipts fork) '
    'pinned and cross-checked: the single bit-89 63h receipt re-folded on '
    'the 65m head 1396 (same root/covers/manifest marginals as at the '
    'merged-1369 head), head 1398/6450/509983/4720/373706 with the child '
    'orbit closed by bit-89 and the 56 merged receipts total (63i 18 + '
    '63j 29 + 65m 8 + 63h 1); the branch head states and blob shas in '
    'the fork record match the pinned heads; this head\'s own git blob '
    'sha is a measured pin (no successor JSON quotes it, the merged-5 '
    'fork record cites it by state and commit only)')

# ---------- 8q. merged-5 canonical-1400 head crosscheck (v12) ----------
h_m5 = h_m5x
f_m5 = h_m5['frontier_after_merged']
endpoint_m5 = {
    'head': MERGED5_HEAD,
    'git_blob_sha': POST70E_PINS[MERGED5_HEAD],
    'solved_s6_in_manifest': f_m5['solved_s6_in_manifest'],
    'unique_remaining_s6': f_m5['unique_remaining_s6'],
    'sum_remaining_cost': f_m5['sum_remaining_cost'],
    's6_needed_by_open_classes': f_m5['s6_needed_by_open_classes'],
    'cost_needed_by_open_classes': f_m5['cost_needed_by_open_classes'],
    'receipts': h_m5['totals']['receipts_folded_here'],
    'child_closed_by_bits': h_m5['totals']['child_closed_by_bits'],
}
assert (endpoint_m5['solved_s6_in_manifest'],
        endpoint_m5['unique_remaining_s6'], endpoint_m5['sum_remaining_cost'],
        endpoint_m5['s6_needed_by_open_classes'],
        endpoint_m5['cost_needed_by_open_classes']) == \
    (1400, 6448, 509842, 4718, 373565), endpoint_m5
assert endpoint_m5['receipts'] == 2
assert endpoint_m5['child_closed_by_bits'] == {
    'cost63h_child': 89, 'cost67d_child': 97}
assert h_m5['totals']['merged_fold_receipts_total'] == 57
assert h_m5['totals']['marginal_in_manifest'] == {
    'cost63h': 2, 'cost67d': 2}
# both records are the published receipts: the 63h record equals the
# merged-4 record and the 67d record equals the 67d head's bit-97 record
assert h_m5['cost63h_addition_on_1396'] == h_m4['cost63h_addition_on_1396']
r67_head = json.loads(
    (OUT / 'class-frontier-cost67d-receipts-recompute-20261116.json')
    .read_text())['cost67d_addition'][0]
r67_m5 = h_m5['cost67d_addition_on_1396']
for k in ('bit', 'root_hex', 'covers', 'marginal', 'marginal_in_manifest',
          'marginal_manifest_hexes', 'marginal_non_manifest_hexes'):
    assert r67_m5[k] == r67_head[k], (k, r67_m5[k], r67_head[k])
# the fork record quotes the common 1396 baseline and both branch heads
fr5 = h_m5['fork_record']
assert '1396/6452/510115/4722/373838' in fr5['common_baseline']
assert '9798a9fc53b2277b17744737511354b1a830c4d2' in fr5['common_baseline']
assert '1398/6450/509983/4720/373706' in fr5['branch_C_merged_63h_63i_63j_65m']
assert '1398/6450/509974/4720/373697' in fr5['branch_D_cost67d']
assert 'class-frontier-cost67d-receipts-recompute-20261116.json' in \
    fr5['branch_D_cost67d']
assert h_m5['parents_at_merged_head'] == {
    'second_candidate_s5': {
        's5_hex': '00000000000000801202000040000000',
        'rows': 7, 'edge_cost': 509},
    'dual_class2_4_s5': {
        's5_hex': '00000000000000801202000000080000',
        'rows': 68, 'edge_cost': 5202},
    'class4_s5': {
        's5_hex': '00000000000000003800000001800000',
        'rows': 75, 'edge_cost': 5416},
    'cost67d_parent2': {
        's5_hex': '00000000000000801002000001080000',
        'rows': 82, 'edge_cost': 6269},
    'cost63i_second_parent': {
        's5_hex': '00000000000000403800000008000000',
        'rows': 24, 'edge_cost': 1704}}
sha_m5, blen_m5 = git_blob_sha(OUT / MERGED5_HEAD)
assert sha_m5 == endpoint_m5['git_blob_sha'] and blen_m5 == 7460
endpoints['endpoint_merged_63h_63i_63j_65m_67d'] = endpoint_m5
claim_crosschecks.append(
    'merged 63h+63i+63j+65m+67d canonical-1400 head pinned and '
    'cross-checked: both branch receipts (the 63h bit-89 record, '
    'identical to the merged-4 record, and the 67d bit-97 record, '
    'identical to the 67d head record) folded on the shared 1396 '
    'baseline, head 1400/6448/509842/4718/373565 with both children '
    'closed (bits 89/97) and the 57 merged receipts total (63i 18 + '
    '63j 29 + 65m 8 + 63h 1 + 67d 1); the reconciled head\'s '
    'canonical-1400 fork_record quote of this head (blob sha + 7460 '
    'bytes) matches the pinned file byte-exact')

# ---------- 8r. reconciled canonical-1405 head crosscheck (v12) ----------
h_rc = json.loads((OUT / RECONCILED_HEAD).read_text())
f_rc = h_rc['frontier_after_reconciled']
endpoint_rc = {
    'head': RECONCILED_HEAD,
    'git_blob_sha': POST70E_PINS[RECONCILED_HEAD],
    'solved_s6_in_manifest': f_rc['solved_s6_in_manifest'],
    'unique_remaining_s6': f_rc['unique_remaining_s6'],
    'sum_remaining_cost': f_rc['sum_remaining_cost'],
    's6_needed_by_open_classes': f_rc['s6_needed_by_open_classes'],
    'cost_needed_by_open_classes': f_rc['cost_needed_by_open_classes'],
    'receipts': h_rc['totals']['receipts'],
    'child_closed_by_bit': h_rc['totals']['child_closed_by_bit'],
}
assert (endpoint_rc['solved_s6_in_manifest'],
        endpoint_rc['unique_remaining_s6'], endpoint_rc['sum_remaining_cost'],
        endpoint_rc['s6_needed_by_open_classes'],
        endpoint_rc['cost_needed_by_open_classes']) == \
    (1405, 6443, 509457, 4713, 373180), endpoint_rc
assert endpoint_rc['receipts'] == 7
assert endpoint_rc['child_closed_by_bit'] == 18
t_rc = h_rc['totals']
assert t_rc['total_marginal'] == 33 and t_rc['total_marginal_in_manifest'] == 5
assert t_rc['zero_marginal_in_manifest'] == ['bit59', 'bit89', 'bit112']
assert t_rc['marginal_in_manifest_at_branch_D_baseline'] == 5
assert t_rc['mim_shrink_vs_branch_D_baseline'] == 0
# the 7 re-based receipts are the published 70g fork head's records:
# same bits, roots, marginal counts and manifest marginals (the mim
# shrink vs the branch-D baseline is 0 and the overlap with the 63h
# cover is 0, so the marginals are unchanged by the re-base)
recs_rc = h_rc['cost70g_addition_on_canonical1400']
recs_70g = json.loads(
    (OUT / 'class-frontier-cost70g-receipts-recompute-20261116.json')
    .read_text())['cost70g_addition']
assert [r['bit'] for r in recs_rc] == [r['bit'] for r in recs_70g]
for a, b in zip(recs_rc, recs_70g):
    assert a['root_hex'] == b['root_hex'], a['bit']
    assert a['marginal'] == b['marginal'], a['bit']
    assert a['marginal_in_manifest'] == b['marginal_in_manifest'], a['bit']
    assert a['marginal_manifest_hexes'] == b['marginal_manifest_hexes'], \
        a['bit']
# the fork record quotes both superseded heads with their blob shas
fr_rc = h_rc['fork_record']
assert '1400/6448/509842/4718/373565' in fr_rc['canonical_1400']
assert '777474faf6730242b7e0080bfcdad390cca3a0ee' in fr_rc['canonical_1400']
assert '7460 bytes' in fr_rc['canonical_1400']
assert '1403/6445/509589/4715/373312' in fr_rc['cost70g_fork_1403']
assert '1398/6450/509974/4720/373697' in fr_rc['cost70g_fork_1403']
assert '8eb71c91bd39f5899171dd588156e0c10a763c63' in fr_rc['cost70g_fork_1403']
assert '9896 bytes' in fr_rc['cost70g_fork_1403']
# the coordination notes flag the 75e/76c inflight claims as re-base
# required onto this head
assert '75e' in h_rc['coordination']['cost75e_inflight_claim']
assert '76c' in h_rc['coordination']['cost76c_inflight_claim']
sha_rc, blen_rc = git_blob_sha(OUT / RECONCILED_HEAD)
assert sha_rc == endpoint_rc['git_blob_sha'] and blen_rc == 11352
# the published second-independent-verification record pins this head
# byte-exact and quotes both CSV blob shas
ver = json.loads((OUT / 'class2-lane-reconciled-canonical1405-'
                  'second-independent-verification-20261116.json')
                 .read_text())
assert ver['result'].startswith('VERIFIED')
assert 'b3ad19d7bfd48c771d5a6827707a9f26940dc1bb' in ver['verified']
assert '11352 bytes' in ver['verified']
assert ver['controls']['frontier'] == '1405/6443/509457/4713/373180'
assert ver['controls']['published_head_json_blob_pinned'] == \
    'b3ad19d7bfd48c771d5a6827707a9f26940dc1bb'
rcsv = 'class-frontier-s5-ranking-after-reconciled-canonical1400-cost70g-20261116.csv'
tcsv = ('class-frontier-top-candidates-s6-after-reconciled-canonical1400-'
        'cost70g-20261116.csv')
assert ver['controls']['ranking_csv_byte_identical'].startswith(
    '26fa720b9935ea3bfa1445409d941a5063c52694'), ver['controls']
assert '7535 B' in ver['controls']['ranking_csv_byte_identical']
assert ver['controls']['top_candidates_csv_byte_identical'].startswith(
    'c3433eeecccf0098a04f227af876b37196c7c0a5'), ver['controls']
assert '3801 B' in ver['controls']['top_candidates_csv_byte_identical']
sha_rcsv, blen_rcsv = git_blob_sha(OUT / rcsv)
sha_tcsv, blen_tcsv = git_blob_sha(OUT / tcsv)
assert sha_rcsv == '26fa720b9935ea3bfa1445409d941a5063c52694' \
    and blen_rcsv == 7535, (sha_rcsv, blen_rcsv)
assert sha_tcsv == 'c3433eeecccf0098a04f227af876b37196c7c0a5' \
    and blen_tcsv == 3801, (sha_tcsv, blen_tcsv)
endpoints['endpoint_reconciled_canonical1405'] = endpoint_rc
claim_crosschecks.append(
    'reconciled canonical-1405 head pinned and cross-checked: the 7 '
    'cost-70g receipts re-based from the superseded branch-D 1398 head '
    'onto the canonical 1400 baseline (per-bit roots, marginal counts '
    'and manifest marginals identical to the 70g fork head records, '
    'mim shrink 0), head 1405/6443/509457/4713/373180 with the child '
    'orbit closed by bit-18; the published second-independent-'
    'verification record pins this head byte-exact (blob sha + 11352 '
    'bytes + both CSV blob shas verified against the local files) and '
    'the coordination notes flag the 75e/76c inflight claims for '
    're-base onto this head')

# ---------- 8s. v12 published prose errata (sweep heads) ----------
# the four v12 sweep heads' method/controls prose carries stale
# template numbers copied from the 63j fold script (the 67d/70g
# baseline lines quote 1394, the closure/bit/root counts contradict the
# heads' own structured records); the structured records (target,
# totals, addition records, claims) are internally consistent and are
# the audit basis - the prose is recorded as a published erratum, not
# an arithmetic anomaly
V12_PROSE_ERRATA = {
    'class-frontier-cost63j-receipts-recompute-20261116.json': [
        'method quotes 45 REFUTED-D10 / 40,372,308 nodes (target: 34 '
        'refuted / 67,040,399 nodes)',
        'method/controls quote 18 roots disjoint vs 649 (29 roots vs '
        'the 667 63i-branch lineage; the 649 figure is the pre-63i '
        'count)',
        'controls set_equality_after_18 (29 receipts folded)'],
    'class-frontier-cost65m-receipts-recompute-20261116.json': [
        'method quotes the 63j sweep numbers (63 candidates / 45 '
        'REFUTED / 40,372,308 nodes; target: 65 candidates / 57 '
        'refuted / 74,130,403 nodes)',
        'method/controls quote 18 roots disjoint vs 649 (8 roots '
        'folded)',
        'target.child_orbit_closure and the controls closure prose '
        'say bit-1 (the child is closed by bit 21 per the totals, '
        'the claim and the bit-21 receipt record)',
        'controls set_equality_after_18 (8 receipts folded)'],
    'class-frontier-cost67d-receipts-recompute-20261116.json': [
        'method/controls quote the 63j baseline 1394 (actual baseline '
        'the 65m head 1396 per the claim chain_head_before)',
        'method quotes the 63j sweep numbers (63 candidates / 8 '
        'WIN7 / 45 REFUTED / 40,372,308 nodes; target: 67 candidates '
        '/ 1 win / 66 refuted / 65,246,890 nodes)',
        'method/controls quote 18 roots disjoint vs 649 (1 root '
        'folded)',
        'target.child_orbit_closure and the controls closure prose '
        'say bit-1 (the child is closed by bit 97 per the totals, '
        'the claim and the bit-97 receipt record)',
        'controls set_equality_after_18 (1 receipt folded)'],
    'class-frontier-cost70g-receipts-recompute-20261116.json': [
        'method/controls quote the 63j baseline 1394 (actual baseline '
        'the 67d branch-D head 1398 per the claim chain_head_before)',
        'method quotes 8 receipts / 18 roots (7 receipts folded)',
        'method quotes the 63j sweep numbers (63 candidates / 8 '
        'WIN7 / 45 REFUTED / 40,372,308 nodes; target: 70 candidates '
        '/ 7 win / 63 refuted / 124,066,734 nodes)',
        'target.child_orbit_closure and the controls closure prose '
        'say bit-1 (the child is closed by bit 18 per the totals, '
        'the claim and the bit-18 receipt record)',
        'controls set_equality_after_18 (7 receipts folded)'],
}
prose_errata_v12 = []
for hname, items in V12_PROSE_ERRATA.items():
    hd = json.loads((OUT / hname).read_text())
    closebit_actual = hd['totals']['child_closed_by_bit']
    if closebit_actual != 1:
        # the structured-data prose contradiction the erratum documents:
        # the target closure prose says bit-1, the totals say otherwise
        assert 'bit-1' in hd['target']['child_orbit_closure'], hname
    entry = {'head': hname, 'prose_errata': items,
             'child_closed_by_bit_structured': closebit_actual,
             'basis': 'the structured records (target counts, totals, '
                      'addition records, completed claim) are internally '
                      'consistent and cross-verified; the method/controls '
                      'prose is template-copied from the 63j fold script '
                      'and is not used by any audit control'}
    prose_errata_v12.append(entry)

# ---------- output ----------
result = {
    'schema': 'n11-class2-lane-published-chain-roots-independent-audit-20261115-v12',
    'date': '2026-11-16',
    'verdict': 'AUDIT PASSED',
    'method': 'independent whole-chain audit over the published files only '
              '(no runpy chain replay, no solved-set reconstruction): 117 git '
              'blob pins asserted byte-exact (26 base certificate files + 52 '
              'pre-70e chain head JSONs + 39 pinned post-70e chain heads '
              'through the reconciled canonical-1405 endpoint, the v2 pin '
              'proposals '
              '71c/70f/73g/70g now pinned, the 77b head pinned from the 77c '
              'baseline quote plus the 77c head pinned from the 77d claim '
              'chain_head_at_claim, the 75d head pinned from the completed '
              '75d claim output_blob_shas, the 77d / merged-75d-77d / 79a / '
              '80d / 82c / 83a / 83b / 83c / 83d / 84a / 62a / 58c / 63h / '
              '63i / merged / 63j / 65m / 67d / 70g heads pinned from their '
              'completed claim fold records, the merged-5 head pinned from '
              'the reconciled head canonical-1400 fork_record quote, the '
              'reconciled head pinned from the second-independent-'
              'verification record, and the merged-4 head pinned by its '
              'measured git blob sha), the root '
              'inventory rebuilt from the published records (194 distinct '
              'WIN7 base roots with the single intra-base duplicate root '
              'enumerated, 402 distinct receipt roots from the 52 chain head '
              'addition records, 104 base-roots re-listed by chain records), '
              'the cumulative published-root inventory reconciled at every '
              'post-70e checkpoint against each fold script\u2019s own '
              'published folded-root count (497@1233, 499@71c, 503@70f, '
              '512@72c, 520@73g, 528@70g, 532@73h, 534@65l / 542@74g / '
              '546@69i branch lines, 544@merged-65l-74g, 548@merged-65l-'
              '74g-69i, 550@76b, 553@77a, 557@77b, 565@77c, 569@75d, '
              '577@77d lane-local, 580@merged-75d-77d, 583@79a, 587@80d, '
              '592@82c, 596@83a, 601@83b, 603@83c, 606@83d, 610@84a, '
              '616@62a, 649@58c, 650@63h lane-local, 667@63i, 668@merged, '
              '696@63j own-branch, 704@65m, 705@merged-4 / 705@67d, '
              '706@merged-5, 712@70g-fork lane-local, 713@reconciled), the '
              'D4 orbit structure of the full inventory audited (702 distinct '
              'D4 orbits over 713 roots; 11 twin pairs with full provenance; '
              'multi-provenance roots enumerated), per-record geometry '
              'checked for every published receipt record and every nested '
              'group-additions record, child-orbit closure bookkeeping '
              'checked at every head declaring a child (including the three '
              'v12 fork/reconciled heads with children declared in their '
              'totals only), convention-external '
              'receipts scanned (each must be a D4 twin of an inventoried '
              'orbit, keeping the orbit inventory complete as a SET), and '
              'the head arithmetic re-derived from the published marginal '
              'records with zero anomalies (the four v12 fork heads '
              'classified fork-merge-rebase / fork-reconcile with their '
              'external-branch marginals re-derived from the named branch '
              'heads; the two stale-baseline sweep heads classified '
              'stale-baseline-quote with the corrected baseline taken from '
              'their completed claims and the corrected delta reconciled '
              'exactly); the canonical-line hex-level '
              'exactly-once check extended to the reconciled canonical-1405 '
              'endpoint (the 63j and 65m folds on the 63i-branch lineage, '
              'the 67d record of the merged-5 canonical-1400 head, and the '
              '7 re-based cost-70g receipts of the reconciled head; the '
              '63h marginals claimed once at the merged-1369 head, the '
              'lane-local merged-4 head adds no new marginal, and the '
              '70g-fork head 1403 stays off the line); '
              'the '
              'bit-78 duplicate root (== the 75d bit-92 receipt root) held '
              'to an explicit exactly-once bookkeeping control; the '
              '77a/77b/77c/75d/77d/79a/80d/82c/83a/83b/83c/83d/84a/62a/58c/63h/'
              '63i/63j/65m/67d/70g endpoint heads '
              'and their '
              'completed-claim fold records cross-checked byte-exact, the '
              'merged 75d+77d head cross-checked against the 77d claim\u2019s '
              'merged_fold record, the merged 63h+63i and merged-4 and '
              'merged-5 heads and the reconciled head pinned and '
              'cross-checked against their successor heads\u2019 fork_record '
              'quotes, the reconciled head further cross-checked against the '
              'published second-independent-verification record (blob sha '
              '+ bytes + both CSV blob shas), and the stale method/controls '
              'prose of the four v12 sweep heads recorded as published '
              'prose errata',
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
                                'published_hex_errata': hex_errata,
                                'symmetric_covers_exceptions':
                                    symmetric_covers_exceptions},
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
        'fork_merge_head_63h_63i': fork63_entry,
        'fork_merge_head_63h_63i_63j_65m': fork4_entry,
        'fork_merge_head_63h_63i_63j_65m_67d': fork5_entry,
        'reconciled_head': reconciled_entry,
        'stale_baseline_quote_errata': stale_baseline_errata,
        'v12_method_prose_errata': prose_errata_v12,
        'canonical_line_hex_exactly_once': canonical_line_report,
        'bit78_duplicate_root_bookkeeping': bit78_report,
        'endpoint_heads': endpoints,
        'completed_claim_crosschecks': claim_crosschecks,
    },
    'supersedes': 'class2-lane-published-chain-roots-independent-audit-'
                  'v11-20261115.json (schema v11, merged 63h+63i endpoint); '
                  'this v12 output extends the pinned chain to the '
                  'reconciled canonical-1405 endpoint (117 pins, 713 roots, '
                  '39 post-70e heads): the second receipts fork at the '
                  '63i head 1367 reconciled (the 63j/65m branch-B folds, '
                  'the merged-4 branch-C re-fold, the 67d branch-D fold, '
                  'the merged-5 canonical-1400 head and the reconciled '
                  'canonical-1405 head), the canonical-line exactly-once '
                  'check extended to 1405 through the 63j and 65m heads, '
                  'the 67d record of the merged-5 head and the re-based '
                  'cost-70g receipts of the reconciled head (the 63h '
                  'marginals claimed once at merged-1369; the lane-local '
                  'merged-4 head adds no new marginal; the 70g fork head '
                  '1403 off the line), the two stale-baseline sweep heads '
                  'classified with their corrected baselines taken from '
                  'their completed claims, and the published second-'
                  'independent-verification record cross-checked against '
                  'the reconciled head byte-exact; the v11 file remains '
                  'published unchanged)',
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
(OUT / 'class2-lane-published-chain-roots-independent-audit-v12-20261115.json').write_text(
    json.dumps(result, indent=1, sort_keys=True) + '\n')
assert not geom_anomalies, geom_anomalies
print('AUDIT PASSED')
print('published hex errata: %d' % len(hex_errata))
print('pins %d (base %d, chain %d, post70e %d)' % (
    n_pins, pin_report['base'], pin_report['chain'], pin_report['post70e']))
print('base roots distinct %d (dup %s), chain distinct %d, overlap %d' % (
    len(base_set), [d['root'] for d in intra_base_duplicates],
    len(chain_set), len(overlap_base_chain)))
print('cumulative inventory @reconciled1405: %d roots / %d D4 orbits / %d twin pairs' % (
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
print('bit-78 duplicate root: identity/marginals/claims/inventory/merged '
      'receipts all exactly-once (%s)' % bit78_report['root_hex'])
