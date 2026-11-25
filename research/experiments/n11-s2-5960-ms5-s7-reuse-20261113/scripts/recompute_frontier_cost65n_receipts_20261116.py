#!/usr/bin/env python3
"""Fold the two cost-65n WIN7-D10 receipts (bits 90 and 117 of the child
00000000000000801202010000800000, roots 00000000040000801202010000800000 and
00200000000000801202010000800000) into the canonical head
1441/174/6407/506945/4680/370859 (2026-11-16).

Protocol (adapted to the independent-basis reconstruction published by the
verification lane, because the runpy cost-64f/64g chain reproduction is not
runnable in this session's environment):

1. independently reconstruct the basis solved set of head 1441 with the
   published fold-projection method (fold_projection_head1441_tool_20261116.py,
   commit a7ac1757): 762 published receipt roots (100 class-frontier recompute
   JSONs incl. the cost-64g fold JSON contributing the bit-89 root, 26 WIN7-only
   base certificate files, 6 named frontier recomputes) + the 498 sweep winners,
   frontier semantics verbatim-ported from the published recompute_frontier_full.py;
   assert the basis head 6 numbers and demand histogram equal both the published
   chain values (class2-lane-cost65n-inflight-20261116.json chain_head_at_claim)
   and the independent pre-registration basis summary (git blob da2b2292,
   commit 0c237017);
2. re-derive the cost-65n sweep from the 8 blob-pinned raw batches plus the
   2 determinism reruns and the v15 crosscheck (2 WIN7-D10 bits 90/117 + 57
   REFUTED-D10 swept + 6 transferred = 65/65, 0 capped, 92530349 nodes),
   re-assert the completed claim v2 and the published raw-sweep audit;
3. re-assert the published head-1441 census v4 bit table (open 59 == swept set,
   6 transferred root canons re-derived, shared family 29/2017 with the child
   row at cost 65, demand c1=0,c2=2,c4=0);
4. re-assert both published certificates byte-for-byte (bit-90 parts joined =
   whole 1,285,412 bytes with md5/sha256 re-hash + whole git blob re-derivation,
   bit-117 whole 721,989 bytes; sorted-unique rows, header/root lines, BigInt
   union 0/0 + Bareiss records, win2 manifest totals, second independent
   verification record byte_identical true);
5. conflict census: all 65 candidate D4 orbits disjoint from the 762 folded
   roots at head 1441;
6. assert the child genuinely remains open at head 1441 on both direct open
   class-2 parents (shared 29/2017, second 48/3498, edge cost 65, dual demand
   c1=0,c2=2,c4=0);
7. fold the two receipts in publication order (bit 90, then bit 117) with
   per-receipt marginals and a set-equality control; every fold result is
   compared field-by-field against the independent pre-registration (blob
   da2b2292) published before this fold;
8. emit the new canonical head 1444/174/6404/506746/4677/370660, per-parent
   deltas, closed-row demand invariants, rankings, and the claim update (v3,
   all v2 fields preserved, v2 restorable byte-identically).

Bookkeeping over published receipts only; solved counts measure manifest
coverage, not the game-theoretic value of any position; WIN7 certificates
prove a first-player win within depth 10 from the individual 7-stone roots
only; REFUTED-D10 is never a LOSS proof; the 11x11 empty board remains
UNKNOWN.
"""
import csv
import gzip
import hashlib
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
MS5 = HERE.parent / "n11-s2-5960-milestone5-20261112" / "output"

BASIS_JSON_BLOBS = {
    "class-frontier-after-cost70c-warm3-recompute-20261115.json": "50735896bfbfdcf99291200ba77e9551559502a4",
    "class-frontier-cost56a-recompute-20261114.json": "7d07267cb0f69d8ac7882c716683bcf36450d247",
    "class-frontier-cost58b-recompute-20261114.json": "cf0fd1e484b11c766ad1dc89eef7c2f883afe57d",
    "class-frontier-cost58c-receipts-recompute-20261116.json": "62a411bb1a6debc33782c07062843650c556c747",
    "class-frontier-cost60b-recompute-20261114.json": "27f69b8e2424366f844fe1b20603ec5f9323a8cd",
    "class-frontier-cost60b-warm-recompute-20261115.json": "8fcb7dee3b28a0125c56dd107883e07ea2455697",
    "class-frontier-cost60c-receipts-recompute-20261116.json": "239a6cf432e53713514d583e3682e1bef6075968",
    "class-frontier-cost61d-recompute-20261114.json": "be4eda7f34bff42b344f8ffd747114930c95f993",
    "class-frontier-cost61e-recompute-20261114.json": "caa81d99a619a4436eeba883e8cdf7ce5e788419",
    "class-frontier-cost61f-recompute-20261114.json": "73604c726243bf469d54ea171af018ae94129745",
    "class-frontier-cost62a-receipts-recompute-20261116.json": "3989e9ddfa43d0951a9a58c10919ce5087eb8733",
    "class-frontier-cost62a-recompute-20261114.json": "b3f3654f29bf75767018f03fbe757edb1596d5c6",
    "class-frontier-cost63a-recompute-20261114.json": "314abb291b637d1506238b0a1291ea2a8a86e405",
    "class-frontier-cost63e-recompute-20261114.json": "fd61b3cc71e532866ff848c1e0466f39f2e1e124",
    "class-frontier-cost63e-warm-recompute-20261114.json": "09c7bf14205031d0027a519962e73f226178a737",
    "class-frontier-cost63f-receipts-recompute-20261115.json": "e1e72b12ca39769f2c4a298d91833b612c97afeb",
    "class-frontier-cost63g-receipts-recompute-20261115.json": "e311e24346adad570e42f145f9190fe8427ae921",
    "class-frontier-cost63h-receipts-recompute-20261115.json": "647498b995770ff87b12e868a5b89015c26be51e",
    "class-frontier-cost63i-receipts-recompute-20261116.json": "db0288f15f1538293e66146542a938c9ebf8b91c",
    "class-frontier-cost63j-receipts-recompute-20261116.json": "35236daf18e6207d2ed20c168bb8a6111f17d4e8",
    "class-frontier-cost64b-recompute-20261114.json": "89893377d6c319cd3ebaacfe569a5350af93d00b",
    "class-frontier-cost64d-receipts-recompute-20261116.json": "082aa7f25596fe52e89ae4b158adba64a7f0d4c9",
    "class-frontier-cost64f-receipts-recompute-20261116.json": "e11f31f303d0f3ab1b6d124403867e9f4ecdbebf",
    "class-frontier-cost64g-receipts-recompute-20261116.json": "aff790021f6f8137ef1bc3ffaec1c980b37fad0c",
    "class-frontier-cost65g-recompute-20261114.json": "1d3e29598ff691c5c5c782c1e04c57908a16eb23",
    "class-frontier-cost65g-warm-recompute-20261114.json": "285d8f48f91e3b70e788282b967a4419aafa1cdc",
    "class-frontier-cost65h-65i-recompute-20261114.json": "a733aa6130320101be2acd0c5bd101c3dbfd0fd7",
    "class-frontier-cost65j-receipts-recompute-20261116.json": "e8c835840f2fad8ffd9a9a8e6f1a9f5944470524",
    "class-frontier-cost65l-receipts-recompute-20261115.json": "0b523e707461b1c4201218a632c3d5c821b8f7f0",
    "class-frontier-cost65m-receipts-recompute-20261116.json": "9798a9fc53b2277b17744737511354b1a830c4d2",
    "class-frontier-cost67-recompute-20261114.json": "81807223a4f04cdf3efe75d6fbf2158cd9b83419",
    "class-frontier-cost67b-recompute-20261114.json": "868d3a179757e7a195a6a42e1fdcfe07c2072a22",
    "class-frontier-cost67c-receipts-recompute-20261115.json": "6d187f48420a9b66d527c3c0fb2764ad5f63235a",
    "class-frontier-cost67d-receipts-recompute-20261116.json": "304c6afe68697ee63162a9de5e91fe2b230255c3",
    "class-frontier-cost68b-recompute-20261114.json": "24a96c2f8e7636f816893867b7c21fdfa153e57a",
    "class-frontier-cost68c-recompute-20261114.json": "67ac08bf8da9d45909325fd35bee077f77ba834d",
    "class-frontier-cost68d-recompute-20261115.json": "452a1b52238f0d12e9915adccc58ed9f010bb5d2",
    "class-frontier-cost69a-recompute-20261114.json": "fdd4edf5b39d347a8a07024f343b7da14add8865",
    "class-frontier-cost69c-recompute-20261114.json": "a4684a59f5aeb77238c5fddc2df027bbab78ee59",
    "class-frontier-cost69e-recompute-20261115.json": "a06e7aec29fe9830755325eb29bf17dcc2eead22",
    "class-frontier-cost69e-recompute-6receipts-20261115.json": "5850d60b8b64dbecc416c21388e1b09cf5053bc1",
    "class-frontier-cost69f-certificate-backed-recompute-20261115.json": "1321254a2e0d15f641436c2e54058fafe5bc8758",
    "class-frontier-cost69f-receipts-recompute-20261115.json": "683cbb8671e12ce0f91cd3c4bd0bbb519878a965",
    "class-frontier-cost69h-receipts-recompute-20261115.json": "d25eb3a00f73cf9ca34fc2816d28045c1e23f3ae",
    "class-frontier-cost69i-receipts-recompute-20261115.json": "8692a7a67fc9e51c440a91cb2e95809b7d1825e8",
    "class-frontier-cost70b-recompute-20261114.json": "357cd3413d65bf205034c2f1b23f3eb7afa60763",
    "class-frontier-cost70c-recompute-20261115.json": "3a566360029d4a25695a9c04b4ea18232724384f",
    "class-frontier-cost70e-receipts-recompute-20261115.json": "a0171d4bb839aeb813d231c7d879d6a89452359f",
    "class-frontier-cost70f-receipts-recompute-20261115.json": "4d0f130e975b6a7bec4759387bd6d54dfe2b6a18",
    "class-frontier-cost70g-receipts-recompute-20261115.json": "73890fe34580ec2f869a97a00b3e6400eda30c0a",
    "class-frontier-cost70g-receipts-recompute-20261116.json": "8eb71c91bd39f5899171dd588156e0c10a763c63",
    "class-frontier-cost71-recompute-20261114.json": "eede9095366880e5a3f6cd7c719030b5aa50fe8a",
    "class-frontier-cost71b-recompute-20261115.json": "49a308144e6e110b9b9a0da289ac043cd853fbfc",
    "class-frontier-cost71c-receipts-recompute-20261115.json": "61af2eb311f938f5ee5bf2bb20d8c1a76787dc87",
    "class-frontier-cost72b-receipts-recompute-20261115.json": "b4f6b821fbe92ebf97669c0712fbd6b1cec9466d",
    "class-frontier-cost72c-receipts-recompute-20261115.json": "42dbb92e1505d05389e840e3368974b1c613b750",
    "class-frontier-cost73a-recompute-20261114.json": "12d2a80fc0f4234edfff037cee8cc44cd7d1caba",
    "class-frontier-cost73d-recompute-20261114.json": "771b84f93ea9d1d7fe34e40da296d885b1a3ee43",
    "class-frontier-cost73g-receipts-recompute-20261115.json": "e4fb98dc8670fbb85786ab02f017a0a95e357648",
    "class-frontier-cost73h-receipts-recompute-20261115.json": "71f79b4bef000aaa1ce16279aa8d08a1ba9f3357",
    "class-frontier-cost74d-receipts-recompute-20261115.json": "06724afe0698ce93319d092521c5887da6eec0f0",
    "class-frontier-cost74g-receipts-recompute-20261115.json": "fce4ce77a64e039709b89f2a78ece9ffff34e533",
    "class-frontier-cost75b-recompute-20261115.json": "1252731811b82603dbb7bfce1405a9213c3845cc",
    "class-frontier-cost75c-recompute-20261115.json": "f6733b0d1954dba2a7cc84e40b86620370321cd2",
    "class-frontier-cost75d-receipts-recompute-20261115.json": "c801e60578ee5c5272e75719e35847052ac58314",
    "class-frontier-cost75e-receipts-recompute-20261116.json": "5cd93de7ee8943681549b8f97918f6112548b373",
    "class-frontier-cost76a-receipts-recompute-20261115.json": "efd83f2637f83c0e1c5c477dcb0cc42162cda534",
    "class-frontier-cost76b-receipts-recompute-20261115.json": "0c35759729663fd561574fd4c5c8ccf2e46550a5",
    "class-frontier-cost77a-receipts-recompute-20261115.json": "a2ba7235793b051d80658818a83aa02c5a5d4958",
    "class-frontier-cost77b-receipts-recompute-20261115.json": "b648ed068a1b9a04624b4c230e011e6fefeddb01",
    "class-frontier-cost77c-receipts-recompute-20261115.json": "7f2badce7132aa7fdf76c9ee0283bd14a9ac9e7b",
    "class-frontier-cost77d-receipts-recompute-20261115.json": "d19c96b7cb0a01f8fd50179b3ff77595408537d7",
    "class-frontier-cost78a-receipts-recompute-20261115.json": "3938bb1668c7dfb80049cdac45f8dee50514c064",
    "class-frontier-cost79a-receipts-recompute-20261115.json": "7dea99ffe76d767223666241964824f005843893",
    "class-frontier-cost80d-receipts-recompute-20261115.json": "289c93373692d6627347dc9bbb9ffdc3653f508b",
    "class-frontier-cost82c-receipts-recompute-20261115.json": "4ee6aaab50b61e8d48e1d37afed373cd01094620",
    "class-frontier-cost83a-receipts-recompute-20261115.json": "74e35f224e4e46f9464bcaed14c5ea073f4bee5c",
    "class-frontier-cost83b-receipts-recompute-20261115.json": "b089bd955efaf51933c892ca1877ca6ac8062f75",
    "class-frontier-cost83c-receipts-recompute-20261115.json": "fc7832edce1f736ea5f15b2632d79d709fa004f4",
    "class-frontier-cost83d-receipts-recompute-20261115.json": "49cb8022bc715fa22d7c2d483160083478676caa",
    "class-frontier-cost84a-receipts-recompute-20261115.json": "f5624e99f8603ea612a862ed63539011989b5506",
    "class-frontier-merged-cost60bwarm-cost71b-inflight-20261115.json": "2864d6271eed3639217b7a136f21e71803644ac3",
    "class-frontier-merged-cost60bwarm-cost71b-recompute-20261115.json": "0512e381ef15f2c64f2304f4aa9905a58f0e246e",
    "class-frontier-merged-cost63h-63i-63j-65m-67d-recompute-20261116.json": "777474faf6730242b7e0080bfcdad390cca3a0ee",
    "class-frontier-merged-cost63h-63i-63j-65m-recompute-20261116.json": "a4cc8e95145a8796ff53b7686bf9cffc3d6e24cb",
    "class-frontier-merged-cost63h-63i-recompute-20261116.json": "c3ff50364499014a7096151bd9893a6510386c05",
    "class-frontier-merged-cost65l-74g-69i-recompute-20261115.json": "8d96b48273248073958b327ff91f7aecccd09944",
    "class-frontier-merged-cost65l-74g-recompute-20261115.json": "0210953083309c1dd2d8f1cf036ec1f91e88f267",
    "class-frontier-merged-cost75d-77d-receipts-recompute-20261115.json": "97130384432e4a0e1e022292748f9fed1e957c0f",
    "class-frontier-merged-cost78a-69h-recompute-20261115.json": "294c4ed3d9fb26143d54ef2e45d400d1068a41dd",
    "class-frontier-merged-recompute-20261114.json": "c200ffd3f6caae13da7dc0bb37eadabb3739ba35",
    "class-frontier-merged-recompute-after-multiband2-68dhyg-20261115.json": "81d39ea38f5e19de7fc2aa637e42963f546baa52",
    "class-frontier-merged-recompute-after61f-63a65e-20261114.json": "b2f2fe4b5fa862795fbceec583f8f707b96fa8b2",
    "class-frontier-merged-recompute-after65h65i-warm67b68c-20261115.json": "fb99e8c01ec0f2a8f31c080c15afe4e352fad0b9",
    "class-frontier-reconciled-canonical1400-cost70g-recompute-20261116.json": "b3ad19d7bfd48c771d5a6827707a9f26940dc1bb",
    "class-frontier-roadmap.json": "ca98996987f8cd76ae22b92f31ae0e734c6fb023",
    "class-frontier-uncoverability-audit-20261114.json": "a19a0a426f48741c1b3c0a6b1b47d6abcc14860c",
    "class-frontier-unified-merge-recompute-20261115.json": "a0789eedd5b81d1c9ea96220acfb487f38e70e08",
    "class-frontier-warm-multiband-recompute-20261115.json": "01fedcb052988bb01881b427faff87e1ed061059",
    "class-frontier-warm-multiband2-recompute-20261115.json": "0830cfc3746baa6ad5b542579dc9d657b61ac72a",
    "priority-certificates-verified.json": "30970ad6f0aef8ceccdc2199090b29930eaecb6f",
    "class2-certificates-verified.json": "9f58be71f986b55632e4be658c4343bba7bd4518",
    "class2-next-certificates-verified.json": "05952496cd040bb614d45ab146598016bc9bffc7",
    "class2-next2-certificates-verified.json": "62171158ea54b0acd9238f6864b2dc7f0a935edc",
    "class2-next3-certificates-verified.json": "6654bfeefe0314d5e6e94578aa36e09de849aaaa",
    "class2-next4-certificates-verified.json": "f0570f152fe5886f0589e5b00de3038fbf783094",
    "class2-batch5-certificates-verified.json": "02bb76b2b0c135356271978cab0fbd03612a704e",
    "class2-batch3-certificates-verified.json": "1fab35b3d598d629406a09d8f431cb5df2eb045b",
    "class2-batch2-certificates-verified.json": "82098bfb0160758127af5c0c0769d89d19582bdd",
    "class2-batch2b-certificates-verified.json": "5d5e339b5bc9dd4dbe294c878412eb0295de8468",
    "class2-batch1-certificates-verified.json": "24ddd94bf60b2f315801cbd48f08962de81485c6",
    "class2-batch1b-certificates-verified.json": "b25598a3d11d031bd7a4df0d3d3d4e3d41cda741",
    "class4-batch1-certificates-verified.json": "6ff00942c9fb20e429194dd6a4ed2e0a2dfd50da",
    "class4-batch2-certificates-verified.json": "d96dc6dbadfdc1284c6cf3c66558afab6f0bf1be",
    "class4-batch3-bit37-certificate.json": "e804eb7d1304a0ecc1ef19fad80cd9d67d39d2c2",
    "class4-batch3-win7-certificates-20261114.json": "a00d963e535ba9717777930deb3c8f443c4a9b07",
    "class4-batch3-win7-certificates-child5-20261114.json": "548294d42deb2ee7fbc4807a41cda09479a3f8ec",
    "class4-batch3-win7-certificates-child7-20261114.json": "f86f4607b23b3e9ba09c0dbd6b047ea01b57b32a",
    "class2-lane-cost58-win7-certificates-20261114.json": "ba89609330174024b72aaf8eb9ad02d7e3674d1a",
    "class2-lane-cost60-win7-certificates-20261114.json": "cc17b20dfefa118ad0b07e01735299435f790feb",
    "class2-lane-cost61-win7-certificates-20261114.json": "498ea98124c3dd3e345470719f32b74c20111cbc",
    "class2-lane-cost61b-win7-certificates-20261114.json": "6eb8689b8b2eba722429348e22294ce9e9513739",
    "class2-lane-cost64-win7-certificates-20261114.json": "b53bcddd5989f3ef807f7d813d422074d49be035",
    "class2-lane-cost65-win7-certificates-20261114.json": "a666843dd9c2033e6fbacee9aea0bf5edb0e878f",
    "class2-lane-cost68-win7-certificates-20261114.json": "a9ab77063746f78d4409debe170f55825064399b",
    "class2-lane-cost75-win7-certificates-20261114.json": "c82ed068a1405d4ac2b898757506e98faa4b605a",
    "class2-lane-cost63cd-frontier-recompute-20261114.json": "2b67dcb5c998721ce8542e7112d75a0ed809d483",
    "class2-lane-cost65c-frontier-recompute-20261114.json": "cefd0fecdd887028d4aac7896c77536d0ac7ef41",
    "class2-lane-cost65d-frontier-recompute-20261114.json": "dbec777893eb5dc74d2b820fa14685e95c16c9b8",
    "class2-lane-cost75-frontier-recompute-20261114.json": "0c08ff3ff6a41c6d421884d889491487137744db",
    "class4-lane-cost78b-frontier-recompute-20261114.json": "4d9c794993ac84dc4ded9febd151f761b07e873c",
    "class4-lane-cost80b-frontier-recompute-20261114.json": "6347cb68de9019f08244cf4b334833f424c3c5e6",
}

GZ_BLOBS = {
    "s5-remaining-after-reuse.csv.gz": "953eec41cab43f19849f31e5879cf5de932d9d3f",
    "s5-s6-remaining-incidences.csv.gz": "7f0d7f4ab87585515d67a393464b2472e5171001",
    "win7-reuse-hits.csv.gz": "9fdad0e922c00af813c5c398277f2bddaa3283cd",
}

MS5_BLOBS = {
    "ms5_s6_manifest_part1.csv": "6b30ad1b224ead35ffc999e1358e2451446adeeb",
    "ms5_s6_manifest_part2.csv": "8aff65fa2942e7be2ee1adf08ffea6a21a4a02c3",
    "ms5_s6_manifest_part3.csv": "203b0fbd071bfe5f4da8a6cd34fcf3a65670df23",
    "ms5_s6_manifest_part4.csv": "1ec608cc12842bd4472a3039fcc0514494e1960c",
    "ms5_s6_manifest_part5.csv": "e2aad9cef9f9a4af3bc659043631558408b6672b",
    "ms5_s6_manifest_part6.csv": "acc1a8b3869a9917be7dd1b55574c756b59b0351",
}

LANE65N_BLOBS = {
    "class2-lane-cost65n-raw-batch1-20261116.jsonl": "8361a5be1cfa801947ba1e9ec48601f188f7cf6e",
    "class2-lane-cost65n-raw-batch2-20261116.jsonl": "4e2bbc51baeb4a65aadb3e9ece6868a9494f2eb4",
    "class2-lane-cost65n-raw-batch3-20261116.jsonl": "c613f71462a82f74e0ed0923c9b5996966b9ef01",
    "class2-lane-cost65n-raw-batch4-20261116.jsonl": "35b53b20b05d1e725aafe7980572e8d1d034d4bb",
    "class2-lane-cost65n-raw-batch5-20261116.jsonl": "c4f810a23f0081ccaa97a5d88f3a79c908fa11c6",
    "class2-lane-cost65n-raw-batch6-20261116.jsonl": "32545b321511f19b75688871d9960ea09efa3e04",
    "class2-lane-cost65n-raw-batch7-20261116.jsonl": "fe5a98c31115e8885385399200b47cec2adadb20",
    "class2-lane-cost65n-raw-batch8-20261116.jsonl": "278e69ba3854b57d2e8a032bd6770352d3a18261",
    "class2-lane-cost65n-v16-determinism-rerun-batch5-20261116.jsonl": "005417e4d4183d73b550cea62a97c92274585d59",
    "class2-lane-cost65n-v16-determinism-rerun-batch7-20261116.jsonl": "cb450e2703f2d98b2d24988e5252623307d6a133",
    "class2-lane-cost65n-v15-crosscheck-20261116.jsonl": "158012b7d5a0d6be20a487b256a4d3d25ab6c9b4",
    "class2-lane-cost65n-sweep-audit-20261116.json": "6b7d3579b2df28c0bffe68d8d994904a1bb80d86",
    "class2-lane-cost65n-win2-certificates-20261116.json": "e2e4e3f5d352e162f2d6e898b285462ff5b4d286",
    "class2-lane-cost65n-claim-structure-verification-20261116.json": "b0dfbef508f5770ce785a326fac258f3d992b7a1",
    "class2-lane-cost65n-claim-v2-agreement-20261116.json": "86abd95bf5025ae188f578aa8e48cff5a976e80d",
    "class2-lane-cost65n-independent-rerun-verification-20261116.json": "304e13316c0083b955df016134adf7b9ae1f7512",
    "class2-lane-cost65n-win2-certificates-independent-verification-20261116.json": "01c4fdeb11d365a1d35589b614e5d2019bc9adbd",
    "class2-lane-cost65n-fold-preregistration-20261116.json": "da2b2292a3a3436f73dc04bae266de2c01a6ef21",
    "class2-lane-cost65n-inflight-20261116.json": "257e7093582f9080a551ec4ef42e1bdccee3c878",
    "class2-lane-next-target-presweep-1441-20261116.json": "3dcb7cb64d38d27a86043b4349faa85bc0e344ea",
    "class2-lane-next-target-rows-1441-20261116.csv": "4ede6c25d7659fc4dc1902c61828a51a70944497",
}

CERT_BLOBS = {
    "class2-lane-cost65n-certificates/bit90-root-00000000040000801202010000800000.cert.part1of2": "a5d67f1d1acef7900453de25f30f0af959837ac0",
    "class2-lane-cost65n-certificates/bit90-root-00000000040000801202010000800000.cert.part2of2": "0b12b216cc5f99e1d8b19f40b5285aac911f8fdd",
    "class2-lane-cost65n-certificates/bit90-root-00000000040000801202010000800000.cert-receipt.json": "a7059800816cf206a8f499b23ef3117370aab9b8",
    "class2-lane-cost65n-certificates/bit90-root-00000000040000801202010000800000.bigint-verify.json": "060400bef23bcd411bb7d411c29f0a98c7cf2082",
    "class2-lane-cost65n-certificates/bit90-root-00000000040000801202010000800000-bareiss-verify.json": "161d5f9c43eb623f917c717111a91f01a8ce4b45",
    "class2-lane-cost65n-certificates/bit90-root-00000000040000801202010000800000.cert.part1of1.summary.json": "37d1fc745ee974756e146a23cb07440838e09d49",
    "class2-lane-cost65n-certificates/bit117-root-00200000000000801202010000800000.cert": "ac0ea37d6d5ace282ef6383f8998dbb6ca8832a1",
    "class2-lane-cost65n-certificates/bit117-root-00200000000000801202010000800000.bigint-verify.json": "e9da28a3ff93434bbce27ef9de1e0c48de0f588a",
    "class2-lane-cost65n-certificates/bit117-root-00200000000000801202010000800000-bareiss-verify.json": "f87fd5d0b33478800ae5cd54cba4f3bc3dc79781",
    "class2-lane-cost65n-certificates/bit117-root-00200000000000801202010000800000.cert.part1of1.summary.json": "8a7f62fd4b295766f84ed6b0142a0c8246971912",
}


CHILD = "00000000000000801202010000800000"
CHILD_V = int(CHILD, 16)
CHILD_STONES = [23, 40, 49, 57, 60, 71]
WIN_BITS = [90, 117]
ROOTS = {90: "00000000040000801202010000800000",
         117: "00200000000000801202010000800000"}
ROOT_V = {b: int(h, 16) for b, h in ROOTS.items()}
PARENT_SH = "00000000000000003800000008002000"
PARENT_2 = "00000000000000801202010000000000"
TRANSFERRED_BITS = [35, 50, 51, 55, 64, 109]
SWEEP_NODES_TOTAL = 92530349
PILOT_NODES = 3402
V15_PILOT_NODES = 5949
V15_ANCHORS = [9, 90, 94, 117]
WIN_BIT_NODES = {90: 1562274, 117: 388910}
WIN_BIT_V15_NODES = {90: 3204116, 117: 865824}
CHILD_EDGE_COST = 65
HEAD_1441 = (1441, 174, 6407, 506945, 4680, 370859)
PINNED_AFTER = (1444, 174, 6404, 506746, 4677, 370660)
PINNED_MARG = {90: 5, 117: 6}
PINNED_MIM = {90: 1, 117: 2}
PINNED_TOTAL_MARG = 11
PINNED_TOTAL_MIM = 3
PINNED_MIM_HEXES = {90: ["00000000000000801202010000800000"],
                    117: ["00000000000020003800000008080000", "00000000000100809002000000000008"]}
PINNED_MARG_HEXES = {90: ["00000000000000801202010000800000", "00000000000100001800000048002000", "00000000000100002800000048002000", "00000000000100003000000048002000", "00000000000100003800000040002000"],
                    117: ["00000000000020003800000008080000", "00000000000100809002000000000008", "00000000001020001800000008080000", "00000000001020002800000008080000", "00000000001020003000000008080000", "00000000001020003800000000080000"]}
PINNED_COVERS_HEXES = {90: ["00000000000000003800000009080000", "00000000000000801202010000800000", "00000000000100001800000048002000", "00000000000100002800000048002000", "00000000000100003000000048002000", "00000000000100003800000040002000", "00000000000100003800000048000000"],
                    117: ["00000000000000801202010000800000", "00000000000020003800000008080000", "00000000000100809002000000000008", "00000000001020001800000008080000", "00000000001020002800000008080000", "00000000001020003000000008080000", "00000000001020003800000000080000"]}
PINNED_BASIS_HIST = {"c2=0,c4=1": 526, "c2=0,c4=2": 3011, "c2=0,c4=3": 12, "c2=1,c4=0": 212, "c2=1,c4=1": 54, "c2=1,c4=2": 9, "c2=2,c4=0": 801, "c2=2,c4=1": 5, "c2=2,c4=2": 50}
PINNED_HIST = {"c2=0,c4=1": 526, "c2=0,c4=2": 3011, "c2=0,c4=3": 12, "c2=1,c4=0": 212, "c2=1,c4=1": 54, "c2=1,c4=2": 9, "c2=2,c4=0": 798, "c2=2,c4=1": 5, "c2=2,c4=2": 50}
PINNED_PARENTS = {
    "00000000000000003800000008002000": ((29, 2017), (27, 1883), ["00000000000000801202010000800000", "00000000000020003800000008080000"]),
    "00000000000000801202000000000080": ((55, 4137), (53, 4003), ["00000000000020003800000008080000", "00000000000100809002000000000008"]),
    "00000000000000801202010000000000": ((48, 3498), (46, 3368), ["00000000000000801202010000800000", "00000000000100809002000000000008"]),
}
PINNED_INCIDENCES = 6
PINNED_COST_DELTA = 398
CLAIM_V2_SCHEMA = "n11-class2-lane-cost65n-completed-20261116-v2"
CLAIM_V3_SCHEMA = "n11-class2-lane-cost65n-fold-complete-20261116-v3"
CLAIM_V2_BLOB = "257e7093582f9080a551ec4ef42e1bdccee3c878"
CLAIM_V1_BLOB = "c16ba5c953db3bd74bb323f9ffd30efea59c7764"
PREREG_BLOB = "da2b2292a3a3436f73dc04bae266de2c01a6ef21"
PREREG_COMMIT = "0c237017"
PRESWEEP_BLOB = "3dcb7cb64d38d27a86043b4349faa85bc0e344ea"
PRESWEEP_ROWS_BLOB = "4ede6c25d7659fc4dc1902c61828a51a70944497"
WIN2_MANIFEST_BLOB = "e2e4e3f5d352e162f2d6e898b285462ff5b4d286"
AUDIT_BLOB = LANE65N_BLOBS["class2-lane-cost65n-sweep-audit-20261116.json"]
RAW_BLOBS = {n: LANE65N_BLOBS[f"class2-lane-cost65n-raw-batch{n}-20261116.jsonl"]
             for n in range(1, 9)}
DET_BLOBS = {n: LANE65N_BLOBS[f"class2-lane-cost65n-v16-determinism-rerun-batch{n}-20261116.jsonl"]
             for n in (5, 7)}
V15_BLOB = LANE65N_BLOBS["class2-lane-cost65n-v15-crosscheck-20261116.jsonl"]
CERT_DIR = OUT / "class2-lane-cost65n-certificates"
CERT90 = "bit90-root-00000000040000801202010000800000"
CERT117 = "bit117-root-00200000000000801202010000800000"
AUDIT_BLOCKED = "00000000000000809082000000000000"


def git_blob_sha(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest(), len(data)


def load_jsonl(path):
    return [json.loads(x) for x in Path(path).read_text().splitlines() if x.strip()]


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
    return bin(x).count("1")


def extract_roots(obj, acc):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("root_hex", "root") and isinstance(v, str):
                x = int(v, 16)
                if popcount(x) == 7:
                    acc.add(x)
            elif k == "roots" and isinstance(v, list):
                for e in v:
                    if isinstance(e, str):
                        x = int(e, 16)
                        if popcount(x) == 7:
                            acc.add(x)
            elif isinstance(v, (dict, list)):
                extract_roots(v, acc)
    elif isinstance(obj, list):
        for e in obj:
            extract_roots(e, acc)


def extract_win7_roots(obj, acc):
    if isinstance(obj, dict):
        certs = None
        if "certificates" in obj and isinstance(obj["certificates"], list):
            certs = obj["certificates"]
        elif "verdict" in obj:
            certs = [obj]
        if certs is not None:
            for c in certs:
                if isinstance(c, dict):
                    v = c.get("verdict")
                    if v is not None and not str(v).startswith("WIN7"):
                        continue
                    for k in ("root", "root_hex"):
                        if k in c and isinstance(c[k], str):
                            x = int(c[k], 16)
                            if popcount(x) == 7:
                                acc.add(x)
            return
        for v in obj.values():
            if isinstance(v, (dict, list)):
                extract_win7_roots(v, acc)
    elif isinstance(obj, list):
        for e in obj:
            extract_win7_roots(e, acc)


BASE_WIN7_ONLY = {
    "priority-certificates-verified.json",
    "class2-certificates-verified.json",
    "class2-next-certificates-verified.json",
    "class2-next2-certificates-verified.json",
    "class2-next3-certificates-verified.json",
    "class2-next4-certificates-verified.json",
    "class2-batch5-certificates-verified.json",
    "class2-batch3-certificates-verified.json",
    "class2-batch2-certificates-verified.json",
    "class2-batch2b-certificates-verified.json",
    "class2-batch1-certificates-verified.json",
    "class2-batch1b-certificates-verified.json",
    "class4-batch1-certificates-verified.json",
    "class4-batch2-certificates-verified.json",
    "class4-batch3-bit37-certificate.json",
    "class4-batch3-win7-certificates-20261114.json",
    "class4-batch3-win7-certificates-child5-20261114.json",
    "class4-batch3-win7-certificates-child7-20261114.json",
    "class2-lane-cost58-win7-certificates-20261114.json",
    "class2-lane-cost60-win7-certificates-20261114.json",
    "class2-lane-cost61-win7-certificates-20261114.json",
    "class2-lane-cost61b-win7-certificates-20261114.json",
    "class2-lane-cost64-win7-certificates-20261114.json",
    "class2-lane-cost65-win7-certificates-20261114.json",
    "class2-lane-cost68-win7-certificates-20261114.json",
    "class2-lane-cost75-win7-certificates-20261114.json",
}

NAMED_FRONTIER = [
    "class2-lane-cost63cd-frontier-recompute-20261114.json",
    "class2-lane-cost65c-frontier-recompute-20261114.json",
    "class2-lane-cost65d-frontier-recompute-20261114.json",
    "class2-lane-cost75-frontier-recompute-20261114.json",
    "class4-lane-cost78b-frontier-recompute-20261114.json",
    "class4-lane-cost80b-frontier-recompute-20261114.json",
]

LOSS6 = ("00000000000000809202000400000000",
         "00000000000000003800004008000008",
         "00000000000000805202000000002000")


def main():
    # ---------- 1. independent basis reconstruction of head 1441 ----------
    for name, blob in {**BASIS_JSON_BLOBS, **GZ_BLOBS, **LANE65N_BLOBS,
                       **CERT_BLOBS}.items():
        sha, _ = git_blob_sha(OUT / name)
        assert sha == blob, (name, sha)
    for name, blob in MS5_BLOBS.items():
        sha, _ = git_blob_sha(MS5 / name)
        assert sha == blob, (name, sha)
    manifest = set()
    for path in sorted(MS5.glob("ms5_s6_manifest_part*.csv")):
        with path.open(newline="") as f:
            for row in csv.DictReader(f):
                manifest.add(int(row["hex"], 16))
    assert len(manifest) == 7867, len(manifest)
    classes = {}
    with gzip.open(OUT / "s5-remaining-after-reuse.csv.gz", "rt", newline="") as f:
        for row in csv.DictReader(f):
            classes[row["s5_hex"]] = int(row["classes"])
    incidences = list(csv.DictReader(
        gzip.open(OUT / "s5-s6-remaining-incidences.csv.gz", "rt", newline="")))
    assert len(incidences) == 14558, len(incidences)
    winners = set()
    with gzip.open(OUT / "win7-reuse-hits.csv.gz", "rt", newline="") as f:
        for row in csv.DictReader(f):
            winners.add(int(row["s6_hex"], 16))
    assert len(winners) == 498, len(winners)
    loss = {int(x, 16) for x in LOSS6}
    rejected = {r["s5_hex"] for r in incidences if int(r["s6_hex"], 16) in loss}

    def frontier(solved):
        remaining = defaultdict(list)
        for row in incidences:
            if row["s5_hex"] not in rejected and int(row["s6_hex"], 16) not in solved:
                remaining[row["s5_hex"]].append(row)
        unique = {r["s6_hex"]: int(r["s6_s7_edge_cost"])
                  for rows in remaining.values() for r in rows}
        demand = defaultdict(lambda: {"c1": 0, "c2": 0, "c4": 0})
        for s5, rows in remaining.items():
            bits = classes.get(s5, 0)
            for row in rows:
                d = demand[row["s6_hex"]]
                if bits & 1:
                    d["c1"] += 1
                if bits & 2:
                    d["c2"] += 1
                if bits & 4:
                    d["c4"] += 1
        open_only = {k: v for k, v in demand.items() if v["c1"] == 0}
        return remaining, unique, demand, open_only

    def summary(solved):
        remaining, unique, demand, open_only = frontier(solved)
        hist = defaultdict(int)
        for v in open_only.values():
            hist[f"c2={v['c2']},c4={v['c4']}"] += 1
        return {"solved_s6_in_manifest": len(solved & manifest),
                "remaining_s5_orbits": len(remaining),
                "unique_remaining_s6": len(unique),
                "sum_remaining_cost": sum(unique.values()),
                "s6_needed_by_open_classes": len(open_only),
                "cost_needed_by_open_classes":
                    sum(int(unique[k]) for k in open_only),
                "hist": dict(sorted(hist.items()))}

    roots = set()
    for name in sorted(BASE_WIN7_ONLY):
        extract_win7_roots(json.loads((OUT / name).read_text()), roots)
    for name, blob in BASIS_JSON_BLOBS.items():
        if name.startswith("class-frontier-") and name.endswith(".json"):
            extract_roots(json.loads((OUT / name).read_text()), roots)
    for name in NAMED_FRONTIER:
        extract_roots(json.loads((OUT / name).read_text()), roots)
    assert len(roots) == 762, len(roots)
    ROOT89 = int("00000000000100003800000008080000", 16) | (1 << 89)
    assert ROOT89 in roots and popcount(ROOT89) == 7
    for b in WIN_BITS:
        assert ROOT_V[b] not in roots, b
    folded_d4 = {canon(r) for r in roots}
    assert len(folded_d4) == 747, len(folded_d4)
    solved = set(winners)
    for r in roots:
        solved |= covers(r)
    st_1441 = summary(solved)
    got = [st_1441[k] for k in
           ("solved_s6_in_manifest", "remaining_s5_orbits", "unique_remaining_s6",
            "sum_remaining_cost", "s6_needed_by_open_classes",
            "cost_needed_by_open_classes")]
    assert tuple(got) == HEAD_1441, got
    assert st_1441["hist"] == PINNED_BASIS_HIST, st_1441["hist"]
    prereg = json.loads((OUT / "class2-lane-cost65n-fold-preregistration-"
                         "20261116.json").read_text())
    assert prereg["schema"] == "n11-class2-lane-cost65n-fold-preregistration-20261116-v1"
    assert prereg["basis_head_numbers"] == list(HEAD_1441)
    assert prereg["basis_roots"] == 762
    assert prereg["basis_summary"]["hist"] == PINNED_BASIS_HIST
    print("CONTROL independent basis reconstruction of head 1441: 762 published "
          "receipt roots (747 distinct D4 canons, incl. the bit-89 root via the "
          "cost-64g fold JSON) + 498 sweep winners; head 6 numbers and demand "
          "histogram equal the published chain head and the pre-registration "
          "basis summary (git blob " + PREREG_BLOB + ")")

    # ---------- 2. re-derive the cost-65n sweep from the raw batches -------
    bit_recs = {}
    batch_nodes = {}
    for n in sorted(RAW_BLOBS):
        p = OUT / f"class2-lane-cost65n-raw-batch{n}-20261116.jsonl"
        sha, _ = git_blob_sha(p)
        assert sha == RAW_BLOBS[n], (n, sha)
        rows = load_jsonl(p)
        ctrl = [r for r in rows if "control" in r]
        cand = [r for r in rows if "bit" in r]
        assert len(ctrl) == 1 and ctrl[0]["control"] == "pilot_d6"
        assert ctrl[0]["nodes"] == PILOT_NODES
        assert ctrl[0]["loss"] is False and ctrl[0]["capped"] is False
        bits = [r["bit"] for r in cand]
        assert len(bits) == len(set(bits)), n
        for r in cand:
            assert r["bit"] not in bit_recs, r["bit"]
            assert r["capped"] is False and r["andclose"] is True
            assert r["terminalStoneRange"] == [13, 17]
            bit_recs[r["bit"]] = r
        batch_nodes[n] = sum(r["nodes"] for r in cand)
    assert len(bit_recs) == 59
    assert sum(batch_nodes.values()) == SWEEP_NODES_TOTAL, batch_nodes
    win_bits = sorted(b for b, r in bit_recs.items() if r["loss"])
    refuted_swept = sorted(b for b, r in bit_recs.items() if not r["loss"])
    assert win_bits == WIN_BITS, win_bits
    assert len(refuted_swept) == 57
    for b in WIN_BITS:
        assert bit_recs[b]["nodes"] == WIN_BIT_NODES[b], b
    for n, blob in DET_BLOBS.items():
        p = OUT / f"class2-lane-cost65n-v16-determinism-rerun-batch{n}-20261116.jsonl"
        sha, _ = git_blob_sha(p)
        assert sha == blob, (n, sha)
        det = load_jsonl(p)
        assert len(det) == 9
        dctl = [r for r in det if "control" in r]
        assert len(dctl) == 1 and dctl[0]["nodes"] == PILOT_NODES
        det_bits = {r["bit"]: (r["loss"], r["nodes"], r["capped"],
                              tuple(r["terminalStoneRange"]))
                    for r in det if "bit" in r}
        raw_bits = {r["bit"]: (r["loss"], r["nodes"], r["capped"],
                              tuple(r["terminalStoneRange"]))
                    for r in load_jsonl(OUT / f"class2-lane-cost65n-raw-"
                                        f"batch{n}-20261116.jsonl")
                    if "bit" in r}
        assert det_bits == raw_bits, n
    p = OUT / "class2-lane-cost65n-v15-crosscheck-20261116.jsonl"
    sha, _ = git_blob_sha(p)
    assert sha == V15_BLOB, sha
    v15 = load_jsonl(p)
    v15p = [r for r in v15 if "control" in r]
    assert len(v15p) == 1 and v15p[0]["nodes"] == V15_PILOT_NODES
    v15_bits = {r["bit"]: r for r in v15 if "bit" in r}
    assert sorted(v15_bits) == V15_ANCHORS, sorted(v15_bits)
    for b in V15_ANCHORS:
        assert v15_bits[b]["loss"] is bit_recs[b]["loss"], b
        assert v15_bits[b]["capped"] is False
    for b in WIN_BITS:
        assert v15_bits[b]["loss"] is True and v15_bits[b]["nodes"] == WIN_BIT_V15_NODES[b]
    print(f"CONTROL cost-65n sweep re-derived from the 8 blob-pinned raw "
          f"batches: 2 WIN7-D10 (bits 90/117, {WIN_BIT_NODES[90]}/{WIN_BIT_NODES[117]}"
          f" nodes) + 57 REFUTED-D10 swept + 6 transferred = 65/65, 0 capped, "
          f"{SWEEP_NODES_TOTAL} nodes; determinism reruns batch5/batch7 "
          f"node-exact; v15 crosscheck anchors {V15_ANCHORS} two-directional "
          f"(WIN bits at {WIN_BIT_V15_NODES[90]}/{WIN_BIT_V15_NODES[117]} v15 nodes)")

    # ---------- 2b. the completed claim v2 ---------------------------------
    claim_path = OUT / "class2-lane-cost65n-inflight-20261116.json"
    claim = json.loads(claim_path.read_text())
    assert claim["schema"] == CLAIM_V2_SCHEMA, claim["schema"]
    sha, blen = git_blob_sha(claim_path)
    assert sha == CLAIM_V2_BLOB, sha
    res = claim["results"]
    assert claim["s6_child"] == CHILD
    assert claim["child_stones_bit_indices"] == CHILD_STONES
    assert claim["candidate_count"] == 65 and claim["open_candidate_count"] == 59
    assert claim["s6_s7_edge_cost"] == CHILD_EDGE_COST
    assert claim["demand"] == {"c1": 0, "c2": 2, "c4": 0}
    assert claim["s5_target"] == PARENT_SH
    assert claim["legal_candidates"] == sorted(list(bit_recs) + TRANSFERRED_BITS)
    assert res["win7_d10_bits"] == WIN_BITS and res["win7_d10_count"] == 2
    assert res["refuted_d10_bits_swept_v16"] == refuted_swept
    assert res["refuted_d10_bits_transferred"] == TRANSFERRED_BITS
    assert res["refuted_d10_count"] == 63 and res["capped_count"] == 0
    assert res["candidate_nodes_excluding_pilots"] == SWEEP_NODES_TOTAL
    assert claim["open_candidates_to_sweep"] == sorted(bit_recs)
    for n in sorted(RAW_BLOBS):
        assert res["batch_bit_lists"][str(n)] == \
            [r["bit"] for r in load_jsonl(OUT / f"class2-lane-cost65n-raw-"
                f"batch{n}-20261116.jsonl") if "bit" in r], n
    for b in TRANSFERRED_BITS:
        tr = claim["transferred_refuted_d10_bits"][str(b)]
        assert tr["root_canon"] == f"{canon(CHILD_V | (1 << b)):032x}", b
        assert popcount(CHILD_V | (1 << b)) == 7, b
    assert claim["unknown_status"] == ("11x11 empty board, two-stone roots "
                                      "{49,60} and {59,60}, S2 {59,60}, and "
                                      "classes 1/2/4 all remain UNKNOWN")
    assert claim["chain_head_at_claim"].startswith("1441/174/6407/506945/4680/370859")
    print("CONTROL the completed claim v2 re-asserted (blob " + CLAIM_V2_BLOB +
          "; supersedes v1 blob " + CLAIM_V1_BLOB + "); 65 candidates, demand "
          "c1=0,c2=2,c4=0, 6 transferred root canons re-derived from the child")

    # ---------- 3. re-assert the published head-1441 census v4 -------------
    p = OUT / "class2-lane-next-target-presweep-1441-20261116.json"
    sha, blen = git_blob_sha(p)
    assert sha == PRESWEEP_BLOB and blen == 149684, (sha, blen)
    sha, _ = git_blob_sha(OUT / "class2-lane-next-target-rows-1441-20261116.csv")
    assert sha == PRESWEEP_ROWS_BLOB, sha
    presweep = json.loads(p.read_text())
    assert presweep["schema"] == "n11-class2-lane-next-target-presweep-1441-20261116-v1"
    assert presweep["chain_head"] == "1441/174/6407/506945/4680/370859"
    assert presweep["receipt_roots"] == {"count": 761, "distinct_canons": 747}
    bt = presweep["cheapest_row_bit_tables"][CHILD]
    assert len(bt) == 64 + 1 or len(bt) == 65, len(bt)
    census_open = sorted(e["bit"] for e in bt if e["status"] == "open")
    census_tr = {e["bit"]: e["root_canon"] for e in bt
                 if e["status"] == "harvested_refuted"}
    assert sorted(census_tr) == TRANSFERRED_BITS
    assert census_open == sorted(bit_recs), "census v4 open set == swept set"
    for e in bt:
        assert canon(CHILD_V | (1 << e["bit"])) == int(e["root_canon"], 16), e["bit"]
    fam = presweep["family_census"][PARENT_SH]
    assert len(fam["rows"]) == 29 and \
        sum(r["cost"] for r in fam["rows"]) == 2017
    fch = [r for r in fam["rows"] if r["s6_hex"] == CHILD]
    assert len(fch) == 1
    fch = fch[0]
    assert fch["cost"] == CHILD_EDGE_COST and \
        fch["demand"] == {"c1": 0, "c2": 2, "c4": 0}
    assert fch["census"] == {"receipt_win": 0, "harvested_win": 0,
                             "harvested_refuted": 6, "open": 59}
    assert fch["open_after_census"] == 59
    print("CONTROL published head-1441 census v4 re-asserted: open 59 == swept "
          "set, 6 transferred root canons re-derived, shared family 29/2017 "
          "with the child row at cost 65, demand c1=0,c2=2,c4=0")

    # ---------- 4. re-assert the published certificates ---------------------
    sha, blen = git_blob_sha(OUT / "class2-lane-cost65n-win2-certificates-20261116.json")
    assert sha == WIN2_MANIFEST_BLOB, sha
    wman = json.loads((OUT / "class2-lane-cost65n-win2-certificates-20261116.json")
                      .read_text())
    assert wman["schema"] == "n11-class2-lane-cost65n-win2-certificates-20261116-v1"
    assert len(wman["certificates"]) == 2
    certs = {c["bit"]: c for c in wman["certificates"]}
    assert sorted(certs) == WIN_BITS
    # bit 90: parts joined == whole
    p1 = CERT_DIR / f"{CERT90}.cert.part1of2"
    p2 = CERT_DIR / f"{CERT90}.cert.part2of2"
    whole90 = p1.read_bytes() + p2.read_bytes()
    assert len(whole90) == 1285412, len(whole90)
    assert hashlib.md5(whole90).hexdigest() == "616b15e76809b3e31064986d804d29a5"
    assert hashlib.sha256(whole90).hexdigest() == \
        "801bfdacbbb5163e3097ef3df57b2fd3db1ecf38c2e5357df972f633802badff"
    ws = hashlib.sha1(b"blob %d\0" % len(whole90) + whole90).hexdigest()
    assert ws == "c2460e597072493195dbd738335ca7b36bdbcf53", ws
    c90 = certs[90]
    assert c90["root_hex"] == ROOTS[90] and c90["child_hex"] == CHILD
    assert c90["verdict"] == "WIN7" and c90["sub_roots"] == 51
    assert c90["d4_canonical_hex"] == f"{canon(ROOT_V[90]):032x}"
    assert c90["root_mobility_matches_legal_candidates_py"] is True
    assert c90["rows"] == 35627 and c90["extraction_nodes"] == 2770239
    assert c90["fbt_drops"] == 0 and c90["fatal"] is None
    assert c90["terminal_range"] == [13, 17]
    assert c90["winner_states"] == 47526 and c90["loser_states"] == 14036
    assert c90["terminal_count"] == 12139
    pc = c90["published_cert"]
    assert pc["whole_bytes"] == 1285412 and pc["whole_md5"] == \
        "616b15e76809b3e31064986d804d29a5"
    assert pc["whole_git_blob_sha"] == ws
    assert pc["parts"][0]["git_blob_sha"] == \
        CERT_BLOBS[f"class2-lane-cost65n-certificates/{CERT90}.cert.part1of2"]
    assert pc["parts"][1]["git_blob_sha"] == \
        CERT_BLOBS[f"class2-lane-cost65n-certificates/{CERT90}.cert.part2of2"]
    text90 = whole90.decode()
    lines90 = text90.splitlines()
    assert len(lines90) == 35627 + 2
    assert lines90[0] == ("n11-terminal-strategy-v1 original_first_WIN7 "
                          "second_to_move_LOSS")
    assert lines90[1] == f"root {ROOTS[90]}"
    row_hexes = [line.split(" ")[0] for line in lines90[2:]]
    assert len(row_hexes) == 35627 and row_hexes == sorted(set(row_hexes))
    # bit 117: whole cert
    p117 = CERT_DIR / f"{CERT117}.cert"
    whole117 = p117.read_bytes()
    assert len(whole117) == 721989
    assert hashlib.md5(whole117).hexdigest() == "9a1e0abe9602b25e5a3dd0ae1bbf4b59"
    assert hashlib.sha256(whole117).hexdigest() == \
        "8c657f44b78b48b298baeef2d3b2cc68c26e334d01c9fbdfb7c6b7c7877572a5"
    c117 = certs[117]
    assert c117["root_hex"] == ROOTS[117] and c117["child_hex"] == CHILD
    assert c117["verdict"] == "WIN7" and c117["sub_roots"] == 49
    assert c117["d4_canonical_hex"] == f"{canon(ROOT_V[117]):032x}"
    assert c117["root_mobility_matches_legal_candidates_py"] is True
    assert c117["rows"] == 20047 and c117["extraction_nodes"] == 769616
    assert c117["fbt_drops"] == 0 and c117["fatal"] is None
    assert c117["terminal_range"] == [13, 17]
    assert c117["winner_states"] == 28468 and c117["loser_states"] == 9004
    assert c117["terminal_count"] == 6753
    pc = c117["published_cert"]
    assert pc["bytes"] == 721989 and pc["git_blob_sha"] == \
        CERT_BLOBS[f"class2-lane-cost65n-certificates/{CERT117}.cert"]
    lines117 = whole117.decode().splitlines()
    assert len(lines117) == 20047 + 2
    assert lines117[0] == ("n11-terminal-strategy-v1 original_first_WIN7 "
                           "second_to_move_LOSS")
    assert lines117[1] == f"root {ROOTS[117]}"
    row_hexes117 = [line.split(" ")[0] for line in lines117[2:]]
    assert row_hexes117 == sorted(set(row_hexes117))
    for c, nh in ((c90, 51), (c117, 49)):
        assert c["bigint_verify"] == {"union_missing": 0, "union_extra": 0,
                                     "subroots_passed": nh,
                                     "winner_states": c["winner_states"],
                                     "loser_states": c["loser_states"],
                                     "terminal_count": c["terminal_count"]}
        assert c["bareiss_verify"]["all_subroots_pass"] is True
    assert wman["totals"] == {"published_certificates": 2, "rows": 55674,
                              "extraction_nodes": 3539855, "sub_roots": 100,
                              "winner_states": 75994, "loser_states": 23040,
                              "terminal_count": 18892, "cert_bytes": 2007401}
    iv = json.loads((OUT / ("class2-lane-cost65n-win2-certificates-"
                            "independent-verification-20261116.json")).read_text())
    assert iv["schema"] == ("n11-class2-lane-cost65n-win2-certificates-"
                            "independent-verification-20261116-v1")
    for c in iv["certificates"]:
        assert c["byte_identical"] is True and c["fatal"] is None
        assert c["fbt_drops_total"] == 0
    assert {c["bit"] for c in iv["certificates"]} == {90, 117}
    print("CONTROL both certificates re-asserted byte-for-byte: bit-90 parts "
          "joined == whole (1,285,412 bytes, md5/sha256 re-hash, whole git "
          "blob " + ws + "), bit-117 whole 721,989 bytes; sorted-unique rows "
          "35,627/20,047; BigInt union 0/0 (51/51, 49/49) + Bareiss records; "
          "win2 manifest totals; second independent verification record "
          "byte_identical true")

    # ---------- 5. conflict census vs the folded roots at 1441 --------------
    census_overlaps = []
    for b in sorted(bit_recs) + TRANSFERRED_BITS:
        if canon(CHILD_V | (1 << b)) in folded_d4:
            census_overlaps.append(b)
    assert census_overlaps == [], census_overlaps
    for b in WIN_BITS:
        assert ROOT_V[b] not in roots
        assert canon(ROOT_V[b]) not in folded_d4
    assert len({canon(CHILD_V | (1 << b))
                for b in sorted(bit_recs) + TRANSFERRED_BITS}) == 65
    print("CONTROL conflict census: all 65 candidate D4 orbits are disjoint "
          "from the 762 folded roots (747 D4 canons) at 1441 - zero overlaps, "
          "zero WIN/LOSS conflicts")

    # ---------- 6. the child genuinely remains open at head 1441 ------------
    rem_1441, uniq_1441, dem_1441, _ = frontier(solved)
    assert CHILD_V in manifest and CHILD_V not in solved
    for h, exp_rows, exp_cost in ((PARENT_SH, 29, 2017), (PARENT_2, 48, 3498)):
        rows = rem_1441.get(h, [])
        assert classes.get(h, 0) == 2, h
        assert len(rows) == exp_rows and \
            sum(int(r["s6_s7_edge_cost"]) for r in rows) == exp_cost, h
        ch = [r for r in rows if int(r["s6_hex"], 16) == CHILD_V]
        assert len(ch) == 1 and int(ch[0]["s6_s7_edge_cost"]) == CHILD_EDGE_COST, h
    d = dem_1441.get(CHILD)
    assert (d["c1"], d["c2"], d["c4"]) == (0, 2, 0), d
    print("CONTROL the child genuinely remains at head 1441: both direct "
          "open class-2 parents hold the child row (shared 29/2017, second "
          "48/3498) at edge cost 65, dual demand c1=0,c2=2,c4=0")

    # ---------- 7. fold the two receipts in publication order ---------------
    s_cur = set(solved)
    addition = []
    child_closed_by = None
    for bit in WIN_BITS:
        root_v = ROOT_V[bit]
        cov = covers(root_v)
        assert CHILD_V in cov, "the receipt must cover the child via its stone"
        marg = cov - s_cur
        marg_m = marg & manifest
        if CHILD_V in marg_m:
            assert child_closed_by is None
            child_closed_by = bit
        rec = {
            "bit": bit,
            "root_hex": ROOTS[bit],
            "d4_canonical_hex": f"{canon(root_v):032x}",
            "source": ("cost-65n raw batches 1-8 (v16) + the published "
                       "head-1441 census v4 transfer census"),
            "certified": True,
            "sweep_nodes": bit_recs[bit]["nodes"],
            "certificate": {
                "rows": certs[bit]["rows"],
                "sub_roots": certs[bit]["sub_roots"],
                "extraction_nodes": certs[bit]["extraction_nodes"],
                "winner_states": certs[bit]["winner_states"],
                "loser_states": certs[bit]["loser_states"],
                "terminal_count": certs[bit]["terminal_count"],
                "md5": certs[bit]["published_cert"].get(
                    "whole_md5", certs[bit]["published_cert"].get("md5")),
                "sha256": certs[bit]["published_cert"].get(
                    "whole_sha256", certs[bit]["published_cert"].get("sha256")),
            },
            "covers": len(cov),
            "covers_hexes": sorted(f"{k:032x}" for k in cov),
            "marginal": len(marg),
            "marginal_in_manifest": len(marg_m),
            "marginal_manifest_hexes": sorted(f"{k:032x}" for k in marg_m),
            "marginal_non_manifest_hexes":
                sorted(f"{k:032x}" for k in marg - marg_m),
        }
        addition.append(rec)
        assert len(marg) == PINNED_MARG[bit], (bit, len(marg))
        assert len(marg_m) == PINNED_MIM[bit], (bit, len(marg_m))
        assert sorted(f"{k:032x}" for k in marg) == PINNED_MARG_HEXES[bit], bit
        assert sorted(f"{k:032x}" for k in marg_m) == PINNED_MIM_HEXES[bit], bit
        assert sorted(f"{k:032x}" for k in cov) == PINNED_COVERS_HEXES[bit], bit
        s_cur |= marg
    assert child_closed_by == 90, child_closed_by
    cov_all = set()
    for bit in WIN_BITS:
        cov_all |= covers(ROOT_V[bit])
    assert s_cur == solved | cov_all, \
        "set-equality: s_after == s_1441 UNION covers(both roots)"
    total_marg = sum(a["marginal"] for a in addition)
    total_mim = sum(a["marginal_in_manifest"] for a in addition)
    assert (total_marg, total_mim) == (PINNED_TOTAL_MARG, PINNED_TOTAL_MIM)
    st_after, rem_after, dem_after = summary(s_cur), None, None
    rem_after, uniq_after, dem_after, _ = frontier(s_cur)
    got_after = [st_after[k] for k in
                 ("solved_s6_in_manifest", "remaining_s5_orbits",
                  "unique_remaining_s6", "sum_remaining_cost",
                  "s6_needed_by_open_classes", "cost_needed_by_open_classes")]
    assert tuple(got_after) == PINNED_AFTER, got_after
    assert st_after["solved_s6_in_manifest"] == 1441 + total_mim
    assert st_after["hist"] == PINNED_HIST, st_after["hist"]
    # agreement with the pre-registration, field by field
    pre_proj = prereg["projected_head"]
    assert [pre_proj[k] for k in
            ("solved_s6_in_manifest", "remaining_s5_orbits",
             "unique_remaining_s6", "sum_remaining_cost",
             "s6_needed_by_open_classes",
             "cost_needed_by_open_classes")] == got_after
    want_hist = {k: PINNED_BASIS_HIST[k] + prereg["demand_histogram_deltas"].get(k, 0)
                 for k in PINNED_BASIS_HIST}
    assert st_after["hist"] == want_hist
    for p_rec, a in zip(prereg["receipts"], addition):
        assert p_rec["root_hex"] == a["root_hex"]
        assert p_rec["marginal"] == a["marginal"]
        assert p_rec["marginal_in_manifest"] == a["marginal_in_manifest"]
        assert p_rec["covers"] == a["covers"]
        assert p_rec["d4_canonical_hex"] == a["d4_canonical_hex"]
        assert p_rec["d4_orbit_distinct_from_all_folded_roots"] is True
    print("AFTER cost-65n fold:", json.dumps(st_after, indent=1))
    print(f"total marginal={total_marg} marginal_in_manifest={total_mim}; "
          f"child closed by bit: {child_closed_by}")

    # ---------- 8. per-parent rows at the new head -------------------------
    cov_hexes = {f"{k:032x}" for k in cov_all}
    parents_after = {}
    lost_detail = {}
    for h in sorted(rem_1441):
        old = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem_1441[h]}
        new = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem_after.get(h, [])}
        lost = {k: v for k, v in old.items() if k not in new}
        if not lost:
            assert new == old, h
            continue
        assert set(lost) <= cov_hexes, (h, sorted(set(lost) - cov_hexes))
        assert new == {k: v for k, v in old.items() if k not in lost}, h
        parents_after[h] = {"s5_hex": h, "classes": classes.get(h, 0),
                            "rows": len(new),
                            "edge_cost": sum(new.values()),
                            "rows_before": len(old),
                            "edge_cost_before": sum(old.values())}
        lost_detail[h] = lost
    incidences = sum(len(v) for v in lost_detail.values())
    cost_delta = sum(sum(v.values()) for v in lost_detail.values())
    assert incidences == PINNED_INCIDENCES, incidences
    assert cost_delta == PINNED_COST_DELTA, cost_delta
    assert sorted(parents_after) == sorted(PINNED_PARENTS), sorted(parents_after)
    for h, pa in parents_after.items():
        old_exp, new_exp, lost_exp = PINNED_PARENTS[h]
        assert (pa["rows_before"], pa["edge_cost_before"]) == old_exp, h
        assert (pa["rows"], pa["edge_cost"]) == new_exp, h
        assert sorted(lost_detail[h]) == lost_exp, h
    closed_hexes = sorted({h for a in addition
                           for h in a["marginal_manifest_hexes"]})
    pre_closed = sorted(h for r in prereg["receipts"]
                         for h in r["marginal_manifest_hexes"])
    assert closed_hexes == pre_closed and CHILD in closed_hexes
    print("per-parent rows at the new head (touched parents): " + "; ".join(
        f"{k} {v['rows_before']}/{v['edge_cost_before']} -> "
        f"{v['rows']}/{v['edge_cost']}" for k, v in parents_after.items()))
    print(f"parent-row incidences {incidences}, parent edge cost delta "
          f"{cost_delta}")

    # ---------- 9. closed-row demand invariants ----------------------------
    s_hex = {f"{k:032x}" for k in s_cur}
    for a in addition:
        for row_hex in a["marginal_manifest_hexes"]:
            assert row_hex in s_hex, row_hex
            dd = dem_1441.get(row_hex)
            assert dd["c1"] == 0 and (dd["c2"] + dd["c4"]) > 0, (row_hex, dd)
    dd = dem_1441[CHILD]
    assert (dd["c1"], dd["c2"], dd["c4"]) == (0, 2, 0), dd

    # ---------- 10. rankings at the new head --------------------------------
    def best(rem, bit_):
        return sorted(
            ({"s5_hex": k, "classes": classes.get(k, 0),
              "remaining_s6_orbits": len(rows),
              "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"])
                                          for r in rows)}
             for k, rows in rem.items() if classes.get(k, 0) & bit_),
            key=lambda r: (r["remaining_s6_orbits"], r["remaining_s7_edge_cost"],
                           r["s5_hex"]))

    class2 = best(rem_after, 2)
    class4 = best(rem_after, 4)
    class1 = best(rem_after, 1)
    coverable = [c for c in class2 if c["s5_hex"] != AUDIT_BLOCKED]
    print("best class-4:", class4[0] if class4 else None)
    print("best class-1:", class1[0] if class1 else None)
    print("best coverable class-2:", coverable[0] if coverable else None,
          "second:", coverable[1] if len(coverable) > 1 else None)
    print("audit-blocked:", next((c for c in class2
                                 if c["s5_hex"] == AUDIT_BLOCKED), None))

    result = {
        "schema": "n11-class-frontier-cost65n-receipts-20261116-v1",
        "date": "2026-11-16",
        "baseline_record": {
            "basis_head_1441": ("1441/174/6407/506945/4680/370859 "
                                "(independently reconstructed from the 762 "
                                "published receipt roots - 100 class-frontier "
                                "recompute JSONs incl. the cost-64g fold JSON "
                                "contributing the bit-89 root, 26 WIN7-only "
                                "base certificate files, 6 named frontier "
                                "recomputes - plus the 498 sweep winners, "
                                "frontier semantics verbatim-ported from the "
                                "published recompute_frontier_full.py; "
                                "identical to the published chain head "
                                "pinned in class2-lane-cost65n-inflight-"
                                "20261116.json chain_head_at_claim and to the "
                                "pre-registration basis summary, git blob " +
                                PREREG_BLOB + ", commit " + PREREG_COMMIT + ")"),
            "receipt_roots": {"count": 762, "distinct_d4_canons": 747,
                              "note": ("the chain reproduction counts 761 "
                                       "receipt roots at head 1441 (census v4 "
                                       "receipt_roots); the independent glob "
                                       "collection differs by one hex within "
                                       "the same D4 canon orbit - equal "
                                       "coverage, recorded as a bookkeeping "
                                       "difference in the cost-64g "
                                       "independent-agreement log "
                                       "(commit 6719f0c6)")},
            "claim": ("class2-lane-cost65n-inflight-20261116.json (v2 "
                      "completed NOT-STERILE, git blob sha " + CLAIM_V2_BLOB +
                      "; supersedes the v1 in-flight claim blob " +
                      CLAIM_V1_BLOB + "; all v1 fields preserved)"),
            "sweep": ("8 raw batch JSONLs (v16), all blob-pinned; 65 "
                      "candidates = 2 WIN7-D10 (bits 90, 117) + 57 REFUTED-D10 "
                      "swept + 6 REFUTED-D10 transferred (D4-canonical "
                      "identity, published head-1441 census v4), 0 capped, "
                      "92530349 nodes + 8 pilots x 3402; determinism reruns "
                      "batch5/batch7 node-exact; v15 crosscheck "
                      "two-directional (anchors 9/90/94/117); independently "
                      "re-verified node-exact 59/59 by the verification lane "
                      "(class2-lane-cost65n-independent-rerun-verification-"
                      "20261116.json)"),
            "census_v4": ("class2-lane-next-target-presweep-1441-20261116.json "
                           f"(git blob sha {PRESWEEP_BLOB}; rows CSV git blob "
                           f"sha {PRESWEEP_ROWS_BLOB})"),
            "certificates": ("class2-lane-cost65n-win2-certificates-20261116."
                             f"json (git blob sha {WIN2_MANIFEST_BLOB}) + "
                             "bit-90 whole 1,285,412 bytes (parts joined "
                             "byte-exactly, whole git blob sha "
                             "c2460e597072493195dbd738335ca7b36bdbcf53) and "
                             "bit-117 whole 721,989 bytes (git blob sha "
                             "ac0ea37d6d5ace282ef6383f8998dbb6ca8832a1); "
                             "BigInt union 0/0 (51/51, 49/49) + Bareiss "
                             "records blob-pinned; second independent "
                             "verification byte_identical true "
                             "(class2-lane-cost65n-win2-certificates-"
                             "independent-verification-20261116.json)"),
            "preregistration": ("class2-lane-cost65n-fold-preregistration-"
                                f"20261116.json (git blob sha {PREREG_BLOB}, "
                                f"commit {PREREG_COMMIT}, published before "
                                "this fold); every machine-checkable field "
                                "re-derived and compared here"),
        },
        "method": ("independent basis reconstruction of head 1441 (published "
                   "fold-projection method), re-derivation of the cost-65n "
                   "sweep from the 8 blob-pinned raw batches plus the 6 "
                   "blob-pinned pre-sweep transferred REFUTED verdicts, "
                   "re-assertion of both certificates byte-for-byte (parts "
                   "join, md5/sha256/whole-blob re-hash, sorted-unique rows, "
                   "BigInt/Bareiss verify records), 65-candidate-orbit "
                   "conflict census vs the 762 folded roots (zero overlaps), "
                   "the child-remaining fact asserted on both direct open "
                   "parents, then the two receipts folded in publication "
                   "order with per-receipt marginals, a set-equality control "
                   "and field-by-field agreement with the pre-registration"),
        "cost65n_additions": addition,
        "totals": {
            "receipts": 2,
            "total_marginal": total_marg,
            "total_marginal_in_manifest": total_mim,
            "child_closed_by_bit": child_closed_by,
            "transferred_refuted_bits": TRANSFERRED_BITS,
            "conflict_census_overlaps": census_overlaps,
            "folded_roots_at_1441": {"receipt_roots": 762,
                                    "distinct_d4_canons": 747},
            "rows_closed_hexes": closed_hexes,
            "sweep_nodes_excluding_pilots": SWEEP_NODES_TOTAL,
            "parent_row_incidences": incidences,
            "parent_edge_cost_delta": cost_delta,
        },
        "frontier_after_cost65n": {
            "solved_s6_in_manifest": st_after["solved_s6_in_manifest"],
            "remaining_s5_orbits": st_after["remaining_s5_orbits"],
            "unique_remaining_s6": st_after["unique_remaining_s6"],
            "sum_remaining_cost": st_after["sum_remaining_cost"],
            "s6_needed_by_open_classes":
                st_after["s6_needed_by_open_classes"],
            "cost_needed_by_open_classes":
                st_after["cost_needed_by_open_classes"],
            "demand_histogram_open_only": st_after["hist"],
            "best_class2": class2[0] if class2 else None,
            "best_class4": class4[0] if class4 else None,
            "best_class1": class1[0] if class1 else None,
            "best_coverable_class2": coverable[0] if coverable else None,
            "second_coverable_class2": coverable[1] if len(coverable) > 1
                                        else None,
        },
        "parents_after": parents_after,
        "lost_rows_per_parent": lost_detail,
        "interpretation_guard": ("bookkeeping over published receipts; solved "
                                "counts measure manifest coverage, not the "
                                "game-theoretic value of any position; WIN7 "
                                "certificates prove a first-player win "
                                "within depth 10 from the individual "
                                "7-stone roots only; REFUTED-D10 proves only "
                                "absence of WIN7-D10 from that root and is "
                                "never a LOSS proof; 11x11 empty board / "
                                "two-stone roots {49,60} and {59,60} / S2 "
                                "{59,60} / class 1 / class 2 / class 4 "
                                "remain UNKNOWN"),
    }
    (OUT / "class-frontier-cost65n-receipts-recompute-20261116.json"
     ).write_text(json.dumps(result, indent=1) + "\n")
    print("written class-frontier-cost65n-receipts-recompute-20261116.json")

    ranking = sorted(
        ({"s5_hex": k, "classes": classes.get(k, 0),
          "remaining_s6_orbits": len(rows),
          "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"])
                                        for r in rows)}
         for k, rows in rem_after.items()),
        key=lambda r: (0 if r["classes"] & 6 else 1, r["remaining_s6_orbits"],
                       r["remaining_s7_edge_cost"], r["s5_hex"]))
    with (OUT / ("class-frontier-s5-ranking-after-cost65n-"
                "receipts-20261116.csv")).open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(("s5_hex", "classes", "remaining_s6_orbits",
                    "remaining_s7_edge_cost"))
        for r in ranking:
            w.writerow((r["s5_hex"], r["classes"], r["remaining_s6_orbits"],
                        r["remaining_s7_edge_cost"]))

    with (OUT / ("class-frontier-top-candidates-s6-after-cost65n-"
                "receipts-20261116.csv")).open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        for label, cand in (("best class-4 blocker-candidate S5",
                             class4[0] if class4 else None),
                            ("best class-1 blocker-candidate S5",
                             class1[0] if class1 else None),
                            ("best class-2 blocker-candidate S5 "
                             "(receipt-unclosable, audit-blocked)",
                             next((c for c in class2
                                   if c["s5_hex"] == AUDIT_BLOCKED), None)),
                            ("best coverable class-2 blocker-candidate S5",
                             coverable[0] if coverable else None),
                            ("second coverable class-2 candidate S5",
                             coverable[1] if len(coverable) > 1 else None)):
            if cand is None:
                continue
            rows = rem_after.get(cand["s5_hex"], [])
            w.writerow([f"# {label}: s5={cand['s5_hex']} "
                        f"classes={cand['classes']} "
                        f"remaining={cand['remaining_s6_orbits']} "
                        f"cost={cand['remaining_s7_edge_cost']}"])
            w.writerow(("s5_hex", "s6_hex", "s6_s7_edge_cost", "demand"))
            for row in sorted(rows, key=lambda r: int(r["s6_s7_edge_cost"])):
                dd = dem_after.get(row["s6_hex"],
                                   {"c1": -1, "c2": -1, "c4": -1})
                w.writerow((cand["s5_hex"], row["s6_hex"],
                            row["s6_s7_edge_cost"],
                            f"c1={dd['c1']},c2={dd['c2']},c4={dd['c4']}"))
    print("written ranking + top-candidates CSVs (after-cost65n-receipts)")

    # ---------- 11. claim v3: add the fold record ---------------------------
    fold_json_sha, _ = git_blob_sha(
        OUT / "class-frontier-cost65n-receipts-recompute-20261116.json")
    head_after = (f"{st_after['solved_s6_in_manifest']}/"
                  f"{st_after['remaining_s5_orbits']}/"
                  f"{st_after['unique_remaining_s6']}/"
                  f"{st_after['sum_remaining_cost']}/"
                  f"{st_after['s6_needed_by_open_classes']}/"
                  f"{st_after['cost_needed_by_open_classes']}")
    v2_fields = {"status": claim["status"],
                 "supersedes": claim["supersedes"],
                 "results_fold": claim["results"]["fold"]}
    claim3 = {k: v for k, v in claim.items()}
    claim3["schema"] = CLAIM_V3_SCHEMA
    claim3["status"] = (
        "FOLD COMPLETE on 2026-11-16 by the long-term lane session: the two "
        "WIN7-D10 receipts (bits 90 and 117, roots "
        "00000000040000801202010000800000 and "
        "00200000000000801202010000800000) are folded on the head-1441 basis "
        "(independent reconstruction of the published fold chain state; "
        "every input blob-pinned) - the child row closes in the manifest "
        "exactly once (child closed by bit 90) and both collateral rows "
        "close with the bit-117 receipt; every fold result agrees "
        "field-by-field with the pre-registration published before the fold "
        "(git blob " + PREREG_BLOB + ", commit " + PREREG_COMMIT + "); new "
        "canonical head " + head_after + "; conflict census vs the 762 "
        "folded roots (747 D4 canons) at 1441: zero overlaps, zero WIN/LOSS "
        "conflicts; all v1/v2 fields preserved (v2 restorable "
        "byte-identically from the fold record); 11x11 empty board, "
        "two-stone roots {49,60} and {59,60}, S2 {59,60}, and classes 1/2/4 "
        "all remain UNKNOWN")
    claim3["supersedes"] = (
        "v2 (completed NOT-STERILE claim, git blob sha " + CLAIM_V2_BLOB +
        ", all fields preserved) which superseded v1 (in-flight claim, "
        "git blob sha " + CLAIM_V1_BLOB + ")")
    claim3["results"]["fold"] = (
        "complete: the two receipts are folded by "
        "recompute_frontier_cost65n_receipts_20261116.py; new canonical "
        "head " + head_after)
    claim3["fold"] = {
        "schema": "n11-class2-lane-cost65n-fold-20261116-v1",
        "fold_json": ("class-frontier-cost65n-receipts-recompute-20261116.json"
                      " (git blob sha " + fold_json_sha + ")"),
        "head_before": "1441/174/6407/506945/4680/370859",
        "head_after": head_after,
        "receipts": 2,
        "win_bits": WIN_BITS,
        "root_hexes": [ROOTS[90], ROOTS[117]],
        "total_marginal": total_marg,
        "total_marginal_in_manifest": total_mim,
        "child_closed_by_bit": child_closed_by,
        "parent_row_incidences": incidences,
        "parent_edge_cost_delta": cost_delta,
        "parents_after": parents_after,
        "v2_fields": v2_fields,
    }
    # v2 restorable byte-identically: the v2 claim file round-trips
    # byte-exactly (claim itself is untouched; the earlier shallow-copy
    # restore mutated claim3.results.fold back to the v2 text - corrected)
    raw = json.dumps(json.loads(claim_path.read_text()),
                     indent=1, ensure_ascii=False) + "\n"
    sha = hashlib.sha1(b"blob %d\0" % len(raw.encode()) +
                       raw.encode()).hexdigest()
    assert sha == CLAIM_V2_BLOB, "v2 round-trip is not byte-identical"
    claim_path.write_text(json.dumps(claim3, indent=1, ensure_ascii=False)
                          + "\n")

    for p in ("class-frontier-cost65n-receipts-recompute-20261116.json",
              "class-frontier-s5-ranking-after-cost65n-receipts-20261116.csv",
              "class-frontier-top-candidates-s6-after-cost65n-"
              "receipts-20261116.csv",
              "class2-lane-cost65n-inflight-20261116.json"):
        sha, blen = git_blob_sha(OUT / p)
        print(f"blob {p}: {sha} ({blen} bytes)")


if __name__ == "__main__":
    main()
