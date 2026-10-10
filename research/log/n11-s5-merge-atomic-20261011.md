# 11×11 S5 cache merge: fail-closed atomic integration (2026-10-11)

Base main: `5afc56fda29255f1e2e285a1fa1d2b664efb1b3e`.
The previous `dfpn_s5_merge.sh` silently skipped missing sources and malformed
rows, did not check D4 canonicality or safe geometry, did not enforce the
quarantine registry, and wrote directly to the destination despite the
atomic-update comment. A failed or concurrent merge could therefore leave
incomplete or untrusted evidence.

The replacement validates all inputs and conflicts before writing, refuses
missing/corrupt evidence and noncanonical/unsafe positions, excludes UNKNOWN
and quarantined keys, then fsyncs a same-directory temporary file and
atomically replaces the output. A conflicting verdict, including on a
quarantined key, fails the entire merge. No new WIN/LOSS claims are made.

Reproduction:
```sh
python3 -m unittest -v research/experiments/n11-search-methods/tests/test_dfpn_s5_merge_safe.py
```
The 10 isolated regressions passed locally (Linux, Python 3), covering
quarantine, UNKNOWN, conflicts, missing inputs/registry, malformed data,
D4 alias, unsafe geometry, deterministic output and preservation of the
previous destination on failure.

This is a merge-integrity improvement only. Secured coverage remains
117/119; two-stone `{60,27}` and the empty 11×11 root remain UNKNOWN.
