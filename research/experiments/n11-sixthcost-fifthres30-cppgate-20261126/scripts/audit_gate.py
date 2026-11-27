#!/usr/bin/env python3
"""Part SR (fifth-resumption 30 LOSS rows C++ scrutiny gate) fail-closed
machine audit (30 delegated resolved-LOSS rows + 3 calibration anchors).

EQ rev4 structure kept via the published SM/SN kit audit script template
(10-capture-group REPLAY regex asserted at import; see input/gate-rows.json
for the machine-derived pins this audit derives from). Gates: G1 raw shape
(replay row + terminal replay_done + driver headers), G2 per-row determinism
(p1 == p2 except wall_s), G3 published-raw pins (legal,budget,result,nodes),
G4 gate-status accounting, G5 input byte-clones (third-impl kit input/ ==
audit_k09k43.py INPINS pins for the 30 targets; SK kit input/ == SK kit
MANIFEST pins for the anchors).

Disclosed vs the SN kit transform rule: docstring + machine-generated
ROWS/RAW_PROV + part/schema strings only; the audit logic is unchanged.
Unlike SN (third-impl ABSENCE), the 30 target rows here DO have
third-implementation verdict-level corroboration (the Part SL batch
32/32 all-pass, LOSS(2) agreement on every row). No verdict is consumed:
the 30 rows stay UNCONSUMED labels (canonical head 02db5ab3 keeps them
absent). 11x11, the two-stone root {60,27}, and its remaining third moves
100/108 stay UNKNOWN throughout.
"""
import hashlib, json, os, re, sys

KIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
KIT = os.path.abspath(KIT)

# key -> (budget, expected "legal,budget,result,nodes",
#          input sha256 pin, provenance of the input pin)
ROWS = {
 "anchor-af039": ["30000000", "89,30000000,2,19234232", "e51a3c9de08c62a54d80547c520876af4245394d05e37bbebf01d74204f64691", "SK kit input/anchor-af039.input.csv (byte-clone; == EQ/EN/EO/EV/SN kit input; SK kit MANIFEST-sha256.txt pin)"],
 "anchor-aj001": ["30000000", "84,30000000,2,5156075", "2f6daea5ca3b3fe6b7713c8d450af3f3c9f203acacb8a1340255d8e8f656496c", "SK kit input/anchor-aj001.input.csv (byte-clone; == EQ/EN/EO/EV/SN kit input; SK kit MANIFEST-sha256.txt pin)"],
 "anchor-at2m": ["2000000", "98,2000000,0,2000000", "ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348", "SK kit input/anchor-at2m.input.csv (byte-clone; == EQ/EN/EO/EV/SN kit input; SK kit MANIFEST-sha256.txt pin)"],
 "k09": ["15000000", "87,15000000,2,4018184", "30f624ad720881d7f0862a87dde4ad0c98334955e0bef9cbb3d13f3e6018f7a5", "third-impl kit input/k09.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"],
 "k10": ["15000000", "84,15000000,2,4295355", "debad4e6882244bd988a048232cc321c8271cdb0c806e57a76b575bcbf0f6bfe", "third-impl kit input/k10.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"],
 "k11": ["15000000", "86,15000000,2,7012218", "397fa6818809dab6753a32ba4a1f461c72053db43eefac416d4751a7f27ebaf4", "third-impl kit input/k11.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"],
 "k12": ["15000000", "83,15000000,2,5688761", "f138355625ee60e2a896841714a36a2a816dc87021593af84ddcc2b051fb6248", "third-impl kit input/k12.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"],
 "k14": ["15000000", "99,15000000,2,6801611", "b3705f4dbc20412de9323d8a7cdc7c69d319b87ac68d0f0f1c242c016e389043", "third-impl kit input/k14.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"],
 "k15": ["15000000", "99,15000000,2,5947870", "c9d9e147cf24ccb1b2a905abd7ac42507ef46894df3a6c356f8e5df2493fe14c", "third-impl kit input/k15.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"],
 "k16": ["15000000", "95,15000000,2,10883904", "d9a02354620fbab2bf401b7e59097d2647de3e22b1c0a2852cdd1696b0ba702d", "third-impl kit input/k16.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"],
 "k17": ["15000000", "96,15000000,2,1241921", "71795886d6f48b47967849e56865d1b99e2348d95d599cec1f4523e028bce664", "third-impl kit input/k17.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"],
 "k18": ["15000000", "91,15000000,2,1838655", "d45a966f2e28c356647d3fbbf2608e12957c0457d12dc4e07b146e2e809607df", "third-impl kit input/k18.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"],
 "k21": ["15000000", "90,15000000,2,3649839", "11be0160ff5f7ae9fe2df718706cfc5513ab098247b698c79f0b3afd1a04edc0", "third-impl kit input/k21.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"],
 "k22": ["15000000", "98,15000000,2,7527812", "f7e1f23551c8c03fe9741f8ca52e219de1be0bbc2c57b54b69b65cf3f3b0e0a2", "third-impl kit input/k22.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"],
 "k23": ["15000000", "97,15000000,2,10938326", "4058bc9fe5bd1bddab42678038eb2494e99ffe614dc7fa2d21eea5e6bdb469a3", "third-impl kit input/k23.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"],
 "k24": ["15000000", "93,15000000,2,4796315", "a707f4484f5df0c1e448099625fb67f33b82574aa87b18a95b7b512dc61d2b01", "third-impl kit input/k24.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"],
 "k25": ["15000000", "91,15000000,2,5496449", "0badeaf933c9b5ce57a807d33ce2354bb5d3c7536076a73f78fa50d8c60a8759", "third-impl kit input/k25.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"],
 "k26": ["15000000", "95,15000000,2,14439424", "f237dd091ffceddfc3160cafaa8049382533edbcfc0176223eb7de54266bcf93", "third-impl kit input/k26.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"],
 "k27": ["15000000", "93,15000000,2,2250306", "a24ae408df6b6fc85fb5556938ca1142146704c39de5f8484e79673e734b2c63", "third-impl kit input/k27.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"],
 "k28": ["2000000", "98,2000000,2,1918850", "b8dd9bab4d7b20e126342e00e7abeb4fe3f298c86c40e98a39177f2791fb8502", "third-impl kit input/k28.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"],
 "k29": ["15000000", "97,15000000,2,4996919", "b5b471b61d5fd6f0378d6514efaa8fdc22442324956f06e847342a3a792c7031", "third-impl kit input/k29.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"],
 "k30": ["15000000", "95,15000000,2,3933511", "6b0d968ddacca16d4776cd7bfda70e0993c833439b92c842c87ba78f0a2e51d6", "third-impl kit input/k30.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"],
 "k31": ["15000000", "92,15000000,2,4560796", "207b670fd26de75f7df7fe4b6e0cb165614e80f7f6805140eb4b08d365cf3e09", "third-impl kit input/k31.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"],
 "k32": ["2000000", "93,2000000,2,1989908", "97e42b8e019ff21e6044c55e5377a6ff4c831c98abb6b8c8a14de4b5e701e135", "third-impl kit input/k32.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"],
 "k34": ["15000000", "96,15000000,2,8567123", "aeac0db59d4d6462004c3f9a70fed9503c8fb77e947fae52f508fcca95cc8860", "third-impl kit input/k34.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"],
 "k35": ["15000000", "100,15000000,2,14273589", "92900664b9a4d71f8c6d629e6d0167eb0c6bb33f7802e2513b4b8ee8015fa4a6", "third-impl kit input/k35.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"],
 "k36": ["15000000", "100,15000000,2,3007021", "95737de8241d394761e2ab7da6eceec93ae12e01ce630beb0bc1c86f1ab96c85", "third-impl kit input/k36.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"],
 "k37": ["15000000", "103,15000000,2,8083885", "c6f15f3d675a49de4bfaabfda338e5a37aa11b9db2a691d9e3f14a729b174d96", "third-impl kit input/k37.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"],
 "k39": ["15000000", "100,15000000,2,5725348", "a155e95d0619b244bc1822e039564729a8160c979f4384f5766a00b89988646e", "third-impl kit input/k39.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"],
 "k40": ["15000000", "102,15000000,2,5926395", "51d7e6ccdd9f1be7442fe6b4e16f5ca1aeb25d06fba2c0122957c16b8658f3bf", "third-impl kit input/k40.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"],
 "k41": ["15000000", "100,15000000,2,6536846", "de03c3cedc9fe936d31469ef5a89468ca8880749ffd6654448e46c2866045a48", "third-impl kit input/k41.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"],
 "k42": ["15000000", "101,15000000,2,8486305", "33a7cd33eb40d1f81330590a5f4bccc328427a41ca8c040f1eccf45d11f180dd", "third-impl kit input/k42.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"],
 "k43": ["15000000", "103,15000000,2,6916669", "ea2279fef225291747d58b6ad6e7f430025b200485f1a7d6b3beb2c2acae7f76", "third-impl kit input/k43.input.csv (byte-clone of the published fifth-resumption batch input of n11-sixthcost-exclusive-selection-v1; sha256 == audit_k09k43.py INPINS pin, the input SSOT)"]
}

RAW_PROV = {
 "anchor-af039": "EV/SK kit raw condition (budget-ceiling baseline); == SK kit anchors block",
 "anchor-aj001": "EV/SK kit raw condition (budget-ceiling baseline); == SK kit anchors block",
 "anchor-at2m": "EV/SK kit raw condition (budget-ceiling baseline); == SK kit anchors block",
 "k09": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at15m-run1-k09.out.csv (published fifth-resumption replica 87,15000000,2,4018184); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)",
 "k10": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at15m-run1-k10.out.csv (published fifth-resumption replica 84,15000000,2,4295355); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)",
 "k11": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at15m-run1-k11.out.csv (published fifth-resumption replica 86,15000000,2,7012218); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)",
 "k12": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at15m-run1-k12.out.csv (published fifth-resumption replica 83,15000000,2,5688761); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)",
 "k14": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at15m-run1-k14.out.csv (published fifth-resumption replica 99,15000000,2,6801611); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)",
 "k15": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at15m-run1-k15.out.csv (published fifth-resumption replica 99,15000000,2,5947870); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)",
 "k16": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at15m-run1-k16.out.csv (published fifth-resumption replica 95,15000000,2,10883904); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)",
 "k17": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at15m-run1-k17.out.csv (published fifth-resumption replica 96,15000000,2,1241921); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)",
 "k18": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at15m-run1-k18.out.csv (published fifth-resumption replica 91,15000000,2,1838655); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)",
 "k21": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at15m-run1-k21.out.csv (published fifth-resumption replica 90,15000000,2,3649839); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)",
 "k22": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at15m-run1-k22.out.csv (published fifth-resumption replica 98,15000000,2,7527812); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)",
 "k23": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at15m-run1-k23.out.csv (published fifth-resumption replica 97,15000000,2,10938326); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)",
 "k24": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at15m-run1-k24.out.csv (published fifth-resumption replica 93,15000000,2,4796315); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)",
 "k25": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at15m-run1-k25.out.csv (published fifth-resumption replica 91,15000000,2,5496449); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)",
 "k26": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at15m-run1-k26.out.csv (published fifth-resumption replica 95,15000000,2,14439424); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)",
 "k27": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at15m-run1-k27.out.csv (published fifth-resumption replica 93,15000000,2,2250306); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)",
 "k28": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at2m-k28.out.csv (published fifth-resumption replica 98,2000000,2,1918850); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)",
 "k29": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at15m-run1-k29.out.csv (published fifth-resumption replica 97,15000000,2,4996919); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)",
 "k30": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at15m-run1-k30.out.csv (published fifth-resumption replica 95,15000000,2,3933511); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)",
 "k31": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at15m-run1-k31.out.csv (published fifth-resumption replica 92,15000000,2,4560796); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)",
 "k32": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at2m-k32.out.csv (published fifth-resumption replica 93,2000000,2,1989908); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)",
 "k34": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at15m-run1-k34.out.csv (published fifth-resumption replica 96,15000000,2,8567123); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)",
 "k35": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at15m-run1-k35.out.csv (published fifth-resumption replica 100,15000000,2,14273589); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)",
 "k36": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at15m-run1-k36.out.csv (published fifth-resumption replica 100,15000000,2,3007021); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)",
 "k37": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at15m-run1-k37.out.csv (published fifth-resumption replica 103,15000000,2,8083885); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)",
 "k39": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at15m-run1-k39.out.csv (published fifth-resumption replica 100,15000000,2,5725348); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)",
 "k40": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at15m-run1-k40.out.csv (published fifth-resumption replica 102,15000000,2,5926395); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)",
 "k41": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at15m-run1-k41.out.csv (published fifth-resumption replica 100,15000000,2,6536846); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)",
 "k42": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at15m-run1-k42.out.csv (published fifth-resumption replica 101,15000000,2,8486305); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)",
 "k43": "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at15m-run1-k43.out.csv (published fifth-resumption replica 103,15000000,2,6916669); cold-pair node-exact vs its run2 raw; third-impl corroboration EXISTS for this row (Part SL batch 32/32 all-pass, verdict-level LOSS(2) agreement)"
}

REPLAY = re.compile(r"^replay,(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),([0-9.]+),(\d+),(\d+)$")
assert len(REPLAY.groupindex) == 0 and REPLAY.groups == 10, "rev4 lesson: exactly 10 capture groups"

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def main():
    gates = {}
    def g(name, ok, detail=""):
        gates[name] = {"status": "PASS" if ok else "FAIL", "detail": detail}
        return ok

    ok = True
    parsed = {}
    for key, (budget, expected, in_pin, prov) in sorted(ROWS.items()):
        rec = {"budget": budget, "expected": expected}
        # G5 input pins
        ipath = os.path.join(KIT, "input", key + ".input.csv")
        if not os.path.isfile(ipath):
            ok &= g("G5:" + key, False, "missing input file")
            continue
        ok &= g("G5:" + key, sha256(ipath) == in_pin,
                "sha256 %s %s" % (sha256(ipath), "==" if sha256(ipath) == in_pin else "!= " + in_pin))
        rows = {}
        for p in ("p1", "p2"):
            rpath = os.path.join(KIT, "output", "raw", key + "." + p + ".out")
            if not os.path.isfile(rpath):
                ok &= g("G1:" + key + ":" + p, False, "missing raw")
                rows[p] = None
                continue
            text = open(rpath).read()
            m = [REPLAY.match(l) for l in text.splitlines() if l.startswith("replay,")]
            done = "# replay_done rows=1" in text
            hdr = "# exact replay: order=0 " in text and "# exact replay: id,stones,legal,is_or,budget,result,nodes,wall_s,key_lo,key_hi" in text
            ok &= g("G1:" + key + ":" + p, bool(len(m) == 1 and done and hdr),
                    "replay_rows=%d done=%s header=%s" % (len(m), done, hdr))
            rows[p] = list(m[0].groups()) if len(m) == 1 and m[0] else None
        if rows["p1"] is None or rows["p2"] is None:
            parsed[key] = rec; continue
        # G2 determinism on all fields except wall_s (index 8)
        a = rows["p1"]; b = rows["p2"]
        det = (a[:7] == b[:7]) and (a[8:] == b[8:])
        ok &= g("G2:" + key, det, "p1=%s p2=%s" % (",".join(a), ",".join(b)))
        # G3 published pins: fields legal(2),budget(4),result(5),nodes(6) -> f3,6,7,8 of csv
        rec["observed_p1"] = ",".join([a[2], a[4], a[5], a[6]])
        ok &= g("G3:" + key, ",".join([a[2], a[4], a[5], a[6]]) == expected,
                "observed %s expected %s (%s)" % (rec["observed_p1"], expected, RAW_PROV[key]))
        parsed[key] = rec
    # G4 status accounting
    spath = os.path.join(KIT, "output", "gate-status.log")
    okp = 0; bad = []
    if os.path.isfile(spath):
        for line in open(spath):
            if " GATE-PASS " in line: okp += 1
            elif "MISMATCH" in line or "GATE-FAIL" in line or "GATE-CRASH" in line:
                bad.append(line.strip())
    ok &= g("G4", okp == len(ROWS) and not bad,
            "passes=%d/%d bad=%d" % (okp, len(ROWS), len(bad)))
    out = {"part": "SR", "schema": "n11-sixthcost-fifthres30-cppgate-audit-v1",
           "rows": parsed, "gates": gates,
           "overall": "PASS" if ok else "FAIL"}
    opath = os.path.join(KIT, "output", "audit_gate.json")
    with open(opath, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
        f.write("\n")
    print("audit_gate:", out["overall"])
    for k, v in sorted(gates.items()):
        if v["status"] == "FAIL":
            print("FAIL", k, v["detail"])
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
