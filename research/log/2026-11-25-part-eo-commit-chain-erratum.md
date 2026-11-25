# Part EO record addendum: outputs-push landing determination and completion-log commit-chain erratum (2026-11-25)

Addendum to `research/log/2026-11-25-part-eo-cppgate-34908win6-completion.md`
(its published bytes stay frozen at sha256
`31e51fb74c59cee46ecb3f5d564a4bde7e4dfa066412b98edd054ebb8cd01c34`, 9,505 B;
this addendum is a separate log file - the completion log is not edited in
place, so every existing reference or pin to it stays valid).

## 1. Landing determination for the interrupted outputs push

The Part EO session was compacted (context limit) between the in-code
construction of the 24-file outputs payload and the receipt of its push
result, so the compaction-era handoff could not tell whether that push had
landed. The re-established session checked the main history first
(list_commits, 2026-11-25T19:39-19:41Z): no Part EO outputs commit existed
between the declaration commit `74ec7b17` (19:26:14Z) and the then-head
`3ce3dda5` (19:39:44Z, a disjoint PG(2,9)-cap lane). Conclusion: the
interrupted push had NOT landed. `16f578a9` (19:41:46Z) is the first and
only Part EO outputs commit in history - no duplicate was created by the
re-push.

## 2. Actual commit chain (erratum for completion-log section 4)

1. `74ec7b17` - declaration + kit (14 files: declaration log, README,
   runner, audit, 9 input CSVs)
2. `16f578a9` - outputs only: 18 raws, gate-status.log, tamper.log,
   audit_gate.json + run1/run2/run3 (24 files)
3. `50acaf6e` - README run-record update, MANIFEST-sha256.txt, the
   completion log (3 files)

Two published-record inaccuracies are corrected by this addendum (the
completion log is otherwise accurate):

- its section 4 describes items 2+3 as a single "this commit"
  ("outputs ..., README run record + honesty notes, MANIFEST-sha256.txt,
  this close-out"); the actual chain is the 3 commits listed above.
- the `16f578a9` commit message names MANIFEST-sha256 / README run record /
  completion log, none of which are in that commit's file set; they landed
  in `50acaf6e` two minutes later. That message was drafted before the
  compaction interruption assuming a single outputs+close-out push.

All published bytes are identical to the sha-gated payloads constructed
before the interruption (close-out gates: README
`2950209b5be6fec89898fc987421d9198399144340e91749ef2dfa0e3fddeda6`,
MANIFEST `b6e2663abf6917ad2999637dcc929c9ba3991a58bf1109d6d2cc78d46e8adadd`,
completion `31e51fb7...` as pinned above; the 24 outputs were rebuilt from
the same spec table and per-file sha gates in the re-established session).
Nothing was re-derived post-hoc and no verdict, label, or measurement is
affected - this is a chain-of-record correction only.

## 3. Same-session fetch-back verification (this addendum's authoring session)

- `16f578a9` fixed-sha fetch-back: 21 of the 24 output files hashed
  byte-identical to the published MANIFEST pins (two sequential batches,
  10/10 and 11/11, with an in-line TS sha256 implementation self-tested on
  the "abc" vector); audit_gate.json + run1/run2/run3 were pushed from one
  byte-gated payload constant (sha256
  `b46f2130e9855204b5d3a12c07833083af1e96fc4dd9013893f6be7ed0bfa057`) and
  were additionally fetched and read-matched, so all 24 outputs are
  byte-covered.
- `50acaf6e` fixed-sha fetch-back: all 3 close-out files byte-identical
  (README 7,656 B, MANIFEST 3,534 B, completion 9,505 B).

A parallel lane has independently published a second-environment
verification of this kit (head `0a7e7263` at the time of this addendum);
this addendum does not touch or contradict it.

## 4. UNKNOWN guard

The standard 11x11 empty board, the 19 two-stone roots, and every closure
class (including 30484 and 34908) remain UNKNOWN. No verdict is consumed by
this record addendum; the 6 unconsumed probe-level WIN rows of class 34908
and the 4 of class 30484 stay unconsumed; nodes are bookkeeping, not
verdicts.
