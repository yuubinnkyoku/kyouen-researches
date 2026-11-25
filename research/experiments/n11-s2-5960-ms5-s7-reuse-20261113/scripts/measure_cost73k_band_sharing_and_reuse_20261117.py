#!/usr/bin/env python3
"""Measured state-sharing, cross-band cache value, confirmation re-search
cost and WIN-transfer certificate reuse for the published cost73k band.

Extends the v1 measurement (class2-lane-cert-state-sharing-and-conf-cost-
measurement-20261117.json, commit 9f2422d3) and its D4-canon addendum
(commit 2700ed3c) from three bands (73j/72d/71e) to four by adding the
cost73k band (22 WIN7-D10 certificates, 966,535 rows, published by the
claim lane in commits 40f8db4b..4c383a14).

Measurements, all from already-published repo data:

1. Band state sharing (exact 32-hex equality and D4-canonical keys) for
   the 73k band, with the three earlier bands recomputed as a regression
   gate against the published v1/addendum values (byte-pinned inputs).
2. Cross-band sharing: all six band pairs plus three/four-way
   intersections, exact and D4-canonical, with stone-count histograms
   for the 73k pairs, and regression gates against the published pairs.
3. Confirmation-bit re-search cost of the 73k sweep (bits 14, 23, 26,
   34, 53, 55, 107), split into WIN-transfer and REFUTED-transfer bits,
   from the published concurrent-session sweep record, with consistency
   gates against the published raw sweep audit.
4. WIN-transfer certificate reuse: the 25 WIN7-D10 bits of the 73k row
   are covered by 22 fresh certificates plus three canon-equal roots
   already certified in earlier bands; the canon equalities are
   re-derived here by an independent implementation and the avoided
   extraction cost is quantified from the published manifests.

Every input file's git blob sha and size are asserted against the
embedded pin table (repo commit PIN_COMMIT) before use. Deterministic:
set operations only; two runs produce byte-identical output.

Usage: python3 measure_cost73k_band_sharing_and_reuse_20261117.py <out.json>
"""
import glob
import hashlib
import json
import os
import sys

PIN_COMMIT = "63f5287e0d0958c9ad6633d625d90af8d49c042a"
BANDS = {
    "71e": "certs71e",
    "72d": "certs72d",
    "73j": "certs73j",
    "73k": "certs73k",
}
JSON_INPUTS = {
    "sweep73k-record.json": "class2-lane-cost73k-concurrent-session-sweep-record-20261117.json",
    "sweep73k-audit.json": "class2-lane-cost73k-raw-sweep-audit-20261117.json",
    "rerun73ij.json": ("class2-lane-cost73ij-sweep-independent-"
                       "rerun-verification-20261117.json"),
    "meas_v1.json": ("class2-lane-cert-state-sharing-and-conf-cost-"
                     "measurement-20261117.json"),
    "meas_d4.json": ("class2-lane-cert-state-sharing-d4canon-"
                     "measurement-20261117.json"),
    "inflight73i.json": "class2-lane-cost73i-inflight-20261117.json",
    "manifest69j.json": "class2-lane-cost69j-win7-certificates-20261117.json",
    "manifest66i.json": "class2-lane-cost66i-win7-certificates-20261116.json",
}
CONFIRMATION_BITS_73K = [14, 23, 26, 34, 53, 55, 107]
WIN_TRANSFER_BITS_73K = [14, 26, 55]
CONFIRMATION_BITS = {
    "73i": [5, 13, 20, 103, 108],
    "73j": [5, 14, 20, 46, 97, 103, 108],
}

PINS = {
 "certs71e/class2-lane-cost71e-win7-certificates-20261117.json": {
  "bytes": 14534,
  "git_blob_sha": "a9ddec439e1931614679c2575e4adeb5fe770d2b"
 },
 "certs71e/n11_s7_00000000000000c09002000000002008.cert.part1of2": {
  "bytes": 649608,
  "git_blob_sha": "16b72b4415630ffc3120f2d6b416fa028bc79003"
 },
 "certs71e/n11_s7_00000000000000c09002000000002008.cert.part2of2": {
  "bytes": 649592,
  "git_blob_sha": "57a1750e285802179580e539428eb30e73e85119"
 },
 "certs71e/n11_s7_00000000000000c09002000000002010.cert.part1of2": {
  "bytes": 919446,
  "git_blob_sha": "72b00cbebe5299247aca7c29c7bcc0ab2e770059"
 },
 "certs71e/n11_s7_00000000000000c09002000000002010.cert.part2of2": {
  "bytes": 919439,
  "git_blob_sha": "db25b9c3c2ecc58cc8ec2acfca240a5cffbb0b63"
 },
 "certs71e/n11_s7_00000000000000c09002000000002100.cert.part1of2": {
  "bytes": 744382,
  "git_blob_sha": "0be4079a6dc1eb6ed4e649b20e857614a112dfe3"
 },
 "certs71e/n11_s7_00000000000000c09002000000002100.cert.part2of2": {
  "bytes": 744349,
  "git_blob_sha": "08921dbbbd7a177d46d9881e9f512a05a0ad80dc"
 },
 "certs71e/n11_s7_00000000000000c09002020000002000.cert": {
  "bytes": 955669,
  "git_blob_sha": "7c8c5a0134972b2707ca4fba0e7eb53fb4fc4930"
 },
 "certs71e/n11_s7_00000000000000c09042000000002000.cert.part1of2": {
  "bytes": 853607,
  "git_blob_sha": "8b77f6061bc252881914e193e47169794e5b6fd9"
 },
 "certs71e/n11_s7_00000000000000c09042000000002000.cert.part2of2": {
  "bytes": 853601,
  "git_blob_sha": "9f14fca6605197bda43464874e56fd0368afbe22"
 },
 "certs71e/n11_s7_00000000000000c09402000000002000.cert": {
  "bytes": 1178240,
  "git_blob_sha": "5cef59d206ae4d553212d436ff68fecbebb25cbc"
 },
 "certs71e/n11_s7_00000000000010c09002000000002000.cert.part1of2": {
  "bytes": 766956,
  "git_blob_sha": "e67ae2417551ea53adc824fab34ea2f0cbf327e9"
 },
 "certs71e/n11_s7_00000000000010c09002000000002000.cert.part2of2": {
  "bytes": 766945,
  "git_blob_sha": "c225f6107f99cf78a4bcbbaf2607d2a8af6f30e5"
 },
 "certs71e/n11_s7_00000000000080c09002000000002000.cert": {
  "bytes": 936287,
  "git_blob_sha": "3bf73f56eb9f6408e47683e714ce572bb225ef14"
 },
 "certs71e/n11_s7_00000000400000c09002000000002000.cert.part1of2": {
  "bytes": 814565,
  "git_blob_sha": "0ff23779c1aec7abf2c1772ce75d8a60d26885f6"
 },
 "certs71e/n11_s7_00000000400000c09002000000002000.cert.part2of2": {
  "bytes": 814537,
  "git_blob_sha": "52af7185685ee3df2b6d886ded2ff7486b7345b2"
 },
 "certs71e/n11_s7_00000001000000c09002000000002000.cert.part1of2": {
  "bytes": 854599,
  "git_blob_sha": "8661b207e014c8c09991dd88f0664428b3df25fc"
 },
 "certs71e/n11_s7_00000001000000c09002000000002000.cert.part2of2": {
  "bytes": 854581,
  "git_blob_sha": "9419ded12565c94f6c5ede2c858094ce4d9acffd"
 },
 "certs71e/n11_s7_00000010000000c09002000000002000.cert.part1of2": {
  "bytes": 610900,
  "git_blob_sha": "780f37c796f0c5aa4666676609f5857ba143587a"
 },
 "certs71e/n11_s7_00000010000000c09002000000002000.cert.part2of2": {
  "bytes": 610894,
  "git_blob_sha": "b543eb35042a19a4a111e8aa4e0e4c4cf02ebb80"
 },
 "certs71e/n11_s7_00100000000000c09002000000002000.cert.part1of2": {
  "bytes": 1008085,
  "git_blob_sha": "bd6d2a54f953ac642e05c8da7a5512b4c15a7b4e"
 },
 "certs71e/n11_s7_00100000000000c09002000000002000.cert.part2of2": {
  "bytes": 1008069,
  "git_blob_sha": "dafa93aed937599fe50b3ceda27d928feca33ed0"
 },
 "certs71e/n11_s7_00800000000000c09002000000002000.cert.part1of2": {
  "bytes": 892908,
  "git_blob_sha": "6c90044dba2ef21ce0e13eaf767f0d669fbe9346"
 },
 "certs71e/n11_s7_00800000000000c09002000000002000.cert.part2of2": {
  "bytes": 892846,
  "git_blob_sha": "43a864871390bb8f5541eaf8b7f0110859031a12"
 },
 "certs72d/class2-lane-cost72d-win7-certificates-20261117.json": {
  "bytes": 13353,
  "git_blob_sha": "b350b714079efb37a15cee812f4657e3682d1a3c"
 },
 "certs72d/n11_s7_00000000000000403800000008004002.cert.part1of2": {
  "bytes": 809957,
  "git_blob_sha": "5170ee22eee337a568d3038a30016d635d687bbf"
 },
 "certs72d/n11_s7_00000000000000403800000008004002.cert.part2of2": {
  "bytes": 809986,
  "git_blob_sha": "7c8418685f56ab0f190ba6578cc412c37cd21cec"
 },
 "certs72d/n11_s7_00000000000000403800000008004040.cert.part1of2": {
  "bytes": 970453,
  "git_blob_sha": "d1898656000772a77c2cc1e5cc16185c7bfcb120"
 },
 "certs72d/n11_s7_00000000000000403800000008004040.cert.part2of2": {
  "bytes": 970521,
  "git_blob_sha": "1f419df00bff456d0afe30d16fc3fa1a14fbec46"
 },
 "certs72d/n11_s7_00000000000000403800000009004000.cert.part1of2": {
  "bytes": 977031,
  "git_blob_sha": "860b6340c55e6f8dedd502f79d1ddbabc3fb3a8d"
 },
 "certs72d/n11_s7_00000000000000403800000009004000.cert.part2of2": {
  "bytes": 977092,
  "git_blob_sha": "2c8c7610b53e8bd676398c85ecb4a39991b3dc5b"
 },
 "certs72d/n11_s7_0000000000000040380000000a004000.cert.part1of2": {
  "bytes": 741336,
  "git_blob_sha": "8fff0ab2cf66527da594398886c8950848fadec9"
 },
 "certs72d/n11_s7_0000000000000040380000000a004000.cert.part2of2": {
  "bytes": 741397,
  "git_blob_sha": "7d936cd45f0f124d0f9ebc301035bad8866f5c3c"
 },
 "certs72d/n11_s7_00000000000000403800080008004000.cert.part1of2": {
  "bytes": 1014224,
  "git_blob_sha": "649c7d15e543ab8e698f7a73d6c278cdffef10d5"
 },
 "certs72d/n11_s7_00000000000000403800080008004000.cert.part2of2": {
  "bytes": 1014248,
  "git_blob_sha": "d66b07853137e2fc7bb873589e2732eea3d168c2"
 },
 "certs72d/n11_s7_00000000000000403802000008004000.cert.part1of2": {
  "bytes": 754148,
  "git_blob_sha": "1efb00ec414137a467cad83353ac62044e09e8cf"
 },
 "certs72d/n11_s7_00000000000000403802000008004000.cert.part2of2": {
  "bytes": 754215,
  "git_blob_sha": "0b746a3313936037c4afcfe4223522477afb17e9"
 },
 "certs72d/n11_s7_00000000000008403800000008004000.cert": {
  "bytes": 1159922,
  "git_blob_sha": "ed0281dcd719ab68190cc0f4f8824eab63b3c58c"
 },
 "certs72d/n11_s7_00000000000100403800000008004000.cert.part1of2": {
  "bytes": 685530,
  "git_blob_sha": "f155a992bb60e15cadc9262b75851eb2e11a9844"
 },
 "certs72d/n11_s7_00000000000100403800000008004000.cert.part2of2": {
  "bytes": 685578,
  "git_blob_sha": "b3eb2d020872d3a364f35ae550aac9babb3b72ef"
 },
 "certs72d/n11_s7_00000000000800403800000008004000.cert.part1of2": {
  "bytes": 1012546,
  "git_blob_sha": "ccc904d4c13273836a52b83f737e00ba7fa55c1a"
 },
 "certs72d/n11_s7_00000000000800403800000008004000.cert.part2of2": {
  "bytes": 1012578,
  "git_blob_sha": "09851c7889bc1b531c4d0a9ec1f2de2593410b73"
 },
 "certs72d/n11_s7_00000004000000403800000008004000.cert.part1of2": {
  "bytes": 822057,
  "git_blob_sha": "4d1c99a85296f5f2629b839a8a8e68c1fd6f5e4a"
 },
 "certs72d/n11_s7_00000004000000403800000008004000.cert.part2of2": {
  "bytes": 822114,
  "git_blob_sha": "adb5ee45a0b560781b52cd00b63ee2440c05a81c"
 },
 "certs72d/n11_s7_00040000000000403800000008004000.cert.part1of2": {
  "bytes": 1057595,
  "git_blob_sha": "f5f522ca15be02a8e2ccc246790fbc8573560e42"
 },
 "certs72d/n11_s7_00040000000000403800000008004000.cert.part2of2": {
  "bytes": 1057640,
  "git_blob_sha": "4a8bfb838fe982018b956d103b659f6545f4df80"
 },
 "certs73j/class2-lane-cost73j-win7-certificates-20261117.json": {
  "bytes": 18020,
  "git_blob_sha": "e88710b5a2d4848be77a03ae5104e46aefc1279a"
 },
 "certs73j/n11_s7_00000000000000403800000408000001.cert.part1of2": {
  "bytes": 841418,
  "git_blob_sha": "864c6030ec51a48b134d559c0d197aac41367962"
 },
 "certs73j/n11_s7_00000000000000403800000408000001.cert.part2of2": {
  "bytes": 841453,
  "git_blob_sha": "1a908087d7e5dfd4d3d56606006cbf67b11f81ac"
 },
 "certs73j/n11_s7_00000000000000403800000408000002.cert.part1of2": {
  "bytes": 864639,
  "git_blob_sha": "ee50039cba29f7f880c411b261060238192aeaf3"
 },
 "certs73j/n11_s7_00000000000000403800000408000002.cert.part2of2": {
  "bytes": 864691,
  "git_blob_sha": "c96aa82d515472e477c7553541196425d014770f"
 },
 "certs73j/n11_s7_00000000000000403800000408000040.cert.part1of2": {
  "bytes": 857811,
  "git_blob_sha": "f21ce92539edcb917eca1439192a04bb5785c3df"
 },
 "certs73j/n11_s7_00000000000000403800000408000040.cert.part2of2": {
  "bytes": 857830,
  "git_blob_sha": "2a68aa53e8c00902be67518849480b05c4572533"
 },
 "certs73j/n11_s7_00000000000000403800000428000000.cert.part1of2": {
  "bytes": 979621,
  "git_blob_sha": "6273910c8cdba81b2292c781dfcc0c58e884223c"
 },
 "certs73j/n11_s7_00000000000000403800000428000000.cert.part2of2": {
  "bytes": 979687,
  "git_blob_sha": "6041054c8957179aee715cf00924eae448dd1047"
 },
 "certs73j/n11_s7_00000000000000403800100408000000.cert.part1of2": {
  "bytes": 967342,
  "git_blob_sha": "5115c78965269b9734d3985e4b3c3936f16f3ec5"
 },
 "certs73j/n11_s7_00000000000000403800100408000000.cert.part2of2": {
  "bytes": 967354,
  "git_blob_sha": "3a59a7ebebc1e06c643c4e90f4594f25341419b8"
 },
 "certs73j/n11_s7_00000000000000403802000408000000.cert.part1of2": {
  "bytes": 602340,
  "git_blob_sha": "1868e53866c50c206e23d52cb85c346436af0f60"
 },
 "certs73j/n11_s7_00000000000000403802000408000000.cert.part2of2": {
  "bytes": 602351,
  "git_blob_sha": "bf4e7d08a0d1004b7358a1e8311c96872a2b243a"
 },
 "certs73j/n11_s7_00000000000000403810000408000000.cert.part1of2": {
  "bytes": 973361,
  "git_blob_sha": "444ec256bc251ead61319d12592cfe3be51f4880"
 },
 "certs73j/n11_s7_00000000000000403810000408000000.cert.part2of2": {
  "bytes": 973364,
  "git_blob_sha": "ee3b43dded780f5d8bdec6a3ce4806ec12acaeba"
 },
 "certs73j/n11_s7_00000000000000603800000408000000.cert": {
  "bytes": 1105284,
  "git_blob_sha": "3b838b0380157ca0cf4ba5b82ad622f4d8b93c0b"
 },
 "certs73j/n11_s7_00000000000004403800000408000000.cert.part1of2": {
  "bytes": 813229,
  "git_blob_sha": "2490106baa5629ec1fbe7fa4c853b78a5e9afe13"
 },
 "certs73j/n11_s7_00000000000004403800000408000000.cert.part2of2": {
  "bytes": 813243,
  "git_blob_sha": "45657b71fe6bb040c146b78a861ae35a4e496713"
 },
 "certs73j/n11_s7_00000000000400403800000408000000.cert": {
  "bytes": 968835,
  "git_blob_sha": "0f99cc936ea008abc11787a586c6395a7a0ccf74"
 },
 "certs73j/n11_s7_00000000008000403800000408000000.cert.part1of2": {
  "bytes": 1040916,
  "git_blob_sha": "58d605a55929bfb605bd134f6a9546c1ca848660"
 },
 "certs73j/n11_s7_00000000008000403800000408000000.cert.part2of2": {
  "bytes": 1040974,
  "git_blob_sha": "e9b8b872ac08869957683ceb7458be2709ede0f8"
 },
 "certs73j/n11_s7_00000000080000403800000408000000.cert.part1of2": {
  "bytes": 625660,
  "git_blob_sha": "ddf35cef03ec282c3025cc570c17160ea9e72578"
 },
 "certs73j/n11_s7_00000000080000403800000408000000.cert.part2of2": {
  "bytes": 625671,
  "git_blob_sha": "c37e2d803e9797ce1d04b97dfcb7dd229aa755f4"
 },
 "certs73j/n11_s7_00000004000000403800000408000000.cert.part1of2": {
  "bytes": 1162311,
  "git_blob_sha": "4d63a90bd9cd04f2f8441ec99f7701a2e4b1e90c"
 },
 "certs73j/n11_s7_00000004000000403800000408000000.cert.part2of2": {
  "bytes": 1162360,
  "git_blob_sha": "d9a42abed17b3c4950f79a08de197027c98ffaff"
 },
 "certs73j/n11_s7_00000010000000403800000408000000.cert.part1of2": {
  "bytes": 739486,
  "git_blob_sha": "ffc39b8c7992ea91c9fb29f1faec0e4d969421cc"
 },
 "certs73j/n11_s7_00000010000000403800000408000000.cert.part2of2": {
  "bytes": 739526,
  "git_blob_sha": "ec29e2b49413f8a5bd24437b359e0fcfc8c59809"
 },
 "certs73j/n11_s7_00004000000000403800000408000000.cert.part1of2": {
  "bytes": 816511,
  "git_blob_sha": "6d6de50d00a0df7061963639037e764a4ee31728"
 },
 "certs73j/n11_s7_00004000000000403800000408000000.cert.part2of2": {
  "bytes": 816540,
  "git_blob_sha": "ed870ea4c7c4dfd07c40ead2d6eec5f2c20ee7d4"
 },
 "certs73j/n11_s7_00400000000000403800000408000000.cert.part1of2": {
  "bytes": 796516,
  "git_blob_sha": "b969ea3840f194da504e75e5133d955e6bbc4ba3"
 },
 "certs73j/n11_s7_00400000000000403800000408000000.cert.part2of2": {
  "bytes": 796527,
  "git_blob_sha": "00ea57a146aad1214ab559f3250faebb2f0a79a0"
 },
 "certs73k/class2-lane-cost73k-win7-certificates-20261117.json": {
  "bytes": 24580,
  "git_blob_sha": "0892aed07d187ae2fb3b4b90a21c7adbc1002b62"
 },
 "certs73k/n11_s7_00000000000000801206000000000401.cert.part1of2": {
  "bytes": 968092,
  "git_blob_sha": "23d91c7546651af714ccce0086caff27ccd277ba"
 },
 "certs73k/n11_s7_00000000000000801206000000000401.cert.part2of2": {
  "bytes": 968148,
  "git_blob_sha": "4b15c217dcfca1ae9c36342371fe3f0727f43704"
 },
 "certs73k/n11_s7_00000000000000801206000000000480.cert.part1of2": {
  "bytes": 835060,
  "git_blob_sha": "da26d7cd3bdabdf196f4d698e36b11961ef29aa7"
 },
 "certs73k/n11_s7_00000000000000801206000000000480.cert.part2of2": {
  "bytes": 835067,
  "git_blob_sha": "8f60ae00af6e3a0f42b3abe2ac8bc5ff9e05fef6"
 },
 "certs73k/n11_s7_00000000000000801206000000000c00.cert.part1of2": {
  "bytes": 681391,
  "git_blob_sha": "ef09f840f7d80c4201fe7d5073853af2f4ed7d22"
 },
 "certs73k/n11_s7_00000000000000801206000000000c00.cert.part2of2": {
  "bytes": 681393,
  "git_blob_sha": "08197d099592295ccc06892d948333dab53398a0"
 },
 "certs73k/n11_s7_00000000000000801206000000008400.cert.part1of2": {
  "bytes": 1069033,
  "git_blob_sha": "ff8acdcaf938aa643f5c2c71fbb7a2037c7d0ad2"
 },
 "certs73k/n11_s7_00000000000000801206000000008400.cert.part2of2": {
  "bytes": 1069095,
  "git_blob_sha": "0a44c13b76aeb7f760408808996d75da0c3701ed"
 },
 "certs73k/n11_s7_00000000000000801206000800000400.cert.part1of2": {
  "bytes": 809584,
  "git_blob_sha": "7f49d279b3f6074f1cfccb399ef007e9287e4b7b"
 },
 "certs73k/n11_s7_00000000000000801206000800000400.cert.part2of2": {
  "bytes": 809639,
  "git_blob_sha": "3b56fa203bfdfdcbe5f3c1c0bca31a06fdbf9d18"
 },
 "certs73k/n11_s7_00000000000000801206008000000400.cert": {
  "bytes": 929706,
  "git_blob_sha": "15ba24c98c998bdf03662c4b46376eba5d7362f5"
 },
 "certs73k/n11_s7_00000000000000801206020000000400.cert": {
  "bytes": 1007281,
  "git_blob_sha": "ec09e602819b10fa62a0a0307107f5029b0061df"
 },
 "certs73k/n11_s7_00000000000000801206100000000400.cert.part1of2": {
  "bytes": 838778,
  "git_blob_sha": "a219da49bca287a96c5d7ed1c95e5c87e2e65e8a"
 },
 "certs73k/n11_s7_00000000000000801206100000000400.cert.part2of2": {
  "bytes": 838829,
  "git_blob_sha": "0850a2d3f9f10f2416e1202433f326336f183059"
 },
 "certs73k/n11_s7_00000000000000801606000000000400.cert.part1of2": {
  "bytes": 741293,
  "git_blob_sha": "94a5ae4da0f32c8790a1ed3946970a1f32b44332"
 },
 "certs73k/n11_s7_00000000000000801606000000000400.cert.part2of2": {
  "bytes": 741307,
  "git_blob_sha": "7325be5c227b3f985bb0de58d0f95833ae8cb19d"
 },
 "certs73k/n11_s7_00000000000000805206000000000400.cert": {
  "bytes": 813180,
  "git_blob_sha": "28c99b8234bc55745198c5597c998db3a48ced6a"
 },
 "certs73k/n11_s7_00000000000002801206000000000400.cert.part1of2": {
  "bytes": 1048155,
  "git_blob_sha": "31b92c908d93e0047a339a06edc81c36bd8bd871"
 },
 "certs73k/n11_s7_00000000000002801206000000000400.cert.part2of2": {
  "bytes": 1048218,
  "git_blob_sha": "4c861374e03d4cce99b951b495724027d4d4975b"
 },
 "certs73k/n11_s7_00000000000010801206000000000400.cert.part1of2": {
  "bytes": 768596,
  "git_blob_sha": "dfdacdd470d53feb3bc22b25e6950b15489d1e59"
 },
 "certs73k/n11_s7_00000000000010801206000000000400.cert.part2of2": {
  "bytes": 768611,
  "git_blob_sha": "8d16964d6f46bb7b04769b1c2230a63fd28eb327"
 },
 "certs73k/n11_s7_00000000008000801206000000000400.cert.part1of2": {
  "bytes": 956569,
  "git_blob_sha": "8122521fee9b25bb04a59f6ba8ce494729972980"
 },
 "certs73k/n11_s7_00000000008000801206000000000400.cert.part2of2": {
  "bytes": 956637,
  "git_blob_sha": "d90d9a0dc3aa7614509e3d7e582648df692915c1"
 },
 "certs73k/n11_s7_00000000020000801206000000000400.cert.part1of2": {
  "bytes": 652586,
  "git_blob_sha": "7302b7581e2754cab9ff6f18f268b86530d4002a"
 },
 "certs73k/n11_s7_00000000020000801206000000000400.cert.part2of2": {
  "bytes": 652656,
  "git_blob_sha": "ff8809f9f3139f2f2f7001084802949a5d93a1f4"
 },
 "certs73k/n11_s7_00000000400000801206000000000400.cert.part1of2": {
  "bytes": 694970,
  "git_blob_sha": "9e44df2740ee3edc40f80def9ec948f65118ce39"
 },
 "certs73k/n11_s7_00000000400000801206000000000400.cert.part2of2": {
  "bytes": 695012,
  "git_blob_sha": "2d25d0506b631c9c45cb6f6457a261e28964128d"
 },
 "certs73k/n11_s7_00000000800000801206000000000400.cert.part1of2": {
  "bytes": 870993,
  "git_blob_sha": "348723c40b838123dc4a0e709a74854de6040525"
 },
 "certs73k/n11_s7_00000000800000801206000000000400.cert.part2of2": {
  "bytes": 871036,
  "git_blob_sha": "d7d9af0056d00be87874105409eb95f7f84f1727"
 },
 "certs73k/n11_s7_00000002000000801206000000000400.cert.part1of2": {
  "bytes": 814507,
  "git_blob_sha": "d6c396fbaee9b6793cf7177796b42310311df463"
 },
 "certs73k/n11_s7_00000002000000801206000000000400.cert.part2of2": {
  "bytes": 814519,
  "git_blob_sha": "9cd04688892ac0a574da0673c715bd57da952de7"
 },
 "certs73k/n11_s7_00000004000000801206000000000400.cert.part1of2": {
  "bytes": 894917,
  "git_blob_sha": "d35a050e4332ed12280b667f01bbbccde27bb1ca"
 },
 "certs73k/n11_s7_00000004000000801206000000000400.cert.part2of2": {
  "bytes": 894941,
  "git_blob_sha": "77de4244b73024a4184f9abab6cd0f9751f91c58"
 },
 "certs73k/n11_s7_00000080000000801206000000000400.cert.part1of2": {
  "bytes": 875607,
  "git_blob_sha": "8bcc492b38ce869eec61d20f3126f7baa2cac311"
 },
 "certs73k/n11_s7_00000080000000801206000000000400.cert.part2of2": {
  "bytes": 875657,
  "git_blob_sha": "52b244c476e21a12a8db1c169ad3b126464f624b"
 },
 "certs73k/n11_s7_00000200000000801206000000000400.cert.part1of2": {
  "bytes": 601691,
  "git_blob_sha": "ea7b502cbbab85d91eac0a35683fc067eeaa55b3"
 },
 "certs73k/n11_s7_00000200000000801206000000000400.cert.part2of2": {
  "bytes": 601691,
  "git_blob_sha": "f5389d6284efe24da4dd737ec73873be9a3625e8"
 },
 "certs73k/n11_s7_00010000000000801206000000000400.cert.part1of2": {
  "bytes": 894166,
  "git_blob_sha": "7021ef26bfe9d04e8c21e05e674dc98478f006d1"
 },
 "certs73k/n11_s7_00010000000000801206000000000400.cert.part2of2": {
  "bytes": 894193,
  "git_blob_sha": "67d6b6a767d59bd46e3b57edc7d46c4581c25a51"
 },
 "certs73k/n11_s7_00200000000000801206000000000400.cert.part1of2": {
  "bytes": 1075354,
  "git_blob_sha": "45310614f6dbc28ed23c4c5521fa2eaa4b9a94a1"
 },
 "certs73k/n11_s7_00200000000000801206000000000400.cert.part2of2": {
  "bytes": 1075380,
  "git_blob_sha": "8f4e5e0bd16d4e252f7f303e0d703271095696c7"
 },
 "inflight73i.json": {
  "bytes": 7983,
  "git_blob_sha": "4a6a17e66fc1a1bfe8efb7dc6fb2400b9af6aa1d"
 },
 "manifest66i.json": {
  "bytes": 10858,
  "git_blob_sha": "8a85ecef573bb6234b2ee1d9f7cb747926bd26ca"
 },
 "manifest69j.json": {
  "bytes": 7445,
  "git_blob_sha": "5e8e72faa1175ffa364849d8d90b73813406fa61"
 },
 "meas_d4.json": {
  "bytes": 2785,
  "git_blob_sha": "cb97fb5f845e191e9180584f4c399a80b3c0acca"
 },
 "meas_v1.json": {
  "bytes": 18430,
  "git_blob_sha": "2d2a47233195f21bbe74af798211838622decd48"
 },
 "rerun73ij.json": {
  "bytes": 49399,
  "git_blob_sha": "4bfad6e156161770ce106cbc75dc2d1cafed11f9"
 },
 "sweep73k-audit.json": {
  "bytes": 7465,
  "git_blob_sha": "85f4f73fa061c02612f5d24320d668e12468ca4e"
 },
 "sweep73k-record.json": {
  "bytes": 13398,
  "git_blob_sha": "0cba988e2a65e9195b0a0e6a3168a518e27079fb"
 },
 "sweep73k-xlane.json": {
  "bytes": 5212,
  "git_blob_sha": "e41143eb0eb79e7d7412596dbb54f1a524f9463c"
 }
}


def git_blob_sha(data):
    h = hashlib.sha1()
    h.update(b"blob %d\x00" % len(data))
    h.update(data)
    return h.hexdigest()


def read_pinned(rel):
    assert rel in PINS, ("unpinned input", rel)
    data = open(rel, "rb").read()
    p = PINS[rel]
    assert len(data) == p["bytes"], ("size mismatch", rel)
    assert git_blob_sha(data) == p["git_blob_sha"], ("blob sha mismatch", rel)
    return data


# D4 canonical form: min int over the eight square symmetries of the
# 11x11 board (generalized from the validated lineage implementation;
# gated below against every published d4_canon_root of five manifests).
def _build_cellmaps():
    maps = []
    for xf in (False, True):
        for yf in (False, True):
            for sw in (False, True):
                m = [0] * 121
                for i in range(121):
                    x, y = i % 11, i // 11
                    if xf:
                        x = 10 - x
                    if yf:
                        y = 10 - y
                    if sw:
                        x, y = y, x
                    m[i] = y * 11 + x
                maps.append(m)
    return maps


CELLMAPS = _build_cellmaps()


def d4_canon_int(v):
    stones = []
    while v:
        b = v & -v
        stones.append(b.bit_length() - 1)
        v ^= b
    best = None
    for m in CELLMAPS:
        w = 0
        for i in stones:
            w |= 1 << m[i]
        if best is None or w < best:
            best = w
    return best


def d4_canon_hex(h):
    return "%032x" % d4_canon_int(int(h, 16))


def popcount(v):
    c = 0
    while v:
        v &= v - 1
        c += 1
    return c


def popcount_hist(states):
    hist = {}
    for v in states:
        c = popcount(v)
        hist[c] = hist.get(c, 0) + 1
    return hist


def load_band(tag):
    band_dir = BANDS[tag]
    groups = []
    for p1 in sorted(glob.glob(os.path.join(band_dir, "*.part1of2"))):
        groups.append([p1, p1.replace("part1of2", "part2of2")])
    for w in sorted(glob.glob(os.path.join(band_dir, "*.cert"))):
        if "part" not in w:
            groups.append([w])
    exact_rows = {}
    canon_rows = {}
    exact_certs = {}
    canon_certs = {}
    memo = {}
    rows = 0
    roots = []
    for parts in groups:
        text = ""
        for p in parts:
            text += read_pinned(p).decode("utf-8")
        lines = text.splitlines()
        roots.append(lines[1].split()[1])
        seen = set()
        seen_c = set()
        for ln in lines[2:]:
            if not ln.strip():
                continue
            v = int(ln.split(" ", 1)[0], 16)
            rows += 1
            exact_rows[v] = exact_rows.get(v, 0) + 1
            c = memo.get(v)
            if c is None:
                c = d4_canon_int(v)
                memo[v] = c
            canon_rows[c] = canon_rows.get(c, 0) + 1
            seen.add(v)
            seen_c.add(c)
        for v in seen:
            exact_certs[v] = exact_certs.get(v, 0) + 1
        for c in seen_c:
            canon_certs[c] = canon_certs.get(c, 0) + 1
    # v1-compatible stats (per-row occurrence counting, as published)
    shared_rows = sum(1 for v in exact_rows.values() if v > 1)
    dup_rows = sum(v - 1 for v in exact_rows.values())
    canon_shared_rows = sum(1 for v in canon_rows.values() if v > 1)
    canon_dup_rows = sum(v - 1 for v in canon_rows.values())
    # stricter per-certificate counting
    shared_certs = sum(1 for v in exact_certs.values() if v > 1)
    dup_certs = sum(v - 1 for v in exact_certs.values())
    canon_shared_certs = sum(1 for v in canon_certs.values() if v > 1)
    canon_dup_certs = sum(v - 1 for v in canon_certs.values())
    hist_certs = {}
    for v in exact_certs.values():
        hist_certs[v] = hist_certs.get(v, 0) + 1
    canon_hist_certs = {}
    for v in canon_certs.values():
        canon_hist_certs[v] = canon_hist_certs.get(v, 0) + 1
    band = {
        "certificates": len(groups),
        "rows_total": rows,
        "distinct_states": len(exact_rows),
        "states_in_multiple_certs_rowcount": shared_rows,
        "states_shared_pct": round(100.0 * shared_rows / len(exact_rows), 3),
        "duplicate_rows": dup_rows,
        "duplicate_rows_pct": round(100.0 * dup_rows / rows, 3),
        "d4_canon_distinct_states": len(canon_rows),
        "canon_reduction_pct": round(
            100.0 * (len(exact_rows) - len(canon_rows)) / len(exact_rows), 3),
        "canon_states_shared_pct": round(
            100.0 * canon_shared_rows / len(canon_rows), 3),
        "canon_duplicate_rows_pct": round(100.0 * canon_dup_rows / rows, 3),
        "states_in_multiple_certs_percert": shared_certs,
        "states_shared_percert_pct": round(
            100.0 * shared_certs / len(exact_certs), 3),
        "duplicate_certs_rows": dup_certs,
        "duplicate_certs_rows_pct": round(100.0 * dup_certs / rows, 3),
        "canon_states_in_multiple_certs_percert": canon_shared_certs,
        "canon_states_shared_percert_pct": round(
            100.0 * canon_shared_certs / len(canon_certs), 3),
        "canon_duplicate_certs_rows": canon_dup_certs,
        "canon_duplicate_certs_rows_pct": round(
            100.0 * canon_dup_certs / rows, 3),
        "cert_count_histogram": {str(k): hist_certs[k]
                                 for k in sorted(hist_certs)},
        "canon_cert_count_histogram": {str(k): canon_hist_certs[k]
                                       for k in sorted(canon_hist_certs)},
        "roots": roots,
    }
    sets_ = {
        "exact": set(exact_certs.keys()),
        "canon": set(canon_certs.keys()),
    }
    return band, sets_


def main():
    out_path = sys.argv[1]

    # ---------- gates: D4 canon reproduces published manifest values ----
    gate_counts = {}
    for tag, fname in (("73k", "certs73k/class2-lane-cost73k-win7-"
                        "certificates-20261117.json"),
                       ("73j", "certs73j/class2-lane-cost73j-win7-"
                        "certificates-20261117.json"),
                       ("72d", "certs72d/class2-lane-cost72d-win7-"
                        "certificates-20261117.json"),
                       ("71e", "certs71e/class2-lane-cost71e-win7-"
                        "certificates-20261117.json")):
        man = json.loads(read_pinned(fname).decode("utf-8"))
        for rec in man["certificates"]:
            got = d4_canon_hex(rec["root"])
            assert got == rec["d4_canon_root"], \
                ("d4_canon_root mismatch", tag, rec["bit"], got)
        gate_counts[tag] = len(man["certificates"])
    man69j = json.loads(read_pinned("manifest69j.json").decode("utf-8"))
    for rec in man69j["certificates"]:
        got = d4_canon_hex(rec["root"])
        assert got == rec["d4_canon_root"], ("d4_canon_root mismatch",
                                             "69j", rec["bit"], got)
    gate_counts["69j"] = len(man69j["certificates"])

    # ---------- WIN-transfer root canon equalities (73k row) ------------
    man73k = json.loads(
        read_pinned("certs73k/class2-lane-cost73k-win7-"
                    "certificates-20261117.json").decode("utf-8"))
    child73k = int(man73k["s6_child_hex"], 16)
    manifest_bits = sorted(rec["bit"] for rec in man73k["certificates"])
    assert manifest_bits == [rec["bit"] for rec in
                             sorted(man73k["certificates"],
                                    key=lambda r: r["bit"])]

    man73j = json.loads(
        read_pinned("certs73j/class2-lane-cost73j-win7-"
                    "certificates-20261117.json").decode("utf-8"))
    src73j110 = [r for r in man73j["certificates"] if r["bit"] == 110][0]
    root14 = child73k | (1 << 14)
    canon14 = d4_canon_int(root14)
    assert canon14 == int(src73j110["d4_canon_root"], 16), \
        ("73k bit14 canon != 73j bit110 canon",)
    src69j110 = [r for r in man69j["certificates"] if r["bit"] == 110][0]
    root55 = child73k | (1 << 55)
    canon55 = d4_canon_int(root55)
    assert canon55 == int(src69j110["d4_canon_root"], 16), \
        ("73k bit55 canon != 69j bit110 canon",)
    child73i = int(json.loads(
        read_pinned("inflight73i.json").decode("utf-8"))["s6_child"], 16)
    root26 = child73k | (1 << 26)
    root73i110 = child73i | (1 << 110)
    canon26 = d4_canon_int(root26)
    canon73i110 = d4_canon_int(root73i110)
    assert canon26 == canon73i110, ("73k bit26 canon != 73i bit110 canon",)
    assert canon14 not in [d4_canon_int(int(r["root"], 16))
                           for r in man73k["certificates"]]

    man66i = json.loads(read_pinned("manifest66i.json").decode("utf-8"))
    child66i = int(man66i["s6_child_hex"], 16)
    root53 = child73k | (1 << 53)
    root66i10 = child66i | (1 << 10)
    bit53_raw_identical = root53 == root66i10

    win_transfer = {
        "bit_14": {
            "root_hex": "%032x" % root14,
            "d4_canon_hex": "%032x" % canon14,
            "source": "cost73j bit 110",
            "source_root_hex": src73j110["root"],
            "source_d4_canon_root": src73j110["d4_canon_root"],
            "source_rows": src73j110["rows"],
            "source_extraction_nodes": src73j110["extraction_nodes"],
            "canon_equality_reproduced": True,
        },
        "bit_26": {
            "root_hex": "%032x" % root26,
            "d4_canon_hex": "%032x" % canon26,
            "source": "cost73i bit 110 (sweep verdict published; "
                      "certificate band not yet on main)",
            "source_root_hex": "%032x" % root73i110,
            "computed_d4_canon_hex": "%032x" % canon73i110,
            "canon_equality_computed": True,
            "certificate_on_main": False,
        },
        "bit_55": {
            "root_hex": "%032x" % root55,
            "d4_canon_hex": "%032x" % canon55,
            "source": "cost69j bit 110",
            "source_root_hex": src69j110["root"],
            "source_d4_canon_root": src69j110["d4_canon_root"],
            "source_rows": src69j110["rows"],
            "source_extraction_nodes": src69j110["extraction_nodes"],
            "canon_equality_reproduced": True,
        },
        "bit_53_refuted_transfer_raw_identity": {
            "root_hex": "%032x" % root53,
            "source": "cost66i bit 10 (REFUTED-D10)",
            "raw_identical": bit53_raw_identical,
        },
    }

    # ---------- band loading --------------------------------------------
    bands = {}
    sets_by_tag = {}
    for tag in sorted(BANDS):
        band, sets_ = load_band(tag)
        bands[tag] = band
        sets_by_tag[tag] = sets_

    # regression gate vs published v1/addendum band stats
    meas_v1 = json.loads(read_pinned("meas_v1.json").decode("utf-8"))
    meas_d4 = json.loads(read_pinned("meas_d4.json").decode("utf-8"))
    for tag in ("71e", "72d", "73j"):
        pub = meas_v1["bands"][tag]
        mine = bands[tag]
        assert pub["certificates"] == mine["certificates"], (tag, "certs")
        assert pub["rows_total"] == mine["rows_total"], (tag, "rows")
        assert pub["distinct_states"] == mine["distinct_states"], (tag, "distinct")
        assert pub["states_shared_pct"] == mine["states_shared_pct"], (tag, "shared")
        assert pub["duplicate_rows_pct"] == mine["duplicate_rows_pct"], (tag, "dup")
        pubc = meas_d4["bands"][tag]
        assert pubc["d4_canon_distinct_states"] == \
            mine["d4_canon_distinct_states"], (tag, "canon distinct")
        assert pubc["canon_states_shared_pct"] == \
            mine["canon_states_shared_pct"], (tag, "canon shared")
        assert pubc["canon_duplicate_rows_pct"] == \
            mine["canon_duplicate_rows_pct"], (tag, "canon dup")

    # ---------- cross-band pairwise --------------------------------------
    tags = sorted(sets_by_tag)
    pairwise_exact = {}
    pairwise_canon = {}
    for i in range(len(tags)):
        for j in range(i + 1, len(tags)):
            a, b = tags[i], tags[j]
            inter_e = sets_by_tag[a]["exact"] & sets_by_tag[b]["exact"]
            inter_c = sets_by_tag[a]["canon"] & sets_by_tag[b]["canon"]
            entry_e = {
                "shared_states": len(inter_e),
                "pct_of_%s" % a: round(100.0 * len(inter_e)
                                       / len(sets_by_tag[a]["exact"]), 3),
                "pct_of_%s" % b: round(100.0 * len(inter_e)
                                       / len(sets_by_tag[b]["exact"]), 3),
            }
            entry_c = {
                "canon_shared_states": len(inter_c),
                "pct_of_%s" % a: round(100.0 * len(inter_c)
                                        / len(sets_by_tag[a]["canon"]), 3),
                "pct_of_%s" % b: round(100.0 * len(inter_c)
                                        / len(sets_by_tag[b]["canon"]), 3),
            }
            entry_e["shared_state_stone_histogram"] = {
                str(k): v for k, v in sorted(
                    popcount_hist(inter_e).items())}
            entry_c["canon_shared_state_stone_histogram"] = {
                str(k): v for k, v in sorted(
                    popcount_hist(inter_c).items())}
            pairwise_exact["%s_and_%s" % (a, b)] = entry_e
            pairwise_canon["%s_and_%s" % (a, b)] = entry_c
    # regression vs published pairs
    for pair, pub in meas_v1["cross_band_pairwise"].items():
        assert pairwise_exact[pair]["shared_states"] == \
            pub["shared_states"], ("pairwise exact regression", pair)
        if "shared_state_stone_histogram" in pub:
            assert pairwise_exact[pair]["shared_state_stone_histogram"] == \
                pub["shared_state_stone_histogram"], ("hist", pair)
    for pair, pub in meas_d4["cross_band_pairwise"].items():
        assert pairwise_canon[pair]["canon_shared_states"] == \
            pub["canon_shared_states"], ("pairwise canon regression", pair)
    inter3c = (sets_by_tag["71e"]["canon"] & sets_by_tag["72d"]["canon"]
               & sets_by_tag["73j"]["canon"])
    assert len(inter3c) == meas_d4["cross_band_three_way_canon_shared_states"]
    inter4e = (sets_by_tag["71e"]["exact"] & sets_by_tag["72d"]["exact"]
               & sets_by_tag["73j"]["exact"] & sets_by_tag["73k"]["exact"])
    inter4c = (sets_by_tag["71e"]["canon"] & sets_by_tag["72d"]["canon"]
               & sets_by_tag["73j"]["canon"] & sets_by_tag["73k"]["canon"])
    inter3c_with_73k = (sets_by_tag["71e"]["canon"]
                        & sets_by_tag["72d"]["canon"]
                        & sets_by_tag["73k"]["canon"])
    union_earlier_c = (sets_by_tag["71e"]["canon"] | sets_by_tag["72d"]["canon"]
                       | sets_by_tag["73j"]["canon"])
    covered_73k = sets_by_tag["73k"]["canon"] & union_earlier_c

    # ---------- confirmation re-search cost (73k) ------------------------
    record = json.loads(read_pinned("sweep73k-record.json")
                        .decode("utf-8"))
    audit = json.loads(read_pinned("sweep73k-audit.json")
                       .decode("utf-8"))
    per_bit = {int(k): v for k, v in record["verdicts"]["per_bit"].items()}
    total_nodes = sum(v["nodes"] for v in per_bit.values())
    assert total_nodes == 128861941, ("record node total", total_nodes)
    assert audit["verdicts"]["candidate_nodes_total"] == total_nodes
    assert len(record["verdicts"]["win7_d10_bits"]) == 25
    assert len(record["verdicts"]["refuted_d10_bits"]) == 48
    assert len(audit["verdicts"]["win7_d10_bits"]) == 25
    assert audit["verdicts"]["refuted_d10_count"] == 48
    assert audit["verdicts"]["capped_count"] == 0
    assert sorted(audit["verdicts"]["win7_d10_bits"]) == \
        sorted(record["verdicts"]["win7_d10_bits"])
    assert sorted(audit["verdicts"]["refuted_d10_bits"]) == \
        sorted(record["verdicts"]["refuted_d10_bits"])
    win_bits = set(record["verdicts"]["win7_d10_bits"])
    assert win_bits == set(manifest_bits) | set(WIN_TRANSFER_BITS_73K)
    conf_nodes = sum(per_bit[b]["nodes"] for b in CONFIRMATION_BITS_73K)
    win_tr_nodes = sum(per_bit[b]["nodes"] for b in WIN_TRANSFER_BITS_73K)
    ref_tr_bits = [b for b in CONFIRMATION_BITS_73K
                   if b not in WIN_TRANSFER_BITS_73K]
    ref_tr_nodes = sum(per_bit[b]["nodes"] for b in ref_tr_bits)
    confirmation = {
        "confirmation_bits": CONFIRMATION_BITS_73K,
        "confirmation_nodes": conf_nodes,
        "total_candidate_nodes": total_nodes,
        "pct_of_sweep": round(100.0 * conf_nodes / total_nodes, 3),
        "win_transfer_bits": WIN_TRANSFER_BITS_73K,
        "win_transfer_nodes": win_tr_nodes,
        "win_transfer_pct_of_sweep": round(
            100.0 * win_tr_nodes / total_nodes, 3),
        "refuted_transfer_bits": ref_tr_bits,
        "refuted_transfer_nodes": ref_tr_nodes,
        "refuted_transfer_pct_of_sweep": round(
            100.0 * ref_tr_nodes / total_nodes, 3),
        "per_bit_nodes": {str(b): per_bit[b]["nodes"]
                          for b in CONFIRMATION_BITS_73K},
        "source": ("class2-lane-cost73k-concurrent-session-sweep-record-"
                   "20261117.json (published; per-bit 73/73 identical to "
                   "the claim lane's third independent execution)"),
    }
    # regression: 73i/73j confirmation costs from the published rerun
    rerun = json.loads(read_pinned("rerun73ij.json").decode("utf-8"))
    conf_regression = {}
    for t in rerun["targets"]:
        tag = t["target"]
        bits = CONFIRMATION_BITS[tag]
        per = {p["bit"]: p for p in t["per_bit"]}
        tot = t["candidate_nodes_total"]
        nodes = sum(per[b]["nodes"] for b in bits)
        pct = round(100.0 * nodes / tot, 3)
        pub = meas_v1["confirmation_bit_research_cost"][tag]
        assert pct == pub["pct_of_sweep"], ("conf regression", tag)
        conf_regression[tag] = {
            "confirmation_bits": bits,
            "confirmation_nodes": nodes,
            "total_candidate_nodes": tot,
            "pct_of_sweep": pct,
        }

    # ---------- assemble --------------------------------------------------
    out = {
        "schema": ("n11-class2-lane-cost73k-band-sharing-and-reuse-"
                   "measurement-20261117-v1"),
        "date": "2026-11-17",
        "pin_commit": PIN_COMMIT,
        "extends": [
            "class2-lane-cert-state-sharing-and-conf-cost-"
            "measurement-20261117.json (commit 9f2422d3)",
            "class2-lane-cert-state-sharing-d4canon-"
            "measurement-20261117.json (commit 2700ed3c)",
        ],
        "method": (
            "Deterministic set measurement over four published WIN7-D10 "
            "certificate bands (73k: 22 certs / 966,535 rows, published by "
            "the claim lane; 73j/72d/71e recomputed as a byte-pinned "
            "regression gate against the v1/addendum measurements). "
            "Exact sharing is 32-hex equality of certificate row states; "
            "D4-canonical sharing maps every state to its min over the "
            "eight square symmetries of the 11x11 board. The canon "
            "function is gated against all %d published d4_canon_root "
            "values of the 73k/73j/72d/71e/69j manifests. The 73k "
            "confirmation and WIN-transfer numbers come from the "
            "published concurrent-session sweep record (per-bit 73/73 "
            "identical to the claim lane's published third independent "
            "execution)." % sum(gate_counts.values())),
        "d4_canon_root_gate": {
            "manifest_assertions": gate_counts,
            "total": sum(gate_counts.values()),
        },
        "win_transfer_roots": win_transfer,
        "win_transfer_reuse": {
            "win_bits_total": 25,
            "fresh_certificates": len(manifest_bits),
            "canon_reused_certificate_backed": 2,
            "pending_source_certificate": 1,
            "avoided_extraction_rows": (src73j110["rows"]
                                        + src69j110["rows"]),
            "avoided_extraction_nodes": (src73j110["extraction_nodes"]
                                         + src69j110["extraction_nodes"]),
            "note": ("25 WIN7-D10 bits - 22 fresh certificates = 3 "
                     "canon-equal roots: bits 14 (73j bit 110) and 55 "
                     "(69j bit 110) are already covered by published "
                     "byte-verified certificates; bit 26 (73i bit 110) "
                     "has only the published sweep verdict so far, its "
                     "certificate coverage pends the cost73i band "
                     "extraction. The avoided extraction cost counts "
                     "only the two certificate-backed reuses."),
        },
        "bands": bands,
        "cross_band_pairwise_exact": pairwise_exact,
        "cross_band_pairwise_d4canon": pairwise_canon,
        "cross_band_three_way_d4canon_71e_72d_73j": len(inter3c),
        "cross_band_three_way_d4canon_71e_72d_73k": len(inter3c_with_73k),
        "cross_band_four_way_exact": len(inter4e),
        "cross_band_four_way_d4canon": len(inter4c),
        "73k_canon_states_covered_by_earlier_band_union": len(covered_73k),
        "73k_canon_states_covered_by_earlier_band_union_pct": round(
            100.0 * len(covered_73k)
            / len(sets_by_tag["73k"]["canon"]), 3),
        "confirmation_bit_research_cost_73k": confirmation,
        "confirmation_bit_research_cost_regression": conf_regression,
        "input_pins": {k: v for k, v in sorted(PINS.items())},
        "interpretation_guard": (
            "Efficiency and bookkeeping measurement only, on published "
            "certificate bytes and published sweep records. WIN7-D10 "
            "certificates prove a first-player win within depth 10 from "
            "the individual 7-stone roots only; REFUTED-D10 is not a "
            "LOSS proof. No manifest row and no S5 parent is closed by "
            "this measurement. The 11x11 empty board, two-stone roots "
            "{49,60}/{59,60}, S2 {59,60} and classes 1/2/4 all remain "
            "UNKNOWN."),
    }
    doc = json.dumps(out, indent=1, ensure_ascii=False) + "\n"
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(doc)
    print("d4_canon_root gate:", sum(gate_counts.values()))
    for tag in tags:
        b = bands[tag]
        print("%s: certs %d rows %d distinct %d shared %.3f%% dup %.3f%% "
              "canon %d canon_shared %.3f%%"
              % (tag, b["certificates"], b["rows_total"],
                 b["distinct_states"], b["states_shared_pct"],
                 b["duplicate_rows_pct"], b["d4_canon_distinct_states"],
                 b["canon_states_shared_pct"]))
    for pair, e in pairwise_exact.items():
        print("exact %s: %d" % (pair, e["shared_states"]))
    for pair, e in pairwise_canon.items():
        print("canon %s: %d" % (pair, e["canon_shared_states"]))
    print("3-way canon (71e,72d,73j):", len(inter3c))
    print("3-way canon (71e,72d,73k):", len(inter3c_with_73k))
    print("4-way canon:", len(inter4c), "4-way exact:", len(inter4e))
    print("73k canon covered by earlier union: %d (%.3f%%)"
          % (len(covered_73k),
             100.0 * len(covered_73k) / len(sets_by_tag["73k"]["canon"])))
    print("73k confirmation: %d / %d nodes = %.3f%% (WIN %d, REFUTED %d)"
          % (conf_nodes, total_nodes,
             100.0 * conf_nodes / total_nodes, win_tr_nodes,
             ref_tr_nodes))
    print("bit53 raw identity:", bit53_raw_identical)
    print("wrote", out_path, "bytes", len(doc.encode("utf-8")))


if __name__ == "__main__":
    main()
