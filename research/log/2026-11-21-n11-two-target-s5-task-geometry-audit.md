# 2026-11-21 n11 two-target S5 candidate supply geometry audit

- Latest main at work start: `3b83004b0b0354fa48a60c402134ebe8063e78f8`; AGENTS.md, knowledge README, K1192/K1193, recent 11×11 logs/experiments were checked. The current 11×11 result remains UNKNOWN.
- Input snapshot `d173632fc19a3d9f9abf8e66d0595f4629748bf0`; current main retained all 7 pinned input blob SHAs unchanged.
- Independent Python 3.13.5 verifier uses direct integer 4-point determinant, D4 canonicalization, legal-move enumeration, S4 parent reconstruction, cache and quarantine checks.
- Initial S5 task supply: 4,577 unique keys; 32,039/32,039 gate passes, errors 0. Post-probe supply: 4,575 keys; 32,025/32,025 gate passes, errors 0. All keys canonical, safe, legal counts and active parent lists match.
- The initial list was built from the 5,741-row cache. The merged cache has 5,743 rows; exactly two new keys are LOSS and removed from post list. Initial-list overlap with merged cache = 2, post-list overlap = 0. No task/cache/quarantine inconsistency.
- The two new LOSS keys update 3 parent classes: `1188950301626859520:536870912` by 2; `1297036692683752448:0` by 1; `1297036830122704896:0` by 1. Active unknown S5 incidence 6,466→6,462; distinct keys 4,577→4,575. S4 status remains 62 UNKNOWN / 53 WIN.
- The lowest truncated-cost proxy among 1,887 two-parent/no-key-history candidates is `1306114260682670080:0` (88 legal moves; parents have 101/102 unknown S5 children). It is a selection candidate only; historical bin data is not key-specific.
- CT204, Python 3.13.5. `py_compile` PASS; two pristine runs produce identical audit SHA-256 `f2bcc59fd1f3ff51d71c96ce918cee74938340ebc6381fe352a100098e4627a1`. Negative control: append one newline to a copy of post-probe tasks; expected pin mismatch, rc=1, no audit file.
- Working copies `/opt/kyouen-researches` and `/root/kyouen-researches` were not modified. Inputs/audit used tmpfs. CT204 root disk remained 99% used (143 MiB free), swap 511/512 MiB, no search process; g++/curl unavailable. No probe was started.
- Files: experiment README, verifier, audit JSON, reproduction log. No K item or generated knowledge README change (verification-only, no new game proposition).
- No new S5 verdict or S4 closure; standard 11×11 empty board remains UNKNOWN.
