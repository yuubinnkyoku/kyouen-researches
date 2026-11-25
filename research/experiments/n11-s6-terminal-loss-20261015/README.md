# N11 six-stone LOSS: cache-free proof and joint-plan overlap (2026-10-15)

**Standard 11×11, q=4, complete-call normal play; all labels are fixed original-first-player outcomes. The empty-board winner remains UNKNOWN.**

The canonical S6 `00000000040004001004000004010000` is LOSS, proved by all 49 canonical S7 children, 29 S8 LOSS witnesses, 1,046 S8→S9 obligations, and 483 canonical S10 LOSS leaves. Each S10 leaf is recomputed to terminal, without loading any verdict cache. Independent C++ and Python implementations agree on 1,028,621 summed memoized terminal states. Certificate SHA-256 (uncompressed) is `cb2e73c277c6fd526689db64b1d8c07ebd1ca1bd8c2a966e0757d22c4471ebf6`.

Removing each of the six stones yields six distinct canonical S5 LOSS parents (an odd-stone AND position needs only one S6 LOSS child). All six are absent from the main S5 exact cache at commit `ebcd4cbb4616c7e027050af62940c077a4c4c792` and distinct from the 14 S5 terminal verdicts listed in K0423/K0424. This is a **new terminal-proof source**, not an assertion that these six have already been merged into the active S5 cache.

Three S5 parents occur in the selected S4 class **16397** (`00000000000000401000400040000000`) of the K0424 joint plan. Its 94 canonical S5 children previously had 93 unknown; three of those 93 are now terminal-proved LOSS, leaving 90 unknown in that selected S4 boundary. The class is used by eight selected third-move groups across first-move representatives 24 (3 groups), 26 (2), and 48 (3). The existing plan's **optimistic required S5 union** can therefore be reduced from **31,774 to 31,771**, holding its S4 selections fixed. This is a three-class coverage improvement, **not** a root verdict, and it does not establish that the other unknown S5 children are LOSS.

The other three S5 LOSS parents do not occur below any selected S4 of this fixed plan. The count is conditional on the frozen `repaired-joint-plan-update6.json` in commit `ebcd4cbb`; future plan revisions require a fresh audit. The joint plan is still optimistic and has a valid but nonmatching integer lower bound 6,585; we do not claim a new optimal plan.

## Reproduction

From the root of a full checkout of the above commit (or a directory containing this bundle in the same paths):

```sh
python3 research/experiments/n11-s6-terminal-loss-20261015/verify_s6_terminal.py
g++ -O3 -std=c++20 research/experiments/n11-s6-terminal-loss-20261015/verify_s8_loss_cpp.cpp -o /tmp/n11_s6_verifier
/tmp/n11_s6_verifier research/experiments/n11-s6-terminal-loss-20261015/s6-loss-optimized.cert
python3 research/experiments/n11-s6-terminal-loss-20261015/audit_joint_plan.py
```

The last command requires the tracked main `repaired-joint-plan-update6.json` and `current-exact-s5.cache` from the pinned commit. It recomputes geometry and checks that the six S5 parents were not in the baseline. The other two commands need no cache, solver, or external dependencies. Python uses at most four processes. `python -O` is refused. The proof and its SHA are bundled; the external plan is a frozen comparison baseline, not a trusted proof leaf.

No new two-stone root is closed. Standard 11×11 empty-board outcome **UNKNOWN**.
