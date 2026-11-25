#!/usr/bin/env python3
"""Fold the seven cost-66c WIN7-D10 receipts (bits 73, 75, 79, 87, 96, 97 and
112 of the child 00000000000000003800000008002008, roots published and
dual-verified as certificates) into the canonical head
1444/174/6404/506746/4677/370660 (the post-cost-65n-fold head, 2026-11-16).

Protocol (adapted from the published cost-65n fold,
recompute_frontier_cost65n_receipts_20261116.py, commits 109cea3f/d99014af):

1. independently reconstruct the basis solved set of head 1444 with the
   published fold-projection method (fold_projection_head1444_tool_20261116.py,
   commit aca9d762): 764 published receipt roots (101 class-frontier recompute
   JSONs incl. the cost-64g fold JSON contributing the bit-89 root and the
   cost-65n fold JSON contributing the bit-90/bit-117 roots, 26 WIN7-only base
   certificate files, 6 named frontier recomputes) + the 498 sweep winners;
   assert the basis head 6 numbers and demand histogram equal both the
   published chain values and the pre-registration basis summary (git blob
   809ad05e1bc560b1086c3d30cc34ad78727e430a, commit aca9d762);
2. re-derive the cost-66c sweep from the 8 blob-pinned raw batches plus the
   bit-112 cap-raise resolution, the determinism reruns (batch 5, bit 112) and
   the v15 crosscheck (anchors 30/73/83/96);
3. re-assert the completed claim v2 (blob ed21be8836214fffe003eabe69bb0b8a75d978b1) and the published
   head-1441 census v4 bit table (open 59 == swept set, 7 transferred root
   canons re-derived, shared family 29/2017 with the child row at cost 66,
   demand c1=0,c2=1,c4=0);
4. re-assert all seven published certificates byte-for-byte (parts joined =
   whole with md5/sha256/whole-blob re-derivation, sorted-unique rows, BigInt
   union 0/0 + Bareiss records, win7 manifest totals);
5. conflict census: all 66 candidate D4 orbits distinct and disjoint from the
   764 folded roots (749 distinct D4 canons) at head 1444;
6. assert the child genuinely remains open at head 1444 on its direct open
   class-2 parent (shared 27/1883, edge cost 66, demand c1=0,c2=1,c4=0);
7. fold the seven receipts in publication order (bit 73, then 75, 79, 87, 96,
   97, 112) with per-receipt marginals and a set-equality control; every fold
   result is compared field-by-field against the pre-registration published
   before this fold;
8. emit the new canonical head 1450/174/6398/506297/4671/370211, per-parent
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
"class-frontier-cost65n-receipts-recompute-20261116.json": "7390c540836d5e8440833aec9b4ac014fd96dd44",
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
"class2-batch1-certificates-verified.json": "24ddd94bf60b2f315801cbd48f08962de81485c6",
"class2-batch1b-certificates-verified.json": "b25598a3d11d031bd7a4df0d3d3d4e3d41cda741",
"class2-batch2-certificates-verified.json": "82098bfb0160758127af5c0c0769d89d19582bdd",
"class2-batch2b-certificates-verified.json": "5d5e339b5bc9dd4dbe294c878412eb0295de8468",
"class2-batch3-certificates-verified.json": "1fab35b3d598d629406a09d8f431cb5df2eb045b",
"class2-batch5-certificates-verified.json": "02bb76b2b0c135356271978cab0fbd03612a704e",
"class2-certificates-verified.json": "9f58be71f986b55632e4be658c4343bba7bd4518",
"class2-lane-cost58-win7-certificates-20261114.json": "ba89609330174024b72aaf8eb9ad02d7e3674d1a",
"class2-lane-cost60-win7-certificates-20261114.json": "cc17b20dfefa118ad0b07e01735299435f790feb",
"class2-lane-cost61-win7-certificates-20261114.json": "498ea98124c3dd3e345470719f32b74c20111cbc",
"class2-lane-cost61b-win7-certificates-20261114.json": "6eb8689b8b2eba722429348e22294ce9e9513739",
"class2-lane-cost63cd-frontier-recompute-20261114.json": "2b67dcb5c998721ce8542e7112d75a0ed809d483",
"class2-lane-cost64-win7-certificates-20261114.json": "b53bcddd5989f3ef807f7d813d422074d49be035",
"class2-lane-cost65-win7-certificates-20261114.json": "a666843dd9c2033e6fbacee9aea0bf5edb0e878f",
"class2-lane-cost65c-frontier-recompute-20261114.json": "cefd0fecdd887028d4aac7896c77536d0ac7ef41",
"class2-lane-cost65d-frontier-recompute-20261114.json": "dbec777893eb5dc74d2b820fa14685e95c16c9b8",
"class2-lane-cost68-win7-certificates-20261114.json": "a9ab77063746f78d4409debe170f55825064399b",
"class2-lane-cost75-frontier-recompute-20261114.json": "0c08ff3ff6a41c6d421884d889491487137744db",
"class2-lane-cost75-win7-certificates-20261114.json": "c82ed068a1405d4ac2b898757506e98faa4b605a",
"class2-next-certificates-verified.json": "05952496cd040bb614d45ab146598016bc9bffc7",
"class2-next2-certificates-verified.json": "62171158ea54b0acd9238f6864b2dc7f0a935edc",
"class2-next3-certificates-verified.json": "6654bfeefe0314d5e6e94578aa36e09de849aaaa",
"class2-next4-certificates-verified.json": "f0570f152fe5886f0589e5b00de3038fbf783094",
"class4-batch1-certificates-verified.json": "6ff00942c9fb20e429194dd6a4ed2e0a2dfd50da",
"class4-batch2-certificates-verified.json": "d96dc6dbadfdc1284c6cf3c66558afab6f0bf1be",
"class4-batch3-bit37-certificate.json": "e804eb7d1304a0ecc1ef19fad80cd9d67d39d2c2",
"class4-batch3-win7-certificates-20261114.json": "a00d963e535ba9717777930deb3c8f443c4a9b07",
"class4-batch3-win7-certificates-child5-20261114.json": "548294d42deb2ee7fbc4807a41cda09479a3f8ec",
"class4-batch3-win7-certificates-child7-20261114.json": "f86f4607b23b3e9ba09c0dbd6b047ea01b57b32a",
"class4-lane-cost78b-frontier-recompute-20261114.json": "4d9c794993ac84dc4ded9febd151f761b07e873c",
"class4-lane-cost80b-frontier-recompute-20261114.json": "6347cb68de9019f08244cf4b334833f424c3c5e6",
"priority-certificates-verified.json": "30970ad6f0aef8ceccdc2199090b29930eaecb6f",
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

LANE66C_BLOBS = {
"class2-lane-cost66c-bit112-cap80m-resolution-20261116.jsonl": "317876ada7bdb23d158ddebce6a0876475bebd3e",
"class2-lane-cost66c-claim-prep-verification-20261116.json": "31c9f9d234f750fe220fd851baf724230e306512",
"class2-lane-cost66c-fold-preregistration-20261116.json": "809ad05e1bc560b1086c3d30cc34ad78727e430a",
"class2-lane-cost66c-inflight-20261116.json": "ed21be8836214fffe003eabe69bb0b8a75d978b1",
"class2-lane-cost66c-raw-batch1-20261116.jsonl": "1ee1146df8ef8ef666df96a69732feabfc87c2fb",
"class2-lane-cost66c-raw-batch2-20261116.jsonl": "b598d6ccff9c93deb5739e96e3b32ce9a110661c",
"class2-lane-cost66c-raw-batch3-20261116.jsonl": "c3a85aca605061fafbc19ce220923386f87c9064",
"class2-lane-cost66c-raw-batch4-20261116.jsonl": "5ff20e15a8d892e930bda28b3198765b9e0d6f57",
"class2-lane-cost66c-raw-batch5-20261116.jsonl": "5899ba17b7d5ee35da2a4716c28a85973d90f797",
"class2-lane-cost66c-raw-batch6-20261116.jsonl": "8d84f6cba95ab80eb397b4ea3a3494947b2b7e54",
"class2-lane-cost66c-raw-batch7-20261116.jsonl": "a805e4101fa657c6b6b2ad029691f06088d31986",
"class2-lane-cost66c-raw-batch8-20261116.jsonl": "ec9adcd267c2943aac144444b43b790a8cc225fe",
"class2-lane-cost66c-raw-sweep-audit-20261116.json": "0854b2e2c6a4bde39405ce0954b966a31ce7f3e7",
"class2-lane-cost66c-v15-crosscheck-20261116.jsonl": "0dce2a3fa7bc02176bb5b4f8b93e9846c2ed6744",
"class2-lane-cost66c-v16-determinism-rerun-batch5-20261116.jsonl": "3da1b0ceba355a9b1a54750399b43174c9597ccc",
"class2-lane-cost66c-v16-determinism-rerun-bit112-20261116.jsonl": "c6f085c6271bc5767ad8324b751ef4c99f6ecd25",
"class2-lane-cost66c-win7-certificates-20261116.json": "463ed0f0aafbf6e21eadc1b7edf1e20051ec7efb",
"class2-lane-fold-projection-basis1444-7roots-20261116.json": "da8cab2f25f0adc4469d09ae1cabf54bf63d9324",
"class2-lane-next-target-presweep-1441-20261116.json": "3dcb7cb64d38d27a86043b4349faa85bc0e344ea",
"class2-lane-next-target-rows-1441-20261116.csv": "4ede6c25d7659fc4dc1902c61828a51a70944497",
}

CERT_BLOBS = {
"class2-lane-cost66c-certificates/bit112-root-00010000000000003800000008002008-bareiss-verify.json": "b70fde80f05443e7192217743239964adc7cc731",
"class2-lane-cost66c-certificates/bit112-root-00010000000000003800000008002008.bigint-verify.json": "b97ee44273733ae84d082863c9d42f67efae2b0f",
"class2-lane-cost66c-certificates/bit112-root-00010000000000003800000008002008.cert-receipt.json": "1836d759b9b4f5b67ca5ddc3b40a670e6d8b2957",
"class2-lane-cost66c-certificates/bit112-root-00010000000000003800000008002008.cert.part1of1.summary.json": "03eb4d529bf3507b66afd6c5590ae6746935966c",
"class2-lane-cost66c-certificates/bit112-root-00010000000000003800000008002008.cert.part1of3": "7446b259b0ebd2875f4540345570ecc5957be4be",
"class2-lane-cost66c-certificates/bit112-root-00010000000000003800000008002008.cert.part2of3": "7f526ef1696eb3f3daa5fe5d14a42fba95113bd8",
"class2-lane-cost66c-certificates/bit112-root-00010000000000003800000008002008.cert.part3of3": "4cc27bb4fe484d7b2b2cd4e11062ece19f94ec94",
"class2-lane-cost66c-certificates/bit73-root-00000000000002003800000008002008-bareiss-verify.json": "73b438cc404b3b56ec81c552e119ebf3fa7dc1a2",
"class2-lane-cost66c-certificates/bit73-root-00000000000002003800000008002008.bigint-verify.json": "717b0a735c49ecb508a3e2fefc17b9a647c96aad",
"class2-lane-cost66c-certificates/bit73-root-00000000000002003800000008002008.cert-receipt.json": "0ef53d5ba0f2abe9b90dd08a30a82ae86a036dec",
"class2-lane-cost66c-certificates/bit73-root-00000000000002003800000008002008.cert.part1of1.summary.json": "858d0250ca57d648f8ff1ae2f2013949ea51b4a8",
"class2-lane-cost66c-certificates/bit73-root-00000000000002003800000008002008.cert.part1of2": "fcf8ce8f069a5ba76780e9237e337ccf6d42fcc9",
"class2-lane-cost66c-certificates/bit73-root-00000000000002003800000008002008.cert.part2of2": "7d3cc1fde2d6c40bd3d18a976a83d3a8e05f44e7",
"class2-lane-cost66c-certificates/bit75-root-00000000000008003800000008002008-bareiss-verify.json": "4734f9871fb063f808fccc001b6da6940e6dc878",
"class2-lane-cost66c-certificates/bit75-root-00000000000008003800000008002008.bigint-verify.json": "de49b7b804d4397638b55b292f878ef32639263a",
"class2-lane-cost66c-certificates/bit75-root-00000000000008003800000008002008.cert-receipt.json": "32eced842cfb010b96ef6937e35ff6034bb09b9b",
"class2-lane-cost66c-certificates/bit75-root-00000000000008003800000008002008.cert.part1of1.summary.json": "7a1e49a052f06900a641e1e8c5351b7db411d342",
"class2-lane-cost66c-certificates/bit75-root-00000000000008003800000008002008.cert.part1of2": "5ede326a698e2b033edc070314867d666676f0c6",
"class2-lane-cost66c-certificates/bit75-root-00000000000008003800000008002008.cert.part2of2": "d928f2a82a5e3bf7a533d7db6e53196370dfa83c",
"class2-lane-cost66c-certificates/bit79-root-00000000000080003800000008002008-bareiss-verify.json": "4cba33636d01e59d4816d637cd1a98b5ab58ab7b",
"class2-lane-cost66c-certificates/bit79-root-00000000000080003800000008002008.bigint-verify.json": "8e3cc3125e138e9ac7be989f6d7b93e0f66acdaf",
"class2-lane-cost66c-certificates/bit79-root-00000000000080003800000008002008.cert": "65e76248f78652d7b26b33efd136d246e520a97b",
"class2-lane-cost66c-certificates/bit79-root-00000000000080003800000008002008.cert.part1of1.summary.json": "7e9611bc50be91cbbe68f5eca4a0cdd237f9bc65",
"class2-lane-cost66c-certificates/bit87-root-00000000008000003800000008002008-bareiss-verify.json": "42cf4d435f0301fe30d5a3d842a759d0716531ab",
"class2-lane-cost66c-certificates/bit87-root-00000000008000003800000008002008.bigint-verify.json": "160c3226e232d32d263d43f1b12214c4389c9ceb",
"class2-lane-cost66c-certificates/bit87-root-00000000008000003800000008002008.cert-receipt.json": "67037515f5b747e1a1c44ec13a556276f45d55ee",
"class2-lane-cost66c-certificates/bit87-root-00000000008000003800000008002008.cert.part1of1.summary.json": "9276d845714f08ef5529945d9e9a926af76cab7c",
"class2-lane-cost66c-certificates/bit87-root-00000000008000003800000008002008.cert.part1of2": "26b7a545368ac096827cb907aa0baad2c5ef0ae1",
"class2-lane-cost66c-certificates/bit87-root-00000000008000003800000008002008.cert.part2of2": "7c37f2b9685c195a1cd90d1816d72327fe75f155",
"class2-lane-cost66c-certificates/bit96-root-00000001000000003800000008002008-bareiss-verify.json": "404c1ac43cc9f2ce0bb6012eacdb7186707a972d",
"class2-lane-cost66c-certificates/bit96-root-00000001000000003800000008002008.bigint-verify.json": "206eaddd5510bc09bf90bba0390b2509e7d1d46f",
"class2-lane-cost66c-certificates/bit96-root-00000001000000003800000008002008.cert-receipt.json": "fe987df1bdab3b20846ccb494484453f17fcca65",
"class2-lane-cost66c-certificates/bit96-root-00000001000000003800000008002008.cert.part1of1.summary.json": "0d315c0120682155b447730c0f180e5f609e9216",
"class2-lane-cost66c-certificates/bit96-root-00000001000000003800000008002008.cert.part1of2": "abec569358c5516503cef7451ded109f56fffa1b",
"class2-lane-cost66c-certificates/bit96-root-00000001000000003800000008002008.cert.part2of2": "22129a2ff0940fbcdda7f3c4d693fba44d9ed0bc",
"class2-lane-cost66c-certificates/bit97-root-00000002000000003800000008002008-bareiss-verify.json": "75ffbc5c1c584bac858c62c4ed414ef7e2c80800",
"class2-lane-cost66c-certificates/bit97-root-00000002000000003800000008002008.bigint-verify.json": "4aad4353851511658e11e92d29e7d11c6f00a836",
"class2-lane-cost66c-certificates/bit97-root-00000002000000003800000008002008.cert": "933bcb870e797874bc31b0786378879bfa115f41",
"class2-lane-cost66c-certificates/bit97-root-00000002000000003800000008002008.cert.part1of1.summary.json": "0ae80aa165ab7c51cd71af114705d0db030b8121",
}


CHILD = "00000000000000003800000008002008"
CHILD_V = int(CHILD, 16)
CHILD_STONES = [3, 13, 27, 59, 60, 61]
WIN_BITS = [73, 75, 79, 87, 96, 97, 112]
ROOTS = {73: '00000000000002003800000008002008', 75: '00000000000008003800000008002008', 79: '00000000000080003800000008002008', 87: '00000000008000003800000008002008', 96: '00000001000000003800000008002008', 97: '00000002000000003800000008002008', 112: '00010000000000003800000008002008'}
ROOT_V = {b: int(h, 16) for b, h in ROOTS.items()}
PARENT_SH = "00000000000000003800000008002000"
TRANSFERRED_BITS = [5, 25, 70, 81, 84, 115, 119]
SWEEP_NODES_TOTAL = 84180263
RAW_AS_RUN_NODES = 81605344
BIT112_CAP_NODES = 10000001
PILOT_NODES = 3402
V15_PILOT_NODES = 5949
V15_ANCHORS = [30, 73, 83, 96]
WIN_BIT_NODES = {73: 1380970, 75: 2092539, 79: 1078921, 87: 2016731,
                 96: 2363101, 97: 689724, 112: 12574920}
WIN_BIT_V15_NODES = {73: 3128502, 96: 5027518}
REF_BIT_V15_NODES = {30: 16840620, 83: 653399}
CHILD_EDGE_COST = 66
HEAD_1444 = (1444, 174, 6404, 506746, 4677, 370660)
PINNED_AFTER = (1450, 174, 6398, 506297, 4671, 370211)
PINNED_CERTS = {73: {'rows': 34822, 'sub_roots': 44, 'extraction_nodes': 2379811, 'winner_states': 51714, 'loser_states': 14964, 'terminal_count': 13191, 'whole_bytes': 1260573, 'nparts': 2}, 75: {'rows': 40267, 'sub_roots': 53, 'extraction_nodes': 3619378, 'winner_states': 57374, 'loser_states': 18247, 'terminal_count': 12992, 'whole_bytes': 1457491, 'nparts': 2}, 79: {'rows': 30590, 'sub_roots': 47, 'extraction_nodes': 2372373, 'winner_states': 46502, 'loser_states': 14294, 'terminal_count': 10945, 'whole_bytes': 1107891, 'nparts': 0}, 87: {'rows': 41870, 'sub_roots': 50, 'extraction_nodes': 3421353, 'winner_states': 58201, 'loser_states': 16544, 'terminal_count': 15948, 'whole_bytes': 1514876, 'nparts': 2}, 96: {'rows': 54558, 'sub_roots': 51, 'extraction_nodes': 6009719, 'winner_states': 73381, 'loser_states': 22976, 'terminal_count': 16945, 'whole_bytes': 1973437, 'nparts': 2}, 97: {'rows': 31205, 'sub_roots': 45, 'extraction_nodes': 1364577, 'winner_states': 48746, 'loser_states': 15490, 'terminal_count': 10960, 'whole_bytes': 1130350, 'nparts': 0}, 112: {'rows': 76817, 'sub_roots': 58, 'extraction_nodes': 23612707, 'winner_states': 107733, 'loser_states': 32594, 'terminal_count': 26289, 'whole_bytes': 2774034, 'nparts': 3}}
PINNED_MARG = {73: 7, 75: 4, 79: 5, 87: 5, 96: 4, 97: 4, 112: 6}
PINNED_MIM = {73: 1, 75: 0, 79: 1, 87: 1, 96: 0, 97: 1, 112: 2}
PINNED_TOTAL_MARG = 35
PINNED_TOTAL_MIM = 6
PINNED_MIM_HEXES = {73: ['00000000000000003800000008002008'], 75: [], 79: ['00000000000000801202000220000000'], 87: ['00000000000020003800000008000080'], 96: [], 97: ['00000000000020801202000000080000'], 112: ['00000000000000801202000100800000', '00000000000000801202000300000000']}
PINNED_MARG_HEXES = {73: ['00000000000000003800000008002008', '00000000000000201800000008080080', '00000000000000202800000008080080', '00000000000000203000000008080080', '00000000000000203800000000080080', '00000000000000203800000008000080', '00000000000000203800000008080000'], 75: ['00000000000000081800000008080080', '00000000000000082800000008080080', '00000000000000083000000008080080', '00000000000000083800000000080080'], 79: ['00000000000000001202000220800000', '00000000000000800202000220800000', '00000000000000801002000220800000', '00000000000000801200000220800000', '00000000000000801202000220000000'], 87: ['00000000000020001800000008080080', '00000000000020002800000008080080', '00000000000020003000000008080080', '00000000000020003800000000080080', '00000000000020003800000008000080'], 96: ['00000000020020001202000040000000', '00000000020020800202000040000000', '00000000020020801002000040000000', '00000000020020801200000040000000'], 97: ['00000000000020801202000000080000', '00000000020000001800000008080080', '00000000020000002800000008080080', '00000000020000003000000008080080'], 112: ['00000000000000001202000300800000', '00000000000000800202000300800000', '00000000000000801002000300800000', '00000000000000801200000300800000', '00000000000000801202000100800000', '00000000000000801202000300000000']}
PINNED_COVERS_HEXES = {73: ['00000000000000003800000008002008', '00000000000000201800000008080080', '00000000000000202800000008080080', '00000000000000203000000008080080', '00000000000000203800000000080080', '00000000000000203800000008000080', '00000000000000203800000008080000'], 75: ['00000000000000003800000008002008', '00000000000000081800000008080080', '00000000000000082800000008080080', '00000000000000083000000008080080', '00000000000000083800000000080080', '00000000000000083800000008000080', '00000000000000083800000008080000'], 79: ['00000000000000001202000220800000', '00000000000000003800000008002008', '00000000000000800202000220800000', '00000000000000801002000220800000', '00000000000000801200000220800000', '00000000000000801202000020800000', '00000000000000801202000220000000'], 87: ['00000000000000003800000008002008', '00000000000020001800000008080080', '00000000000020002800000008080080', '00000000000020003000000008080080', '00000000000020003800000000080080', '00000000000020003800000008000080', '00000000000020003800000008080000'], 96: ['00000000000000003800000008002008', '00000000000020801202000040000000', '00000000020000801202000040000000', '00000000020020001202000040000000', '00000000020020800202000040000000', '00000000020020801002000040000000', '00000000020020801200000040000000'], 97: ['00000000000000003800000008002008', '00000000000020801202000000080000', '00000000020000001800000008080080', '00000000020000002800000008080080', '00000000020000003000000008080080', '00000000020000003800000000080080', '00000000020000003800000008080000'], 112: ['00000000000000001202000300800000', '00000000000000003800000008002008', '00000000000000800202000300800000', '00000000000000801002000300800000', '00000000000000801200000300800000', '00000000000000801202000100800000', '00000000000000801202000300000000']}
PINNED_BASIS_HIST = {"c2=0,c4=1": 526, "c2=0,c4=2": 3011, "c2=0,c4=3": 12,
                     "c2=1,c4=0": 212, "c2=1,c4=1": 54, "c2=1,c4=2": 9,
                     "c2=2,c4=0": 798, "c2=2,c4=1": 5, "c2=2,c4=2": 50}
PINNED_HIST = {"c2=0,c4=1": 526, "c2=0,c4=2": 3011, "c2=0,c4=3": 12,
               "c2=1,c4=0": 208, "c2=1,c4=1": 54, "c2=1,c4=2": 8,
               "c2=2,c4=0": 797, "c2=2,c4=1": 5, "c2=2,c4=2": 50}
PINNED_PARENTS = {'00000000000000003800000008002000': ((27, 1883), (25, 1748), ['00000000000000003800000008002008', '00000000000000801202000100800000']), '00000000000000801202000000000080': ((53, 4003), (52, 3929), ['00000000000020003800000008000080']), '00000000000000801202000000080000': ((66, 5066), (65, 4988), ['00000000000020801202000000080000']), '00000000000000801202000020000000': ((46, 3497), (45, 3420), ['00000000000000801202000220000000']), '00000000000000801202000100000000': ((71, 5912), (69, 5758), ['00000000000000801202000100800000', '00000000000000801202000300000000']), '00000000000020801002000000080000': ((88, 7439), (87, 7361), ['00000000000020801202000000080000'])}
PINNED_INCIDENCES = 8
PINNED_COST_DELTA = 596
PINNED_FOLDED_ROOTS = 764
PINNED_FOLDED_D4 = 749
CLAIM_V2_SCHEMA = "n11-class2-lane-cost66c-completed-20261116-v2"
CLAIM_V3_SCHEMA = "n11-class2-lane-cost66c-fold-complete-20261116-v3"
CLAIM_V2_BLOB = "ed21be8836214fffe003eabe69bb0b8a75d978b1"
PREREG_BLOB = "809ad05e1bc560b1086c3d30cc34ad78727e430a"
PREREG_COMMIT = "aca9d762"
PROJECTION_BLOB = "da8cab2f25f0adc4469d09ae1cabf54bf63d9324"
PRESWEEP_BLOB = "3dcb7cb64d38d27a86043b4349faa85bc0e344ea"
PRESWEEP_ROWS_BLOB = "4ede6c25d7659fc4dc1902c61828a51a70944497"
WIN7_MANIFEST_BLOB = LANE66C_BLOBS["class2-lane-cost66c-win7-certificates-20261116.json"]
AUDIT_BLOB = LANE66C_BLOBS["class2-lane-cost66c-raw-sweep-audit-20261116.json"]
RAW_BLOBS = {n: LANE66C_BLOBS[f"class2-lane-cost66c-raw-batch{n}-20261116.jsonl"]
             for n in range(1, 9)}
DET5_BLOB = LANE66C_BLOBS["class2-lane-cost66c-v16-determinism-rerun-batch5-20261116.jsonl"]
DET112_BLOB = LANE66C_BLOBS["class2-lane-cost66c-v16-determinism-rerun-bit112-20261116.jsonl"]
V15_BLOB = LANE66C_BLOBS["class2-lane-cost66c-v15-crosscheck-20261116.jsonl"]
CAPRES_BLOB = LANE66C_BLOBS["class2-lane-cost66c-bit112-cap80m-resolution-20261116.jsonl"]
CERT_DIR = OUT / "class2-lane-cost66c-certificates"
CERTBASE = {73: 'bit73-root-00000000000002003800000008002008', 75: 'bit75-root-00000000000008003800000008002008', 79: 'bit79-root-00000000000080003800000008002008', 87: 'bit87-root-00000000008000003800000008002008', 96: 'bit96-root-00000001000000003800000008002008', 97: 'bit97-root-00000002000000003800000008002008', 112: 'bit112-root-00010000000000003800000008002008'}
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
    # ---------- 1. independent basis reconstruction of head 1444 ----------
    for name, blob in {**BASIS_JSON_BLOBS, **GZ_BLOBS, **LANE66C_BLOBS}.items():
        sha, _ = git_blob_sha(OUT / name)
        assert sha == blob, (name, sha)
    for name, blob in CERT_BLOBS.items():
        fname = name.split("/", 1)[1]
        sha, _ = git_blob_sha(CERT_DIR / fname)
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
    assert len(roots) == PINNED_FOLDED_ROOTS, len(roots)
    ROOT89 = int("00000000000100003800000008080000", 16) | (1 << 89)
    R90 = int("00000000040000801202010000800000", 16)
    R117 = int("00200000000000801202010000800000", 16)
    assert ROOT89 in roots and R90 in roots and R117 in roots
    for b in WIN_BITS:
        assert ROOT_V[b] not in roots, b
    folded_d4 = {canon(r) for r in roots}
    assert len(folded_d4) == PINNED_FOLDED_D4, len(folded_d4)
    solved = set(winners)
    for r in roots:
        solved |= covers(r)
    st_1444 = summary(solved)
    got = [st_1444[k] for k in
           ("solved_s6_in_manifest", "remaining_s5_orbits", "unique_remaining_s6",
            "sum_remaining_cost", "s6_needed_by_open_classes",
            "cost_needed_by_open_classes")]
    assert tuple(got) == HEAD_1444, got
    assert st_1444["hist"] == PINNED_BASIS_HIST, st_1444["hist"]
    prereg = json.loads((OUT / "class2-lane-cost66c-fold-preregistration-"
                         "20261116.json").read_text())
    assert prereg["schema"] == "n11-class2-lane-cost66c-fold-preregistration-20261116-v1"
    assert prereg["basis_head_numbers"] == list(HEAD_1444)
    assert prereg["basis_roots"] == PINNED_FOLDED_ROOTS
    assert prereg["basis_summary"]["hist"] == PINNED_BASIS_HIST
    print("CONTROL independent basis reconstruction of head 1444: " + str(PINNED_FOLDED_ROOTS) +
          " published receipt roots (" + str(PINNED_FOLDED_D4) + " distinct D4 canons, "
          "incl. the bit-89 root via the cost-64g fold JSON and the bit-90/bit-117 "
          "roots via the cost-65n fold JSON) + 498 sweep winners; head 6 numbers "
          "and demand histogram equal the published chain head and the "
          "pre-registration basis summary (git blob " + PREREG_BLOB + ")")

    # ---------- 2. re-derive the cost-66c sweep from the raw batches -------
    bit_recs = {}
    batch_nodes = {}
    for n in sorted(RAW_BLOBS):
        p = OUT / f"class2-lane-cost66c-raw-batch{n}-20261116.jsonl"
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
            assert r["andclose"] is True
            assert r["terminalStoneRange"] == [13, 17]
            if r["bit"] != 112:
                assert r["capped"] is False, r["bit"]
            bit_recs[r["bit"]] = r
        batch_nodes[n] = sum(r["nodes"] for r in cand)
    assert len(bit_recs) == 59
    as_run = sum(batch_nodes.values())
    assert as_run == RAW_AS_RUN_NODES, as_run
    assert bit_recs[112]["capped"] is True
    assert bit_recs[112]["nodes"] == BIT112_CAP_NODES
    p = OUT / "class2-lane-cost66c-bit112-cap80m-resolution-20261116.jsonl"
    sha, _ = git_blob_sha(p)
    assert sha == CAPRES_BLOB, sha
    capres = load_jsonl(p)
    assert len(capres) == 1 and capres[0]["bit"] == 112
    assert capres[0]["loss"] is True and capres[0]["capped"] is False
    assert capres[0]["nodes"] == WIN_BIT_NODES[112]
    assert as_run - BIT112_CAP_NODES + WIN_BIT_NODES[112] == SWEEP_NODES_TOTAL
    win_bits = sorted(b for b, r in bit_recs.items() if r["loss"] or b == 112)
    refuted_swept = sorted(b for b, r in bit_recs.items()
                           if not r["loss"] and b != 112)
    assert win_bits == WIN_BITS, win_bits
    assert len(refuted_swept) == 52
    for b in WIN_BITS:
        if b != 112:
            assert bit_recs[b]["nodes"] == WIN_BIT_NODES[b], b
    p = OUT / "class2-lane-cost66c-v16-determinism-rerun-batch5-20261116.jsonl"
    sha, _ = git_blob_sha(p)
    assert sha == DET5_BLOB, sha
    det = load_jsonl(p)
    assert len(det) == 9
    dctl = [r for r in det if "control" in r]
    assert len(dctl) == 1 and dctl[0]["nodes"] == PILOT_NODES
    det_bits = {r["bit"]: (r["loss"], r["nodes"], r["capped"],
                           tuple(r["terminalStoneRange"]))
                for r in det if "bit" in r}
    raw_bits = {r["bit"]: (r["loss"], r["nodes"], r["capped"],
                           tuple(r["terminalStoneRange"]))
                for r in load_jsonl(OUT / "class2-lane-cost66c-raw-"
                                    f"batch5-20261116.jsonl")
                if "bit" in r}
    assert det_bits == raw_bits, "det batch5"
    p = OUT / "class2-lane-cost66c-v16-determinism-rerun-bit112-20261116.jsonl"
    sha, _ = git_blob_sha(p)
    assert sha == DET112_BLOB, sha
    det112 = load_jsonl(p)
    assert len(det112) == 1 and det112[0]["bit"] == 112
    assert (det112[0]["loss"], det112[0]["nodes"], det112[0]["capped"]) == \
        (True, WIN_BIT_NODES[112], False)
    p = OUT / "class2-lane-cost66c-v15-crosscheck-20261116.jsonl"
    sha, _ = git_blob_sha(p)
    assert sha == V15_BLOB, sha
    v15 = load_jsonl(p)
    v15p = [r for r in v15 if "control" in r]
    assert len(v15p) == 1 and v15p[0]["nodes"] == V15_PILOT_NODES
    v15_bits = {r["bit"]: r for r in v15 if "bit" in r}
    assert sorted(v15_bits) == V15_ANCHORS, sorted(v15_bits)
    for b in V15_ANCHORS:
        assert v15_bits[b]["capped"] is False, b
        if b in WIN_BITS:
            assert v15_bits[b]["loss"] is True
            assert v15_bits[b]["nodes"] == WIN_BIT_V15_NODES[b], b
        else:
            assert v15_bits[b]["loss"] is False
            assert v15_bits[b]["nodes"] == REF_BIT_V15_NODES[b], b
    print(f"CONTROL cost-66c sweep re-derived from the 8 blob-pinned raw "
          f"batches: 7 WIN7-D10 + 52 REFUTED-D10 swept + 7 transferred = "
          f"66/66, bit-112 cap event resolved at a raised cap (capped attempt "
          f"{BIT112_CAP_NODES} -> {WIN_BIT_NODES[112]} nodes WIN7-D10, "
          f"determinism rerun node-exact), {SWEEP_NODES_TOTAL} definitive "
          f"nodes ({as_run} as run incl. the capped attempt); determinism "
          f"rerun batch5 8 bits node-exact; v15 crosscheck anchors "
          f"{V15_ANCHORS} two-directional")

    # ---------- 2b. the completed claim v2 ---------------------------------
    claim_path = OUT / "class2-lane-cost66c-inflight-20261116.json"
    claim = json.loads(claim_path.read_text())
    assert claim["schema"] == CLAIM_V2_SCHEMA, claim["schema"]
    sha, blen = git_blob_sha(claim_path)
    assert sha == CLAIM_V2_BLOB, sha
    res = claim["results"]
    assert claim["s6_child"] == CHILD
    assert claim["child_stones_bit_indices"] == CHILD_STONES
    assert claim["candidate_count"] == 66 and claim["open_candidate_count"] == 59
    assert claim["s6_s7_edge_cost"] == CHILD_EDGE_COST
    assert claim["demand"] == {"c1": 0, "c2": 1, "c4": 0}
    assert claim["s5_target"] == PARENT_SH
    assert claim["legal_candidates"] == sorted(list(bit_recs) + TRANSFERRED_BITS)
    assert res["win7_d10_bits"] == WIN_BITS
    assert res["win7_d10_root_hexes"] == {str(b): ROOTS[b] for b in WIN_BITS}
    assert res["refuted_d10_swept_bits"] == refuted_swept
    assert sorted(int(k) for k in claim["transferred_refuted_d10_bits"]) == \
        TRANSFERRED_BITS
    assert claim["transferred_refuted_d10_count"] == 7
    assert res["refuted_d10_swept_count"] == 52 and res["capped_count"] == 0
    assert res["total_definitive_swept_nodes"] == SWEEP_NODES_TOTAL
    assert res["raw_batches_as_run_nodes"] == RAW_AS_RUN_NODES
    assert res["win7_d10_swept_nodes"] == {str(b): WIN_BIT_NODES[b]
                                           for b in WIN_BITS}
    assert claim["open_candidates_to_sweep"] == sorted(bit_recs)
    for n in sorted(RAW_BLOBS):
        assert claim["planned_batch_bit_lists"][str(n)] == \
            [r["bit"] for r in load_jsonl(OUT / f"class2-lane-cost66c-raw-"
                f"batch{n}-20261116.jsonl") if "bit" in r], n
    for b in TRANSFERRED_BITS:
        tr = claim["transferred_refuted_d10_bits"][str(b)]
        assert tr["root_canon"] == f"{canon(CHILD_V | (1 << b)):032x}", b
        assert popcount(CHILD_V | (1 << b)) == 7, b
    assert claim["unknown_status"] == ("11x11 empty board, two-stone roots "
                                      "{49,60} and {59,60}, S2 {59,60}, and "
                                      "classes 1/2/4 all remain UNKNOWN")
    assert claim["chain_head_at_claim"].startswith("1441/174/6407/506945/4680/370859")
    assert "supersedes" not in claim
    assert "fold" not in res
    print("CONTROL the completed claim v2 re-asserted (blob " + CLAIM_V2_BLOB +
          "); 66 candidates, demand c1=0,c2=1,c4=0, 7 transferred root canons "
          "re-derived from the child")

    # ---------- 3. re-assert the published head-1441 census v4 -------------
    p = OUT / "class2-lane-next-target-presweep-1441-20261116.json"
    sha, blen = git_blob_sha(p)
    assert sha == PRESWEEP_BLOB, (sha, blen)
    sha, _ = git_blob_sha(OUT / "class2-lane-next-target-rows-1441-20261116.csv")
    assert sha == PRESWEEP_ROWS_BLOB, sha
    presweep = json.loads(p.read_text())
    assert presweep["schema"] == "n11-class2-lane-next-target-presweep-1441-20261116-v1"
    assert presweep["chain_head"] == "1441/174/6407/506945/4680/370859"
    bt = presweep["cheapest_row_bit_tables"][CHILD]
    assert len(bt) == 66, len(bt)
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
        fch["demand"] == {"c1": 0, "c2": 1, "c4": 0}
    assert fch["census"] == {"receipt_win": 0, "harvested_win": 0,
                             "harvested_refuted": 7, "open": 59}
    assert fch["open_after_census"] == 59
    print("CONTROL published head-1441 census v4 re-asserted: open 59 == swept "
          "set, 7 transferred root canons re-derived, shared family 29/2017 "
          "with the child row at cost 66, demand c1=0,c2=1,c4=0")

    # ---------- 4. re-assert the seven published certificates ---------------
    sha, blen = git_blob_sha(OUT / "class2-lane-cost66c-win7-certificates-20261116.json")
    assert sha == WIN7_MANIFEST_BLOB, sha
    wman = json.loads((OUT / "class2-lane-cost66c-win7-certificates-20261116.json")
                      .read_text())
    assert wman["schema"] == "n11-class2-lane-cost66c-win7-certificates-20261116-v1"
    assert len(wman["certificates"]) == 7
    certs = {c["bit"]: c for c in wman["certificates"]}
    assert sorted(certs) == WIN_BITS
    for bit in WIN_BITS:
        c = certs[bit]
        pc = c["published_cert"]
        pin = PINNED_CERTS[bit]
        base = CERTBASE[bit]
        assert c["root_hex"] == ROOTS[bit] and c["child_hex"] == CHILD
        assert c["verdict"] == "WIN7"
        assert c["rows"] == pin["rows"] and c["sub_roots"] == pin["sub_roots"]
        assert c["extraction_nodes"] == pin["extraction_nodes"]
        assert c["winner_states"] == pin["winner_states"]
        assert c["loser_states"] == pin["loser_states"]
        assert c["terminal_count"] == pin["terminal_count"]
        assert c["d4_canonical_hex"] == f"{canon(ROOT_V[bit]):032x}"
        assert c["root_mobility_matches_legal_candidates_py"] is True
        assert c["fbt_drops"] == 0 and c["fatal"] is None
        assert c["terminal_range"] == [13, 17]
        if pc.get("parts"):
            assert len(pc["parts"]) == pin["nparts"], bit
            whole = b""
            for part in pc["parts"]:
                fname = part["path"].rsplit("/", 1)[-1]
                sha, blen = git_blob_sha(CERT_DIR / fname)
                assert sha == part["git_blob_sha"], (bit, fname, sha)
                assert sha == CERT_BLOBS["class2-lane-cost66c-certificates/" + fname]
                assert blen == part["bytes"], (bit, fname, blen)
                whole += (CERT_DIR / fname).read_bytes()
            assert len(whole) == pc["whole_bytes"] == pin["whole_bytes"], bit
            assert hashlib.md5(whole).hexdigest() == pc["whole_md5"], bit
            assert hashlib.sha256(whole).hexdigest() == pc["whole_sha256"], bit
            ws = hashlib.sha1(b"blob %d\0" % len(whole) + whole).hexdigest()
            assert ws == pc["whole_git_blob_sha"], (bit, ws)
        else:
            fname = base + ".cert"
            assert pc["path"].endswith(fname), (bit, pc["path"])
            whole = (CERT_DIR / fname).read_bytes()
            sha, blen = git_blob_sha(CERT_DIR / fname)
            assert sha == pc["git_blob_sha"], (bit, sha)
            assert sha == CERT_BLOBS["class2-lane-cost66c-certificates/" + fname]
            assert blen == pc["bytes"] == pin["whole_bytes"], (bit, blen)
            assert hashlib.md5(whole).hexdigest() == pc["md5"], bit
            assert hashlib.sha256(whole).hexdigest() == pc["sha256"], bit
        lines = whole.decode().splitlines()
        assert len(lines) == c["rows"] + 2, bit
        assert lines[0] == ("n11-terminal-strategy-v1 original_first_WIN7 "
                            "second_to_move_LOSS"), bit
        assert lines[1] == f"root {ROOTS[bit]}", bit
        row_hexes = [line.split(" ")[0] for line in lines[2:]]
        assert len(row_hexes) == c["rows"] and row_hexes == sorted(set(row_hexes)), bit
        bv = json.loads((CERT_DIR / (base + "-bareiss-verify.json")).read_text())
        assert bv["schema"] == "n11-class2-lane-cost66c-bareiss-verify-20261116-v1"
        assert bv["all_subroots_pass"] is True, bit
        assert bv["subroots_verified"] == c["sub_roots"], bit
        biv = json.loads((CERT_DIR / (base + ".bigint-verify.json")).read_text())
        br = biv["bigint_record"]
        assert biv["schema"] == "n11-class2-lane-cost66c-bigint-verify-20261116-v1"
        assert br["verdict"] == "WIN7 certificate independently verified", bit
        assert br["rows_sorted_unique"] is True, bit
        assert br["union_missing"] == 0 and br["union_extra"] == 0, bit
        assert br["subroots_passed"] == c["sub_roots"], bit
        assert br["winner_states"] == c["winner_states"] and \
            br["loser_states"] == c["loser_states"] and \
            br["terminal_count"] == c["terminal_count"], bit
        assert br["root_hex"] == ROOTS[bit], bit
        assert br["root_stones"] == 7 and br["root_safe"] is True, bit
        assert br["strategy_rows"] == c["rows"], bit
        assert br["terminal_range"] == [13, 17], bit
        assert bv["winner_states_seen_across_subroots"] == \
            c["bareiss_verify"]["winner_states_seen_across_subroots"], bit
        assert bv["terminal_count"] == c["terminal_count"], bit
        assert bv["rows"] == c["rows"], bit
        assert c["bigint_verify"] == {"union_missing": 0, "union_extra": 0,
                                      "subroots_passed": c["sub_roots"],
                                      "winner_states": c["winner_states"],
                                      "loser_states": c["loser_states"],
                                      "terminal_count": c["terminal_count"]}, bit
        assert c["bareiss_verify"]["all_subroots_pass"] is True, bit
    assert wman["totals"] == {"published_certificates": 7, "rows": 310129,
                              "extraction_nodes": 42779918, "sub_roots": 348,
                              "winner_states": 443651, "loser_states": 135109,
                              "terminal_count": 107270, "cert_bytes": 11218652}
    print("CONTROL all seven certificates re-asserted byte-for-byte: split "
          "certs bit 73 (1,260,573 B, 2 parts), 75 (1,457,491 B, 2 parts), "
          "87 (1,514,876 B, 2 parts), 96 (1,973,437 B, 2 parts), 112 "
          "(2,774,034 B, 3 parts - first 3-part split) joined == whole with "
          "md5/sha256/whole-blob re-hash; whole certs bit 79 (1,107,891 B) and "
          "97 (1,130,350 B) blob-pinned; sorted-unique rows; BigInt union 0/0 "
          "+ Bareiss records; win7 manifest totals")

    # ---------- 5. conflict census vs the folded roots at 1444 --------------
    census_overlaps = []
    for b in sorted(bit_recs) + TRANSFERRED_BITS:
        if canon(CHILD_V | (1 << b)) in folded_d4:
            census_overlaps.append(b)
    assert census_overlaps == [], census_overlaps
    for b in WIN_BITS:
        assert ROOT_V[b] not in roots
        assert canon(ROOT_V[b]) not in folded_d4
    assert len({canon(CHILD_V | (1 << b))
                for b in sorted(bit_recs) + TRANSFERRED_BITS}) == 66
    print("CONTROL conflict census: all 66 candidate D4 orbits are distinct "
          "and disjoint from the " + str(PINNED_FOLDED_ROOTS) + " folded roots ("
          + str(PINNED_FOLDED_D4) + " D4 canons) at 1444 - zero overlaps, "
          "zero WIN/LOSS conflicts")

    # ---------- 6. the child genuinely remains open at head 1444 ------------
    rem_1444, uniq_1444, dem_1444, _ = frontier(solved)
    assert CHILD_V in manifest and CHILD_V not in solved
    h = PARENT_SH
    rows = rem_1444.get(h, [])
    assert classes.get(h, 0) == 2, h
    assert len(rows) == 27 and \
        sum(int(r["s6_s7_edge_cost"]) for r in rows) == 1883, h
    ch = [r for r in rows if int(r["s6_hex"], 16) == CHILD_V]
    assert len(ch) == 1 and int(ch[0]["s6_s7_edge_cost"]) == CHILD_EDGE_COST, h
    d = dem_1444.get(CHILD)
    assert (d["c1"], d["c2"], d["c4"]) == (0, 1, 0), d
    print("CONTROL the child genuinely remains at head 1444: the shared open "
          "class-2 parent holds the child row (27/1883) at edge cost 66, "
          "demand c1=0,c2=1,c4=0")

    # ---------- 7. fold the seven receipts in publication order ------------
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
        pc = certs[bit]["published_cert"]
        rec = {
            "bit": bit,
            "root_hex": ROOTS[bit],
            "d4_canonical_hex": f"{canon(root_v):032x}",
            "source": ("cost-66c raw batches 1-8 (v16; bit-112 cap-raise "
                       "resolution) + the published head-1441 census v4 "
                       "transfer census"),
            "certified": True,
            "sweep_nodes": WIN_BIT_NODES[bit],
            "certificate": {
                "rows": certs[bit]["rows"],
                "sub_roots": certs[bit]["sub_roots"],
                "extraction_nodes": certs[bit]["extraction_nodes"],
                "winner_states": certs[bit]["winner_states"],
                "loser_states": certs[bit]["loser_states"],
                "terminal_count": certs[bit]["terminal_count"],
                "md5": pc["whole_md5"] if pc.get("parts") else pc["md5"],
                "sha256": (pc["whole_sha256"] if pc.get("parts")
                           else pc["sha256"]),
            },
            "covers": len(cov),
            "covers_hexes": sorted(f"{k:032x}" for k in cov),
            "marginal": len(marg),
            "marginal_in_manifest": len(marg_m),
            "marginal_hexes": sorted(f"{k:032x}" for k in marg),
            "marginal_manifest_hexes": sorted(f"{k:032x}" for k in marg_m),
            "marginal_non_manifest_hexes":
                sorted(f"{k:032x}" for k in marg - marg_m),
        }
        addition.append(rec)
        assert len(marg) == PINNED_MARG[bit], (bit, len(marg))
        assert len(marg_m) == PINNED_MIM[bit], (bit, len(marg_m))
        assert rec["marginal_hexes"] == PINNED_MARG_HEXES[bit], bit
        assert rec["marginal_manifest_hexes"] == PINNED_MIM_HEXES[bit], bit
        assert rec["covers_hexes"] == PINNED_COVERS_HEXES[bit], bit
        s_cur |= marg
    assert child_closed_by == 73, child_closed_by
    cov_all = set()
    for bit in WIN_BITS:
        cov_all |= covers(ROOT_V[bit])
    assert s_cur == solved | cov_all, \
        "set-equality: s_after == s_1444 UNION covers(all seven roots)"
    total_marg = sum(a["marginal"] for a in addition)
    total_mim = sum(a["marginal_in_manifest"] for a in addition)
    assert (total_marg, total_mim) == (PINNED_TOTAL_MARG, PINNED_TOTAL_MIM)
    st_after = summary(s_cur)
    rem_after, uniq_after, dem_after, _ = frontier(s_cur)
    got_after = [st_after[k] for k in
                 ("solved_s6_in_manifest", "remaining_s5_orbits",
                  "unique_remaining_s6", "sum_remaining_cost",
                  "s6_needed_by_open_classes", "cost_needed_by_open_classes")]
    assert tuple(got_after) == PINNED_AFTER, got_after
    assert st_after["solved_s6_in_manifest"] == 1444 + total_mim
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
        assert p_rec["marginal_hexes"] == a["marginal_hexes"]
        assert p_rec["marginal_manifest_hexes"] == a["marginal_manifest_hexes"]
        assert p_rec["covers_hexes"] == a["covers_hexes"]
    print("AFTER cost-66c fold:", json.dumps(st_after, indent=1))
    print(f"total marginal={total_marg} marginal_in_manifest={total_mim}; "
          f"child closed by bit: {child_closed_by}")

    # ---------- 8. per-parent rows at the new head -------------------------
    cov_hexes = {f"{k:032x}" for k in cov_all}
    parents_after = {}
    lost_detail = {}
    for h in sorted(rem_1444):
        old = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem_1444[h]}
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
    incidences2 = sum(len(v) for v in lost_detail.values())
    cost_delta = sum(sum(v.values()) for v in lost_detail.values())
    assert incidences2 == PINNED_INCIDENCES, incidences2
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
    print(f"parent-row incidences {incidences2}, parent edge cost delta "
          f"{cost_delta}")

    # ---------- 9. closed-row demand invariants ----------------------------
    s_hex = {f"{k:032x}" for k in s_cur}
    for a in addition:
        for row_hex in a["marginal_manifest_hexes"]:
            assert row_hex in s_hex, row_hex
            dd = dem_1444.get(row_hex)
            assert dd["c1"] == 0 and (dd["c2"] + dd["c4"]) > 0, (row_hex, dd)
    dd = dem_1444[CHILD]
    assert (dd["c1"], dd["c2"], dd["c4"]) == (0, 1, 0), dd

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
        "schema": "n11-class-frontier-cost66c-receipts-20261116-v1",
        "date": "2026-11-16",
        "baseline_record": {
            "basis_head_1444": ("1444/174/6404/506746/4677/370660 "
                               "(independently reconstructed from the 764 "
                               "published receipt roots - 101 class-frontier "
                               "recompute JSONs incl. the cost-64g fold JSON "
                               "contributing the bit-89 root and the cost-65n "
                               "fold JSON contributing the bit-90/bit-117 "
                               "roots, 26 WIN7-only base certificate files, "
                               "6 named frontier recomputes - plus the 498 "
                               "sweep winners, frontier semantics "
                               "verbatim-ported from the published "
                               "recompute_frontier_full.py; identical to the "
                               "published chain head in class-frontier-"
                               "cost65n-receipts-recompute-20261116.json "
                               "frontier_after_cost65n and to the "
                               "pre-registration basis summary, git blob " +
                               PREREG_BLOB + ", commit " + PREREG_COMMIT + ")"),
            "receipt_roots": {"count": PINNED_FOLDED_ROOTS,
                              "distinct_d4_canons": PINNED_FOLDED_D4},
            "claim": ("class2-lane-cost66c-inflight-20261116.json (v2 "
                      "completed NOT-STERILE, git blob sha " + CLAIM_V2_BLOB +
                      "; superseded the v1 in-flight claim; all fields "
                      "preserved)"),
            "sweep": ("8 raw batch JSONLs (v16), all blob-pinned; 66 "
                      "candidates = 7 WIN7-D10 (bits 73, 75, 79, 87, 96, 97, "
                      "112; bit 112 resolved at a raised cap of 80000000: "
                      "capped attempt 10000001 -> 12574920 nodes WIN7-D10) + "
                      "52 REFUTED-D10 swept + 7 REFUTED-D10 transferred "
                      "(D4-canonical identity, published head-1441 census v4), "
                      "0 capped after the resolution, 84180263 definitive "
                      "nodes (81605344 as run) + 8 pilots x 3402; "
                      "determinism reruns batch5 (8 bits) and bit112 "
                      "node-exact; v15 crosscheck two-directional (anchors "
                      "30/73/83/96); independent stdlib raw-sweep audit 21/21 "
                      "ALL PASS (class2-lane-cost66c-raw-sweep-audit-"
                      "20261116.json, blob-pinned)"),
            "census_v4": ("class2-lane-next-target-presweep-1441-20261116.json "
                          f"(git blob sha {PRESWEEP_BLOB}; rows CSV git blob "
                          f"sha {PRESWEEP_ROWS_BLOB})"),
            "certificates": ("class2-lane-cost66c-win7-certificates-"
                             f"20261116.json (git blob sha {WIN7_MANIFEST_BLOB}) "
                             "+ 7 certificates re-hashed byte-for-byte (whole "
                             "git blobs re-derived; BigInt union 0/0 + Bareiss "
                             "records blob-pinned; 5 split certs joined "
                             "byte-exactly incl. the first 3-part split for "
                             "bit 112)"),
            "preregistration": ("class2-lane-cost66c-fold-preregistration-"
                                f"20261116.json (git blob sha {PREREG_BLOB}, "
                                f"commit {PREREG_COMMIT}, published before "
                                "this fold); every machine-checkable field "
                                "re-derived and compared here; projection "
                                "artifact class2-lane-fold-projection-"
                                f"basis1444-7roots-20261116.json (git blob "
                                f"sha {PROJECTION_BLOB})"),
        },
        "method": ("independent basis reconstruction of head 1444 (published "
                   "fold-projection method), re-derivation of the cost-66c "
                   "sweep from the 8 blob-pinned raw batches plus the "
                   "bit-112 cap-raise resolution and the 7 blob-pinned "
                   "pre-sweep transferred REFUTED verdicts, re-assertion of "
                   "all seven certificates byte-for-byte (parts join, "
                   "md5/sha256/whole-blob re-hash, sorted-unique rows, "
                   "BigInt/Bareiss verify records), 66-candidate-orbit "
                   "conflict census vs the 764 folded roots (zero overlaps), "
                   "the child-remaining fact asserted on the direct open "
                   "parent, then the seven receipts folded in publication "
                   "order with per-receipt marginals, a set-equality control "
                   "and field-by-field agreement with the pre-registration"),
        "cost66c_additions": addition,
        "totals": {
            "receipts": 7,
            "total_marginal": total_marg,
            "total_marginal_in_manifest": total_mim,
            "child_closed_by_bit": child_closed_by,
            "transferred_refuted_bits": TRANSFERRED_BITS,
            "conflict_census_overlaps": census_overlaps,
            "folded_roots_at_1444": {"receipt_roots": PINNED_FOLDED_ROOTS,
                                     "distinct_d4_canons": PINNED_FOLDED_D4},
            "rows_closed_hexes": closed_hexes,
            "sweep_nodes_excluding_pilots": SWEEP_NODES_TOTAL,
            "parent_row_incidences": incidences2,
            "parent_edge_cost_delta": cost_delta,
        },
        "frontier_after_cost66c": {
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
                                "within depth 10 from the individual 7-stone "
                                "roots only; REFUTED-D10 proves only absence "
                                "of WIN7-D10 from that root and is never a "
                                "LOSS proof; 11x11 empty board / two-stone "
                                "roots {49,60} and {59,60} / S2 {59,60} / "
                                "class 1 / class 2 / class 4 remain UNKNOWN"),
    }
    (OUT / "class-frontier-cost66c-receipts-recompute-20261116.json"
     ).write_text(json.dumps(result, indent=1) + "\n")
    print("written class-frontier-cost66c-receipts-recompute-20261116.json")

    ranking = sorted(
        ({"s5_hex": k, "classes": classes.get(k, 0),
          "remaining_s6_orbits": len(rows),
          "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"])
                                        for r in rows)}
         for k, rows in rem_after.items()),
        key=lambda r: (0 if r["classes"] & 6 else 1, r["remaining_s6_orbits"],
                       r["remaining_s7_edge_cost"], r["s5_hex"]))
    with (OUT / ("class-frontier-s5-ranking-after-cost66c-"
                 "receipts-20261116.csv")).open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(("s5_hex", "classes", "remaining_s6_orbits",
                    "remaining_s7_edge_cost"))
        for r in ranking:
            w.writerow((r["s5_hex"], r["classes"], r["remaining_s6_orbits"],
                         r["remaining_s7_edge_cost"]))

    with (OUT / ("class-frontier-top-candidates-s6-after-cost66c-"
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
            w.writerow([f"# {label}: s5={cand['s5_hex']} "
                        f"classes={cand['classes']} "
                        f"remaining={cand['remaining_s6_orbits']} "
                        f"cost={cand['remaining_s7_edge_cost']}"])
            w.writerow(("s5_hex", "s6_hex", "s6_s7_edge_cost", "demand"))
            for row in sorted(rem_after.get(cand["s5_hex"], []),
                              key=lambda r: int(r["s6_s7_edge_cost"])):
                dd = dem_after.get(row["s6_hex"],
                                   {"c1": -1, "c2": -1, "c4": -1})
                w.writerow((cand["s5_hex"], row["s6_hex"],
                            row["s6_s7_edge_cost"],
                            f"c1={dd['c1']},c2={dd['c2']},c4={dd['c4']}"))
    print("written ranking + top-candidates CSVs (after-cost66c-receipts)")

    # ---------- 11. claim v3: add the fold record ---------------------------
    fold_json_sha, _ = git_blob_sha(
        OUT / "class-frontier-cost66c-receipts-recompute-20261116.json")
    head_after = (f"{st_after['solved_s6_in_manifest']}/"
                  f"{st_after['remaining_s5_orbits']}/"
                  f"{st_after['unique_remaining_s6']}/"
                  f"{st_after['sum_remaining_cost']}/"
                  f"{st_after['s6_needed_by_open_classes']}/"
                  f"{st_after['cost_needed_by_open_classes']}")
    v2_status = claim["status"]
    v2_fields = {"status": v2_status}
    claim3 = {k: v for k, v in claim.items()}
    claim3["results"] = {k: v for k, v in claim["results"].items()}
    claim3["schema"] = CLAIM_V3_SCHEMA
    claim3["status"] = (
        "FOLD COMPLETE on 2026-11-16 by the long-term lane session: the seven "
        "WIN7-D10 receipts (bits 73, 75, 79, 87, 96, 97, 112, roots published "
        "and dual-verified as certificates) are folded on the head-1444 basis "
        "(independent reconstruction of the published fold chain state; every "
        "input blob-pinned) - the child row closes in the manifest exactly "
        "once (child closed by bit 73) and five collateral manifest rows "
        "close with the bit-79/87/97/112 receipts; every fold result agrees "
        "field-by-field with the pre-registration published before the fold "
        "(git blob " + PREREG_BLOB + ", commit " + PREREG_COMMIT + "); new "
        "canonical head " + head_after + "; conflict census vs the 764 "
        "folded roots (749 D4 canons) at 1444: zero overlaps, zero WIN/LOSS "
        "conflicts; all v1/v2 fields preserved (v2 restorable "
        "byte-identically from the fold record); 11x11 empty board, "
        "two-stone roots {49,60} and {59,60}, S2 {59,60}, and classes 1/2/4 "
        "all remain UNKNOWN")
    claim3["supersedes"] = (
        "v2 (completed NOT-STERILE claim, git blob sha " + CLAIM_V2_BLOB +
        ", all fields preserved) which superseded the v1 IN FLIGHT claim")
    claim3["results"]["fold"] = (
        "complete: the seven receipts are folded by "
        "recompute_frontier_cost66c_receipts_20261116.py; new canonical "
        "head " + head_after)
    claim3["fold"] = {
        "schema": "n11-class2-lane-cost66c-fold-20261116-v1",
        "fold_json": ("class-frontier-cost66c-receipts-recompute-20261116.json"
                      " (git blob sha " + fold_json_sha + ")"),
        "head_before": "1444/174/6404/506746/4677/370660",
        "head_after": head_after,
        "receipts": 7,
        "win_bits": WIN_BITS,
        "root_hexes": [ROOTS[b] for b in WIN_BITS],
        "total_marginal": total_marg,
        "total_marginal_in_manifest": total_mim,
        "child_closed_by_bit": child_closed_by,
        "parent_row_incidences": incidences2,
        "parent_edge_cost_delta": cost_delta,
        "parents_after": parents_after,
        "v2_fields": v2_fields,
    }
    # v2 restorable byte-identically: the v2 claim file round-trips
    # byte-exactly through json.loads/json.dumps (claim file untouched here)
    t = json.loads(claim_path.read_text())
    rt = [json.dumps(t, indent=1) + "\n",
          json.dumps(t, indent=1, ensure_ascii=False) + "\n"]
    shas = [hashlib.sha1(b"blob %d\0" % len(s.encode()) + s.encode()).hexdigest()
            for s in rt]
    assert CLAIM_V2_BLOB in shas, "v2 round-trip is not byte-identical"
    claim_path.write_text(json.dumps(claim3, indent=1, ensure_ascii=False)
                          + "\n")

    for p in ("class-frontier-cost66c-receipts-recompute-20261116.json",
              "class-frontier-s5-ranking-after-cost66c-receipts-20261116.csv",
              "class-frontier-top-candidates-s6-after-cost66c-"
              "receipts-20261116.csv",
              "class2-lane-cost66c-inflight-20261116.json"):
        sha, blen = git_blob_sha(OUT / p)
        print(f"blob {p}: {sha} ({blen} bytes)")


if __name__ == "__main__":
    main()
