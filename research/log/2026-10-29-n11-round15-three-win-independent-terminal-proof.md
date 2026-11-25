# 2026-10-29: N11 round15, three WIN9 and 29 LOSS9 independently terminal-verified

Latest main, AGENTS.md, research/knowledge/README.md, K0023/K0105, round14 replan, round14 terminal/lift, and recent N11 experiment/log records were reviewed before continuing.

The previously queued [round15 discovery workflow 40769366166](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40769366166) succeeded. Its artifact `12850709605` was recovered and inspected. ZIP SHA-256: `8e140cc84c0b2e00d815d4558556cfdf4d51c7b2756c045b2483dc83ab219cab`; extracted JSON SHA-256: `3c3b1bc1e9aef3b99e636de5b4a4b73e98423ad8848c6a64a6d9a1887977c5f0`.

The discovered witness bytes and all metadata are frozen in `research/experiments/n11-s9-post-round14-round15-20261029/certificate.json`. The independent verifier `verify_compact.js` replays minimal obligations with two exact integer geometries, checks parent incidence, source selection and witness SHA-256, and rejects forged WIN9, LOSS9, and out-of-range witness indices. The [independent verification workflow 40777064073](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40777064073) **succeeded**, including full discovery replay against the frozen certificate.

| Measure | Verified result |
| --- | ---: |
| Selected S9 classes | 32 |
| WIN9 / LOSS9 | **3 / 29** |
| All legal S9→S10 edges | 814 |
| WIN9 universal child edges | 77 |
| Discovery unique S10 terminal leaves | 256 |
| Discovery terminal states per geometry | 43,161 |
| **Independent minimal verifier unique S10 leaves** | **106** |
| **Independent minimal verifier states per geometry** | **18,312** |
| Reverse LOSS9 parents from LOSS10 witnesses (not necessarily new) | 289 |
| Cross-batch WIN9/LOSS9 conflict in this batch | 0 |
| New two-stone closures | 0 |

The independent verifier's 106 leaves are 58.6% fewer than discovery's 256, and its 18,312 terminal states are 57.6% fewer than discovery's 43,161. This is certificate replay work, not a faster discovery search. No S8 lift, S7/S5 verdict, or conditional coverage improvement is claimed until the separate lift is independently completed.

The 289 reverse parents are a closure count, **not** 289 newly proved S9 classes; overlap with existing certificates must be deducted separately. The 77 WIN10 edges establish the three WIN9 certificates; the remaining 29 S9 LOSS verdicts each have a checked LOSS10 witness. The proof does not close any two-stone root.

**Standard 11×11 empty-board winner remains UNKNOWN.**
